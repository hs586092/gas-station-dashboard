# 빠른 시작 가이드

## 5분 안에 시작하기

### 1단계: Python 패키지 설치 (1분)

```bash
pip install -r requirements.txt
```

### 2단계: Google API 설정 (3분)

1. **Google Cloud Console 접속**
   - https://console.cloud.google.com/ 방문
   - 새 프로젝트 생성

2. **Drive API 활성화**
   - 검색창에 "Google Drive API" 입력
   - "사용 설정" 클릭

3. **인증 정보 다운로드**
   - 좌측 메뉴: API 및 서비스 → 사용자 인증 정보
   - "사용자 인증 정보 만들기" → OAuth 클라이언트 ID
   - 애플리케이션 유형: "데스크톱 앱"
   - JSON 다운로드 → `credentials.json`으로 저장

### 3단계: 실행 (1분)

```bash
python google_drive_uploader.py
```

첫 실행 시 브라우저가 열리면:
1. Google 계정 로그인
2. "계속" 클릭하여 권한 승인
3. 완료!

### 이제 바탕화면에 파일을 추가하면 자동으로 업로드됩니다! 🎉

---

## 모드 선택

### 계속 실행 (백그라운드 모니터링)
```bash
python google_drive_uploader.py
```
- 계속 실행되면서 60초마다 체크
- 종료: `Ctrl+C`

### 한 번만 실행
```bash
python google_drive_uploader.py --once
```
- 현재 파일만 업로드하고 종료

---

## 업로드된 파일 확인

https://drive.google.com 접속 → "Desktop Uploads" 폴더

---

## 자주 묻는 질문

**Q: 어떤 파일이 업로드되나요?**
A: 바탕화면의 모든 일반 파일 (숨김 파일 제외)

**Q: 같은 파일이 여러 번 업로드되나요?**
A: 아니요, 파일이 수정되지 않으면 다시 업로드하지 않습니다.

**Q: 폴더도 업로드되나요?**
A: 현재 버전은 파일만 업로드합니다.

**Q: 다른 폴더를 모니터링할 수 있나요?**
A: 네! `google_drive_uploader.py`에서 `DESKTOP_PATH` 변경

**Q: 업로드 간격을 바꿀 수 있나요?**
A: 네! `CHECK_INTERVAL` 값을 변경하세요 (초 단위)

---

## 문제 해결

### credentials.json 오류
→ Google Cloud Console에서 다운로드한 JSON 파일을 프로젝트 폴더에 저장

### 권한 오류
→ `token.pickle` 파일 삭제 후 재실행

### 파일이 업로드 안 됨
→ 인터넷 연결 및 Google Drive 용량 확인

---

## 더 자세한 정보

전체 문서: `README_DRIVE_UPLOADER.md` 참조
