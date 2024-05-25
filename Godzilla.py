import pygame
import random
import time
import math
import os
import sys


pygame.init()
pygame.font.init()


bar_height = 45


screen_width = 800
screen_height = 600+bar_height
black = (0, 0, 0)
red = (213, 50, 80)
white = (255, 255, 255)
blue = (0, 255, 255)
frame_rate = 60  
clock = pygame.time.Clock()

  
retro_font = pygame.font.Font('./assets/retro_computer.ttf', 20) 




screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Godzilla: Destroyer of Boats")
clock = pygame.time.Clock()


background_img = pygame.image.load('./assets/4final.png')
background_img = pygame.transform.scale(background_img, (screen_width, 600))


godzilla_img = pygame.image.load('./assets/godzilla2.png')
godzilla_img = pygame.transform.scale(godzilla_img, (120, 120))
boat_img = pygame.image.load('./assets/boat.png')
boat_img = pygame.transform.scale(boat_img, (120, 120))


explosion_sprite_sheet = pygame.image.load('./assets/explosion_sprite_sheet.png')
num_frames = 5  
explosion_frames = []

frame_width = explosion_sprite_sheet.get_width() // num_frames
frame_height = explosion_sprite_sheet.get_height()


for i in range(num_frames):
    
    frame_rect = pygame.Rect(i * frame_width, 0, frame_width, frame_height)
    frame = explosion_sprite_sheet.subsurface(frame_rect)
    explosion_frames.append(pygame.transform.scale(frame, (60, 60)))



sprite_sheet_path = './assets/res1.png'
sprite_sheet = pygame.image.load(sprite_sheet_path)
frame_width = 330  
frame_height = 135  
num_wave_frames = 8

wave_frames = []


for i in range(num_wave_frames):
    frame_rect = pygame.Rect(i * frame_width, 0, frame_width, frame_height)
    frame = sprite_sheet.subsurface(frame_rect)  
    wave_frames.append(frame)
    

pygame.mixer.init()
destruction_sound = pygame.mixer.Sound('./assets/destruction_sound.wav')
background_music = './assets/background_music.mp3'
pygame.mixer.music.load(background_music)
pygame.mixer.music.play(-1)  


block_size = 20
godzilla_speed = 10


font_style = pygame.font.SysFont(None, 50)

def message(msg, color):
    mesg = font_style.render(msg, True, color)
    screen.blit(mesg, [screen_width / 6, screen_height / 3])


def display_score(score):
    score_text = retro_font.render("Score: " + str(score), True, red)
    screen.blit(score_text, [10, 5])


class Explosion:
    def __init__(self, x, y, frames, speed=10):
        self.x = x
        self.y = y
        self.frames = frames
        self.speed = speed
        self.current_frame = 0
        self.active = True  

    def update(self):
        
        self.current_frame += 1
        if self.current_frame >= len(self.frames):
            self.active = False
    
    def draw(self, surface):
        if self.active:
            
            surface.blit(self.frames[self.current_frame], (self.x, self.y))

def draw_godzilla(x, y, facing_right):
    if facing_right:
        screen.blit(godzilla_img, (x, y))
    else:
        flipped_image = pygame.transform.flip(godzilla_img, True, False)  
        screen.blit(flipped_image, (x, y))

class WaveParticle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.lifetime = random.randint(30, 60)  
        self.size = random.randint(2, 5)  
        self.angle = random.uniform(0, 2 * math.pi)  
        self.angular_velocity = random.uniform(-0.05, 0.05)  
        self.radius = random.uniform(10, 25)  

    def update(self):
        
        self.angle += self.angular_velocity
        self.x += math.cos(self.angle) * self.radius
        self.y += math.sin(self.angle) * self.radius
        self.lifetime -= 1

    def draw(self, surface):
        pygame.draw.circle(surface, (0, 191, 255), (int(self.x), int(self.y)), self.size)  

class WaveParticleSystem:
    def __init__(self):
        self.particles = []

    def create_wave_particles(self, x, y):
        
        for _ in range(10):  
            self.particles.append(WaveParticle(x, y))

    def update(self):
        
        for particle in self.particles[:]:
            particle.update()
            if particle.lifetime <= 0:
                self.particles.remove(particle)

    def draw(self, surface):
        
        for particle in self.particles:
            particle.draw(surface)

