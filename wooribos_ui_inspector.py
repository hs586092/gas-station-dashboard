#!/usr/bin/env python3
"""
Wooribos후방 UI 검사 도구
프로그램의 UI 요소를 분석하여 자동화에 필요한 정보를 추출합니다.
"""

import os
import json
from datetime import datetime
from pywinauto import Desktop, Application
from pywinauto.findwindows import ElementNotFoundError


class UIInspector:
    def __init__(self, program_name="Wooribos후방"):
        """초기화"""
        self.program_name = program_name
        self.app = None
        self.main_window = None

    def connect_to_program(self):
        """실행 중인 프로그램에 연결"""
        try:
            desktop = Desktop(backend="uia")
            print(f"\n실행 중인 '{self.program_name}' 프로그램을 찾는 중...")

            # 프로그램 찾기
            self.main_window = desktop.window(title_re=f".*{self.program_name}.*")

            if self.main_window.exists():
                print(f"✓ 프로그램을 찾았습니다: {self.main_window.window_text()}")
                self.app = Application(backend="uia").connect(title_re=f".*{self.program_name}.*")
                return True
            else:
                print(f"✗ '{self.program_name}' 프로그램이 실행 중이지 않습니다.")
                print(f"프로그램을 먼저 실행한 후 다시 시도하세요.")
                return False

        except ElementNotFoundError:
            print(f"✗ '{self.program_name}' 프로그램을 찾을 수 없습니다.")
            print("\n실행 중인 모든 창 목록:")
            self.list_all_windows()
            return False
        except Exception as e:
            print(f"✗ 연결 실패: {e}")
            return False

    def list_all_windows(self):
        """실행 중인 모든 창 나열"""
        try:
            desktop = Desktop(backend="uia")
            windows = desktop.windows()

            print("\n" + "="*60)
            print("현재 실행 중인 모든 창:")
            print("="*60)

            for idx, window in enumerate(windows, 1):
                try:
                    title = window.window_text()
                    if title:  # 빈 제목 제외
                        print(f"{idx}. {title}")
                except:
                    pass

            print("="*60)

        except Exception as e:
            print(f"창 목록 가져오기 실패: {e}")

    def print_tree(self, element=None, depth=0, max_depth=5):
        """UI 트리 구조 출력"""
        if element is None:
            element = self.main_window

        if depth > max_depth:
            return

        try:
            # 요소 정보 가져오기
            control_type = element.element_info.control_type
            name = element.window_text()
            class_name = element.class_name()

            # 들여쓰기
            indent = "  " * depth

            # 정보 출력
            info = f"{indent}├─ [{control_type}]"
            if name:
                info += f" '{name}'"
            if class_name:
                info += f" ({class_name})"

            print(info)

            # 자식 요소들 재귀적으로 출력
            try:
                children = element.children()
                for child in children:
                    self.print_tree(child, depth + 1, max_depth)
            except:
                pass

        except Exception as e:
            pass

    def find_buttons(self):
        """모든 버튼 찾기"""
        print("\n" + "="*60)
        print("버튼 목록:")
        print("="*60)

        try:
            buttons = self.main_window.descendants(control_type="Button")
            for idx, btn in enumerate(buttons, 1):
                try:
                    name = btn.window_text()
                    if name:
                        print(f"{idx}. 버튼: '{name}'")
                except:
                    pass

            if not buttons:
                print("버튼을 찾을 수 없습니다.")

        except Exception as e:
            print(f"버튼 찾기 실패: {e}")

    def find_menus(self):
        """모든 메뉴 찾기"""
        print("\n" + "="*60)
        print("메뉴 목록:")
        print("="*60)

        try:
            # MenuBar 찾기
            menubars = self.main_window.descendants(control_type="MenuBar")
            for menubar in menubars:
                items = menubar.descendants(control_type="MenuItem")
                for idx, item in enumerate(items, 1):
                    try:
                        name = item.window_text()
                        if name:
                            print(f"{idx}. 메뉴: '{name}'")
                    except:
                        pass

            # MenuItem 직접 찾기
            menu_items = self.main_window.descendants(control_type="MenuItem")
            if menu_items:
                print("\n기타 메뉴 항목:")
                for idx, item in enumerate(menu_items, 1):
                    try:
                        name = item.window_text()
                        if name:
                            print(f"{idx}. '{name}'")
                    except:
                        pass

        except Exception as e:
            print(f"메뉴 찾기 실패: {e}")

    def find_lists(self):
        """모든 리스트/그리드 찾기"""
        print("\n" + "="*60)
        print("리스트/그리드 목록:")
        print("="*60)

        try:
            # List 찾기
            lists = self.main_window.descendants(control_type="List")
            for idx, lst in enumerate(lists, 1):
                try:
                    name = lst.window_text()
                    items = lst.children(control_type="ListItem")
                    print(f"{idx}. 리스트: '{name}' (항목: {len(items)}개)")

                    # 처음 5개 항목만 표시
                    for i, item in enumerate(items[:5], 1):
                        item_name = item.window_text()
                        if item_name:
                            print(f"    {i}. {item_name}")
                    if len(items) > 5:
                        print(f"    ... 외 {len(items) - 5}개")

                except:
                    pass

            # DataGrid 찾기
            grids = self.main_window.descendants(control_type="DataGrid")
            for idx, grid in enumerate(grids, 1):
                try:
                    name = grid.window_text()
                    items = grid.children()
                    print(f"{idx}. 데이터그리드: '{name}' (항목: {len(items)}개)")
                except:
                    pass

        except Exception as e:
            print(f"리스트 찾기 실패: {e}")

    def export_structure(self, filename="wooribos_ui_structure.json"):
        """UI 구조를 JSON 파일로 저장"""
        print(f"\n UI 구조를 '{filename}' 파일로 저장 중...")

        try:
            structure = {
                "timestamp": datetime.now().isoformat(),
                "program_name": self.program_name,
                "window_title": self.main_window.window_text(),
                "buttons": [],
                "menus": [],
                "lists": []
            }

            # 버튼 정보
            buttons = self.main_window.descendants(control_type="Button")
            for btn in buttons:
                try:
                    name = btn.window_text()
                    if name:
                        structure["buttons"].append({
                            "name": name,
                            "class": btn.class_name()
                        })
                except:
                    pass

            # 메뉴 정보
            menu_items = self.main_window.descendants(control_type="MenuItem")
            for item in menu_items:
                try:
                    name = item.window_text()
                    if name:
                        structure["menus"].append({
                            "name": name,
                            "class": item.class_name()
                        })
                except:
                    pass

            # 리스트 정보
            lists = self.main_window.descendants(control_type="List")
            for lst in lists:
                try:
                    name = lst.window_text()
                    items = lst.children(control_type="ListItem")
                    structure["lists"].append({
                        "name": name,
                        "item_count": len(items),
                        "class": lst.class_name()
                    })
                except:
                    pass

            # JSON 파일로 저장
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(structure, f, ensure_ascii=False, indent=2)

            print(f"✓ UI 구조가 '{filename}' 파일로 저장되었습니다.")
            return True

        except Exception as e:
            print(f"✗ 저장 실패: {e}")
            return False

    def interactive_menu(self):
        """대화형 메뉴"""
        while True:
            print("\n" + "="*60)
            print("Wooribos후방 UI 검사 도구")
            print("="*60)
            print("1. UI 트리 구조 보기")
            print("2. 모든 버튼 찾기")
            print("3. 모든 메뉴 찾기")
            print("4. 모든 리스트/그리드 찾기")
            print("5. UI 구조를 JSON 파일로 저장")
            print("6. 실행 중인 모든 창 보기")
            print("0. 종료")
            print("="*60)

            choice = input("\n선택 (0-6): ").strip()

            if choice == "1":
                print("\nUI 트리 구조:")
                print("="*60)
                self.print_tree()
            elif choice == "2":
                self.find_buttons()
            elif choice == "3":
                self.find_menus()
            elif choice == "4":
                self.find_lists()
            elif choice == "5":
                self.export_structure()
            elif choice == "6":
                self.list_all_windows()
            elif choice == "0":
                print("\n종료합니다.")
                break
            else:
                print("\n잘못된 선택입니다.")


def main():
    """메인 함수"""
    print("="*60)
    print("Wooribos후방 UI 검사 도구")
    print("="*60)
    print("\n이 도구는 Wooribos후방 프로그램의 UI 요소를 분석합니다.")
    print("자동화 스크립트 작성에 필요한 버튼, 메뉴 이름을 찾을 수 있습니다.")

    # 프로그램 이름 입력
    print("\n프로그램 창 제목에 포함된 텍스트를 입력하세요.")
    program_name = input("(기본값: Wooribos후방): ").strip()

    if not program_name:
        program_name = "Wooribos후방"

    # UI 검사기 시작
    inspector = UIInspector(program_name)

    if inspector.connect_to_program():
        inspector.interactive_menu()
    else:
        print("\n프로그램을 찾을 수 없습니다.")
        print("다음을 확인하세요:")
        print("1. Wooribos후방 프로그램이 실행 중인지 확인")
        print("2. 창 제목이 정확한지 확인")
        print("3. 위에 표시된 창 목록에서 정확한 이름 찾기")


if __name__ == "__main__":
    main()
