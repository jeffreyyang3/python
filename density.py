import sys
import random
import pygame
import os
pill_width = 7
pill_height = 25
yellow = (255, 255, 0)
red = (255,0,0)
blue = (0,0,255)
black = (0,0,0)




# Constants
def gen_random():
    xval_density = []
    for _ in range(3000):
        xval_density.append((
            random.randrange(0, (1200 / 2) - 5), int(random.choice('1111111111111111111122222334'))))
    return xval_density


class Game():
    def __init__(self):

        self.WIN_W = 1200
        self.WIN_H = 670
        self.fps = 60
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((self.WIN_W, self.WIN_H), pygame.SRCALPHA)

        self.black = (0, 0, 0)
        self.white = (255, 255, 255)
        self.play = True

        self.SHIP_WIDTH = self.SHIP_HEIGHT = self.WIN_W / 120

# Classes
class Ship(pygame.sprite.Sprite):
    def __init__(self, x, y, player, game):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.player = player
        self.speed = 5
        self.image = pygame.Surface((game.SHIP_WIDTH, game.SHIP_HEIGHT)).convert()
        self.rect = pygame.Rect(x, y, game.SHIP_WIDTH, game.SHIP_HEIGHT)
        self.density = 0
        self.width = game.SHIP_WIDTH
        self.height = game.SHIP_HEIGHT
    def grow(self):
        self.image = pygame.transform.scale(self.image, (10 + self.density, 10 + self.density))
        self.rect.width += self.density
        self.rect.height += self.density



    def update(self, pill_group):
        key = pygame.key.get_pressed()
        print(self.density)
        if self.player == "right":
            if self.rect.y > 650:
                self.rect.y = 650
            if self.rect.y < 50:
                self.rect.y = 50
            if self.rect.x < 600 - 10:
                self.rect.x = 590
            if self.rect.x > 1195:
                self.rect.x = 1195
            if key[pygame.K_DOWN]:
                self.rect.y += self.speed
            elif key[pygame.K_UP]:
                self.rect.y -= self.speed
            elif key[pygame.K_LEFT]:
                self.rect.x -= self.speed
            elif key[pygame.K_RIGHT]:
                self.rect.x += self.speed
        if self.player == "left":
            if self.rect.y > 650:
                self.rect.y = 650
            if self.rect.y < 50:
                self.rect.y = 50
            if self.rect.x < 0:
                self.rect.x = 0
            if self.rect.x > 600 - 10:
                self.rect.x = 590

            if key[pygame.K_s]:
                self.rect.y += self.speed
            elif key[pygame.K_w]:
                self.rect.y -= self.speed
            elif key[pygame.K_a]:
                self.rect.x -= self.speed
            elif key[pygame.K_d]:
                self.rect.x += self.speed

        collisions = pygame.sprite.spritecollide(self, pill_group, True)
        for pill in collisions:
            self.density += pill.density
            self.grow()



class Pill(pygame.sprite.Sprite):
    def __init__(self, xval, density):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 5
        self.image = pygame.Surface((pill_width, pill_height)).convert()
        self.rect = pygame.Rect(xval, 50, pill_width, pill_height)
        self.density = density
    def update(self):
        self.rect.y += self.speed
        self.set_color()

    def set_color(self):
        if self.density == 1:
            self.image.fill(yellow)
        elif self.density == 2:
            self.image.fill(red)
        elif self.density == 3:
            self.image.fill(blue)
        elif self.density == 4:
            self.image.fill(black)


def main():
    # Initialize variables
    TIMER = 0
    pill_count = 0

    # Create Game Objects
    xval_density = gen_random()

    max_pill_count = len(xval_density)
    game = Game()
    ship_left = Ship((game.WIN_W / 4) - (game.SHIP_WIDTH / 2), game.WIN_H - (game.SHIP_HEIGHT * 4), 'left', game)
    ship_right = Ship((game.WIN_W / 1.5) - (game.SHIP_WIDTH / 2), game.WIN_H - (game.SHIP_HEIGHT * 4), 'right', game)
    vert_partition = pygame.Surface((1, game.WIN_H))
    horizontal = pygame.Surface((game.WIN_W, 1))
    # Create Groups
    ship_group = pygame.sprite.Group()
    ship_group.add(ship_left, ship_right)
    pill_group = pygame.sprite.Group()


    # Intro Loop

    # Game Loop
    while game.play:
        # Checks if window exit button pressed
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            # Keypresses
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        # Update Groups
        ship_group.update(pill_group)
        pill_group.update()



        # Adding Pills
        if pill_count < max_pill_count and TIMER % 10 == 0:
            pill = Pill(xval_density[pill_count][0], xval_density[pill_count][1])
            pill_group.add(pill)
            pill = Pill(xval_density[pill_count][0] + game.WIN_W/2, xval_density[pill_count][1])
            pill_group.add(pill)
            pill_count += 1

        # Print Groups
        game.screen.fill(game.white)
        ship_group.draw(game.screen)
        pill_group.draw(game.screen)

        game.screen.blit(vert_partition, (game.WIN_W / 2, game.WIN_H / 15))
        game.screen.blit(horizontal, (game.WIN_W / 1000, game.WIN_H / 15))

        # Limits frames per iteration of while loop
        game.clock.tick(game.fps)
        # Writes to main surface
        pygame.display.flip()
        TIMER += 1


if __name__ == "__main__":
    # Force static position of screen
    os.environ['SDL_VIDEO_CENTERED'] = '1'

    # Runs imported module
    pygame.init()

main()