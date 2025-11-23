#!/usr/bin/env python3
"""
Google Drive Desktop Uploader
자동으로 바탕화면의 파일을 구글 드라이브에 업로드합니다.
"""

import os
import time
import json
from pathlib import Path
from datetime import datetime
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from googleapiclient.errors import HttpError
import pickle

# Google Drive API 스코프
SCOPES = ['https://www.googleapis.com/auth/drive.file']

# 설정
DESKTOP_PATH = str(Path.home() / "Desktop")  # 바탕화면 경로
UPLOAD_FOLDER_NAME = "Desktop Uploads"  # 구글 드라이브 폴더 이름
CHECK_INTERVAL = 60  # 파일 체크 간격 (초)
UPLOAD_LOG_FILE = "upload_log.json"


class GoogleDriveUploader:
    def __init__(self):
        self.service = None
        self.upload_folder_id = None
        self.uploaded_files = self.load_upload_log()

    def authenticate(self):
        """Google Drive API 인증"""
        creds = None

        # token.pickle 파일에 저장된 인증 정보 확인
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)

        # 유효한 인증 정보가 없으면 로그인 필요
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)

            # 인증 정보 저장
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)

        self.service = build('drive', 'v3', credentials=creds)
        print("✓ Google Drive 인증 완료")

    def get_or_create_upload_folder(self):
        """업로드용 폴더 가져오기 또는 생성"""
        try:
            # 기존 폴더 검색
            response = self.service.files().list(
                q=f"name='{UPLOAD_FOLDER_NAME}' and mimeType='application/vnd.google-apps.folder' and trashed=false",
                spaces='drive',
                fields='files(id, name)'
            ).execute()

            folders = response.get('files', [])

            if folders:
                self.upload_folder_id = folders[0]['id']
                print(f"✓ 기존 폴더 사용: {UPLOAD_FOLDER_NAME}")
            else:
                # 새 폴더 생성
                file_metadata = {
                    'name': UPLOAD_FOLDER_NAME,
                    'mimeType': 'application/vnd.google-apps.folder'
                }
                folder = self.service.files().create(
                    body=file_metadata,
                    fields='id'
                ).execute()
                self.upload_folder_id = folder.get('id')
                print(f"✓ 새 폴더 생성: {UPLOAD_FOLDER_NAME}")

        except HttpError as error:
            print(f"✗ 폴더 생성/검색 오류: {error}")

    def load_upload_log(self):
        """업로드 기록 로드"""
        if os.path.exists(UPLOAD_LOG_FILE):
            with open(UPLOAD_LOG_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}

    def save_upload_log(self):
        """업로드 기록 저장"""
        with open(UPLOAD_LOG_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.uploaded_files, f, ensure_ascii=False, indent=2)

    def upload_file(self, file_path):
        """파일을 구글 드라이브에 업로드"""
        try:
            file_name = os.path.basename(file_path)
            file_metadata = {
                'name': file_name,
                'parents': [self.upload_folder_id]
            }

            media = MediaFileUpload(file_path, resumable=True)
            file = self.service.files().create(
                body=file_metadata,
                media_body=media,
                fields='id, webViewLink'
            ).execute()

            # 업로드 기록 저장
            file_stat = os.stat(file_path)
            self.uploaded_files[file_path] = {
                'drive_id': file.get('id'),
                'upload_time': datetime.now().isoformat(),
                'file_size': file_stat.st_size,
                'modified_time': file_stat.st_mtime,
                'web_link': file.get('webViewLink')
            }
            self.save_upload_log()

            print(f"✓ 업로드 완료: {file_name}")
            print(f"  링크: {file.get('webViewLink')}")
            return True

        except HttpError as error:
            print(f"✗ 업로드 실패 ({file_name}): {error}")
            return False

    def should_upload(self, file_path):
        """파일을 업로드해야 하는지 확인"""
        # 숨김 파일 제외
        if os.path.basename(file_path).startswith('.'):
            return False

        # 이 스크립트와 관련 파일들 제외
        excluded_files = {
            'token.pickle',
            'credentials.json',
            UPLOAD_LOG_FILE,
            'google_drive_uploader.py',
            'config.json'
        }
        if os.path.basename(file_path) in excluded_files:
            return False

        # 이미 업로드된 파일인지 확인
        if file_path in self.uploaded_files:
            # 파일이 수정되었는지 확인
            current_mtime = os.path.getmtime(file_path)
            uploaded_mtime = self.uploaded_files[file_path].get('modified_time', 0)

            if current_mtime <= uploaded_mtime:
                return False

        return True

    def scan_and_upload(self):
        """바탕화면 스캔 및 업로드"""
        if not os.path.exists(DESKTOP_PATH):
            print(f"✗ 바탕화면 경로를 찾을 수 없습니다: {DESKTOP_PATH}")
            return

        files_to_upload = []

        # 바탕화면의 모든 파일 검사
        for item in os.listdir(DESKTOP_PATH):
            file_path = os.path.join(DESKTOP_PATH, item)

            # 디렉토리는 제외 (파일만 업로드)
            if os.path.isfile(file_path) and self.should_upload(file_path):
                files_to_upload.append(file_path)

        if files_to_upload:
            print(f"\n발견된 새 파일: {len(files_to_upload)}개")
            for file_path in files_to_upload:
                self.upload_file(file_path)
        else:
            print(".", end="", flush=True)

    def run_continuous(self):
        """지속적으로 바탕화면 모니터링"""
        print(f"\n{'='*60}")
        print("Google Drive 자동 업로더 시작")
        print(f"{'='*60}")
        print(f"모니터링 경로: {DESKTOP_PATH}")
        print(f"업로드 폴더: {UPLOAD_FOLDER_NAME}")
        print(f"체크 간격: {CHECK_INTERVAL}초")
        print(f"{'='*60}\n")

        self.authenticate()
        self.get_or_create_upload_folder()

        print("\n모니터링 시작... (종료하려면 Ctrl+C)")

        try:
            while True:
                self.scan_and_upload()
                time.sleep(CHECK_INTERVAL)
        except KeyboardInterrupt:
            print("\n\n프로그램 종료")

    def run_once(self):
        """한 번만 실행 (스캔 및 업로드)"""
        print(f"\n{'='*60}")
        print("Google Drive 업로더 - 일회성 실행")
        print(f"{'='*60}\n")

        self.authenticate()
        self.get_or_create_upload_folder()
        self.scan_and_upload()

        print("\n완료!")


def main():
    import sys

    uploader = GoogleDriveUploader()

    # 명령줄 인수 확인
    if len(sys.argv) > 1 and sys.argv[1] == '--once':
        uploader.run_once()
    else:
        uploader.run_continuous()


if __name__ == "__main__":
    main()
