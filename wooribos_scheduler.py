#!/usr/bin/env python3
"""
Wooribos후방 스케줄러
매일 정해진 시간에 자동으로 프로그램을 실행합니다.
"""

import schedule
import time
import logging
from datetime import datetime
from wooribos_automation import WooribosAutomation

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('wooribos_scheduler.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class WooribosScheduler:
    def __init__(self, run_times=None):
        """
        초기화

        Args:
            run_times (list): 실행 시간 리스트 (예: ["09:00", "14:00"])
        """
        self.run_times = run_times or ["09:00"]  # 기본값: 매일 오전 9시
        self.automation = WooribosAutomation()

    def run_automation(self):
        """자동화 실행"""
        try:
            logger.info("="*60)
            logger.info(f"예약된 자동화 시작: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            logger.info("="*60)

            success = self.automation.run()

            if success:
                logger.info("✓ 예약된 작업이 성공적으로 완료되었습니다.")
            else:
                logger.error("✗ 예약된 작업 실행 중 오류가 발생했습니다.")

        except Exception as e:
            logger.error(f"✗ 스케줄러 실행 중 오류: {e}")

    def setup_schedule(self):
        """스케줄 설정"""
        logger.info("스케줄 설정 중...")

        for run_time in self.run_times:
            schedule.every().day.at(run_time).do(self.run_automation)
            logger.info(f"✓ 매일 {run_time}에 실행되도록 설정됨")

    def run(self):
        """스케줄러 실행"""
        logger.info("="*60)
        logger.info("Wooribos후방 스케줄러 시작")
        logger.info(f"시작 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        logger.info("="*60)

        self.setup_schedule()

        logger.info("\n예약된 작업:")
        for job in schedule.get_jobs():
            logger.info(f"  - {job}")

        logger.info("\n스케줄러가 실행 중입니다... (종료하려면 Ctrl+C)")
        logger.info("다음 실행 시간을 기다리는 중...\n")

        try:
            while True:
                schedule.run_pending()
                time.sleep(60)  # 1분마다 체크

        except KeyboardInterrupt:
            logger.info("\n\n스케줄러 종료")


def main():
    """메인 함수"""
    import sys
    import json

    print("="*60)
    print("Wooribos후방 스케줄러 설정")
    print("="*60)

    # 설정 파일에서 시간 읽기
    config_file = "wooribos_scheduler_config.json"

    if not os.path.exists(config_file):
        print("\n스케줄 설정 파일이 없습니다.")
        print("새로운 스케줄을 설정합니다.\n")

        # 사용자로부터 실행 시간 입력받기
        print("자동 실행 시간을 입력하세요 (24시간 형식, 예: 09:00)")
        print("여러 시간을 설정하려면 쉼표로 구분하세요 (예: 09:00,14:00,18:00)")
        print("(Enter를 누르면 기본값 09:00 사용)")

        time_input = input("\n실행 시간: ").strip()

        if time_input:
            run_times = [t.strip() for t in time_input.split(",")]
        else:
            run_times = ["09:00"]

        # 설정 저장
        config = {
            "run_times": run_times,
            "created_at": datetime.now().isoformat()
        }

        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, ensure_ascii=False, indent=2)

        print(f"\n✓ 설정이 '{config_file}' 파일로 저장되었습니다.")

    else:
        # 기존 설정 로드
        with open(config_file, 'r', encoding='utf-8') as f:
            config = json.load(f)
        run_times = config.get("run_times", ["09:00"])
        print(f"\n기존 설정을 로드했습니다: {', '.join(run_times)}")

    # 스케줄러 시작
    scheduler = WooribosScheduler(run_times=run_times)
    scheduler.run()


if __name__ == "__main__":
    import os
    main()
