# 📱 스마트 난방 조절기 - 유저 플로우 및 동작 방식

## 🎯 전체 시스템 플로우 다이어그램

```
[스마트폰] → [Supabase DB] → [라즈베리파이] → [서보모터] → [보일러 스위치]
   (UI)         (클라우드)        (제어기)        (액추에이터)    (실제 장치)
```

---

## 🔄 상세 유저 플로우

### 1️⃣ 초기 접속 및 인증 단계

#### 웹 페이지 접속
- 사용자가 스마트폰 브라우저로 웹 UI URL 접속
- HTML 파일이 로드됨

#### PIN 인증 (web/index.html:332-362)

```332:362:web/index.html
        function checkPin() {
            const pin = ['pin1', 'pin2', 'pin3', 'pin4']
                .map(id => document.getElementById(id).value)
                .join('');
            
            const pinError = document.getElementById('pinError');
            const pinLoading = document.getElementById('pinLoading');
            
            if (pin.length !== 4) {
                return;
            }

            pinLoading.classList.add('active');
            pinError.textContent = '';

            // PIN 확인 (실제로는 서버에서 확인해야 하지만, 예제에서는 클라이언트에서 처리)
            setTimeout(() => {
                if (pin === CORRECT_PIN) {
                    document.getElementById('pinModal').classList.remove('active');
                    document.getElementById('mainContainer').style.display = 'flex';
                    initApp();
                } else {
                    pinError.textContent = 'PIN 번호가 올바르지 않습니다.';
                    ['pin1', 'pin2', 'pin3', 'pin4'].forEach(id => {
                        document.getElementById(id).value = '';
                    });
                    document.getElementById('pin1').focus();
                }
                pinLoading.classList.remove('active');
            }, 500);
        }
```

**동작 과정:**
1. 사용자가 4자리 PIN 입력 (각 자리별로 입력 필드 분리)
2. 4자리 모두 입력 시 자동으로 `checkPin()` 함수 호출
3. 입력된 PIN과 `CORRECT_PIN` (기본값: '1234') 비교
4. **성공 시**: PIN 모달 숨김, 메인 컨테이너 표시, `initApp()` 호출
5. **실패 시**: 에러 메시지 표시, 입력 필드 초기화

---

### 2️⃣ 앱 초기화 단계

#### Supabase 클라이언트 초기화 (web/index.html:274-284)

```274:284:web/index.html
        // Supabase 초기화
        function initSupabase() {
            if (!SUPABASE_URL || !SUPABASE_KEY || SUPABASE_URL.includes('YOUR_') || SUPABASE_KEY.includes('YOUR_')) {
                console.error('Supabase 설정이 필요합니다!');
                alert('Supabase URL과 KEY를 설정해주세요.');
                return false;
            }
            
            supabaseClient = supabase.createClient(SUPABASE_URL, SUPABASE_KEY);
            return true;
        }
```

**동작:**
- Supabase URL과 KEY로 클라이언트 생성
- 설정이 없으면 에러 메시지 표시

#### 현재 상태 조회 (web/index.html:377-396)

```377:396:web/index.html
        // 현재 모드 조회
        async function loadCurrentMode() {
            try {
                const { data, error } = await supabaseClient
                    .from('boiler_control')
                    .select('mode')
                    .eq('id', 1)
                    .single();

                if (error) throw error;

                if (data) {
                    updateStatusDisplay(data.mode);
                    updateButtonStates(data.mode);
                }
            } catch (error) {
                console.error('모드 조회 실패:', error);
                document.getElementById('currentStatus').textContent = '조회 실패';
            }
        }
```

**동작:**
1. Supabase `boiler_control` 테이블에서 `id=1`인 레코드의 `mode` 값 조회
2. 조회 성공 시 화면에 현재 모드 표시 (`updateStatusDisplay`)
3. 버튼 상태 업데이트 (`updateButtonStates`)

#### Realtime 구독 시작 (web/index.html:432-452)

