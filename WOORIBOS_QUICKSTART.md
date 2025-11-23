# Wooribos후방 자동화 빠른 시작

## 📋 3단계로 시작하기

### 1️⃣ 설치 (2분)

```bash
pip install -r requirements.txt
```

### 2️⃣ UI 분석 (5분)

1. **Wooribos후방 프로그램 실행**

2. **UI 검사 도구 실행:**
```bash
python wooribos_ui_inspector.py
```

3. **메뉴에서 선택:**
   - `3` - 모든 메뉴 찾기 → 메뉴 이름 메모
   - `2` - 모든 버튼 찾기 → 다운로드 버튼 이름 메모
   - `5` - JSON 파일로 저장

### 3️⃣ 설정 및 실행 (3분)

1. **설정 파일 복사:**
```bash
copy wooribos_config.json.example wooribos_config.json
```

2. **`wooribos_config.json` 수정:**
   - `program_path` - Wooribos.exe 파일 경로
   - `menu_clicks` - UI 검사 도구에서 찾은 메뉴 이름 입력

3. **테스트 실행:**
```bash
python wooribos_automation.py
```

---

## 🎯 매일 자동 실행 설정

### Windows 작업 스케줄러 (권장)

1. `Win + R` → `taskschd.msc`
2. "작업 만들기"
3. **트리거:** 매일 09:00
4. **동작:** `run_wooribos_automation.bat` 실행
5. 완료!

### Python 스케줄러

```bash
python wooribos_scheduler.py
```
- 실행 시간 입력 (예: 09:00)
- 백그라운드에서 계속 실행

---

## ❓ 문제 해결

### "프로그램을 찾을 수 없습니다"
→ UI 검사 도구에서 `6` 선택, 정확한 창 제목 확인

### "메뉴를 찾을 수 없습니다"
→ UI 검사 도구에서 `3` 선택, 정확한 메뉴 이름 복사

### "느리게 작동합니다"
→ `wooribos_config.json`의 `wait_time` 값 증가 (2 → 3)

---

## 📖 자세한 설명

전체 문서: `README_WOORIBOS_AUTOMATION.md` 참조

---

**핵심:** UI 검사 도구로 찾은 **정확한 이름**을 사용하는 것이 성공의 열쇠!
