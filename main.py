
import arcade

# Constants

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


class MyGame(arcade.Window):
    # Main application class.
    def __init__(self):
        # call the parent class and set up the window
        super().__init__(screen_w, screen_h, screen_t)

        arcade.set_background_color(arcade.csscolor.BLACK)

        self.coin_list = None
        self.wall_list = None
        self.player_list = None
        self.player_sprite = arcade.Sprite("pic/default/char.png", char_scaling)

        # Our physics engine
        self.physics_engine = None

        # physics engine
        # Track the current state of what key is pressed
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False

        # Used to keep track of our scrolling
        self.view_bottom = 0
        self.view_left = 0

        # variables for map reading
        self.map_title = None
        self.map_author = None
        self.char_x = None
        self.char_y = None

    def map_read(self, map_file):
        m_f = open(map_file, "r")
        while True:
            temp_l = m_f.readlines()

    def wall_line(self, start, end, height, img):
        for x in range(start, end, 32):
            wall = arcade.Sprite(img, char_scaling)
            wall.center_x = x
            wall.center_y = height
            self.wall_list.append(wall)

    def setup(self):
        # sprite lists
        self.player_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList(use_spatial_hash=True)
        self.coin_list = arcade.SpriteList(use_spatial_hash=True)

        self.map_read("map/map.pm")

        # player_sprite attributes
        self.player_sprite.center_x = self.char_x
        self.player_sprite.center_y = self.char_y
        self.player_list.append(self.player_sprite)

        # call this function to restart the game.
        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player_sprite, self.wall_list, GRAVITY)
        self.physics_engine.enable_multi_jump(2)

    def on_key_press(self, key, modifiers):
        # called whenever a key is pressed
        if key == arcade.key.UP or key == arcade.key.W:
            if self.physics_engine.can_jump():
                self.player_sprite.change_y = player_jump_speed
                self.physics_engine.increment_jump_counter()
        elif key == arcade.key.LEFT:
            self.left_pressed = True
        elif key == arcade.key.RIGHT:
            self.right_pressed = True

    def on_key_release(self, key, modifiers):
        # called when the user releases a key
        if key == arcade.key.LEFT:
            self.left_pressed = False
        elif key == arcade.key.RIGHT:
            self.right_pressed = False

    def on_update(self, delta_time):
        # movement & game logic

        # Calculate speed based on the keys pressed
        self.player_sprite.change_x = 0

        if self.left_pressed and not self.right_pressed:
            self.player_sprite.change_x = -MOVEMENT_SPEED
        elif self.right_pressed and not self.left_pressed:
            self.player_sprite.change_x = MOVEMENT_SPEED

        # move the player with the physics engine
        self.physics_engine.update()

        # --- Manage Scrolling ---

        # Track if we need to change the viewport

        changed = False

        # Scroll left
        left_boundary = self.view_left + LEFT_VIEWPORT_MARGIN
        if self.player_sprite.left < left_boundary:
            self.view_left -= left_boundary - self.player_sprite.left
            changed = True

        # Scroll right
        right_boundary = self.view_left + screen_w - RIGHT_VIEWPORT_MARGIN
        if self.player_sprite.right > right_boundary:
            self.view_left += self.player_sprite.right - right_boundary
            changed = True

        # Scroll up
        top_boundary = self.view_bottom + screen_h - TOP_VIEWPORT_MARGIN
        if self.player_sprite.top > top_boundary:
            self.view_bottom += self.player_sprite.top - top_boundary
            changed = True

        # Scroll down
        bottom_boundary = self.view_bottom + BOTTOM_VIEWPORT_MARGIN
        if self.player_sprite.bottom < bottom_boundary:
            self.view_bottom -= bottom_boundary - self.player_sprite.bottom
            changed = True

        if changed:
            # Only scroll to integers. Otherwise we end up with pixels that
            # don't line up on the screen
            self.view_bottom = int(self.view_bottom)
            self.view_left = int(self.view_left)

            # Do the scrolling
            arcade.set_viewport(self.view_left,
                                screen_w + self.view_left,
                                self.view_bottom,
                                screen_h + self.view_bottom)

    def on_draw(self):
        # render the screen.
        arcade.start_render()
        # code to draw the screen goes here
        self.wall_list.draw()
        self.coin_list.draw()
        self.player_list.draw()


def main():
    # Main method.
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
