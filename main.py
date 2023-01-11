import pygame
import k8062

k8062.start_device()  # Start the k8062's driver
k8062.set_channel_count(512)  # Set the maximum channel number
pygame.joystick.init()
joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
print(joysticks)
run = True


def _map(x, in_min, in_max, out_min, out_max):
    return int((x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)


def map_x_movement(x):
    return int((x - 95) * (255 - 0) / (375 - 95) + 0)


def map_y_movement(y):
    return int((y - 66) * (255 - 0) / (346 - 66) + 0)


class Player(object):

    def __init__(self):
        self.player = pygame.rect.Rect((140, 140, 20, 20))
        self.color = "white"
        self.x_start = 95
        self.y_start = 66

    def move(self, x_speed, y_speed):
        self.player.move_ip(x_speed, y_speed)
        if self.player.x >= screen.get_width() - self.player.width:
            self.player.x = screen.get_width() - self.player.width
        if self.player.x <= 0:
            self.player.x = 0
        if self.player.y >= screen.get_height() - self.player.height:
            self.player.y = screen.get_height() - self.player.height
        if self.player.y <= 0:
            self.player.y = 0

    def change_color(self, color):
        self.color = color

    def draw(self, game_screen):
        pygame.draw.rect(game_screen, self.color, self.player)

    def get_position(self):
        x = self.player.x
        y = self.player.y
        return x, y

    def processed_data(self):
        x1 = map_x_movement(self.x_start + player.get_position()[0])
        x2 = map_x_movement(self.x_start + player.get_position()[0])

        y1 = map_y_movement(self.y_start + player.get_position()[1])
        y2 = map_y_movement(self.y_start + player.get_position()[1])
        return x1, y1, x2, y2

    def send_over_DMX(self, x1, y1, x2, y2, dimmer):
        k8062.set_data(115, y1)
        k8062.set_data(116, x1)
        k8062.set_data(129, y2)
        k8062.set_data(130, x2)
        k8062.set_data(128, dimmer)
        k8062.set_data(142, dimmer)
        k8062.set_data(127, 255)
        k8062.set_data(141, 255)


pygame.init()

player = Player()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((300, 300))

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.JOYAXISMOTION:
            #print(event)
            pass

    if pygame.joystick.Joystick(0).get_axis(4) >= 0:
        x_speed = -1
    elif pygame.joystick.Joystick(0).get_axis(5) >= 0:
        x_speed = 1
    else:
        x_speed = 0

    y_speed = round(pygame.joystick.Joystick(0).get_axis(3))
    if pygame.joystick.Joystick(0).get_axis(5) == -1.0 and pygame.joystick.Joystick(0).get_axis(4) == -1.0:
        x_speed = round(pygame.joystick.Joystick(0).get_axis(2))

    player.move(x_speed, y_speed)

    if pygame.joystick.Joystick(0).get_button(0):
        player.change_color("green")
    elif pygame.joystick.Joystick(0).get_button(1):
        player.change_color("red")
    elif pygame.joystick.Joystick(0).get_button(2):
        player.change_color("blue")
    elif pygame.joystick.Joystick(0).get_button(3):
        player.change_color("orange")

    print(pygame.joystick.Joystick(0).get_axis(3))
    dimmer = 0

    player.send_over_DMX(player.processed_data()[0], player.processed_data()[1],
                         player.processed_data()[2], player.processed_data()[3], dimmer)

    screen.fill((0, 0, 0))
    player.draw(screen)
    pygame.display.update()

    clock.tick(180)

pygame.quit()
k8062.stop_device()
exit()
