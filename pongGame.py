import sys
import pygame
import time
# i lost the sound files but they were pretty funny
# the paddles work around 95% of the time its a game feature that it doesnt work sometimes :)
WIN_W = 920
WIN_H = 570

pygame.init()
pygame.mixer.pre_init(44100, -16, 2, 2048)
pygame.mixer.init()
sound = {}
sound["beep"] = pygame.mixer.Sound("sound/beep.ogg")
sound["boom"] = pygame.mixer.Sound("sound/boom.ogg")
sound["bop"] = pygame.mixer.Sound("sound/bop.ogg")
sound["choose"] = pygame.mixer.Sound("sound/choose.ogg")
sound["count"] = pygame.mixer.Sound("sound/count.ogg")
sound["end"] = pygame.mixer.Sound("sound/end.ogg")
sound["music"] = pygame.mixer.Sound("sound/music.ogg")
sound["select"] = pygame.mixer.Sound("sound/select.ogg")
WHITE = (0,255,255)
BLACK = (255, 255, 255)
paddle_width = 20
paddle_height = 120
pygame.init()
ball_height = 30
ball_width = 30


class Paddle():
    def __init__(self, x, y):
        self.speed = 15
        self.score = 0
        self.height = paddle_height
        self.width = paddle_width
        self.image = pygame.Surface((self.width, self.height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self, moveDOWN, moveUP):
        # Adjust speed
        if moveUP or moveDOWN:
            if moveUP:
                self.rect.y -= self.speed
            if moveDOWN:
                self.rect.y += self.speed
                # paddle movement
        if self.rect.y < 0:
            self.rect.y = 0
        elif self.rect.y + self.height > WIN_H:
            self.rect.y = WIN_H - self.height


class Ball():
    def __init__(self, x, y):
        self.speed = [5, 5]
        self.height = ball_height
        self.width = ball_width
        self.image = pygame.Surface((20, 20))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self, game):

        self.rect = self.rect.move(self.speed)

        if self.rect.top > WIN_H - self.height or self.rect.top < 0:
            self.speed[1] = - self.speed[1]
            sound["bop"].set_volume(10)
            sound["bop"].play()
        if self.rect.top > game.right_paddle.rect.y - 20 and self.rect.bottom < game.right_paddle.rect.y + paddle_height + 20:
            if (game.right_paddle.rect.x - paddle_width - 5) < self.rect.x < (game.right_paddle.rect.x - paddle_width + 5):
                self.speed[0] = -self.speed[0]
                sound["beep"].set_volume(10)
                sound["beep"].play()

        elif self.rect.top > game.left_paddle.rect.y - 20 and self.rect.bottom < game.left_paddle.rect.y + paddle_height + 20:
            if (game.left_paddle.rect.x + paddle_width + 5) > self.rect.x > (game.left_paddle.rect.x + paddle_width - 5):
                self.speed[0] = -self.speed[0]
                sound["beep"].set_volume(10)
                sound["beep"].play()

    def restart(self, game):
        if game.right_paddle.score >= 3 or game.left_paddle.score >= 3:
            game.play = False
        time.sleep(1)
        self.rect.y = WIN_H / 2 - (ball_height / 2)
        self.rect.x = WIN_W / 2
        game.left_paddle.rect.y = (WIN_H / 2) - (paddle_height / 2)
        game.right_paddle.rect.y = (WIN_H / 2) - (paddle_height / 2)
        pygame.display.flip()
        pygame.time.wait(500)



