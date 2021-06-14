import arcade
import Menu
import json
import Game
import time
from GlobalConsts import *
import math
import tkinter as tk
from tkinter import filedialog
import os


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
        self.mobject_list = None
        self.press_b = False
        self.press_t = False
        self.cursor_status = -1
        self.window.set_mouse_visible(False)
        self.status_list = None
        self.cur_block_list = None
        self.map_pos_x = 0
        self.map_pos_y = 0
        self.map_list = self.init_dic
        self.def_floor_rot = 0
        self.cor_floor_rot = 0
        self.thorn_rot = 0
        self.map_string_list = {"walls", "thorns", "coins", "flags", "spring", "portal"}
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False
        self.char_x = None
        self.char_y = None
        self.tool_list = None
        self.toolOn = False
        self.f_spath = None
        self.f_opath = None

    def setup(self):
        self.bsq_list = arcade.SpriteList(use_spatial_hash=True)
        self.base_square("pic/default/blank_dot_block.png")
        self.menu_list = arcade.SpriteList(use_spatial_hash=True)
        self.status_list = arcade.SpriteList(use_spatial_hash=True)
        self.object_sqlist = arcade.SpriteList(use_spatial_hash=True)
        self.object_list = arcade.SpriteList(use_spatial_hash=True)
        self.cur_block_list = arcade.SpriteList(use_spatial_hash=True)
        self.mouse_list = arcade.SpriteList(use_spatial_hash=True)
        self.mobject_list = arcade.SpriteList(use_spatial_hash=True)
        self.tool_list = arcade.SpriteList(use_spatial_hash=True)
        self.mouse_sprite = arcade.Sprite("pic/default/cursor.png", char_scaling)
        self.mouse_list.append(self.mouse_sprite)
        self.menu_line(screen_w - 144, 32, "pic/mapedit/tools.png")
        self.menu_line(screen_w - 144, 96, "pic/mapedit/objects.png")
        self.status_line(screen_w - 118, screen_h - 32, "pic/mapedit/blank_square.png", 1)
        self.status_line(screen_w - 268, screen_h - 32, "pic/mapedit/pt6_sq.png", 1)


    def map_read(self, map_file):
        data = map_file
        self.mobject_list = None
        self.mobject_list = arcade.SpriteList(use_spatial_hash=True)
        location_x = data["char"][0]
        location_y = data["char"][1]
        self.user_pos(location_x, location_y)
        for i in self.map_string_list:
            for k in data[i]:
                if i == "walls":
                    self.mobject_line(k["pos"][0] - 16 + self.map_pos_x, k["pos"][2] - 16 + self.map_pos_y, k["tex"], char_scaling)
                elif i == "thorns":
                    self.mobject_line(k["pos"][0] - 16 + self.map_pos_x, k["pos"][2] - 16 + self.map_pos_y, k["tex"], char_scaling)
                elif i == "coins":
                    self.mobject_line(k["pos"][0] - 16 + self.map_pos_x, k["pos"][2] - 16 + self.map_pos_y, k["tex"], char_scaling)
                elif i == "flags":
                    self.mobject_line(k["pos"][0] - 16 + self.map_pos_x, k["pos"][1] - 16 + self.map_pos_y, k["tex"], char_scaling)
                elif i == "spring":
                    self.mobject_line(k["pos"][0] - 16 + self.map_pos_x, k["pos"][2] - 16 + self.map_pos_y, k["tex"], char_scaling)
                elif i == "portal":
                    self.mobject_line(k["pos"][0] - 16 + self.map_pos_x, k["pos"][2] - 16 + self.map_pos_y, k["tex"], char_scaling)

    def user_pos(self, u_x, u_y):
        self.char_x = u_x
        self.char_y = u_y

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
        object_sqa = arcade.Sprite(img, rate)
        object_sqa.center_x = center_x
        object_sqa.center_y = center_y
        self.object_sqlist.append(object_sqa)

    def status_line(self, center_x, center_y, img, rate):
        status_a = arcade.Sprite(img, rate)
        status_a.center_x = center_x
        status_a.center_y = center_y
        self.status_list.append(status_a)

    def cur_block_line(self, center_x, center_y, img, rate):
        self.cur_block_list = None
        self.cur_block_list = arcade.SpriteList(use_spatial_hash=True)
        block_a = arcade.Sprite(img, rate)
        block_a.center_x = center_x
        block_a.center_y = center_y
        self.cur_block_list.append(block_a)

    def mobject_line(self, center_x, center_y, img, rate):
        mobject_a = arcade.Sprite(img, rate)
        mobject_a.center_x = center_x
        mobject_a.center_y = center_y
        self.mobject_list.append(mobject_a)

    def tool_line(self, center_x, center_y, img):
        tool_a = arcade.Sprite(img)
        tool_a.center_x = center_x
        tool_a.center_y = center_y
        self.tool_list.append(tool_a)

    def new_file(self):
        t = open("temp/temp.json", "w")
        with open("temp/temp.json", encoding='utf-8') as f_r:
            # load file
            data = json.load(f_r)
            data.dumps(self.init_dic, indent = 4)

    def rot_f(self, signal):
        if signal == 0:
            if self.press_b:
                self.object_list = None
                self.object_list = arcade.SpriteList(use_spatial_hash=True)
                self.object_sqlist = None
                self.object_sqlist = arcade.SpriteList(use_spatial_hash=True)
                self.press_b = False
                print("if worked")
                return
            self.press_b = True
            for a in range(6):
                self.object_sqline(992 - (64 * a + 32), 32, "pic/mapedit/pt6_sq.png", 1)
            if self.def_floor_rot == 0:
                self.object_line(960, 32, "pic/platforms/def_floor.png", char_scaling)
            elif self.def_floor_rot == 1:
                self.object_line(960, 32, "pic/platforms/def_floor_l.png", char_scaling)
            elif self.def_floor_rot == 2:
                self.object_line(960, 32, "pic/platforms/def_floor_d.png", char_scaling)
            elif self.def_floor_rot == 3:
                self.object_line(960, 32, "pic/platforms/def_floor_r.png", char_scaling)

            if self.cor_floor_rot == 0:
                self.object_line(896, 32, "pic/platforms/corner_floor_left.png", char_scaling)
            elif self.cor_floor_rot == 1:
                self.object_line(896, 32, "pic/platforms/corner_floor_down_left.png", char_scaling)
            elif self.cor_floor_rot == 2:
                self.object_line(896, 32, "pic/platforms/corner_floor_down_right.png", char_scaling)
            elif self.cor_floor_rot == 3:
                self.object_line(896, 32, "pic/platforms/corner_floor_right.png", char_scaling)

            self.object_line(832, 32, "pic/object_interact/bit_w.png", char_scaling)

            self.object_line(768, 32, "pic/object_interact/portal.png", char_scaling / 2)

            self.object_line(704, 32, "pic/object_interact/flag.png", char_scaling / 2)

            if self.thorn_rot == 0:
                self.object_line(640, 32, "pic/object_interact/thorn_0.png", char_scaling)
            elif self.thorn_rot == 1:
                self.object_line(640, 32, "pic/object_interact/thorn_1.png", char_scaling)
            elif self.thorn_rot == 2:
                self.object_line(640, 32, "pic/object_interact/thorn_2.png", char_scaling)
            elif self.thorn_rot == 3:
                self.object_line(640, 32, "pic/object_interact/thorn_3.png", char_scaling)
        elif signal == 1:
            self.object_list = None
            self.object_list = arcade.SpriteList(use_spatial_hash=True)
            self.object_sqlist = None
            self.object_sqlist = arcade.SpriteList(use_spatial_hash=True)
            self.press_b = True
            for a in range(6):
                self.object_sqline(992 - (64 * a + 32), 32, "pic/mapedit/pt6_sq.png", 1)
            if self.def_floor_rot == 0:
                self.object_line(960, 32, "pic/platforms/def_floor.png", char_scaling)
            elif self.def_floor_rot == 1:
                self.object_line(960, 32, "pic/platforms/def_floor_l.png", char_scaling)
            elif self.def_floor_rot == 2:
                self.object_line(960, 32, "pic/platforms/def_floor_d.png", char_scaling)
            elif self.def_floor_rot == 3:
                self.object_line(960, 32, "pic/platforms/def_floor_r.png", char_scaling)

            if self.cor_floor_rot == 0:
                self.object_line(896, 32, "pic/platforms/corner_floor_left.png", char_scaling)
            elif self.cor_floor_rot == 1:
                self.object_line(896, 32, "pic/platforms/corner_floor_down_left.png", char_scaling)
            elif self.cor_floor_rot == 2:
                self.object_line(896, 32, "pic/platforms/corner_floor_down_right.png", char_scaling)
            elif self.cor_floor_rot == 3:
                self.object_line(896, 32, "pic/platforms/corner_floor_right.png", char_scaling)

            self.object_line(832, 32, "pic/object_interact/bit_w.png", char_scaling)

            self.object_line(768, 32, "pic/object_interact/portal.png", char_scaling / 2)

            self.object_line(704, 32, "pic/object_interact/flag.png", char_scaling / 2)

            if self.thorn_rot == 0:
                self.object_line(640, 32, "pic/object_interact/thorn_0.png", char_scaling)
            elif self.thorn_rot == 1:
                self.object_line(640, 32, "pic/object_interact/thorn_1.png", char_scaling)
            elif self.thorn_rot == 2:
                self.object_line(640, 32, "pic/object_interact/thorn_2.png", char_scaling)
            elif self.thorn_rot == 3:
                self.object_line(640, 32, "pic/object_interact/thorn_3.png", char_scaling)

    def toolview(self):
        if self.press_t:
            self.tool_list = None
            self.tool_list = arcade.SpriteList(use_spatial_hash=True)
            self.press_t = False
            self.toolOn = False
            return
        self.press_t = True
        self.tool_line(142.5, 32, "pic/mapedit/back.png")
        self.tool_line(142.5, 96, "pic/mapedit/open.png")
        self.tool_line(142.5, 160, "pic/mapedit/save.png")
        self.tool_line(142.5, 224, "pic/mapedit/meta.png")
        self.toolOn = True

    def on_show(self):
        arcade.set_background_color(arcade.csscolor.BLACK)
        arcade.set_viewport(0, screen_w - 1, 0, screen_h - 1)

    def on_draw(self):
        arcade.start_render()
        self.bsq_list.draw()
        self.menu_list.draw()
        self.mobject_list.draw()
        self.object_sqlist.draw()
        self.object_list.draw()
        self.status_list.draw()
        self.cur_block_list.draw()
        self.tool_list.draw()

        arcade.draw_text(f'{self.map_pos_x}, {self.map_pos_y}', screen_w - 118, screen_h - 32,
                         arcade.color.WHITE, font_size=24, anchor_x="center", anchor_y="center")

        self.mouse_list.draw()

    def on_mouse_motion(self, x, y, dx, dy):
        self.mouse_sprite.center_x = x
        self.mouse_sprite.center_y = y
    def on_mouse_press(self, _x, _y, button, _modifiers):
        menu_hit_list = arcade.check_for_collision_with_list(self.mouse_sprite, self.menu_list)
        object_hit_list = arcade.check_for_collision_with_list(self.mouse_sprite, self.object_list)
        object_sqa_hit_list = arcade.check_for_collision_with_list(self.mouse_sprite, self.object_list)
        tool_hit_list = arcade.check_for_collision_with_list(self.mouse_sprite, self.tool_list)

        for menu_index in menu_hit_list:
            if button == arcade.MOUSE_BUTTON_LEFT:
                if menu_index == self.menu_list[0]: # tools
                    print("run")
                    self.toolview()
                elif menu_index == self.menu_list[1]: # objects
                    self.rot_f(0)

        for object_index in object_hit_list:
            if button == arcade.MOUSE_BUTTON_LEFT:
                if object_index == self.object_list[0]: # press def_floor
                    self.cursor_status = 0
                elif object_index == self.object_list[1]: # press corner_floor
                    self.cursor_status = 1
                elif object_index == self.object_list[2]: # press bit_w
                    self.cursor_status = 2
                elif object_index == self.object_list[3]: # press portal
                    self.cursor_status = 3
                elif object_index == self.object_list[4]:  # press flag
                    self.cursor_status = 4
                elif object_index == self.object_list[5]:  # press thorn
                    self.cursor_status = 5
            elif button == arcade.MOUSE_BUTTON_RIGHT:
                if object_index == self.object_list[0]:
                    if self.def_floor_rot == 3:
                        self.def_floor_rot = 0
                    else:
                        self.def_floor_rot += 1
                elif object_index == self.object_list[1]:
                    if self.cor_floor_rot == 3:
                        self.cor_floor_rot = 0
                    else:
                        self.cor_floor_rot += 1
                elif object_index == self.object_list[5]:
                    if self.thorn_rot == 3:
                        self.thorn_rot = 0
                    else:
                        self.thorn_rot += 1
                self.rot_f(1)


        for object_sqa_index in object_sqa_hit_list:
            if button == arcade.MOUSE_BUTTON_LEFT:
                if object_sqa_index == self.object_sqlist[0]:  # press def_floor
                    self.cursor_status = 0
                elif object_sqa_index == self.object_sqlist[1]:  # press corner_floor
                    self.cursor_status = 1
                elif object_sqa_index == self.object_sqlist[2]:  # press bit_w
                    self.cursor_status = 2
                elif object_sqa_index == self.object_sqlist[3]:  # press portal
                    self.cursor_status = 3
                elif object_sqa_index == self.object_sqlist[4]:  # press flag
                    self.cursor_status = 4
                elif object_sqa_index == self.object_sqlist[5]:  # press thorn
                    self.cursor_status = 5

        for tool_index in tool_hit_list:
            if button == arcade.MOUSE_BUTTON_LEFT:
                if tool_index == self.tool_list[0]:
                    self.press_t = True
                    self.toolview()
                elif tool_index == self.tool_list[1]:
                    self.file_operation(1)
                elif tool_index == self.tool_list[2]:
                    self.file_operation(0)

        if 0 <= self.cursor_status <= 5:
            for object_sqa_index in object_sqa_hit_list:
                for i in range(6):
                    if object_sqa_index == self.object_sqlist[i]:
                        return 0
            for object_index in object_hit_list:
                for i in range(6):
                    if object_index == self.object_list[i]:
                        return 0
            for menu_index in menu_hit_list:
                for i in range(3):
                    if menu_index == self.menu_list[i]:
                        return 0
            if button == arcade.MOUSE_BUTTON_LEFT:
                self.block_put()
            elif button == arcade.MOUSE_BUTTON_RIGHT:
                self.block_remove()


    def on_key_press(self, key, modifiers):
        if key == arcade.key.LEFT:
            self.left_pressed = True
        elif key == arcade.key.RIGHT:
            self.right_pressed = True
        elif key == arcade.key.UP:
            self.up_pressed = True
        elif key == arcade.key.DOWN:
            self.down_pressed = True
        elif key == arcade.key.ESCAPE:
            if self.toolOn:
                self.press_t = True
                self.toolview()
            else:
                main_view = Menu.MainView()
                main_view.setup()
                self.window.show_view(main_view)


    def on_key_release(self, key, modifiers):
        if key == arcade.key.LEFT:
            self.left_pressed = False
        elif key == arcade.key.RIGHT:
            self.right_pressed = False
        elif key == arcade.key.UP:
            self.up_pressed = False
        elif key == arcade.key.DOWN:
            self.down_pressed = False

    def on_update(self, delta_time):
        self.map_read(self.map_list)
        # 좌표
        if self.left_pressed:
            time.sleep(0.125)
            self.map_pos_x -= 32
        elif self.right_pressed:
            time.sleep(0.125)
            self.map_pos_x += 32
        elif self.up_pressed:
            time.sleep(0.125)
            self.map_pos_y += 32
        elif self.down_pressed:
            time.sleep(0.125)
            self.map_pos_y -= 32

        # 블록
        if self.cursor_status == 0:
            if self.def_floor_rot == 0:
                self.cur_block_line(screen_w - 268, screen_h - 32, "pic/platforms/def_floor.png", char_scaling)
            elif self.def_floor_rot == 1:
                self.cur_block_line(screen_w - 268, screen_h - 32, "pic/platforms/def_floor_l.png", char_scaling)
            elif self.def_floor_rot == 2:
                self.cur_block_line(screen_w - 268, screen_h - 32, "pic/platforms/def_floor_d.png", char_scaling)
            elif self.def_floor_rot == 3:
                self.cur_block_line(screen_w - 268, screen_h - 32, "pic/platforms/def_floor_r.png", char_scaling)
        elif self.cursor_status == 1:
            if self.cor_floor_rot == 0:
                self.cur_block_line(screen_w - 268, screen_h - 32, "pic/platforms/corner_floor_left.png", char_scaling)
            elif self.cor_floor_rot == 1:
                    self.cur_block_line(screen_w - 268, screen_h - 32, "pic/platforms/corner_floor_down_left.png",
                                        char_scaling)
            elif self.cor_floor_rot == 2:
                    self.cur_block_line(screen_w - 268, screen_h - 32, "pic/platforms/corner_floor_down_right.png",
                                        char_scaling)
            elif self.cor_floor_rot == 3:
                self.cur_block_line(screen_w - 268, screen_h - 32, "pic/platforms/corner_floor_right.png", char_scaling)
        elif self.cursor_status == 2:
            self.cur_block_line(screen_w - 268, screen_h - 32, "pic/object_interact/bit_w.png", char_scaling)
        elif self.cursor_status == 3:
            self.cur_block_line(screen_w - 268, screen_h - 32, "pic/object_interact/portal.png", char_scaling / 2)
        elif self.cursor_status == 4:
            self.cur_block_line(screen_w - 268, screen_h - 32, "pic/object_interact/flag.png", char_scaling / 2)
        elif self.cursor_status == 5:
            if self.thorn_rot == 0:
                self.cur_block_line(screen_w - 268, screen_h - 32, "pic/object_interact/thorn_0.png", char_scaling)
            elif self.thorn_rot == 1:
                self.cur_block_line(screen_w - 268, screen_h - 32, "pic/object_interact/thorn_1.png", char_scaling)
            elif self.thorn_rot == 2:
                self.cur_block_line(screen_w - 268, screen_h - 32, "pic/object_interact/thorn_2.png", char_scaling)
            elif self.thorn_rot == 3:
                self.cur_block_line(screen_w - 268, screen_h - 32, "pic/object_interact/thorn_3.png", char_scaling)


    def block_put(self):
        update_dict = {}
        if self.cursor_status == 0:
            update_dict['pos'] = [math.ceil(self.mouse_sprite.center_x / 32) * 32 - self.map_pos_x, math.ceil((self.mouse_sprite.center_x + 32) / 32) * 32, math.ceil(self.mouse_sprite.center_y / 32) * 32 - self.map_pos_y]
            if self.def_floor_rot == 0:
                update_dict['tex'] = "pic/platforms/def_floor.png"
            elif self.def_floor_rot == 1:
                update_dict['tex'] = "pic/platforms/def_floor_l.png"
            elif self.def_floor_rot == 2:
                update_dict['tex'] = "pic/platforms/def_floor_d.png"
            elif self.def_floor_rot == 3:
                update_dict['tex'] = "pic/platforms/def_floor_r.png"
            update_dict['rot'] = "0"
            for a in self.map_list['walls']:
                if a['pos'] == update_dict['pos']:
                    return 0
            self.map_list['walls'].append(update_dict)
        elif self.cursor_status == 1:
            update_dict['pos'] = [math.ceil(self.mouse_sprite.center_x / 32) * 32 - self.map_pos_x, math.ceil((self.mouse_sprite.center_x + 32) / 32) * 32, math.ceil(self.mouse_sprite.center_y / 32) * 32 - self.map_pos_y]
            if self.cor_floor_rot == 0:
                update_dict['tex'] = "pic/platforms/corner_floor_left.png"
            elif self.cor_floor_rot == 1:
                update_dict['tex'] = "pic/platforms/corner_floor_down_left.png"
            elif self.cor_floor_rot == 2:
                update_dict['tex'] = "pic/platforms/corner_floor_down_right.png"
            elif self.cor_floor_rot == 3:
                update_dict['tex'] = "pic/platforms/corner_floor_right.png"
            update_dict['rot'] = "0"
            for a in self.map_list['walls']:
                if a['pos'] == update_dict['pos']:
                    return 0
            self.map_list['walls'].append(update_dict)
        elif self.cursor_status == 2:
            update_dict['pos'] = [math.ceil(self.mouse_sprite.center_x / 32) * 32 - self.map_pos_x, math.ceil((self.mouse_sprite.center_x + 32) / 32) * 32, math.ceil(self.mouse_sprite.center_y / 32) * 32 - self.map_pos_y]
            update_dict['tex'] = "pic/object_interact/bit_w.png"
            for a in self.map_list['coins']:
                if a['pos'] == update_dict['pos']:
                    return 0
            self.map_list['coins'].append(update_dict)
        elif self.cursor_status == 3:
            update_dict['pos'] = [math.ceil(self.mouse_sprite.center_x / 32) * 32 - self.map_pos_x, math.ceil((self.mouse_sprite.center_x + 32) / 32) * 32, math.ceil(self.mouse_sprite.center_y / 32) * 32 - self.map_pos_y]
            update_dict['tex'] = "pic/object_interact/portal.png"
            for a in self.map_list['portal']:
                if a['pos'] == update_dict['pos']:
                    return 0
            self.map_list['portal'].append(update_dict)
        elif self.cursor_status == 4:
            update_dict['pos'] = [math.ceil(self.mouse_sprite.center_x / 32) * 32 - self.map_pos_x, math.ceil(self.mouse_sprite.center_y / 32) * 32 - self.map_pos_y]
            update_dict['tex'] = "pic/object_interact/flag.png"
            for a in self.map_list['flags']:
                if a['pos'] == update_dict['pos']:
                    return 0
            self.map_list['flags'].append(update_dict)
        elif self.cursor_status == 5:
            update_dict['pos'] = [math.ceil(self.mouse_sprite.center_x / 32) * 32 - self.map_pos_x,
                                  math.ceil((self.mouse_sprite.center_x + 32) / 32) * 32,
                                  math.ceil(self.mouse_sprite.center_y / 32) * 32 - self.map_pos_y]
            if self.thorn_rot == 0:
                update_dict['tex'] = "pic/object_interact/thorn_0.png"
            elif self.thorn_rot == 1:
                update_dict['tex'] = "pic/object_interact/thorn_1.png"
            elif self.cor_floor_rot == 2:
                update_dict['tex'] = "pic/object_interact/thorn_2.png"
            elif self.cor_floor_rot == 3:
                update_dict['tex'] = "pic/object_interact/thorn_3.png"
            update_dict['rot'] = "0"
            for a in self.map_list['thorns']:
                if a['pos'] == update_dict['pos']:
                    return 0
            self.map_list['thorns'].append(update_dict)

    def block_remove(self):
        if self.cursor_status == 0:
            for a in self.map_list['walls']:
                if a['pos'][0] == math.ceil(self.mouse_sprite.center_x / 32) * 32 - self.map_pos_x and a['pos'][2] == math.ceil(self.mouse_sprite.center_y / 32) * 32 - self.map_pos_y:
                    self.map_list["walls"].remove(a)
                    break
        elif self.cursor_status == 1:
            for a in self.map_list['walls']:
                if a['pos'][0] == math.ceil(self.mouse_sprite.center_x / 32) * 32 - self.map_pos_x and a['pos'][2] == math.ceil(self.mouse_sprite.center_y / 32) * 32 - self.map_pos_y:
                    self.map_list["walls"].remove(a)
                    break
        elif self.cursor_status == 2:
            for a in self.map_list['coins']:
                if a['pos'][0] == math.ceil(self.mouse_sprite.center_x / 32) * 32 - self.map_pos_x and a['pos'][2] == math.ceil(self.mouse_sprite.center_y / 32) * 32 - self.map_pos_y:
                    self.map_list["coins"].remove(a)
                    break
        elif self.cursor_status == 3:
            for a in self.map_list['portal']:
                if a['pos'][0] == math.ceil(self.mouse_sprite.center_x / 32) * 32 - self.map_pos_x and a['pos'][2] == math.ceil(self.mouse_sprite.center_y / 32) * 32 - self.map_pos_y:
                    self.map_list["portal"].remove(a)
                    break
        elif self.cursor_status == 4:
            for a in self.map_list['flags']:
                if a['pos'][0] == math.ceil(self.mouse_sprite.center_x / 32) * 32 - self.map_pos_x and a['pos'][1] == math.ceil(self.mouse_sprite.center_y / 32) * 32 - self.map_pos_y:
                    self.map_list["flags"].remove(a)
                    break
        elif self.cursor_status == 5:
            for a in self.map_list['portal']:
                if a['pos'][0] == math.ceil(self.mouse_sprite.center_x / 32) * 32 - self.map_pos_x and a['pos'][1] == math.ceil(self.mouse_sprite.center_y / 32) * 32 - self.map_pos_y:
                    self.map_list["portal"].remove(a)
                    break

    def file_operation(self, switch):
        root = tk.Tk()
        root.withdraw()

        if switch == 0:
            self.f_spath = filedialog.asksaveasfilename()
            json_save = json.dumps(self.map_list, indent = 4)
            with open(self.f_spath, "w") as outfile:
                outfile.write(json_save)
        elif switch == 1:
            self.f_opath = filedialog.askopenfilename()
            with open(self.f_opath, encoding='utf-8') as f_r:
                # load file
                self.map_list = json.load(f_r)