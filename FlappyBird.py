import pygame
import random
import os
import neat

# Parameters Game
WIDTH, HEIGHT = 1000, 800

IMG_BACKGROUND = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bg.png")))
IMG_FLOOR = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "base.png")))
IMG_PIPE = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "pipe.png")))
IMGS_BIRDS = [
    pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird1.png"))),
    pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird2.png"))),
    pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird3.png")))
]

pygame.font.init()
FONT_SCORE = pygame.font.SysFont(name="arial", size=50)

geracao = 0


class Bird:
    IMGS = IMGS_BIRDS
    # Max rotation of the bird
    MAX_ROTATION = 25
    # Rotation velocity
    ROT_VEL = 20
    # Animation time
    ANIMATION_TIME = 5

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.angle = 0
        self.velocity = 0
        self.height = self.y
        self.time = 0
        self.img_count = 0
        self.img = self.IMGS[0]
        self.next_pipe = None

    def jump(self):
        self.velocity = -10.5
        self.time = 0
        self.height = self.y

    def move(self):
        # Calculate the displacement
        self.time += 1
        displacement = 1.5 * (self.time**2) + self.velocity * self.time
        # Restrict the displacement
        if displacement > 16:
            displacement = 16
        elif displacement < 0:
            displacement -= 2

        self.y += displacement

        # Adjust the angle of the bird
        if displacement < 0 or self.y < self.height + 50:
            if self.angle < self.MAX_ROTATION:
                self.angle = self.MAX_ROTATION
        else:
            if self.angle > -90:
                self.angle -= self.ROT_VEL

    def draw(self, win):
        # Define the image of the bird
        self.img_count += 1
        if self.img_count < self.ANIMATION_TIME:
            self.img = self.IMGS[0]
        elif self.img_count < self.ANIMATION_TIME * 2:
            self.img = self.IMGS[1]
        elif self.img_count < self.ANIMATION_TIME * 3:
            self.img = self.IMGS[2]
        elif self.img_count < self.ANIMATION_TIME * 4:
            self.img = self.IMGS[1]
        elif self.img_count == self.ANIMATION_TIME * 4 + 1:
            self.img = self.IMGS[0]
            self.img_count = 0

        # If the bird is falling, it will not flap
        if self.angle <= -80:
            self.img = self.IMGS[1]
            self.img_count = self.ANIMATION_TIME * 2

        # Draw the bird
        rotated_image = pygame.transform.rotate(self.img, self.angle)
        new_rect = rotated_image.get_rect(center=self.img.get_rect(topleft=(self.x, self.y)).center)
        win.blit(rotated_image, new_rect.topleft)

        if self.next_pipe is not None:
            pygame.draw.line(win, (255, 0, 0), (self.x + self.img.get_width(), self.y + self.img.get_height() // 2),
                             (self.next_pipe.x, self.next_pipe.top + self.next_pipe.PIPE_TOP.get_height()), 2)
            pygame.draw.line(win, (255, 0, 0), (self.x + self.img.get_width(), self.y + self.img.get_height() // 2),
                             (self.next_pipe.x, self.next_pipe.bottom), 2)

    def get_mask(self):
        return pygame.mask.from_surface(self.img)


class Pipe:
    DISTANCE = 200
    VELOCITY = 5

    def __init__(self, x):
        self.x = x
        self.height = 0
        self.top = 0
        self.bottom = 0
        self.PIPE_TOP = pygame.transform.flip(IMG_PIPE, flip_x=False, flip_y=True)
        self.PIPE_BOTTOM = IMG_PIPE
        self.passed = False
        self.set_height()

    def set_height(self):
        self.height = random.randrange(start=50, stop=450)
        self.top = self.height - self.PIPE_TOP.get_height()
        self.bottom = self.height + self.DISTANCE

    def move(self):
        self.x -= self.VELOCITY

    def draw(self, win):
        win.blit(self.PIPE_TOP, (self.x, self.top))
        win.blit(self.PIPE_BOTTOM, (self.x, self.bottom))

    def collide(self, bird):
        bird_mask = bird.get_mask()
        top_mask = pygame.mask.from_surface(self.PIPE_TOP)
        bottom_mask = pygame.mask.from_surface(self.PIPE_BOTTOM)

        top_offset = (self.x - bird.x, self.top - round(bird.y))
        bottom_offset = (self.x - bird.x, self.bottom - round(bird.y))

        b_point = bird_mask.overlap(bottom_mask, bottom_offset)
        t_point = bird_mask.overlap(top_mask, top_offset)

        if t_point or b_point:
            return True
        else:
            return False


class Floor:
    VELOCITY = 5
    WIDTH = IMG_FLOOR.get_width()
    IMG = IMG_FLOOR

    def __init__(self, y):
        self.y = y
        self.x1 = 0
        self.x2 = self.WIDTH
        self.x3 = self.WIDTH * 2

    def move(self):
        self.x1 -= self.VELOCITY
        self.x2 -= self.VELOCITY
        self.x3 -= self.VELOCITY

        if self.x1 + self.WIDTH < 0:
            self.x1 = self.x3 + self.WIDTH

        if self.x2 + self.WIDTH < 0:
            self.x2 = self.x1 + self.WIDTH

        if self.x3 + self.WIDTH < 0:
            self.x3 = self.x2 + self.WIDTH

    def draw(self, win):
        win.blit(self.IMG, (self.x1, self.y))
        win.blit(self.IMG, (self.x2, self.y))
        win.blit(self.IMG, (self.x3, self.y))


def draw_window(win, birds, pipes, floor, score, geracao=None):
    win.blit(IMG_BACKGROUND, (0, 0))
    win.blit(IMG_BACKGROUND, (500, 0))
    for bird in birds:
        bird.draw(win)
    for pipe in pipes:
        pipe.draw(win)
    floor.draw(win)

    score_text = FONT_SCORE.render("Score: " + str(score), True, (255, 255, 255))
    win.blit(score_text, (WIDTH - 10 - score_text.get_width(), 10))

    if geracao is not None:
        score_text = FONT_SCORE.render("Geracao: " + str(geracao), True, (255, 255, 255))
        win.blit(score_text, (10, 10))

    pygame.display.update()


def main(genomas, config, ia_player=True):
    win = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    if ia_player:
        global geracao
        geracao += 1
        redes = []
        genomas_list = []
        birds = []

        for _, genoma in genomas:
            rede = neat.nn.FeedForwardNetwork.create(genoma, config)
            redes.append(rede)
            genoma.fitness = 0
            genomas_list.append(genoma)
            birds.append(Bird(230, 350))
    else:
        birds = [Bird(230, 350)]
    floor = Floor(730)
    pipes = [Pipe(1000)]
    score = 0

    while len(birds) > 0:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not ia_player:
                    for bird in birds:
                        bird.jump()

        for _, bird in enumerate(birds):
            bird.move()
            if ia_player:
                genomas_list[_].fitness += 0.1
                next_pipe = None
                for pipe in pipes:
                    if not pipe.passed:
                        next_pipe = pipe
                        break
                output = redes[_].activate((bird.y, abs(bird.y - next_pipe.height), abs(bird.y - next_pipe.bottom)))
                bird.next_pipe = next_pipe
                if output[0] > 0.5:
                    bird.jump()

        floor.move()
        remove = []
        for pipe in pipes:
            for index, bird in enumerate(birds):
                if pipe.collide(bird):
                    birds.pop(index)
                    if ia_player:
                        genomas_list[index].fitness -= 5
                        redes.pop(index)
                        genomas_list.pop(index)
                if not pipe.passed and bird.x > pipe.x + IMG_PIPE.get_width():
                    pipe.passed = True
                    score += 1
                    if ia_player:
                        for genoma in genomas_list:
                            genoma.fitness += 5

            pipe.move()

        if pipes[-1].x + IMG_PIPE.get_width() < 900:
            pipes.append(Pipe(pipes[-1].x + 300))

        for r in remove:
            pipes.remove(r)

        for index, bird in enumerate(birds):
            if bird.y + bird.img.get_height() >= 730 or bird.y < 0:
                birds.pop(index)
                if ia_player:
                    genomas_list[index].fitness -= 10
                    redes.pop(index)
                    genomas_list.pop(index)

        if ia_player:
            draw_window(win, birds, pipes, floor, score, geracao)
        else:
            draw_window(win, birds, pipes, floor, score)


def run(config_path):
    config = neat.config.Config(neat.DefaultGenome,
                                neat.DefaultReproduction,
                                neat.DefaultSpeciesSet,
                                neat.DefaultStagnation, config_path)

    population = neat.Population(config)

    population.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    population.add_reporter(stats)

    winner = population.run(fitness_function=main, n=50)

    print('\nBest genome:\n{!s}'.format(winner))


if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config.txt")
    #run(config_path)
    main(None, None, False)


