#!/usr/bin/env python3
"""
스마트 난방 조절기 - 라즈베리파이 제어 코드
Supabase의 실시간 변경 사항을 감지하여 서보모터 제어
"""

import time
import logging
from typing import Optional
from supabase import create_client, Client
from gpiozero import Servo
from gpiozero.pins.pigpio import PiGPIOFactory
from signal import pause
import os

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/var/log/boiler_controller.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Supabase 설정 (환경 변수에서 읽기)
SUPABASE_URL = os.getenv('SUPABASE_URL', '')
SUPABASE_KEY = os.getenv('SUPABASE_KEY', '')
TABLE_NAME = 'boiler_control'

# GPIO 설정
SERVO_PIN = 18  # GPIO 18번 (물리 번호 12번)

# 서보모터 각도 설정 (마이크로초 단위)
# SG90 서보모터: 0도 = 1000μs, 90도 = 2000μs (약 1ms ~ 2ms)
SERVO_MIN_PULSE_WIDTH = 0.0005  # 0도 (0.5ms)
SERVO_MAX_PULSE_WIDTH = 0.0025  # 180도 (2.5ms)
ANGLE_0 = -1.0    # 0도 위치
ANGLE_60 = 0.33   # 60도 위치 (gpiozero Servo는 -1 ~ 1 범위 사용)


