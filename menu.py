import pyglet
from typing import Callable, Tuple, Dict


class Menu:
    """
    A collection of buttons and text labels
    that takes place in a 100x100 that scales with the screen
    """
    def __init__(self, x: int, y: int, width: int, height: int,
                 colour_tuple: Tuple[int, int, int] = (255, 0, 0),
                 font_name=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.multiplier = (width//100, height//100)
        self.offset = (x + ((width % 100)//2), y + ((height % 100)//2))

        self.batch = pyglet.graphics.Batch()
        self.user_fore = pyglet.graphics.OrderedGroup(3)
        self.fore = pyglet.graphics.OrderedGroup(2)
        self.mid = pyglet.graphics.OrderedGroup(1)
        self.back = pyglet.graphics.OrderedGroup(0)

        # self.font = pyglet.font.load(font_name, 50)
        self.font = font_name 
        self.button_dict: Dict[str, Menu.Button] = {}
        self.texttag_dict: Dict[str, Menu.TextTag] = {}

        self.vertex_list = self.batch.add(4, pyglet.gl.GL_QUADS, self.back,
                                          ("v2i", (x, y, x, y + height,
                                           x + width, y + height, x + width,
                                           y)),
                                          ("c3B", (colour_tuple * 4)))

    def add_button(self, name: str, text: str, x: int, y: int, width: int,
                   height: int, on_click: Callable,
                   colour_tuple: Tuple[int, int, int] = (0, 255, 255),):

        if name not in self.button_dict:
            self.button_dict[name] = self.Button(text, x, y, width,
                                                 height, on_click,
                                                 colour_tuple, self.batch,
                                                 self.fore, self.mid,
                                                 self.multiplier, self.offset,
                                                 self.font)
            return self.button_dict[name]
        raise Exception("A button of that name already exists")

    def add_texttag(self, name: str, text: str, x: int, y: int, width: int,
                    height: int,
                    colour_tuple: Tuple[int, int, int] = (0, 255, 255)):
        if name not in self.texttag_dict:
            self.texttag_dict[name] = self.TextTag(text, x, y, width,
                                                   height, colour_tuple,
                                                   self.batch, self.fore,
                                                   self.mid, self.multiplier,
                                                   self.offset, self.font)
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

    def resize(self, x: int, y: int, width: int, height: int):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.multiplier = (width//100, height//100)
        self.offset = (((width % 100)//2), ((height % 100)//2))

        self.vertex_list.vertices = [x, y, x, y + height, x + width, y +
                                     height, x + width, y]

        for button in self.button_dict.values():
            button.resize(self.multiplier, self.offset)

        for texttag in self.texttag_dict.values():
            texttag.resize(self.multiplier, self.offset)

    class TextTag:
        def __init__(self, text: str, x: int, y: int, width: int, height: int,
                     colour_tuple: Tuple[int, int, int], batch, fore_group,
                     mid_group, multiplier, offset, font_name: str):
            self.text = text
            self.x = x
            self.y = y
            self.height = height
            self.width = width
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
                                           font_size=min(self.width,
                                           self.height)*min(mul_x/2, mul_y),
                                           group=fore_group,
                                           x=x + width//2,
                                           y=y + height//2,
                                           anchor_x="center",
                                           anchor_y="center",
                                           batch=self.batch)

        def draw(self):
            """For testing purposes as label will normally be drawn
            with batch function in menu"""
            self.vertex_list.draw(pyglet.gl.GL_QUADS)
            self.label.draw()

        def resize(self, multiplier, offset):
            mul_x, mul_y = multiplier
            off_x, off_y = offset

            x = self.x * mul_x
            x += off_x
            width = self.width * mul_x
            y = self.y * mul_y
            y += off_y
            height = self.height * mul_y

            self.vertex_list.vertices = [x, y, x + width, y, x + width,
                                         y + height, x, y + height]
            self.label.x = x + width//2
            self.label.y = y + height//2
            # add font size changing
            self.label.font_size=min(self.width, self.height) * min(mul_x /2,
                                                                         mul_y)

    class Button(TextTag):
        def __init__(self, text: str, x: int, y: int, width: int, height: int,
                     on_click: Callable,
                     colour_tuple: Tuple[int, int, int], batch, fore_group,
                     mid_group, multiplier, offset, font_name: str):

            super().__init__(text, x, y, width, height, colour_tuple, batch,
                             fore_group, mid_group, multiplier, offset,
                             font_name)
            self.on_click = on_click

        def check_click(self, cur_x: int, cur_y: int):
            if(self.x < cur_x < self.x + self.width and
               self.y < cur_y < self.y + self.height):
                self.on_click()


def main():
    window = pyglet.window.Window(resizable=True)
    menu = Menu(100, 100, 700, 700)
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

    @window.event
    def on_resize(x, y):
        menu.resize(0, 0, x, y)
    pyglet.app.run()


if __name__ == "__main__":
    main()
