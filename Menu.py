#김태인, 이정주
import arcade
import Mapedit
import Setting
import Game
from GlobalConsts import * #최영훈

class MainView(arcade.View):

    def __init__(self): #김태인, 이정주
        super().__init__()
        self.menu_list = None
        self.menu_list = None

        self.mouse_list = None
        self.mouse_sprite = None
        self.remember_menu = 0
        self.window.set_mouse_visible(False)

    def setup(self): #김태인, 이정주
        self.menu_list = arcade.SpriteList(use_spatial_hash=True)
        self.mouse_sprite = arcade.Sprite("pic/default/cursor.png", char_scaling)
        self.menu_line(screen_w / 2, screen_h / 2 + 32 * 5, "pic/menu/start.png")  # start
        self.menu_line(screen_w / 2, screen_h / 2 + 32 * 2, "pic/menu/setting.png")  # setting
        self.menu_line(screen_w / 2, screen_h / 2 - 32 * 1, "pic/menu/mapedit.png")  # map_edit
        self.menu_line(screen_w / 2, screen_h / 2 - 32 * 4, "pic/menu/quit.png")  # quit
        self.menu_line(96, 32, "pic/menu/back.png")  # back
        self.mouse_list = arcade.SpriteList()
        self.mouse_list.append(self.mouse_sprite)

    def menu_line(self, center_x, center_y, img): #김태인, 이정주
        menu = arcade.Sprite(img)
        menu.center_x = center_x
        menu.center_y = center_y
        self.menu_list.append(menu)


    def on_show(self): #김태인, 이정주
        arcade.set_background_color(arcade.csscolor.BLACK)
        arcade.set_viewport(0, screen_w - 1, 0, screen_h - 1)

    def on_draw(self): #김태인, 이정주
        arcade.start_render()
        self.menu_list.draw()
        self.mouse_list.draw()

        arcade.draw_text("JUMPER", screen_w / 2, screen_h / 2 + 32 * 8, arcade.color.WHITE, font_size=30,
                         anchor_x="center")

    # 마우스로 화면 클릭시 게임화면으로 전환
    def on_mouse_motion(self, x, y, dx, dy): #이정주
        self.mouse_sprite.center_x = x
        self.mouse_sprite.center_y = y

    def on_mouse_press(self, _x, _y, button, _modifiers): #이정주

        menu_hit_list = arcade.check_for_collision_with_list(self.mouse_sprite, self.menu_list)

        for menu_index in menu_hit_list :

            if button == arcade.MOUSE_BUTTON_LEFT :

                if menu_index == self.menu_list[0]: # start
                    game_view = Game.GameView()
                    game_view.setup()
                    self.window.show_view(game_view)

                if menu_index == self.menu_list[1]: # setting
                    setting_view = Setting.SettingView()
                    setting_view.setup()
                    self.window.show_view(setting_view)

                if menu_index == self.menu_list[2]: # map edit
                    mapedit_view = Mapedit.MapeditView()
                    mapedit_view.setup()
                    self.window.show_view(mapedit_view)

                if menu_index == self.menu_list[3]: # quit
                    arcade.close_window()
                    return 0

                if menu_index == self.menu_list[4]: # back
                    return 0
