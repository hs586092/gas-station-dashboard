# Wooribos후방 자동화 시스템

Windows 데스크톱 프로그램 "Wooribos후방"을 자동으로 실행하고 파일을 다운로드하는 시스템입니다.

## 🎯 주요 기능

- ✅ 프로그램 자동 시작
- ✅ 메뉴 자동 클릭 (6단계)
- ✅ 여러 파일 자동 다운로드 (수십 개)
- ✅ 매일 정해진 시간에 자동 실행
- ✅ 좌표 기반이 아닌 **UI 요소 기반** 자동화 (안정적!)
- ✅ 로그 기록 및 오류 추적

## 📦 파일 구성

```
wooribos_automation.py           # 메인 자동화 스크립트
wooribos_ui_inspector.py         # UI 검사 도구 (설정용)
wooribos_scheduler.py            # 스케줄러 (매일 자동 실행)
run_wooribos_automation.bat      # Windows 배치 파일
wooribos_config.json.example     # 설정 파일 예시
```

## 🚀 빠른 시작 가이드

### 1단계: Python 패키지 설치

```bash
pip install -r requirements.txt
```

필요한 패키지:
- `pywinauto` - Windows UI 자동화
- `schedule` - 스케줄링
- `comtypes` - Windows COM 인터페이스

### 2단계: UI 검사 도구로 프로그램 분석

**중요!** 자동화하기 전에 먼저 프로그램의 UI 구조를 파악해야 합니다.

1. **Wooribos후방 프로그램 실행**
2. **UI 검사 도구 실행:**

```bash
python wooribos_ui_inspector.py
```

3. **메뉴에서 선택:**
   - `2` - 모든 버튼 찾기
   - `3` - 모든 메뉴 찾기
   - `4` - 모든 리스트/그리드 찾기
   - `5` - UI 구조를 JSON 파일로 저장

4. **필요한 정보 기록:**
   - 프로그램 창 제목
   - 클릭해야 할 메뉴/버튼의 **정확한 이름**
   - 다운로드 버튼 이름
   - 파일 리스트의 위치

### 3단계: 설정 파일 작성

1. **예시 파일 복사:**

```bash
copy wooribos_config.json.example wooribos_config.json
```

2. **`wooribos_config.json` 파일 수정:**

```json
{
  "program_path": "C:\\Program Files\\Wooribos\\Wooribos.exe",
  "program_name": "Wooribos후방",
  "download_folder": "C:\\Users\\YourName\\Downloads",
  "wait_time": 2,
  "menu_clicks": [
    {
      "type": "menu",
      "name": "파일",
      "description": "1단계: 파일 메뉴 클릭"
    },
    {
      "type": "menu",
      "name": "데이터관리",
      "description": "2단계: 데이터관리 메뉴 클릭"
    },
    ...
  ],
  "download_settings": {
    "max_files": 100
  }
}
```

**주의:** UI 검사 도구에서 찾은 **정확한 이름**을 사용하세요!

### 4단계: 수동 테스트

설정이 올바른지 확인:

```bash
python wooribos_automation.py
```

로그를 보면서 각 단계가 정상 작동하는지 확인하세요.

### 5단계: 스케줄 설정 (매일 자동 실행)

#### 방법 A: Python 스케줄러 사용

```bash
python wooribos_scheduler.py
```

- 실행 시간 입력 (예: `09:00` 또는 `09:00,14:00`)
- 백그라운드에서 계속 실행됨
- 종료: `Ctrl+C`

#### 방법 B: Windows 작업 스케줄러 사용 (권장)

**장점:**
- 컴퓨터 시작 시 자동 실행
- 백그라운드 실행
- Windows에서 관리

**설정 방법:**

1. **작업 스케줄러 열기**
   - `Win + R` → `taskschd.msc` 입력

2. **새 작업 만들기**
   - 우측 "작업 만들기" 클릭

3. **일반 탭:**
   - 이름: `Wooribos 자동화`
   - "가장 높은 수준의 권한으로 실행" 체크

