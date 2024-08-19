import pygame,sys
from random import randint, choice

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.player_walk_1 = pygame.image.load("graphics/player.png").convert_alpha()
        self.player_walk_2 = pygame.image.load("graphics/player_run.png").convert_alpha()
        self.player_walk = [self.player_walk_1, self.player_walk_2]

        self.player_index = 0
        self.player_jump = pygame.image.load("graphics/player_jump.png").convert_alpha()

        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom = (150,350)).inflate(-35,-35)  #you cant have a sprite class without slef.image and self.rect
        self.gravity = 0

        self.jump_sound = pygame.mixer.Sound("audio/jump sound.mp3")

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 320:
            self.gravity = -20
            self.jump_sound.play()
    
    def apply_gravity(self):
        self.gravity +=1
        self.rect.y += self.gravity

        if self.rect.bottom >= 320:
            self.rect.bottom = 320

    def animation_state(self):
        if self.rect.bottom < 255:
            self.image = self.player_jump
        else:
            self.player_index += 0.1
            if self.player_index >=  len(self.player_walk):
                self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_state()

class Obstacle(pygame.sprite.Sprite):
    def __init__(self,type):
        super().__init__()

        if type == "alien":
            alien_1 = pygame.image.load("graphics/alien.png").convert_alpha()
            alien_2 = pygame.image.load("graphics/alien_2.png").convert_alpha()
            self.frames = [alien_1, alien_2]
            y_pos = 330
        else:
            obstacle2_1 = pygame.image.load("graphics/obst2.png").convert_alpha()
            obstacle2_2 = pygame.image.load("graphics/obst2_2.png").convert_alpha()
            self.frames = [obstacle2_1, obstacle2_2]
            y_pos = 230

        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(bottomright = (randint(700,1100),y_pos)).inflate(-30,-30)

    def animation_state(self):
        self.animation_index += 0.1

        if self.animation_index >= len(self.frames):
            self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    def update(self):
        self.animation_state()
        self.rect.x -= 6
        self.destroy()

    def destroy(self):
        if self.rect.x > 1000:
            self.kill()

def display_score():
    current_time = int(pygame.time.get_ticks() / 1000) - start_time
    score_surf = test_font.render(f"Score: {current_time}", False, "white")
    score_rect = score_surf.get_rect(center = (400,60))
    screen.blit(score_surf, score_rect)
    return current_time

def collison_sprite():
    if pygame.sprite.spritecollide(player_c.sprite, obstacle_group,False):
        #emptying the obstacle group so that when collision occurs, all the obstacles are deleted
        obstacle_group.empty()
        return False
    else:
        return True

pygame.init()
screen = pygame.display.set_mode((800,400))
pygame.display.set_caption("Runner")
 
#setting the frame rate of game
clock = pygame.time.Clock()

game_active = False 
start_time = 0
score = 0
bg_music = pygame.mixer.Sound("audio/bg music.mp3")
bg_music.play(loops = -1)  #-1 means forever

#groups
player_c = pygame.sprite.GroupSingle()
player_c.add(Player())
obstacle_group = pygame.sprite.Group()

#creating a font
test_font = pygame.font.Font("font/Pixeltype.ttf", 50)

#convert alpha makes ur game smooth
sky_surface = pygame.image.load("graphics/background.png").convert()
ground_surface = pygame.image.load("graphics/ground.png").convert_alpha()

#player at the intro screen
player_intro = pygame.image.load("graphics/intro_astronaut.png").convert_alpha()
player_intro = pygame.transform.scale(player_intro,(100,100))
player_intro_rect = player_intro.get_rect(center = (750,60))

#intro screen
intro_text1 = test_font.render("Welcome  to  Astro-player", False, "white")
intro_text1_rect = intro_text1.get_rect(center = (400,50))

intro_text2 = test_font.render("Instructions: ", False, "white")
intro_text2_rect = intro_text2.get_rect(center = (130,100))

intro_text3 = test_font.render("1.  Press  Space  to  Jump", False, "white")
intro_text3_rect = intro_text3.get_rect(center = (200,150))

intro_text4 = test_font.render("2.  Avoid  the  aliens", False, "white")
intro_text4_rect = intro_text4.get_rect(center = (155,210))

intro_text5 = test_font.render("Press  Space  Bar  to  start  playing", False, "white")
intro_text5_rect = intro_text5.get_rect(center = (400,300))

#timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1500)    #triggering the timer every 900 miliseconds, so that after this time, the obstacle should appear

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if game_active: 
            if event.type == obstacle_timer:
                obstacle_group.add(Obstacle(choice(["alien", "alien", "obstacle"])))

        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                start_time = int(pygame.time.get_ticks()/1000)

    if game_active:
        screen.blit(sky_surface, (0,0))
        screen.blit(ground_surface, (0,100))

        score = display_score()

        #there are two main functions of sprite: to draw and to update
        #calling the group
        player_c.draw(screen) 
        player_c.update()

        obstacle_group.draw(screen)
        obstacle_group.update()

        game_active = collison_sprite()
        
    else:
        screen.fill((67, 47, 115))
        screen.blit(player_intro, player_intro_rect)
        
        score_message = test_font.render(f"Score: {score}", False, "white")
        score_message_rect = score_message.get_rect(center = (400,300))

        if score == 0:
            screen.blit(intro_text1, intro_text1_rect)
            screen.blit(intro_text2, intro_text2_rect)
            screen.blit(intro_text3, intro_text3_rect)
            screen.blit(intro_text4, intro_text4_rect)
            screen.blit(intro_text5, intro_text5_rect)
        else:
            screen.blit(intro_text1, intro_text1_rect)
            screen.blit(intro_text2, intro_text2_rect)
            screen.blit(intro_text3, intro_text3_rect)
            screen.blit(intro_text4, intro_text4_rect)
            screen.blit(score_message, score_message_rect)

    pygame.display.update()
    clock.tick(60)