import arcade
import Menu

screen_w = 1280
screen_h = 720
screen_t = "Platformer"

MOVEMENT_SPEED = 8

GRAVITY = 1
player_jump_speed = 18

# How many pixels to keep as a minimum margin between the character
# and the edge of the screen.
LEFT_VIEWPORT_MARGIN = 100
RIGHT_VIEWPORT_MARGIN = 100
BOTTOM_VIEWPORT_MARGIN = 50
TOP_VIEWPORT_MARGIN = 100

# Scaling
char_scaling = 0.25

class SettingView(arcade.View):

    def __init__(self):
        super().__init__()
        self.menu_list = None
        self.menu_list = None

        self.mouse_list = None
        self.mouse_sprite = None
        self.window.set_mouse_visible(False)

    def setup(self):
        self.menu_list = arcade.SpriteList(use_spatial_hash=True)
        self.mouse_sprite = arcade.Sprite("pic/default/char.png", char_scaling)
        self.menu_line(96, 32, "pic/menu/back.png")  # back
        self.mouse_list = arcade.SpriteList()
        self.mouse_list.append(self.mouse_sprite)

    def menu_line(self, center_x, center_y, img):

        menu = arcade.Sprite(img)
        menu.center_x = center_x
        menu.center_y = center_y
        self.menu_list.append(menu)

    def on_show(self):
        arcade.set_background_color(arcade.csscolor.BLACK)
        arcade.set_viewport(0, screen_w - 1, 0, screen_h - 1)

    def on_draw(self):
        arcade.start_render()
        self.menu_list.draw()
        self.mouse_list.draw()

        arcade.draw_text("JUMPER", screen_w / 2, screen_h / 2 + 32 * 8, arcade.color.WHITE, font_size=30,
                         anchor_x="center")

    def on_mouse_motion(self, x, y, dx, dy):
        self.mouse_sprite.center_x = x
        self.mouse_sprite.center_y = y

    def on_mouse_press(self, _x, _y, button, _modifiers):

        menu_hit_list = arcade.check_for_collision_with_list(self.mouse_sprite, self.menu_list)

        for menu_index in menu_hit_list:
            if button == arcade.MOUSE_BUTTON_LEFT:
                if menu_index == self.menu_list[0]:
                    main_view = Menu.MainView()
                    main_view.setup()
                    self.window.show_view(main_view)