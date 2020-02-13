import menu
from typing import Dict


class Menu_Manager:
    """
    A collection of menus and regulates the transition between them
    """
    def __init__(self, x: int, y: int, width: int, height: int):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.menu_pointer = None
        self.menu_dict: Dict[str, menu.Menu] = {}

    def draw(self):
        if self.menu_pointer is menu.Menu:
            self.menu_pointer.draw()