4. **트리거 탭:**
   - "새로 만들기" 클릭
   - 작업 시작: "일정에 따라"
   - 설정: 매일
   - 시작 시간: 원하는 시간 (예: 오전 9:00)
   - "사용" 체크

5. **동작 탭:**
   - "새로 만들기" 클릭
   - 작업: "프로그램 시작"
   - 프로그램/스크립트: `run_wooribos_automation.bat` 파일 경로
   - 시작 위치: 프로젝트 폴더 경로

6. **조건 탭:**
   - "AC 전원을 사용할 때만 작업 시작" 체크 해제 (선택)

7. **설정 탭:**
   - "작업이 실패할 경우 다시 시작 간격": 1분
   - "다시 시도 횟수": 3회

8. **확인** 클릭

## 🔧 설정 파일 상세 설명

### `wooribos_config.json`

```json
{
  "program_path": "프로그램 실행 파일 전체 경로",
  "program_name": "프로그램 창 제목 (일부만 입력 가능)",
  "download_folder": "다운로드 폴더 경로",
  "wait_time": 2,  // 각 동작 후 대기 시간 (초)
  "max_retries": 3,  // 최대 재시도 횟수

  "menu_clicks": [
    // 순차적으로 클릭할 메뉴 목록
    // UI 검사 도구로 찾은 정확한 이름 사용!
  ],

  "download_settings": {
    "file_pattern": "*",  // 다운로드할 파일 패턴
    "auto_download_all": true,  // 모든 파일 자동 다운로드
    "max_files": 100  // 최대 다운로드 파일 수
  }
}
```

## 📊 로그 확인

자동화 실행 로그는 다음 파일에 저장됩니다:

- `wooribos_automation.log` - 자동화 실행 로그
- `wooribos_scheduler.log` - 스케줄러 로그

로그 확인:
```bash
type wooribos_automation.log
# 또는
tail -f wooribos_automation.log
```

## 🛠️ 문제 해결

### 1. "프로그램을 찾을 수 없습니다"

**원인:** 프로그램 경로 또는 창 제목이 잘못됨

**해결:**
1. UI 검사 도구 실행
2. `6` 선택 - 실행 중인 모든 창 보기
3. 정확한 창 제목 확인
4. `wooribos_config.json`의 `program_name` 수정

### 2. "메뉴를 찾을 수 없습니다"

**원인:** 메뉴 이름이 정확하지 않음

**해결:**
1. Wooribos 프로그램 실행
2. UI 검사 도구 실행
3. `3` 선택 - 모든 메뉴 찾기
4. 출력된 **정확한 메뉴 이름** 복사
5. `wooribos_config.json`의 `menu_clicks`에 정확히 입력

**예:**
```
잘못된 예: "파일"
올바른 예: "파일(F)"  // UI 검사 도구에서 확인한 정확한 이름
```

### 3. "다운로드가 작동하지 않습니다"

**원인:** 다운로드 버튼 찾기 실패

**해결:**
1. UI 검사 도구에서 `2` 선택 - 모든 버튼 찾기
2. 다운로드 관련 버튼 이름 확인
3. 코드 수정이 필요할 수 있음 (아래 커스터마이징 섹션 참조)

### 4. "클릭 위치가 맞지 않습니다"

**원인:** 화면 해상도 또는 창 위치 변경

**장점:** pywinauto는 좌표가 아닌 UI 요소 이름으로 클릭하므로 이 문제가 발생하지 않습니다!

좌표 기반 방식과 달리, 창 위치나 해상도가 바뀌어도 정상 작동합니다.

### 5. 프로그램이 느리게 반응합니다

**해결:**
- `wooribos_config.json`의 `wait_time` 값을 증가 (예: 2 → 3 또는 5)

### 6. Windows 작업 스케줄러에서 실행 안 됨

**확인 사항:**
1. Python 경로가 시스템 PATH에 등록되어 있는지 확인
2. 배치 파일의 Python 경로를 절대 경로로 수정:
   ```batch
   set PYTHON=C:\Python39\python.exe
   ```