class BoilerController:
    """보일러 제어기 클래스"""
    
    def __init__(self):
        """초기화"""
        self.supabase: Optional[Client] = None
        self.servo: Optional[Servo] = None
        self.current_mode: Optional[str] = None
        self.reconnect_count = 0
        self.max_reconnect = 5
        
    def init_supabase(self) -> bool:
        """Supabase 클라이언트 초기화"""
        try:
            if not SUPABASE_URL or not SUPABASE_KEY:
                logger.error("Supabase URL 또는 KEY가 설정되지 않았습니다.")
                logger.error("환경 변수를 설정하세요: export SUPABASE_URL=... export SUPABASE_KEY=...")
                return False
                
            self.supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
            logger.info("Supabase 클라이언트 초기화 완료")
            return True
        except Exception as e:
            logger.error(f"Supabase 초기화 실패: {e}")
            return False
    
    def init_servo(self) -> bool:
        """서보모터 초기화"""
        try:
            # pigpio 팩토리 사용 (더 안정적)
            factory = PiGPIOFactory()
            self.servo = Servo(
                SERVO_PIN,
                pin_factory=factory,
                min_pulse_width=SERVO_MIN_PULSE_WIDTH,
                max_pulse_width=SERVO_MAX_PULSE_WIDTH
            )
            logger.info(f"서보모터 초기화 완료 (GPIO {SERVO_PIN})")
            return True
        except Exception as e:
            logger.error(f"서보모터 초기화 실패: {e}")
            return False
    
    def move_servo_to_angle(self, angle: float):
        """서보모터를 지정된 각도로 이동"""
        if self.servo is None:
            logger.error("서보모터가 초기화되지 않았습니다.")
            return
        
        try:
            logger.info(f"서보모터 이동 중: {angle}")
            self.servo.value = angle
            time.sleep(0.5)  # 회전 시간 대기
            # 떨림 방지를 위해 서보 신호 차단
            self.servo.detach()
            logger.info(f"서보모터 이동 완료: {angle}")
        except Exception as e:
            logger.error(f"서보모터 제어 실패: {e}")
    
    def set_mode(self, mode: str):
        """보일러 모드 설정"""
        if mode == self.current_mode:
            logger.debug(f"이미 {mode} 모드입니다. 동작 스킵.")
            return
        
        logger.info(f"모드 변경: {self.current_mode} -> {mode}")
        
        if mode == 'mode_0':
            # 실내 난방 모드 (0도)
            self.move_servo_to_angle(ANGLE_0)
            self.current_mode = 'mode_0'
        elif mode == 'mode_60':
            # 온수 전용 모드 (60도)
            self.move_servo_to_angle(ANGLE_60)
            self.current_mode = 'mode_60'
        else:
            logger.warning(f"알 수 없는 모드: {mode}")
            return
        
        # 로그를 Supabase에 기록 (선택사항)
        self.log_action(mode)
    
    def log_action(self, mode: str):
        """동작 로그 기록 (선택사항)"""
        try:
            if self.supabase:
                self.supabase.table('boiler_logs').insert({
                    'mode': mode,
                    'source': 'raspberry_pi'
                }).execute()
        except Exception as e:
            logger.debug(f"로그 기록 실패 (무시 가능): {e}")
    
    def get_current_mode(self) -> Optional[str]:
        """현재 DB의 모드 조회"""
        try:
            if not self.supabase:
                return None
            
            response = self.supabase.table(TABLE_NAME).select('mode').eq('id', 1).execute()
            if response.data:
                return response.data[0]['mode']
            return None
        except Exception as e:
            logger.error(f"현재 모드 조회 실패: {e}")
            return None
    
    def handle_realtime_change(self, payload):
        """Realtime 변경 사항 처리"""
        try:
            if payload.event_type in ['UPDATE', 'INSERT']:
                new_mode = payload.new_record.get('mode')
                if new_mode:
                    self.set_mode(new_mode)
        except Exception as e:
            logger.error(f"실시간 변경 처리 오류: {e}")
    
    def start(self):
        """제어기 시작"""
        logger.info("=== 스마트 난방 조절기 시작 ===")
        
        # 초기화
        if not self.init_supabase():
            logger.error("Supabase 초기화 실패. 프로그램을 종료합니다.")
            return
        
        if not self.init_servo():
            logger.error("서보모터 초기화 실패. 프로그램을 종료합니다.")
            return
        
        # 초기 모드 설정
        initial_mode = self.get_current_mode()
        if initial_mode:
            logger.info(f"초기 모드: {initial_mode}")
            self.set_mode(initial_mode)
        else:
            logger.warning("초기 모드를 가져올 수 없습니다.")
        
        # Realtime 구독 시작
        self.subscribe_realtime()
    
    def subscribe_realtime(self):
        """Supabase Realtime 구독"""
        while True:
            try:
                logger.info("Realtime 구독 시작...")
                
                channel = self.supabase.channel('boiler_control_channel')
                channel.on('postgres_changes', 
                          event='UPDATE',
                          schema='public',
                          table=TABLE_NAME,
                          callback=self.handle_realtime_change)
                channel.on('postgres_changes',
                          event='INSERT',
                          schema='public',
                          table=TABLE_NAME,
                          callback=self.handle_realtime_change)
                
                channel.subscribe()
                
                # 구독이 성공적으로 시작되면 재연결 카운터 리셋
                self.reconnect_count = 0
                logger.info("Realtime 구독 성공. 대기 중...")
                
                # 영구 대기
                pause()
                
            except KeyboardInterrupt:
                logger.info("사용자에 의해 중단되었습니다.")
                break
            except Exception as e:
                self.reconnect_count += 1
                logger.error(f"Realtime 구독 오류 (재시도 {self.reconnect_count}/{self.max_reconnect}): {e}")
                
                if self.reconnect_count >= self.max_reconnect:
                    logger.error("최대 재시도 횟수에 도달했습니다. 프로그램을 종료합니다.")
                    break
                
                # 재연결 대기 (지수 백오프)
                wait_time = min(2 ** self.reconnect_count, 60)
                logger.info(f"{wait_time}초 후 재연결 시도...")
                time.sleep(wait_time)
    
    def cleanup(self):
        """리소스 정리"""
        logger.info("리소스 정리 중...")
        if self.servo:
            try:
                self.servo.detach()
            except:
                pass
        logger.info("프로그램 종료")


def main():
    """메인 함수"""
    controller = BoilerController()
    
    try:
        controller.start()
    except KeyboardInterrupt:
        logger.info("키보드 인터럽트 감지")
    except Exception as e:
        logger.error(f"예기치 않은 오류: {e}")
    finally:
        controller.cleanup()


if __name__ == '__main__':
    main()