```432:452:web/index.html
        // Realtime 구독
        function subscribeToChanges() {
            supabaseClient
                .channel('boiler_control_channel')
                .on('postgres_changes', 
                    { 
                        event: 'UPDATE', 
                        schema: 'public', 
                        table: 'boiler_control',
                        filter: 'id=eq.1'
                    }, 
                    (payload) => {
                        console.log('변경 감지:', payload);
                        if (payload.new) {
                            updateStatusDisplay(payload.new.mode);
                            updateButtonStates(payload.new.mode);
                        }
                    }
                )
                .subscribe();
        }
```

**동작:**
- Supabase Realtime 기능으로 `boiler_control` 테이블 변경사항 구독
- 테이블이 업데이트되면 자동으로 콜백 함수 실행
- 화면 상태 자동 업데이트

---

### 3️⃣ 모드 변경 요청 단계

#### 사용자 버튼 클릭 (web/index.html:398-430)

```398:430:web/index.html
        // 모드 설정
        async function setMode(mode) {
            const loading = document.getElementById('loading');
            loading.classList.add('active');

            // 버튼 비활성화
            document.getElementById('mode0Btn').classList.add('disabled');
            document.getElementById('mode60Btn').classList.add('disabled');

            try {
                const { error } = await supabaseClient
                    .from('boiler_control')
                    .update({ 
                        mode: mode,
                        updated_at: new Date().toISOString()
                    })
                    .eq('id', 1);

                if (error) throw error;

                // 상태 업데이트 (Realtime을 통해 자동으로 업데이트되지만 즉시 반영)
                updateStatusDisplay(mode);
                updateButtonStates(mode);

            } catch (error) {
                console.error('모드 설정 실패:', error);
                alert('모드 변경에 실패했습니다. 다시 시도해주세요.');
            } finally {
                loading.classList.remove('active');
                document.getElementById('mode0Btn').classList.remove('disabled');
                document.getElementById('mode60Btn').classList.remove('disabled');
            }
        }
```

**동작 과정:**
1. 사용자가 "🔥 실내 난방 (0도)" 또는 "💧 온수 전용 (60도)" 버튼 클릭
2. 로딩 표시 및 버튼 비활성화
3. Supabase API를 통해 `boiler_control` 테이블의 `mode` 컬럼 업데이트
   - `mode_0`: 실내 난방 모드
   - `mode_60`: 온수 전용 모드
4. `updated_at` 타임스탬프 자동 업데이트
5. 성공 시 화면 즉시 업데이트

---

### 4️⃣ Supabase Realtime 전파 단계

#### 데이터베이스 변경 감지
- Supabase가 테이블 변경사항을 Realtime 이벤트로 발행
- 구독 중인 모든 클라이언트에 실시간으로 전달

**전파 경로:**
```
DB 업데이트 → Supabase Realtime 서버 → WebSocket → 클라이언트들
                                        ↓
                                   [웹 UI]
                                   [라즈베리파이]
```

---

### 5️⃣ 라즈베리파이 감지 및 제어 단계

#### 라즈베리파이 초기화 (raspberry_pi/boiler_controller.py:160-182)

```160:182:raspberry_pi/boiler_controller.py
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
```

**동작:**
1. Supabase 클라이언트 초기화
2. 서보모터(GPIO 18) 초기화
3. 현재 DB의 모드 조회하여 서보모터 위치 초기화
4. Realtime 구독 시작

#### Realtime 변경 감지 (raspberry_pi/boiler_controller.py:150-158)

```150:158:raspberry_pi/boiler_controller.py
    def handle_realtime_change(self, payload):
        """Realtime 변경 사항 처리"""
        try:
            if payload.event_type in ['UPDATE', 'INSERT']:
                new_mode = payload.new_record.get('mode')
                if new_mode:
                    self.set_mode(new_mode)
        except Exception as e:
            logger.error(f"실시간 변경 처리 오류: {e}")
```

**동작:**
- Supabase에서 Realtime 이벤트 수신 (약 0.1초 이내)
- `UPDATE` 또는 `INSERT` 이벤트 발생 시 새 모드 값 추출
- `set_mode()` 함수 호출하여 서보모터 제어

