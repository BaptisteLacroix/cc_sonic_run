from typing import List

import pygame
from projectile import Projectile
from glob import glob

# jump_height = 50

img_loader = lambda img: pygame.transform.scale(pygame.image.load(img), (200, 200))
left_anim_imgs = list(map(img_loader, glob("./img/running/left/SonicRun*.png")))
right_anim_imgs = list(map(img_loader, glob("./img/running/right/SonicRun*.png")))


# Joueur Sonic
class Player(pygame.sprite.Sprite):
    """
    Un joueur contenant toutes ses caractéristiques.
    """
    left_anim_iter = iter(left_anim_imgs)
    right_anim_iter = iter(right_anim_imgs)
    anim_counter = 0

    def __init__(self, game):
        """
        Initalise le joueur en créant:
            - son image
            - ses points de vie
            - ses points d'attaque
            - sa vitesse
            - ses projectiles
        :param game:
        """
        super().__init__()
        self.game = game
        self.attack = 50
        self.health = 102
        self.max_health = 102
        self.velocity = 4
        self.all_projectiles = pygame.sprite.Group()
        self.image = pygame.image.load("img/SonicStatiqueRight.png")
        self.rect = self.image.get_rect()
        self.rect.x = 50
        self.rect.y = 200
        self.onGround = False

    def jump(self):
        """
        Permet de faire sauter le personnage.
        :return:
        """
        if not self.onGround:
            print("self.onGround")
            return
        self.velocity = 8
        self.onGround = False

    def damage(self, amount):
        """
        Permet d'infliger des dégats au Joueur et de lancer la fonction game Over si le perosnnage n'a plus de vie.
        :param amount:
        :return:
        """
        if self.health - amount > amount:
            self.health -= amount
        else:
            # si le joueur n'a plus de points de vie
            self.game.game_over()

    def update_health_bar(self, surface):
        """
        Permet de mettre à jour la barre de vie du Player et des monstres.
        :param surface: Surface sur laquelle afficher les éléments graphiques.
        :return:
        """
        # dessiner la barre de vie
        pygame.draw.rect(surface, (60, 63, 60), [self.rect.x + 15, self.rect.y - 20, self.max_health, 7])
        pygame.draw.rect(surface, (229, 25, 25), [self.rect.x + 15, self.rect.y - 20, self.health, 7])

    def launch_projectile(self):
        """
        Permet l'apparition des projectiles en jeu.
        :return:
        """
        # créer une nouvelle instance de la classe projectile
        self.all_projectiles.add(Projectile(self))

    def move_right(self):
        """
        Permet le déplacement vers la droite tant qu'il n'y a pas de colision.
        :return:
        """
        if not self.game.check_collision(self, self.game.all_pics):
            self.rect.x += self.velocity

    def move_left(self):
        """
        Permet le déplacement vers la gauche tant qu'il n'y a pas de colision.
        :return:
        """
        if not self.game.check_collision(self, self.game.all_pics):
            self.rect.x -= self.velocity

    def move_up(self):
        """
        Permet le déplacement vers le haut tant qu'il n'y a pas de colision.
        :return:
        """
        if not self.game.check_collision(self, self.game.all_pics):
            self.rect.y -= self.velocity

    def process_movement_animation(self, keys: List[bool]) -> None:
        """
        Processes the character movement animation
        :type keys: list[bool]
        :param keys: Pressed keys status
        :return: None
        """
        if Player.anim_counter % self.velocity == 0:
            if keys[pygame.K_a]:
                try:
                    self.image = next(Player.left_anim_iter)
                except(StopIteration):
                    Player.left_anim_iter = iter(left_anim_imgs)
                    self.image = next(Player.left_anim_iter)
            elif keys[pygame.K_d]:
                try:
                    self.image = next(Player.right_anim_iter)
                except(StopIteration):
                    Player.right_anim_iter = iter(right_anim_imgs)
                    self.image = next(Player.right_anim_iter)
            else:
                self.image = pygame.image.load("img/SonicStatiqueRight.png")
        Player.anim_counter += 1