class Text():
    def __init__(self, x, y, font, text):
        self.font = pygame.font.Font(None, font)
        self.image = font.render(text, 5, BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Game():
    def __init__(self):
        self.screen = pygame.display.set_mode((WIN_W, WIN_H), pygame.SRCALPHA)
        self.left_paddle = Paddle(WIN_W / 15, (WIN_H / 2) - (paddle_height / 2))
        self.right_paddle = Paddle(WIN_W / 1.1, (WIN_H / 2) - (paddle_height / 2))

        self.ball = Ball(WIN_W / 2, (WIN_H / 2) - (ball_height / 2))
        self.clock = pygame.time.Clock()
        self.beg_time = pygame.time.get_ticks()
        self.intro = self.play = self.outro = True
        self.moveUP = self.moveDOWN = self.moveUP1 = self.moveDOWN1 = False

        # Creating our text objects
        self.font = pygame.font.Font(None, 40)
        self.title = self.font.render("Pong", 5, BLACK)
        self.outtitle = self.font.render("play again?", 5, BLACK)
        self.outtitlepos = self.outtitle.get_rect()
        self.outtitlepos.centerx = self.screen.get_rect().centerx
        self.outtitlepos.centery = self.screen.get_rect().centery - 50

        ## wins
        self.p1win = self.font.render("player 1 wins, click to play again", 5, BLACK)
        self.p1winpos = self.outtitle.get_rect()
        self.p1winpos.centerx = self.screen.get_rect().centerx
        self.p1winpos.centery = self.screen.get_rect().centery - 50
        self.p2win = self.font.render("player 2 wins, click to play again", 5, BLACK)
        self.p2winpos = self.outtitle.get_rect()
        self.p2winpos.centerx = self.screen.get_rect().centerx
        self.p2winpos.centery = self.screen.get_rect().centery - 50



        self.titlepos = self.title.get_rect()
        self.titlepos.centerx = self.screen.get_rect().centerx
        self.titlepos.centery = self.screen.get_rect().centery - 50

        self.font = pygame.font.Font(None, 60)
        self.start = self.font.render("Click here to start", 5, BLACK)
        self.startpos = self.start.get_rect()
        self.startpos.centerx = self.screen.get_rect().centerx
        self.startpos.centery = self.screen.get_rect().centery + 50

    def restart(self):
        self.left_paddle.score = 0
        self.right_paddle.score = 0
        self.play = True


def main():
    pygame.display.set_caption('Pong')
    game = Game()

    while True:
        sound["music"].set_volume(5)
        sound["music"].play()

        while game.intro:
            # Print background
            game.screen.fill(WHITE)
            game.screen.blit(game.title, game.titlepos)

            # Blinking Text: Click here to start
            cur_time = pygame.time.get_ticks()
            click = game.start
            if ((cur_time - game.beg_time) % 1000) < 500:
                game.screen.blit(click, game.startpos)

            # Checks if window exit button pressed
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN or pygame.key.get_pressed()[pygame.K_RETURN] != 0:
                    pygame.display.flip()
                    pygame.time.wait(1500)
                    game.intro = False

            # Limits frames per iteration of while loop
            game.clock.tick(60)
            # Writes to main surface
            pygame.display.flip()

        while game.play:
            for event in pygame.event.get():
                game.outro = True
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        game.moveUP = True
                        game.moveDOWN = False
                    elif event.key == pygame.K_DOWN:
                        game.moveUP = False
                        game.moveDOWN = True
                    elif event.key == pygame.K_w:
                        game.moveUP1 = True
                        game.moveDOWN1 = False
                    elif event.key == pygame.K_s:
                        game.moveUP1 = False
                        game.moveDOWN1 = True
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_UP:
                        game.moveUP = False
                    elif event.key == pygame.K_DOWN:
                        game.moveDOWN = False
                    elif event.key == pygame.K_w:
                        game.moveUP1 = False
                    elif event.key == pygame.K_s:
                        game.moveDOWN1 = False

            if game.ball.rect.left < 0 - game.ball.rect.width or game.ball.rect.left > WIN_W + game.ball.rect.width:

                if game.ball.rect.left < 0:
                    sound["choose"].set_volume(100)
                    sound["choose"].play()
                    game.right_paddle.score += 1
                    game.ball.restart(game)
                elif game.ball.rect.left > WIN_H + game.ball.rect.width:
                    sound["choose"].set_volume(10)
                    sound["choose"].play()
                    game.left_paddle.score += 1
                    game.ball.restart(game)



            game.left_paddle.update(game.moveDOWN1, game.moveUP1)
            game.right_paddle.update(game.moveDOWN, game.moveUP)
            game.ball.update(game)

            font = pygame.font.Font(None, 40)
            score1 = font.render("Player 2    " + str(game.right_paddle.score), 3, BLACK)
            score1pos = score1.get_rect()
            score1pos.x = game.screen.get_rect().centerx + 200

            font = pygame.font.Font(None, 40)
            score2 = font.render("Player 1    " + str(game.left_paddle.score), 3, BLACK)
            score2pos = score2.get_rect()
            score2pos.x = game.screen.get_rect().centerx - 400

            # Reading in the keyboard inputs from the user
            game.screen.fill(WHITE)
            game.screen.blit(score1, score1pos)
            game.screen.blit(score2, score2pos)
            game.screen.blit(game.left_paddle.image, game.left_paddle.rect)
            game.screen.blit(game.right_paddle.image, game.right_paddle.rect)
            game.screen.blit(game.ball.image, game.ball.rect)

            # Limits frames per iteration of while loop
            game.clock.tick(1000)

            # Writes to main surface
            pygame.display.flip()

        while game.outro:
            game.screen.fill(WHITE)

            # Blinking Text: Click here to start
            cur_time = pygame.time.get_ticks()
            click = game.start
            if game.left_paddle.score == 3:
                game.screen.blit(game.p1win, game.p1winpos)

            else:
                game.screen.blit(game.p2win, game.p2winpos)


            # Checks if window exit button pressed
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN or pygame.key.get_pressed()[pygame.K_RETURN] != 0:
                    game.screen.blit(game.outtitle, game.outtitlepos)
                    pygame.display.flip()
                    print("asdfff")
                    pygame.time.wait(200)
                    game.outro = False
                    game.restart()


            # Limits frames per iteration of while loop
            game.clock.tick(60)
            # Writes to main surface
            pygame.display.flip()



if __name__ == "__main__":
    main()