import pyglet
from typing import Callable, Tuple, Dict


class Menu:
    """
    A collection of buttons and text labels
    that takes place in a 100x100 that scales with the screen
    """
    def __init__(self, x: int, y: int, width: int, height: int,
                 colour_tuple: Tuple[int, int, int] = (0, 0, 0)):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.multiplier = (width//100, height//100)
        self.offset = (((width % 100)//2), ((height % 100)//2))

        self.batch = pyglet.graphics.Batch()
        self.user_fore = pyglet.graphics.OrderedGroup(3)
        self.fore = pyglet.graphics.OrderedGroup(2)
        self.mid = pyglet.graphics.OrderedGroup(1)
        self.back = pyglet.graphics.OrderedGroup(0)

        self.button_dict: Dict[str, Menu.Button] = {}
        self.texttag_dict: Dict[str, Menu.TextTag] = {}

        self.vertex_list = self.batch.add(4, pyglet.gl.GL_QUADS, self.back,
                                          ("v2i", (x, y, x, y + height,
                                           x + width, y + height, x + width,
                                           y)),
                                          ("c3B", (colour_tuple * 4)))

    def add_button(self, name: str, text: str, x: int, y: int, width: int,
                   height: int, on_click: Callable,
                   colour_tuple: Tuple[int, int, int] = (0, 255, 255),
                   font_name: str = "Times New Roman",
                   font_size: int = 100):
        if name not in self.button_dict:
            self.button_dict[name] = self.Button(text, x, y, width,
                                                 height, on_click,
                                                 colour_tuple, self.batch,
                                                 self.fore, self.mid,
                                                 self.multiplier, self.offset,
                                                 font_name, font_size)
            return self.button_dict[name]
        raise Exception("A button of that name already exists")

    def add_texttag(self, name: str, text: str, x: int, y: int, width: int,
                    height: int,
                    colour_tuple: Tuple[int, int, int] = (0, 255, 255),
                    font_name: str = "Times New Roman",
                    font_size: int = 100):
        if name not in self.texttag_dict:
            self.texttag_dict[name] = self.TextTag(text, x, y, width,
                                                   height, colour_tuple,
                                                   self.batch, self.fore,
                                                   self.mid, self.multiplier,
                                                   self.offset, font_name,
                                                   font_size)
            return self.texttag_dict[name]
        raise Exception("A texttag of that name already exits")

    def draw(self):
        """draw all the elements of the menu"""
        self.batch.draw()

    def on_click(self, x, y):
        """
        Check all the buttons for if the cursor was in their domain
        """
        mul_x, mul_y = self.multiplier
        off_x, off_y = self.offset
        x -= off_x
        x /= mul_x
        y -= off_y
        y /= mul_y
        for button in self.button_dict.values():
            button.check_click(x, y)

    def resize_contents(self):
        for button in self.button_dict.values():
            button.resize(self.multiplier)

        for texttag in self.texttag_dict.values():
            texttag.resize(self.multiplier)

    class TextTag:
        def __init__(self, text: str, x: int, y: int, width: int, height: int,
                     colour_tuple: Tuple[int, int, int], batch, fore_group,
                     mid_group, multiplier, offset, font_name: str,
                     font_size: int):
            self.text = text
            self.x = x
            self.y = y
            self.height = height
            self.width = width
            self.font_size = font_size
            self.font_name = font_name
            self.batch = batch

            mul_x, mul_y = multiplier
            off_x, off_y = offset

            x *= mul_x
            x += off_x
            width *= mul_x
            y *= mul_y
            y += off_y
            height *= mul_y

            self.vertex_list = batch.add(4, pyglet.gl.GL_QUADS, mid_group,
                                         ("v2i", (x, y, x + width, y, x +
                                          width, y + height, x,
                                          y + height)),
                                         ("c3B", (colour_tuple * 4)))

            self.label = pyglet.text.Label(self.text, font_name=self.font_name,
                                           font_size=self.font_size,
                                           group=fore_group,
                                           x=x + width/2,
                                           y=y + height/2,
                                           anchor_x="center",
                                           anchor_y="center",
                                           batch=self.batch)

        def draw(self):
            """For testing purposes as label will normally be drawn
            with batch function in menu"""
            self.vertex_list.draw(pyglet.gl.GL_QUADS)
            self.label.draw()

        def resize(self, multiplier, offset):
            pass

    class Button(TextTag):
        def __init__(self, text: str, x: int, y: int, width: int, height: int,
                     on_click: Callable,
                     colour_tuple: Tuple[int, int, int], batch, fore_group,
                     mid_group, multiplier, offset, font_name: str,
                     font_size: int):

            super().__init__(text, x, y, width, height, colour_tuple, batch,
                             fore_group, mid_group, multiplier, offset,
                             font_name, font_size)
            self.on_click = on_click

        def check_click(self, cur_x: int, cur_y: int):
            if(self.x < cur_x < self.x + self.width and
               self.y < cur_y < self.y + self.height):
                self.on_click()


def main():
    window = pyglet.window.Window(resizable=True)
    menu = Menu(0, 0, window.width, window.height)
    menu.add_button("he", "hi", 0, 0, 25, 25, lambda: print("hi"))
    menu.add_button("hi", "bye", 25, 25, 25, 45, lambda: print("bye"))
    menu.add_texttag("hl", "la", 50, 70, 50, 30)
    @window.event
    def on_mouse_press(x, y, button, modifiers):
        if button == pyglet.window.mouse.LEFT:
            menu.on_click(x, y)

    @window.event
    def on_draw():
        window.clear()
        menu.draw()

    pyglet.app.run()


if __name__ == "__main__":
    main()
