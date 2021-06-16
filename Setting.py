#김태인, 이정주
import arcade

import GlobalConsts #
import Menu
from GlobalConsts import * #최영훈

class SettingView(arcade.View):

    def __init__(self):
        super().__init__()
        self.menu_list = None
        self.menu_list = None

        self.volb_list = None

        self.mouse_list = None
        self.mouse_sprite = None

        self.master_vol = 1.0
        self.music_vol = 1.0

        self.window.set_mouse_visible(True)

    def setup(self):
        self.menu_list = arcade.SpriteList(use_spatial_hash=True)
        self.volb_list = arcade.SpriteList(use_spatial_hash=True)
        self.mouse_list = arcade.SpriteList(use_spatial_hash=True)
        self.mouse_sprite = arcade.Sprite("pic/default/cursor.png", char_scaling)
        self.mouse_list.append(self.mouse_sprite)
        self.menu_line(96, 32, "pic/menu/back.png")  # back
        self.volb_line(screen_w / 2 - 64, screen_h / 2 + 112, "pic/menu/list_l.png", 0.5) #윤후성
        self.volb_line(screen_w / 2, screen_h / 2 + 112, "pic/menu/list_cell.png", 0.5)
        self.volb_line(screen_w / 2 + 64, screen_h / 2 + 112, "pic/menu/list_r.png", 0.5)
        self.volb_line(screen_w / 2 - 64, screen_h / 2 - 48, "pic/menu/list_l.png", 0.5)
        self.volb_line(screen_w / 2, screen_h / 2 - 48, "pic/menu/list_cell.png", 0.5)
        self.volb_line(screen_w / 2 + 64, screen_h / 2 - 48, "pic/menu/list_r.png", 0.5)

    def volume_up(self, input):
        if 0 <= input < 1.0:
            input += 0.1

    def volume_down(self, input):
        if 0 <= input < 1.0:
            input -= 0.1

    def volb_line(self, center_x, center_y, img, rate):

        volb = arcade.Sprite(img, rate)
        volb.center_x = center_x
        volb.center_y = center_y
        self.volb_list.append(volb)

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
        self.volb_list.draw()
        self.mouse_list.draw()

        arcade.draw_text("Setting", screen_w / 2, screen_h / 2 + 32 * 7, arcade.color.WHITE, font_size=30, #윤후성
                         anchor_x="center")
        arcade.draw_text("Master Volume", screen_w / 2, screen_h / 2 + 32 * 5, arcade.color.WHITE, font_size=30,
                         anchor_x="center")
        arcade.draw_text("Music Volume", screen_w / 2, screen_h / 2, arcade.color.WHITE, font_size=30, anchor_x="center")

        arcade.draw_text(str(int(self.master_vol * 10)), screen_w / 2, screen_h / 2 + 90, arcade.color.WHITE, font_size=30,
                         anchor_x="center")
        arcade.draw_text(str(int(self.music_vol * 10)), screen_w / 2, screen_h / 2 - 70, arcade.color.WHITE,
                         font_size=30,
                         anchor_x="center")

    def on_mouse_motion(self, x, y, dx, dy):
        self.mouse_sprite.center_x = x
        self.mouse_sprite.center_y = y

    def on_mouse_press(self, _x, _y, button, _modifiers):

        menu_hit_list = arcade.check_for_collision_with_list(self.mouse_sprite, self.menu_list)
        volb_hit_list = arcade.check_for_collision_with_list(self.mouse_sprite, self.volb_list) #윤후성

        for volb_index in volb_hit_list: #윤후성
            if button == arcade.MOUSE_BUTTON_LEFT:
                if volb_index == self.volb_list[0]:
                    self.volume_down(self.master_vol)
                elif volb_index == self.volb_list[1]:
                    self.volume_up(self.master_vol)
                elif volb_index == self.volb_list[2]:
                    self.volume_down(self.music_vol)
                elif volb_index == self.volb_list[3]:
                    self.volume_up(self.music_vol)

        for menu_index in menu_hit_list: #윤후성
            if button == arcade.MOUSE_BUTTON_LEFT:
                if menu_index == self.menu_list[0]:
                    main_view = Menu.MainView()
                    main_view.setup()
                    self.window.show_view(main_view)
