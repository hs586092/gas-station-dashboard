#!/usr/bin/env python3
"""
Wooribos후방 자동화 스크립트
매일 자동으로 프로그램을 실행하고 파일을 다운로드합니다.
"""

import os
import time
import json
import logging
from datetime import datetime
from pathlib import Path
from pywinauto import Application, Desktop
from pywinauto.findwindows import ElementNotFoundError
from pywinauto.timings import TimeoutError as PywinautoTimeoutError

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('wooribos_automation.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# 설정 파일 경로
CONFIG_FILE = "wooribos_config.json"


class WooribosAutomation:
    def __init__(self, config_file=CONFIG_FILE):
        """초기화"""
        self.config = self.load_config(config_file)
        self.app = None
        self.main_window = None
        self.download_count = 0

    def load_config(self, config_file):
        """설정 파일 로드"""
        if os.path.exists(config_file):
            with open(config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            logger.warning(f"설정 파일을 찾을 수 없습니다: {config_file}")
            return self.get_default_config()

    def get_default_config(self):
        """기본 설정 반환"""
        return {
            "program_path": r"C:\Program Files\Wooribos\Wooribos.exe",  # 프로그램 경로
            "program_name": "Wooribos후방",  # 프로그램 창 제목
            "download_folder": str(Path.home() / "Downloads"),  # 다운로드 폴더
            "wait_time": 2,  # 각 동작 후 대기 시간 (초)
            "max_retries": 3,  # 최대 재시도 횟수
            "menu_clicks": [
                # 메뉴 클릭 순서 (실제 메뉴명으로 수정 필요)
                {"type": "menu", "name": "파일", "description": "파일 메뉴 클릭"},
                {"type": "menu", "name": "데이터", "description": "데이터 메뉴 클릭"},
                {"type": "menu", "name": "다운로드", "description": "다운로드 메뉴 클릭"},
                # 더 많은 메뉴 단계 추가 가능
            ],
            "download_settings": {
                "file_pattern": "*",  # 다운로드할 파일 패턴
                "auto_download_all": True,  # 모든 파일 자동 다운로드
                "max_files": 100  # 최대 다운로드 파일 수
            }
        }

    def save_config(self, config_file=CONFIG_FILE):
        """설정 파일 저장"""
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, ensure_ascii=False, indent=2)
        logger.info(f"설정 파일 저장됨: {config_file}")

    def start_program(self):
        """프로그램 시작"""
        try:
            program_path = self.config.get("program_path")
            logger.info(f"프로그램 시작: {program_path}")

            # 이미 실행 중인지 확인
            try:
                desktop = Desktop(backend="uia")
                existing_window = desktop.window(title_re=f".*{self.config['program_name']}.*")
                if existing_window.exists():
                    logger.info("프로그램이 이미 실행 중입니다.")
                    self.app = Application(backend="uia").connect(title_re=f".*{self.config['program_name']}.*")
                    self.main_window = self.app.window(title_re=f".*{self.config['program_name']}.*")
                    return True
            except ElementNotFoundError:
                pass

            # 프로그램 시작
            self.app = Application(backend="uia").start(program_path)
            time.sleep(self.config.get("wait_time", 2))

            # 메인 창 찾기
            self.main_window = self.app.window(title_re=f".*{self.config['program_name']}.*")
            self.main_window.wait('visible', timeout=30)

            logger.info("✓ 프로그램 시작 완료")
            return True

        except Exception as e:
            logger.error(f"✗ 프로그램 시작 실패: {e}")
            return False

    def wait_and_log(self, message, wait_time=None):
        """대기 및 로그"""
        if wait_time is None:
            wait_time = self.config.get("wait_time", 2)
        logger.info(message)
        time.sleep(wait_time)

    def click_menu_sequence(self):
        """메뉴 순차적으로 클릭"""
        try:
            menu_clicks = self.config.get("menu_clicks", [])

            for idx, menu_item in enumerate(menu_clicks, 1):
                self.wait_and_log(f"[{idx}/6] {menu_item['description']}")

                try:
                    # 메뉴 아이템 찾기 시도 (여러 방법)
                    menu_name = menu_item.get("name")

                    # 방법 1: 이름으로 찾기
                    try:
                        element = self.main_window.child_window(title=menu_name, control_type="MenuItem")
                        if element.exists():
                            element.click_input()
                            continue
                    except:
                        pass

                    # 방법 2: 버튼으로 찾기
                    try:
                        element = self.main_window.child_window(title=menu_name, control_type="Button")
                        if element.exists():
                            element.click_input()
                            continue
                    except:
                        pass

                    # 방법 3: 텍스트가 포함된 모든 요소 찾기
                    try:
                        element = self.main_window.child_window(title_re=f".*{menu_name}.*")
                        if element.exists():
                            element.click_input()
                            continue
                    except:
                        pass

                    logger.warning(f"메뉴를 찾을 수 없습니다: {menu_name}")
                    logger.info("UI 검사 도구를 사용하여 정확한 이름을 확인하세요.")

                except Exception as e:
                    logger.error(f"메뉴 클릭 실패 ({menu_name}): {e}")
                    return False

            logger.info("✓ 메뉴 클릭 완료")
            return True

        except Exception as e:
            logger.error(f"✗ 메뉴 클릭 중 오류: {e}")
            return False

    def download_files(self):
        """파일 다운로드"""
        try:
            max_files = self.config.get("download_settings", {}).get("max_files", 100)
            logger.info(f"파일 다운로드 시작 (최대 {max_files}개)")

            downloaded = 0

            # 다운로드 가능한 모든 항목 찾기
            # 실제 프로그램 구조에 따라 수정 필요
            try:
                # 리스트뷰, 데이터그리드 등에서 항목 찾기
                list_view = self.main_window.child_window(control_type="List")
                if not list_view.exists():
                    list_view = self.main_window.child_window(control_type="DataGrid")

                if list_view.exists():
                    # 모든 리스트 아이템 가져오기
                    items = list_view.children(control_type="ListItem")
                    logger.info(f"발견된 항목: {len(items)}개")

                    for idx, item in enumerate(items[:max_files], 1):
                        try:
                            # 항목 선택
                            item.click_input()
                            self.wait_and_log(f"[{idx}/{min(len(items), max_files)}] 파일 선택", 0.5)

                            # 다운로드 버튼 찾기 및 클릭
                            download_btn = self.main_window.child_window(title_re=".*다운로드.*", control_type="Button")
                            if download_btn.exists():
                                download_btn.click_input()
                                downloaded += 1
                                self.wait_and_log(f"✓ 다운로드 완료 ({downloaded}개)", 1)

                        except Exception as e:
                            logger.warning(f"항목 다운로드 실패: {e}")
                            continue

                else:
                    logger.warning("다운로드 가능한 항목 목록을 찾을 수 없습니다.")
                    logger.info("대안: 반복 클릭 방식 사용")
                    downloaded = self.download_files_by_repetition(max_files)

            except Exception as e:
                logger.warning(f"리스트 방식 실패: {e}")
                logger.info("대안: 반복 클릭 방식 사용")
                downloaded = self.download_files_by_repetition(max_files)

            logger.info(f"✓ 총 {downloaded}개 파일 다운로드 완료")
            self.download_count = downloaded
            return True

        except Exception as e:
            logger.error(f"✗ 파일 다운로드 실패: {e}")
            return False

    def download_files_by_repetition(self, max_files):
        """반복 클릭으로 파일 다운로드"""
        downloaded = 0

        for i in range(max_files):
            try:
                # 다운로드 버튼 찾기
                download_btn = self.main_window.child_window(title_re=".*다운로드.*", control_type="Button")

                if not download_btn.exists():
                    logger.info("더 이상 다운로드할 파일이 없습니다.")
                    break

                download_btn.click_input()
                downloaded += 1
                self.wait_and_log(f"✓ 다운로드 ({downloaded}개)", 1)

                # "다음" 버튼이 있으면 클릭
                try:
                    next_btn = self.main_window.child_window(title_re=".*다음.*", control_type="Button")
                    if next_btn.exists():
                        next_btn.click_input()
                        time.sleep(0.5)
                except:
                    pass

            except Exception as e:
                logger.warning(f"다운로드 중단: {e}")
                break

        return downloaded

    def close_program(self):
        """프로그램 종료"""
        try:
            if self.main_window:
                logger.info("프로그램 종료 중...")
                self.main_window.close()
                time.sleep(2)
                logger.info("✓ 프로그램 종료 완료")
            return True
        except Exception as e:
            logger.warning(f"프로그램 종료 중 오류: {e}")
            return False

    def run(self):
        """전체 자동화 실행"""
        logger.info("="*60)
        logger.info("Wooribos후방 자동화 시작")
        logger.info(f"시작 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        logger.info("="*60)

        try:
            # 1. 프로그램 시작
            if not self.start_program():
                logger.error("프로그램 시작 실패. 종료합니다.")
                return False

            # 2. 메뉴 클릭
            if not self.click_menu_sequence():
                logger.error("메뉴 클릭 실패. 종료합니다.")
                self.close_program()
                return False

            # 3. 파일 다운로드
            if not self.download_files():
                logger.error("파일 다운로드 실패.")
                self.close_program()
                return False

            # 4. 프로그램 종료
            self.close_program()

            logger.info("="*60)
            logger.info(f"✓ 자동화 완료! 다운로드된 파일: {self.download_count}개")
            logger.info(f"종료 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            logger.info("="*60)

            return True

        except Exception as e:
            logger.error(f"✗ 자동화 실행 중 오류: {e}")
            try:
                self.close_program()
            except:
                pass
            return False


def main():
    """메인 함수"""
    automation = WooribosAutomation()

    # 설정 파일이 없으면 생성
    if not os.path.exists(CONFIG_FILE):
        logger.info("설정 파일이 없습니다. 기본 설정 파일을 생성합니다.")
        automation.save_config()
        logger.info(f"'{CONFIG_FILE}' 파일을 수정한 후 다시 실행하세요.")
        return

    # 자동화 실행
    automation.run()


if __name__ == "__main__":
    main()