wave_particle_system = WaveParticleSystem()
wobble_amplitude_x = 5  
wobble_amplitude_y = 5  
wobble_frequency = 0.05 


def load_sprites_from_folder(folder):
    filenames = sorted([f for f in os.listdir(folder) if f.endswith(".png")])
    frames = []
    for filename in filenames:
        filepath = os.path.join(folder, filename)
        frame = pygame.image.load(filepath)
        frames.append(frame)
        return frames

wave_folder_under = "./water8/png"
wave_folder_left = "./water5/png"
wave_folder_top = "./Water2/png"


wave_under_path = load_sprites_from_folder(wave_folder_under)
wave_left_path = load_sprites_from_folder(wave_folder_left)
wave_top_path = load_sprites_from_folder(wave_folder_top)

common_frame_width = 300  
common_frame_height = 300  


def load_and_scale_frames(folder_path, frame_width, frame_height):
    frames = []
    file_names = sorted([f for f in os.listdir(folder_path) if f.endswith(".png")])
    for file_name in file_names:
        frame_path = os.path.join(folder_path, file_name)
        frame = pygame.image.load(frame_path)  
        scaled_frame = pygame.transform.scale(frame, (frame_width, frame_height))  
        frames.append(scaled_frame)
    return frames


wave_frames_under = load_and_scale_frames(wave_folder_under, common_frame_width, common_frame_height)
wave_frames_left = load_and_scale_frames(wave_folder_left, common_frame_width, common_frame_height)
wave_frames_top = load_and_scale_frames(wave_folder_top, common_frame_width, common_frame_height)

class WaveAnimation:
    def __init__(self, frames, speed=10):
        self.frames = frames
        self.speed = speed
        self.current_frame = 0
        self.timer = 0
        self.flipped = False  

    def update(self):
        self.timer += 1
        if self.timer >= self.speed:
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.timer = 0
    
    def draw(self, x, y, surface):
        if self.flipped:
            current_frame = pygame.transform.flip(self.frames[self.current_frame], True, False)
        else:
            current_frame = self.frames[self.current_frame]
        surface.blit(current_frame, (x, y))

'''

offset_under = (-100, 200)  
offset_left = (400, 0)  
offset_top = (0, -400) 
animation_under = WaveAnimation(wave_frames_under, speed=10)
animation_left = WaveAnimation(wave_frames_left, speed=10)
animation_top = WaveAnimation(wave_frames_top, speed=10)
'''

animation_under = WaveAnimation(wave_frames_under, speed=10)
animation_left = WaveAnimation(wave_frames_left, speed=10)
animation_top = WaveAnimation(wave_frames_top, speed=10)

class AtomicBreath:
    def __init__(self, x, y, frames, speed=30, direction='right', impact_radius=40):
        self.x = x
        self.y = y
        self.frames = frames
        self.speed = speed
        self.direction = direction
        self.impact_radius = impact_radius  
        self.current_frame = 0
        self.active = True

    def update(self):
        self.current_frame = (self.current_frame + 1) % len(self.frames)

        if self.direction == 'right':
            self.x += 10  
        elif self.direction == 'left':
            self.x -= 10  

        
        if self.x < 0 or self.x > screen_width:
            self.active = False

    def draw(self, surface):
        if self.active:
            surface.blit(self.frames[self.current_frame], (self.x, self.y))

folder_path = "./atomic breath"
atomic_breath_frames = load_and_scale_frames(folder_path, 60, 60)

atomic_breath_sprite_sheet_path = "./assets/kame.png"
atomic_breath_sprite_sheet = pygame.image.load(atomic_breath_sprite_sheet_path)
number_of_atomic_breath_frames = 5

sprite_sheet_height = atomic_breath_sprite_sheet.get_height()  
frame_width = atomic_breath_sprite_sheet.get_width()  
frame_height = sprite_sheet_height // number_of_atomic_breath_frames

def display_text(text, position, font, color):
    text_surface = retro_font.render(text, True, color)
    screen.blit(text_surface, position)


