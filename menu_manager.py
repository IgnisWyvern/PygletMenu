import menu
from typing import Dict, Optional


class Menu_Manager:
    """
    A collection of menus and regulates the transition between them
    """
    def __init__(self, x: int, y: int, width: int, height: int):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.menu_pointer: Optional[menu.Menu] = None
        self.menu_dict: Dict[str, menu.Menu] = {}

    def draw(self):
        if isinstance(self.menu_pointer, menu.Menu):
            self.menu_pointer.draw()

    def change_menu(self, menu_name: str) -> bool:
        if menu_name == "None":
            self.menu_pointer = None
            return True
        temp_pointer = self.menu_dict.get(menu_name)
        if temp_pointer is not None:
            self.menu_pointer = temp_pointer
            return True
        return False


if __name__ == "__main__":
    pass
