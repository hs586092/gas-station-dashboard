# 구글 드라이브 자동 업로더

바탕화면의 파일을 자동으로 구글 드라이브에 업로드하는 파이썬 프로그램입니다.

## 주요 기능

- ✅ 바탕화면 파일 자동 모니터링
- ✅ 새 파일 자동 업로드
- ✅ 수정된 파일 재업로드
- ✅ 중복 업로드 방지
- ✅ 업로드 기록 관리
- ✅ 연속 모니터링 또는 일회성 실행 모드

## 설치 방법

### 1. Python 설치 확인

```bash
python --version
# 또는
python3 --version
```

Python 3.7 이상이 필요합니다.

### 2. 필요한 패키지 설치

```bash
pip install -r requirements.txt
# 또는
pip3 install -r requirements.txt
```

### 3. Google Drive API 설정

#### 3-1. Google Cloud Console에서 프로젝트 생성

1. [Google Cloud Console](https://console.cloud.google.com/) 접속
2. 새 프로젝트 생성 (또는 기존 프로젝트 선택)
3. 프로젝트 이름 입력 (예: "Desktop Uploader")

#### 3-2. Google Drive API 활성화

1. 좌측 메뉴 → "API 및 서비스" → "라이브러리"
2. "Google Drive API" 검색
3. "사용 설정" 클릭

#### 3-3. OAuth 2.0 인증 정보 생성

1. 좌측 메뉴 → "API 및 서비스" → "사용자 인증 정보"
2. "사용자 인증 정보 만들기" → "OAuth 클라이언트 ID"
3. 동의 화면 구성 (처음인 경우):
   - 사용자 유형: "외부" 선택
   - 앱 이름, 사용자 지원 이메일 입력
   - 범위는 건너뛰기 가능
   - 테스트 사용자에 본인 이메일 추가
4. OAuth 클라이언트 ID 생성:
   - 애플리케이션 유형: "데스크톱 앱"
   - 이름: "Desktop Uploader Client"
5. JSON 파일 다운로드

#### 3-4. credentials.json 파일 저장

다운로드한 JSON 파일을 `credentials.json` 이름으로 이 프로젝트 폴더에 저장합니다.

```
gas-station-dashboard/
├── google_drive_uploader.py
├── requirements.txt
├── credentials.json  ← 여기에 저장
└── README_DRIVE_UPLOADER.md
```

## 사용 방법

### 모드 1: 연속 모니터링 모드 (권장)

바탕화면을 계속 모니터링하면서 새 파일이 생기면 자동으로 업로드합니다.

```bash
python google_drive_uploader.py
```

- 60초마다 바탕화면 체크
- 새 파일 또는 수정된 파일 자동 업로드
- 종료하려면 `Ctrl+C`

### 모드 2: 일회성 실행 모드

현재 바탕화면의 파일을 한 번만 스캔하고 업로드합니다.

```bash
python google_drive_uploader.py --once
```

### 첫 실행 시

1. 브라우저가 자동으로 열립니다
2. Google 계정으로 로그인
3. 앱 권한 승인 ("계속" 클릭)
4. 인증 완료 후 자동으로 업로드 시작

인증 정보는 `token.pickle` 파일에 저장되어 다음부터는 자동 로그인됩니다.

## 설정 커스터마이징

`google_drive_uploader.py` 파일 상단의 설정을 수정할 수 있습니다:

```python
DESKTOP_PATH = str(Path.home() / "Desktop")  # 모니터링할 폴더 경로
UPLOAD_FOLDER_NAME = "Desktop Uploads"        # 구글 드라이브 폴더 이름
CHECK_INTERVAL = 60                           # 체크 간격 (초)
```

### 다른 폴더 모니터링하기

바탕화면 대신 다른 폴더를 모니터링하려면:

```python
DESKTOP_PATH = "/path/to/your/folder"  # 원하는 경로로 변경
# 예: DESKTOP_PATH = str(Path.home() / "Documents" / "Important")
```

### 체크 간격 변경

더 자주 또는 덜 자주 체크하려면:

```python
CHECK_INTERVAL = 30   # 30초마다 체크
# 또는
CHECK_INTERVAL = 300  # 5분마다 체크
```

## 업로드된 파일 확인

1. [Google Drive](https://drive.google.com) 접속
2. "Desktop Uploads" 폴더 확인
3. 업로드된 파일 및 링크 확인

## 파일 구조

```
gas-station-dashboard/
├── google_drive_uploader.py      # 메인 프로그램
├── requirements.txt               # 필요한 패키지 목록
├── credentials.json               # Google API 인증 정보 (직접 추가)
├── token.pickle                   # 자동 생성되는 인증 토큰
├── upload_log.json                # 업로드 기록 (자동 생성)
└── README_DRIVE_UPLOADER.md       # 이 파일
```

## 업로드 제외 파일

다음 파일들은 자동으로 업로드에서 제외됩니다:

- 숨김 파일 (`.`으로 시작하는 파일)
- 프로그램 관련 파일 (`token.pickle`, `credentials.json`, 등)
- 폴더 (파일만 업로드)

## 문제 해결

### "credentials.json을 찾을 수 없습니다"

- Google Cloud Console에서 OAuth 2.0 인증 정보를 다운로드했는지 확인
- 파일 이름이 정확히 `credentials.json`인지 확인
- 파일이 프로그램과 같은 폴더에 있는지 확인

### "권한이 없습니다" 오류

- `token.pickle` 파일 삭제 후 다시 실행
- Google 계정에서 앱 권한 재승인

### 파일이 업로드되지 않습니다

- 바탕화면 경로가 올바른지 확인
- 파일 크기가 너무 크지 않은지 확인 (Google Drive 용량 확인)
- 인터넷 연결 상태 확인

### 인증이 만료되었습니다

프로그램이 자동으로 토큰을 갱신합니다. 문제가 지속되면:

```bash
rm token.pickle
python google_drive_uploader.py
```

## 백그라운드 실행 (선택사항)

### Linux/Mac

```bash
nohup python google_drive_uploader.py > uploader.log 2>&1 &
```

종료:
```bash
ps aux | grep google_drive_uploader
kill [PID]
```

### Windows

작업 스케줄러를 사용하거나 `.bat` 파일 생성:

```batch
@echo off
pythonw google_drive_uploader.py
```

## 보안 주의사항

- ⚠️ `credentials.json`과 `token.pickle` 파일을 공유하지 마세요
- ⚠️ Git에 업로드하지 마세요 (`.gitignore`에 추가 권장)
- ⚠️ 이 파일들은 당신의 Google Drive에 접근할 수 있는 권한을 포함합니다

## 대안 소프트웨어

파이썬 프로그램 외에 다음 대안들도 있습니다:

1. **Google Backup and Sync** (공식)
   - 장점: 공식 앱, 안정적, 양방향 동기화
   - 단점: 커스터마이징 제한적

2. **rclone** (CLI)
   - 장점: 강력한 기능, 다양한 클라우드 지원
   - 단점: 명령줄 인터페이스, 학습 곡선

3. **이 파이썬 프로그램**
   - 장점: 완전한 커스터마이징, 가볍고 빠름, 코드 수정 가능
   - 단점: 초기 설정 필요, API 할당량 제한

## 라이선스

MIT License

## 지원

문제가 발생하거나 질문이 있으면 이슈를 등록해주세요.