def main_menu():
    menu_active = True
    current_selection = 0  
    menu_image_path = "./assets/tit.png"  
    menu_image = pygame.image.load(menu_image_path)
    desire1_width = 800  
    desire1_height = 700  
    resized_menu_image = pygame.transform.scale(menu_image, (desire1_width, desire1_height))
    image_x2 = (screen_width - desired_width) / 2
    image_y2 = 20  

    menu_options = ["Start Game", "Quit Game", "Super Secret Third Option", "Super Secret Fourth Option"]  
    menu_y_positions = [screen_height // 3, (screen_height // 3) + 50, (screen_height // 3) + 100, (screen_height // 3) + 150]

    while menu_active:
        screen.fill(black)  
        screen.blit(resized_menu_image, (image_x2, image_y2))

        
        display_text("Main Menu", (screen_width // 3, screen_height // 4), font_style, red)

        
        for i, option in enumerate(menu_options):
            if i == current_selection:
                display_text(f"> {option}", (screen_width // 3 - 20, menu_y_positions[i]), font_style, white)  
            else:
                display_text(option, (screen_width // 3, menu_y_positions[i]), font_style, red)

        pygame.display.update()  

        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                menu_active = False
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    current_selection = (current_selection + 1) % len(menu_options)  
                elif event.key == pygame.K_UP:
                    current_selection = (current_selection - 1) % len(menu_options)  
                elif event.key == pygame.K_RETURN:  
                    if current_selection == 0:
                        menu_active = False  
                        return  
                    elif current_selection == 2:
                        view_image()  
                    elif current_selection == 3:
                        view_image2() 
                    elif current_selection == 1:
                        menu_active = False
                        pygame.quit()
                        quit()  

image_path = "./assets/ily.jpg"
desired_width = 500  
desired_height = 500  


image = pygame.image.load(image_path)
image = pygame.transform.scale(image, (desired_width, desired_height))


image_x = (screen_width - desired_width) // 2
image_y = (screen_height - desired_height) // 2

image_path2 = "./assets/fart.jpg"
image2 = pygame.image.load(image_path2)
image2 = pygame.transform.scale(image2, (desired_width, desired_height))


back_text_x = 10  
back_text_y = screen_height - 50  




def view_image():
    image_displayed = True
    while image_displayed:
        screen.fill(black)  
        screen.blit(image, (image_x, image_y))  
        display_text("Press BACKSPACE to return", (back_text_x, back_text_y), font_style, red)  

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    image_displayed = False  
def view_image2():
    image_displayed = True
    while image_displayed:
        screen.fill(black)  
        screen.blit(image2, (image_x, image_y))  
        display_text("Press BACKSPACE to return", (back_text_x, back_text_y), font_style, red)  

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    image_displayed = False 
atomic_breaths = []

def gameLoop():
    time_elapsed = 0  
    game_over = False
    game_close = False
    score = 0
    explosions = []  

    offset_under = (-90, -70)  
    offset_left = (0, 0)  
    offset_top = (-80, -160) 

    
    x1 = screen_width / 2
    y1 = screen_height / 2
    facing_right = True
    offset_right = (40, -20)  
    offset_left = (-40, -20)

    
    x1_change = 0
    y1_change = 0

    
    boat_x = round(random.randrange(0, screen_width - block_size) / 20.0) * 20.0
    boat_y = round(random.randrange(0, screen_height - block_size) / 20.0) * 20.0  

    

    while not game_over:
        while game_close:
            screen.fill(black)  
            game_over_text = retro_font.render("Game Over", True, red)
            final_score_text = retro_font.render(f"Final Score: {score}", True, red)
            continue_quit_text = retro_font.render("Press Enter to continue or Backspace to Main Menu", True, red)
            top_margin = 50  
            line_spacing = 40  
            game_over_pos = (screen_width / 2 - game_over_text.get_width() / 2, top_margin)  
            final_score_pos = (screen_width / 2 - final_score_text.get_width() / 2, game_over_pos[1] + line_spacing)  
            continue_quit_pos = (screen_width / 2 - continue_quit_text.get_width() / 2, final_score_pos[1] + line_spacing)  
            image_path = "./assets/ily5.jpg"
            game_over_image = pygame.image.load(image_path)
            image_width, image_height = game_over_image.get_size()
            image_x = screen_width / 2 - image_width / 2
            image_y = continue_quit_pos[1] + line_spacing + 40
            screen.blit(game_over_text, game_over_pos)
            screen.blit(final_score_text, final_score_pos)
            screen.blit(continue_quit_text, continue_quit_pos)
    
    
            screen.blit(game_over_image, (image_x, image_y))
            pygame.display.update()
            time.sleep(1)  

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        main_menu()
                    elif event.key == pygame.K_RETURN:
                        gameLoop()  

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change = -block_size
                    y1_change = 0
                    facing_right = False
                elif event.key == pygame.K_RIGHT:
                    x1_change = block_size
                    y1_change = 0
                    facing_right = True
                elif event.key == pygame.K_UP:
                    y1_change = -block_size
                    x1_change = 0
                elif event.key == pygame.K_DOWN:
                    y1_change = block_size
                    x1_change = 0
                elif event.key == pygame.K_SPACE:
                    if facing_right:
                        
                        atomic_breaths.append(
                            AtomicBreath(x1 + offset_right[0], y1 + offset_right[1], atomic_breath_frames, direction='right')
                        )
                    else:
                        
                        atomic_breaths.append(
                            AtomicBreath(x1 + offset_left[0], y1 + offset_left[1], atomic_breath_frames, direction='left')
                        )
        for breath in list(atomic_breaths):
            breath.update()
            breath.draw(screen)

        


        
        if x1 >= screen_width or x1 < 0 or y1 >= screen_height or y1 < bar_height:
            game_close = True  
            
        animation_under.update()
        animation_left.update()
        animation_top.update()

        x1 += x1_change
        y1 += y1_change

        
        

        time_elapsed += clock.get_time()  
        wobble_offset_x = math.sin(time_elapsed * wobble_frequency) * wobble_amplitude_x  
        wobble_offset_y = math.sin(time_elapsed * wobble_frequency * 1.5) * wobble_amplitude_y  

        
        screen.blit(background_img, (0, bar_height))

        screen.fill(black, rect=[0, 0, screen_width, bar_height])

        
        screen.blit(boat_img, (boat_x, boat_y))

        

        
        
        animation_under.update()
        
        animation_top.update()

        
        if not facing_right:
            animation_under.flipped = True
            animation_left.flipped = True
            animation_top.flipped = True
        else:
            animation_under.flipped = False
            animation_left.flipped = False
            animation_top.flipped = False


        
        
        
        
        
        draw_godzilla(x1 + wobble_offset_x, y1 + wobble_offset_y, facing_right)
        animation_top.draw(x1 + offset_top[0], y1 + offset_top[1], screen)  

        

        
        if x1 < boat_x + 60 and x1 + 120 > boat_x and y1 < boat_y + 60 and y1 + 120 > boat_y:
            
            pygame.mixer.Sound.play(destruction_sound)
            score += 1  

            
            explosions.append(Explosion(boat_x, boat_y, explosion_frames, speed=5))  

            
            boat_x = round(random.randrange(0, screen_width - block_size) / 20.0) * 20.0
            boat_y = round(random.randrange(bar_height, screen_height - block_size) / 20.0) * 20.0  
        
        for breath in list(atomic_breaths):
            breath.update()
            breath.draw(screen)

            
            if breath.active and (
                breath.x + breath.impact_radius  >= boat_x and breath.x - breath.impact_radius <= boat_x + 120 and
                breath.y + breath.impact_radius>= boat_y and breath.y - breath.impact_radius <= boat_y + 120 ):
                
                atomic_breaths.remove(breath)  
                pygame.mixer.Sound.play(destruction_sound)  
                score += 1  

                
                explosions.append(Explosion(boat_x, boat_y, explosion_frames, speed=5))

                boat_x = round(random.randrange(0, screen_width - block_size) / 20.0) * 20.0
                boat_y = round(random.randrange(bar_height, screen_height - block_size) / 20.0) * 20.0
        


        
        for explosion in list(explosions):
            if explosion.active:
                explosion.update()
                explosion.draw(screen)  
            else:
                explosions.remove(explosion)  


        display_score(score)

        pygame.display.update() 
        clock.tick(godzilla_speed)  

    pygame.quit()  
    quit()
    
main_menu()
gameLoop()
