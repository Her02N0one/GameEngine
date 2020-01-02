import pygame

import constants


class Player(pygame.sprite.Sprite):

    def __init__(self, x=0, y=0):
        self.groups = constants.all_sprites, constants.entities
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.image = pygame.Surface((constants.TILE_SIZE, constants.TILE_SIZE))
        self.image.fill(constants.YELLOW)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.can_jump = False
        self.jumping = False
        self.velocity_index = 0

        self.velocity = list([(i / 2.0) - 15 for i in range(0, 31)])

        self.downward_force = constants.GRAVITY

    def move(self, dt, dx=0.0, dy=0.0):
        if not self.collide_with_tiles(dx, dy):
            self.x += (dx * dt) * 100
            self.y += (dy * dt) * 100

    def collide_with_tiles(self, dx=0.0, dy=0.0):
        # TODO: add better collision because quite frankly this system just aint' workin all that great.
        for tile in constants.tiles:
            if tile.rect.colliderect(self.rect.move(dx, dy)):
                self.can_jump = True
                return True
        self.can_jump = False
        return False

    def jump(self, dt):
        if (self.can_jump or self.jumping) and self.velocity_index >= 0:
            self.jumping = True
        else:
            self.jumping = False

    def update(self, dt):

        # update gravity
        if not self.collide_with_tiles(dt, dy=self.downward_force):
            self.move(dt, dy=self.downward_force)
            self.downward_force = constants.GRAVITY
        else:
            self.downward_force -= 1

        # check if the player is jumping and do this complicated bullshit that took me like, 3 hours to find
        if self.jumping:
            self.move(dt, dy=self.velocity[self.velocity_index])
            self.velocity_index += 1
            if self.velocity_index >= len(self.velocity) - 1:
                self.velocity_index = len(self.velocity) - 1
        if self.velocity_index == len(self.velocity) - 1:
            self.jumping = False
            self.velocity_index = 0

        self.rect.x = self.x
        self.rect.y = self.y