#### 서보모터 제어 (raspberry_pi/boiler_controller.py:102-123)

```102:123:raspberry_pi/boiler_controller.py
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
```

**동작:**
1. 현재 모드와 동일하면 스킵 (중복 동작 방지)
2. 모드에 따라 서보모터 각도 설정:
   - `mode_0`: `ANGLE_0` (-1.0) → 0도 위치
   - `mode_60`: `ANGLE_60` (0.33) → 60도 위치
3. 동작 로그를 Supabase `boiler_logs` 테이블에 기록

#### 서보모터 물리적 이동 (raspberry_pi/boiler_controller.py:86-100)

```86:100:raspberry_pi/boiler_controller.py
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
```

**동작:**
1. `gpiozero` 라이브러리를 통해 GPIO 18번 핀으로 PWM 신호 전송
2. 서보모터가 지정된 각도로 회전 (0.5초 대기)
3. 회전 완료 후 `detach()` 호출하여 신호 차단 (떨림 방지)
4. 서보모터가 보일러 스위치를 물리적으로 회전시킴

---

## ⏱️ 전체 타이밍 다이어그램

```
시간축 →
[사용자]
  │
  ├─[0.0초] 버튼 클릭
  │
[웹 UI]
  │
  ├─[0.0초] setMode() 호출
  ├─[0.1초] Supabase API 업데이트 요청
  │
[Supabase]
  │
  ├─[0.1초] DB 업데이트 완료
  ├─[0.1초] Realtime 이벤트 발행
  │
[웹 UI]          [라즈베리파이]
  │                    │
  ├─[0.2초]            ├─[0.2초] Realtime 이벤트 수신
  │  화면 업데이트      │
  │                    ├─[0.2초] handle_realtime_change() 호출
  │                    │
  │                    ├─[0.3초] set_mode() 호출
  │                    │
  │                    ├─[0.3초] move_servo_to_angle() 실행
  │                    │
  │                    ├─[0.8초] 서보모터 회전 완료
  │                    │
  │                    └─[0.8초] detach() 호출 (떨림 방지)
  │
[보일러]
  │
  └─[0.8초] 스위치 물리적 회전 완료
```

**총 소요 시간: 약 0.8초** (인터넷 연결 상태에 따라 변동 가능)

---

## 🔁 에러 처리 및 재연결 로직

### 라즈베리파이 재연결 메커니즘 (raspberry_pi/boiler_controller.py:184-225)

```184:225:raspberry_pi/boiler_controller.py
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
```

**동작:**
- Realtime 연결이 끊기면 자동으로 재연결 시도
- 지수 백오프 방식 (2초, 4초, 8초, 16초, ... 최대 60초)
- 최대 5회 재시도 후 포기

---

## 📊 데이터 흐름 요약

1. **사용자 입력** → 웹 UI 버튼 클릭
2. **API 호출** → Supabase REST API로 DB 업데이트
3. **Realtime 전파** → Supabase가 변경사항을 실시간으로 브로드캐스트
4. **웹 UI 반영** → 화면 자동 업데이트
5. **라즈베리파이 감지** → Realtime 이벤트 수신
6. **서보모터 제어** → GPIO 신호로 물리적 회전
7. **보일러 작동** → 스위치 회전으로 모드 변경

---

## 🔒 보안 및 인증

- **PIN 인증**: 웹 UI 접근 제어 (클라이언트 사이드)
- **Supabase API 키**: 서버 사이드에서 검증
- **RLS (Row Level Security)**: Supabase에서 추가 보안 설정 가능

---

## 📝 주요 특징

1. **실시간 동기화**: Supabase Realtime으로 즉각적인 반영
2. **중복 방지**: 현재 모드와 동일하면 서보모터 동작 스킵
3. **떨림 방지**: 서보모터 회전 후 신호 차단
4. **자동 재연결**: 네트워크 오류 시 자동 복구
5. **로깅**: 모든 동작을 로그 파일 및 DB에 기록

