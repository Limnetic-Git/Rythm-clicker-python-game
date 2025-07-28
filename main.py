import pygame
import sys
from rect import Rect

#FDCBAS
def game_tier(mistakes):
    if mistakes >= 60: return 'F'
    elif mistakes >= 40: return 'D'
    elif mistakes >= 20: return 'C'
    elif mistakes >= 10: return 'B'
    elif mistakes >= 5: return 'A'
    elif mistakes == 0: return 'S'
    else: return 'A+'
    
def percentages(a, b):
    return round((a * 100) / b, 1)

def restart_game():
    global game_map, reader, mistakes, tick 
    reader, mistakes, tick = 0, 0, 0
    game_map = []
    for x in range(8):
        game_map.append([])
        for y in range(8):
            game_map[-1].append(Rect(x, y, 160))
    pygame.mixer.music.stop()
    
FPS = 60

pygame.init()
pygame.font.init()


W, H = 800, 800
sc = pygame.display.set_mode((W, H))
bg_color = [0, 0, 0]
clock = pygame.time.Clock()
default_font = pygame.font.Font(None, 36)


song_name = 'bleed'
try:
    with open(f'songs/{song_name}.songlvl') as f:
        pack = eval(f.readlines()[0])
    song, drops = pack['song'], pack['drops']
except FileNotFoundError:
    song, drops = [], []


game_map = []
for x in range(8):
    game_map.append([])
    for y in range(8):
        game_map[-1].append(Rect(x, y, 160))
        
tick = 0

last_song_tick = song[-1]['tick']

pygame.mixer.music.load(f'songs/{song_name}.mp3')
pygame.mixer.music.set_volume(0.25)
reader = 0
game = True
mistakes = 0
current_position = 0
while True:
    current_position = percentages(tick, last_song_tick)
    
    xm, ym = pygame.mouse.get_pos()
    sc.fill(bg_color)
    if game:
        for x in range(len(game_map)):
            for y in range(len(game_map)):
                game_map[x][y].draw(sc)
                mistakes = game_map[x][y].tick(mistakes)
        try:
            if tick >= song[reader]['tick'] - 55:
                game_map[song[reader]['x']][song[reader]['y']].active = True
                reader += 1
        except IndexError: game = False
        text = default_font.render(f'{current_position}%', True, (210, 210, 255))
        sc.blit(text, (385, 3))
    else:

        text = default_font.render(f'Вы сделали {mistakes} ошибок!', True, (210, 210, 255))
        grade = default_font.render(f'Ранг прохождения: {game_tier(mistakes)}', True, (255, 210, 210))
        sc.blit(text, (250, 310))
        sc.blit(grade, (260, 355))
    
        
        
        
    clock.tick(FPS)

    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            sys.exit()
        if ev.type == pygame.MOUSEBUTTONDOWN:
            if ev.button == 1:
                game_map[xm // 160][ym // 160].click()
                #song.append({'x':  xm // 160, 'y': ym // 160, 'tick': tick})
            if ev.button == 2:
                print(drops)
            if ev.button == 3:
                drops.append(tick)
        if ev.type == pygame.KEYDOWN:
            if ev.key == pygame.K_r:
                restart_game()
                print('ssvsv')
            
                
    if tick == 300:
        pygame.mixer.music.play()
        
    if tick in drops:
        bg_color[0] = 45
        
    if bg_color[0] > 0: bg_color[0] -= 1
    pygame.display.update()
    tick += 1