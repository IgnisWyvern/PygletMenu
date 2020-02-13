import pyglet
from typing import Callable, Tuple, List


class Menu:
    def __init__(self, width, height, colour_tuple: Tuple[int, int, int] = (0, 0, 0)):
        self.batch = pyglet.graphics.Batch()
        self.fore = pyglet.graphics.OrderedGroup(2)
        self.mid = pyglet.graphics.OrderedGroup(1)
        self.back = pyglet.graphics.OrderedGroup(0)
        self.button_list: List[Menu.Button] = []
        self.text_list: List[Menu.TextTag] = []

        self.vertex_list = self.batch.add(4, pyglet.gl.GL_QUADS, self.back,
                                          ("v2i", (0, 0, 0, height, width,
                                           height, width, 0)),
                                          ("c3B", (colour_tuple * 4)))

    def add_button(self, text: str, x: int, y: int, width: int, height: int,
                   on_click: Callable,
                   colour_tuple: Tuple[int, int, int] = (0, 255, 255),
                   font_name: str = "Times New Roman",
                   font_size: int = 100):
        self.button_list.append(self.Button(text, x, y, width,
                                            height, on_click,
                                            colour_tuple=colour_tuple,
                                            fore_group=self.fore,
                                            mid_group=self.mid,
                                            batch=self.batch,
                                            font_name=font_name,
                                            font_size=font_size))

    def add_texttag(self, text: str, x: int, y: int, width: int, height: int,
                    colour_tuple: Tuple[int, int, int] = (0, 255, 255),
                    font_name: str = "Times New Roman",
                    font_size: int = 100):
        self.text_list.append(self.TextTag(text, x, y, width,
                                           height, colour_tuple, self.batch,
                                           self.fore, self.mid,
                                           font_name, font_size))

    def draw(self):
        """draw all the elements of the menu"""
        self.batch.draw()

    def on_click(self, x, y):
        for button in self.button_list:
            button.check_click(x, y)

    class TextTag:
        def __init__(self, text: str, x: int, y: int, width: int, height: int,
                     colour_tuple: Tuple[int, int, int], batch, fore_group,
                     mid_group, font_name: str, font_size: int):
            self.text = text
            self.x = x
            self.y = y
            self.height = height
            self.width = width
            self.font_size = font_size
            self.font_name = font_name
            self.batch = batch

            if isinstance(batch, pyglet.graphics.Batch):
                self.vertex_list = batch.add(4, pyglet.gl.GL_QUADS, mid_group,
                                        ("v2i", (x, y, x + width, y, x + width,
                                                 y + height,
                                                 x, y + height)),
                                        ("c3B", (colour_tuple * 4)))
            else:
                self.vertex_list = pyglet.graphics.vertex_list(4,
                                            ("v2i", (x, y, x + width, y, x +
                                                     width, y + height,
                                                     x, y + height)),
                                            ("c3B", (colour_tuple * 4)))

            self.label = pyglet.text.Label(self.text, font_name=self.font_name,
                                           font_size=self.font_size,
                                           group=fore_group,
                                           x=self.x + self.width/2,
                                           y=self.y + self.height/2,
                                           anchor_x="center",
                                           anchor_y="center",
                                           batch=self.batch)

        def draw(self):
            """For testing purposes as label will normally be drawn
            with batch function in menu"""
            self.vertex_list.draw(pyglet.gl.GL_QUADS)
            self.label.draw()

    class Button(TextTag):
        def __init__(self, text: str, x: int, y: int, width: int, height: int,
                     on_click: Callable,
                     colour_tuple: Tuple[int, int, int], batch, fore_group,
                     mid_group, font_name: str, font_size: int):
            super().__init__(text, x, y, width, height, colour_tuple, batch,
                             fore_group, mid_group, font_name, font_size)
            self.on_click = on_click

        def check_click(self, cur_x: int, cur_y: int):
            if(self.x < cur_x < self.x + self.width and
               self.y < cur_y < self.y + self.height):
                self.on_click()


def main():
    window = pyglet.window.Window()
    menu = Menu(window.width, window.height)
    menu.add_button("hi", 0, 0, 200, 200, lambda: print("hi"))
    menu.add_button("bye", 200, 200, 200, 200, lambda: print("bye"))
    menu.add_texttag("la", 400, 400, 100, 100)

    @window.event
    def on_mouse_press(x, y, button, modifiers):
        if button == pyglet.window.mouse.LEFT:
            menu.on_click(x, y)

    @window.event
    def on_draw():
        window.clear()
        menu.draw()
        menu.button_list[0].draw()
    pyglet.app.run()


if __name__ == "__main__":
    main()
