import arcade
import Menu
import json
import Game
from GlobalConsts import *

class MapeditView(arcade.View):

    def __init__(self):
        super().__init__()
        self.menu_list = None
        self.map_file = "temp/temp.json"
        self.mouse_list = None
        self.mouse_sprite = None
        self.window.set_mouse_visible(False)
        self.GameFunc = Game.GameView()
        self.bsq_list = None
        self.init_dic = {'meta': ['name', 'author'], 'char': [64, 64], 'walls': [], 'thorns': [], 'coins': [], 'flags': [], 'spring': [], 'portal': []}
        self.object_list = None
        self.object_sqlist = None

    def setup(self):
        self.bsq_list = arcade.SpriteList(use_spatial_hash=True)
        self.base_square("pic/default/blank_dot_block.png")
        self.menu_list = arcade.SpriteList(use_spatial_hash=True)
        self.mouse_sprite = arcade.Sprite("pic/default/cursor.png", char_scaling)
        self.base_square("pic/default/blank_dot_block.png")
        self.menu_line(96, screen_h - 32, "pic/menu/back.png")  # back
        self.menu_line(screen_w - 144, 32, "pic/mapedit/tools.png")
        self.menu_line(screen_w - 144, 96, "pic/mapedit/objects.png")
        self.menu_line(screen_w - 144, 160, "pic/mapedit/blocks.png")
        self.mouse_list = arcade.SpriteList()
        self.mouse_list.append(self.mouse_sprite)
        self.GameFunc.map_read("temp/temp.json")
        self.object_list = arcade.SpriteList(use_spatial_hash=True)
        self.object_sqlist = arcade.SpriteList(use_spatial_hash=True)

    def base_square(self, img):
        for y in range(16, 720, 32):
            for x in range(16, 1280, 32):
                bsq = arcade.Sprite(img, char_scaling)
                bsq.center_x = x
                bsq.center_y = y
                self.bsq_list.append(bsq)

    def menu_line(self, center_x, center_y, img):
        menu = arcade.Sprite(img)
        menu.center_x = center_x
        menu.center_y = center_y
        self.menu_list.append(menu)

    def object_line(self, center_x, center_y, img, rate):
        object_a = arcade.Sprite(img, rate)
        object_a.center_x = center_x
        object_a.center_y = center_y
        self.object_list.append(object_a)

    def object_sqline(self, center_x, center_y, img, rate):
        object_a = arcade.Sprite(img, rate)
        object_a.center_x = center_x
        object_a.center_y = center_y
        self.object_list.append(object_a)

    def new_file(self):
        t = open("temp/temp.json", "w")
        with open("temp/temp.json", encoding='utf-8') as f_r:
            # load file
            data = json.load(f_r)
            data.dumps(self.init_dic, indent = 4)

    def on_show(self):
        arcade.set_background_color(arcade.csscolor.BLACK)
        arcade.set_viewport(0, screen_w - 1, 0, screen_h - 1)

    def on_draw(self):
        arcade.start_render()
        self.bsq_list.draw()
        self.menu_list.draw()
        self.object_list.draw()
        self.mouse_list.draw()

    def on_mouse_motion(self, x, y, dx, dy):
        self.mouse_sprite.center_x = x
        self.mouse_sprite.center_y = y

    def on_mouse_press(self, _x, _y, button, _modifiers):
        menu_hit_list = arcade.check_for_collision_with_list(self.mouse_sprite, self.menu_list)

        for menu_index in menu_hit_list:
            if button == arcade.MOUSE_BUTTON_LEFT:
                press_b = False
                if menu_index == self.menu_list[0]: # back
                    main_view = Menu.MainView()
                    main_view.setup()
                    self.window.show_view(main_view)
                elif menu_index == self.menu_list[1]: # tools
                    pass
                elif menu_index == self.menu_list[2]: # objects
                    if press_b:
                        self.object_list = None
                        self.object_list = arcade.SpriteList(use_spatial_hash=True)
                        self.object_sqlist = None
                        self.object_sqlist = arcade.SpriteList(use_spatial_hash=True)
                        press_b ^= 0
                    for a in range(6):
                        self.object_sqline(992 - (64 * a + 32), 32, "pic/mapedit/pt6_sq.png", 1)
                    self.object_line(960, 32, "pic/platforms/def_floor.png", char_scaling)
                    self.object_line(896, 32, "pic/platforms/corner_floor_left.png", char_scaling)
                    self.object_line(832, 32, "pic/object_interact/bit_w.png", char_scaling)
                    self.object_line(768, 32, "pic/object_interact/portal.png", char_scaling/2)
                    self.object_line(704, 32, "pic/object_interact/flag.png", char_scaling/2)
                    self.object_line(640, 32, "pic/object_interact/thorn_0.png", char_scaling)
                    press_b ^= 1

                elif menu_index == self.menu_list[3]: # blocks
                    pass
