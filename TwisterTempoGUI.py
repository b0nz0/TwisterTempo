import pyglet
from pyglet import gl, shapes, text, image, resource, sprite
from pyglet.window import FPSDisplay


class TwisterTempoGUI(object):
    WINDOW_HEIGHT = 600
    WINDOW_WIDTH = 800
    CIRCLES_RADIUS = 190
    LARGE_CIRCLES_RADIUS = 225

    def __init__(self):
        config = gl.Config(double_buffer=True)
        self.window = pyglet.window.Window(height=TwisterTempoGUI.WINDOW_HEIGHT,
                                           width=TwisterTempoGUI.WINDOW_WIDTH,
                                           caption='TwisterTempo', config=config)
        gl.glEnable(gl.GL_BLEND)
        gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)

        resource.path = ['resources']
        resource.reindex()

        self._right_circle_pos = (self.window.width // 4 * 3 - TwisterTempoGUI.CIRCLES_RADIUS,
                                  self.window.height // 2 - TwisterTempoGUI.CIRCLES_RADIUS)
        self._left_circle_pos = (self.window.width // 4 - TwisterTempoGUI.CIRCLES_RADIUS,
                                 self.window.height // 2 - TwisterTempoGUI.CIRCLES_RADIUS)
        self._large_circle_pos = (self.window.width // 2 - TwisterTempoGUI.LARGE_CIRCLES_RADIUS,
                                  self.window.height // 2 - TwisterTempoGUI.LARGE_CIRCLES_RADIUS)

        self._pause_label = text.Label('pause',
                                       font_name='Courier',
                                       font_size=36,
                                       x=self.window.width // 2, y=self.window.height // 10,
                                       anchor_x='center', anchor_y='center',
                                       color=(255, 255, 255, 255))

        self._cloud_image = resource.image('cloud_white.png')
        # self._cloud_image.anchor_x = self._cloud_image.width // 2
        # self._cloud_image.anchor_y = self._cloud_image.height // 2

        sprite_sheet = pyglet.resource.image('tt_animation.png')
        image_grid = pyglet.image.ImageGrid(sprite_sheet, rows=4, columns=4)

        self._green_circle_animation = pyglet.image.Animation.from_image_sequence([image_grid[0, 0],
                                                                                   image_grid[0, 1],
                                                                                   image_grid[0, 2],
                                                                                   image_grid[0, 3],
                                                                                   image_grid[0, 2]],
                                                                                  duration=0.04, loop=False)
        self._yellow_circle_animation = pyglet.image.Animation.from_image_sequence([image_grid[1, 0],
                                                                                    image_grid[1, 1],
                                                                                    image_grid[1, 2],
                                                                                    image_grid[1, 3],
                                                                                    image_grid[1, 2]],
                                                                                   duration=0.04, loop=False)
        self._blue_circle_animation = pyglet.image.Animation.from_image_sequence([image_grid[2, 0],
                                                                                  image_grid[2, 1],
                                                                                  image_grid[2, 2],
                                                                                  image_grid[2, 3],
                                                                                  image_grid[2, 2]],
                                                                                 duration=0.04, loop=False)
        self._red_circle_animation = pyglet.image.Animation.from_image_sequence([image_grid[3, 0],
                                                                                 image_grid[3, 1],
                                                                                 image_grid[3, 2],
                                                                                 image_grid[3, 3],
                                                                                 image_grid[3, 2]],
                                                                                duration=0.04, loop=False)
        self._right_circle_sprite = None
        self._left_circle_sprite = None

        sprite_large_sheet = pyglet.resource.image('tt_animation_large.png')
        image_large_grid = pyglet.image.ImageGrid(sprite_large_sheet, rows=4, columns=4)

        self._green_large_circle_animation = pyglet.image.Animation.from_image_sequence([image_large_grid[0, 0],
                                                                                         image_large_grid[0, 1],
                                                                                         image_large_grid[0, 2],
                                                                                         image_large_grid[0, 3],
                                                                                         image_large_grid[0, 2]],
                                                                                        duration=0.04, loop=False)
        self._yellow_large_circle_animation = pyglet.image.Animation.from_image_sequence([image_large_grid[1, 0],
                                                                                          image_large_grid[1, 1],
                                                                                          image_large_grid[1, 2],
                                                                                          image_large_grid[1, 3],
                                                                                          image_large_grid[1, 2]],
                                                                                         duration=0.04, loop=False)
        self._blue_large_circle_animation = pyglet.image.Animation.from_image_sequence([image_large_grid[2, 0],
                                                                                        image_large_grid[2, 1],
                                                                                        image_large_grid[2, 2],
                                                                                        image_large_grid[2, 3],
                                                                                        image_large_grid[2, 2]],
                                                                                       duration=0.04, loop=False)
        self._red_large_circle_animation = pyglet.image.Animation.from_image_sequence([image_large_grid[3, 0],
                                                                                       image_large_grid[3, 1],
                                                                                       image_large_grid[3, 2],
                                                                                       image_large_grid[3, 3],
                                                                                       image_large_grid[3, 2]],
                                                                                      duration=0.04, loop=False)
        self._large_circle_sprite = None

        self.show_pause = False
        self._draw_on_air = (False, 0, 0)
        self._animate = False
        self._show_circles = True
        self._show_large_circle = False

        self._fps_display = None
        # uncomment if you want to see the FPS on screen
        # self._fps_display = FPSDisplay(self.window)

    def set_right_color(self, color, on_air=False):
        # self._right_circle.color = color
        if color == 'GREEN':
            self._right_circle_sprite = sprite.Sprite(self._green_circle_animation)
        elif color == 'YELLOW':
            self._right_circle_sprite = sprite.Sprite(self._yellow_circle_animation)
        elif color == 'BLUE':
            self._right_circle_sprite = sprite.Sprite(self._blue_circle_animation)
        elif color == 'RED':
            self._right_circle_sprite = sprite.Sprite(self._red_circle_animation)
        else:
            raise RuntimeError("No valid color given: %s" % str(color))
        self._right_circle_sprite.position = self._right_circle_pos
        self._show_circles = True
        self._show_large_circle = False
        if on_air:
            self._draw_on_air = (True, self._right_circle_pos[0], self._right_circle_pos[1])
        else:
            self._draw_on_air = (False, 0, 0)

    def set_left_color(self, color, on_air=False):
        # self._left_circle.color = color
        if color == 'GREEN':
            self._left_circle_sprite = sprite.Sprite(self._green_circle_animation)
        elif color == 'YELLOW':
            self._left_circle_sprite = sprite.Sprite(self._yellow_circle_animation)
        elif color == 'BLUE':
            self._left_circle_sprite = sprite.Sprite(self._blue_circle_animation)
        elif color == 'RED':
            self._left_circle_sprite = sprite.Sprite(self._red_circle_animation)
        else:
            raise RuntimeError("No valid color given: %s" % str(color))
        self._left_circle_sprite.position = self._left_circle_pos
        self._show_circles = True
        self._show_large_circle = False
        if on_air:
            self._draw_on_air = (True, self._left_circle_pos[0], self._left_circle_pos[1])
        else:
            self._draw_on_air = (False, 0, 0)

    def set_large_color(self, color):
        if color == 'GREEN':
            self._large_circle_sprite = sprite.Sprite(self._green_large_circle_animation)
        elif color == 'YELLOW':
            self._large_circle_sprite = sprite.Sprite(self._yellow_large_circle_animation)
        elif color == 'BLUE':
            self._large_circle_sprite = sprite.Sprite(self._blue_large_circle_animation)
        elif color == 'RED':
            self._large_circle_sprite = sprite.Sprite(self._red_large_circle_animation)
        else:
            raise RuntimeError("No valid color given: %s" % str(color))
        self._large_circle_sprite.position = self._large_circle_pos
        self._show_circles = False
        self._show_large_circle = True

    def draw(self):
        # print("in draw @ %f" % perf_counter())
        self.window.clear()

        if self._show_circles:
            self._right_circle_sprite.draw()
            self._left_circle_sprite.draw()
            # if a foot is on air
            (o, x, y) = self._draw_on_air
            if o:
                self._cloud_image.blit(x, y, 0)
        elif self._show_large_circle:
            self._large_circle_sprite.draw()
        # if paused
        if self.show_pause:
            (r, g, b, a) = self._pause_label.color
            r = r - 10
            if r < 0:
                r = 255
            self._pause_label.color = (r, g, b, a)
            self._pause_label.draw()

        if self._fps_display:
            self._fps_display.draw()
