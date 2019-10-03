import sys, logging, open_color, arcade, random

#check to make sure we are running the right version of Python
version = (3,7)
assert sys.version_info >= version, "This script requires at least Python {0}.{1}".format(version[0],version[1])

#turn on logging, in case we have to leave ourselves debugging messages
logging.basicConfig(format='[%(filename)s:%(lineno)d] %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Space Shooters"

NUM_ENEMIES = 5
STARTING_LOCATION = (400,100)
BULLET_DAMAGE = 10
ENEMY_HP = 100
HIT_SCORE = 10
KILL_SCORE = 100
PLAYER_HP = 50

class Bullet(arcade.Sprite):
    def __init__(self, position, velocity, damage):
        super().__init__("bullet.png", 0.5)
        (self.center_x, self.center_y) = position
        (self.dx, self.dy) = velocity
        self.damage = damage

    def update(self):
        self.center_x += self.dx
        self.center_y += self.dy

class Player(arcade.Sprite):
    def __init__(self):
        super().__init__("SpaceShipNormal.png", 0.5)
        (self.center_x, self.center_y) = STARTING_LOCATION
        self.hp = PLAYER_HP

class Enemy(arcade.Sprite):
    def __init__(self, position):
        super().__init__("ship.png", 0.5)
        self.hp = ENEMY_HP
        (self.center_x, self.center_y) = position
    def shoot(self):
        x = self.center_x
        y = self.center_y - 50
        bullet = Bullet((x,y),(0,-10),BULLET_DAMAGE)
        return bullet


class Window(arcade.Window):

    def __init__(self, width, height, title):

        # Call the parent class's init function
        super().__init__(width, height, title)

        # Make the mouse disappear when it is over the window.
        # So we just see our object, not the pointer.
        self.set_mouse_visible(False)

        arcade.set_background_color(open_color.black)
        self.bullet_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()
        self.player = Player()
        self.score = 0
        self.player_list = arcade.SpriteList()
        self.player_list.append(self.player)



    def setup(self):
        for i in range(NUM_ENEMIES):
            x = 120 * (i+1) + 40
            y = 500
            enemy = Enemy((x,y))
            self.enemy_list.append(enemy)
        pass 

    def update(self, delta_time):
        self.bullet_list.update()
        for e in self.enemy_list:
            chanceOfShooting = (random.random() < .01)
            damage = arcade.check_for_collision_with_list(e, self.bullet_list)
            if chanceOfShooting:
                bullet = e.shoot()
                self.bullet_list.append(bullet)
            for d in damage:
                e.hp -= d.damage
                d.kill()
                if e.hp <= 0:
                    e.kill()
                    self.score = self.score + KILL_SCORE
                else:
                    self.score = self.score + HIT_SCORE
        damage = arcade.check_for_collision_with_list(self.player, self.bullet_list) 
        for p in self.player_list:   
            for d in damage:
                p.hp -= d.damage
                d.kill()
                if p.hp <= 0:
                    p.kill()
        pass

    def on_draw(self):
        """ Called whenever we need to draw the window. """
        arcade.start_render()
        arcade.draw_text(str(self.score), 20, SCREEN_HEIGHT - 40, open_color.white, 16)
        self.player_list.draw()
        self.bullet_list.draw()
        self.enemy_list.draw()




    def on_mouse_motion(self, x, y, dx, dy):
        """ Called to update our objects. Happens approximately 60 times per second."""
        self.player.center_x = x
        pass

    def on_mouse_press(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            x = self.player.center_x
            y = self.player.center_y + 50
            bullet = Bullet((x,y),(0,10),BULLET_DAMAGE)
            self.bullet_list.append(bullet)
            
        pass

    def on_mouse_release(self, x, y, button, modifiers):
        """
        Called when a user releases a mouse button.
        """
        pass

    def on_key_press(self, key, modifiers):
        """ Called whenever the user presses a key. """
        if key == arcade.key.LEFT:
            print("Left")
        elif key == arcade.key.RIGHT:
            print("Right")
        elif key == arcade.key.UP:
            print("Up")
        elif key == arcade.key.DOWN:
            print("Down")

    def on_key_release(self, key, modifiers):
        """ Called whenever a user releases a key. """
        pass


def main():
    window = Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    arcade.run()


if __name__ == "__main__":
    main()