3. 작업 스케줄러 로그 확인

## 🎨 커스터마이징

### 다운로드 로직 수정

프로그램 구조에 따라 `wooribos_automation.py`의 `download_files()` 함수를 수정해야 할 수 있습니다.

**예시 1: 테이블에서 각 행 클릭 후 다운로드**

```python
def download_files(self):
    # 테이블 찾기
    table = self.main_window.child_window(control_type="DataGrid")
    rows = table.children(control_type="DataItem")

    for row in rows:
        row.click_input()  # 행 선택
        time.sleep(1)

        # 다운로드 버튼 클릭
        download_btn = self.main_window.child_window(title="다운로드", control_type="Button")
        download_btn.click_input()
        time.sleep(2)
```

**예시 2: 체크박스 선택 후 일괄 다운로드**

```python
def download_files(self):
    # "전체 선택" 체크박스 클릭
    select_all = self.main_window.child_window(title="전체선택", control_type="CheckBox")
    select_all.click_input()
    time.sleep(1)

    # "다운로드" 버튼 클릭
    download_btn = self.main_window.child_window(title="다운로드", control_type="Button")
    download_btn.click_input()
```

### 로그인 자동화 추가

로그인이 필요한 경우:

```python
def login(self, username, password):
    """로그인"""
    # 아이디 입력
    id_field = self.main_window.child_window(control_type="Edit", found_index=0)
    id_field.set_text(username)

    # 비밀번호 입력
    pw_field = self.main_window.child_window(control_type="Edit", found_index=1)
    pw_field.set_text(password)

    # 로그인 버튼 클릭
    login_btn = self.main_window.child_window(title="로그인", control_type="Button")
    login_btn.click_input()
    time.sleep(3)
```

## 🔒 보안 주의사항

- ⚠️ `wooribos_config.json`에 비밀번호를 저장하지 마세요
- ⚠️ Git에 로그 파일을 업로드하지 마세요
- ⚠️ 스크립트는 로컬에서만 실행하세요

비밀번호가 필요한 경우 환경 변수 사용을 권장합니다:

```python
import os
password = os.getenv('WOORIBOS_PASSWORD')
```

## 📈 고급 기능

### 다운로드한 파일을 자동으로 Google Drive에 업로드

`google_drive_uploader.py`와 연동할 수 있습니다:

```python
from wooribos_automation import WooribosAutomation
from google_drive_uploader import GoogleDriveUploader

# 1. Wooribos에서 파일 다운로드
automation = WooribosAutomation()
automation.run()

# 2. 다운로드 폴더를 Google Drive에 업로드
uploader = GoogleDriveUploader()
uploader.scan_and_upload()
```

### 이메일 알림 추가

작업 완료 시 이메일 전송:

```python
import smtplib
from email.mime.text import MIMEText

def send_notification(subject, body):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = 'your@email.com'
    msg['To'] = 'recipient@email.com'

    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login('your@email.com', 'password')
        server.send_message(msg)
```

## 💡 팁

1. **처음에는 작은 단위로 테스트**
   - 먼저 프로그램 시작만 테스트
   - 그 다음 메뉴 1개 클릭 테스트
   - 점진적으로 확장

2. **로그를 자주 확인**
   - 어느 단계에서 실패하는지 파악

3. **wait_time 조정**
   - 프로그램이 느리면 대기 시간 증가

4. **UI 검사 도구 적극 활용**
   - 정확한 요소 이름이 성공의 핵심!

5. **백업 설정 파일 보관**
   - 작동하는 설정을 백업해두세요

## 🤝 도움받기

문제가 해결되지 않으면:

1. **로그 파일 확인** (`wooribos_automation.log`)
2. **UI 검사 도구로 요소 재확인**
3. **설정 파일 다시 검토**

## 📝 라이선스

MIT License

---

**만든 날짜:** 2025-11-23
**버전:** 1.0.0
