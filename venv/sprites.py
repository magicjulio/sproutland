import pygame
from settings import *
from random import randint, choice
from timer import Timer


class Generic(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups, z = LAYERS["main"]):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft= pos)
        self.z = z
        self.hitbox = self.rect.copy().inflate((-self.rect.width * 0.2, -self.rect.height * 0.75))

class Interaction(Generic):
    def __init__(self, pos, size, groups, name):
        surf = pygame.Surface(size)
        super().__init__(pos, surf, groups)
        self.name = name


# wasser (moving)
class Water(Generic):
    def __init__(self, pos, frames, groups):

        # animation setup
        self.frames = frames
        self.frames_index = 0

        # sprite setup
        super().__init__(pos=pos,
                         surf=self.frames[self.frames_index],
                         groups=groups,
                         z = LAYERS["water"],
                         )
    def animate(self, dt):
        self.frames_index += 5 * dt
        if self.frames_index >= len(self.frames):
            self.frames_index = 0

        self.image = self.frames[int(self.frames_index)]

    def update(self, dt):
        self.animate(dt)

# blumen
class WildFlower(Generic):
    def __init__(self, pos, surf, groups):
        super().__init__(pos, surf, groups)
        self.hitbox = self.rect.copy().inflate(-20, -self.rect.height * 0.9)

# partikel effekt
class Particle(Generic):
    def __init__(self, pos, surf, groups, z, duration= 200):
        super().__init__(pos, surf, groups, z)
        self.start_time = pygame.time.get_ticks()
        self.duration = duration

        # weißer umriss
        mask = pygame.mask.from_surface(self.image)
        new_surf = mask.to_surface()
        new_surf.set_colorkey((0, 0, 0))
        self.image = new_surf


    def update(self, dt):
        current_time = pygame.time.get_ticks()
        if current_time - self.start_time > self.duration:
            self.kill()

class Tree(Generic):
    def __init__(self, pos, surf, groups, name, player_add):
        super().__init__(pos, surf, groups)

        self.health = 5
        self.alive = True
        stump_path = f"../graphics/stumps/{'small' if name == 'Small' else 'large'}.png"
        self.stump_surf = pygame.image.load(stump_path).convert_alpha()
        self.invole_tim = Timer(200)


        self.apples_surf = pygame.image.load("../graphics/fruit/apple.png")
        self.apples_pos = APPLE_POS[name]
        self.apples_sprite = pygame.sprite.Group()
        self.create_fruit()

        self.player_add = player_add

    def damage(self):
        self.health -= 1
        # rm apple if apple
        if len(self.apples_sprite.sprites()) >0:
            random_apple = choice(self.apples_sprite.sprites())
            Particle(pos= random_apple.rect.topleft,
                     surf= random_apple.image,
                     groups=self.groups()[0],
                     z=LAYERS["fruit"])
            self.player_add("apple")
            random_apple.kill()


    def check_dead(self):
        if self.health <= 0:
            Particle(pos=self.rect.topleft,
                     surf=self.image,
                     groups=self.groups()[0],
                     z=LAYERS["fruit"],
                     duration=300)

            self.image = self.stump_surf
            self.rect = self.image.get_rect(midbottom= self.rect.midbottom)
            self.hitbox = self.rect.copy().inflate(-10, -self.rect.height * 0.6)
            self.alive = False
            self.player_add("wood")

    def update(self, dt):
        if self.alive:
            self.check_dead()

    def create_fruit(self):
        for pos in self.apples_pos:
            if randint(0, 10) < 2:
                x = pos[0] + self.rect.left
                y = pos[1] + self.rect.top

                Generic(
                        pos=(x, y),
                        surf=self.apples_surf,
                        groups=[self.apples_sprite,self.groups()[0]],
                        z = LAYERS["fruit"]
                )