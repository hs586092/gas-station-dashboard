@echo off
REM Wooribos후방 자동화 실행 배치 파일
REM Windows 작업 스케줄러에서 사용할 수 있습니다.

echo ============================================================
echo Wooribos후방 자동화 실행 중...
echo ============================================================
echo.

REM Python 경로 설정 (필요시 수정)
set PYTHON=python

REM 스크립트 디렉토리로 이동
cd /d "%~dp0"

REM Python 스크립트 실행
%PYTHON% wooribos_automation.py

echo.
echo ============================================================
echo 완료
echo ============================================================

REM 로그 확인을 위해 5초 대기
timeout /t 5

exit
