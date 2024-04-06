from button import Button
import pygame
from pygame import mixer
from settings import *
from player import *
from world import *

# initialize pygame and mixer
pygame.init()
mixer.init()

# fonts
menu_font = pygame.font.SysFont('Calibri', SCALE)
ui_font = pygame.font.SysFont('gomarice_no_continue', 36, 'bold')
ui_font_2 = pygame.font.SysFont('gomarice_no_continue', 55, 'bold')
ui_font_3 = pygame.font.SysFont('gomarice_no_continue', 24)

# menu image
menu_img = pygame.transform.scale(
    pygame.image.load('graphics/menu.jpg'), (W, H))
game_over_img = pygame.transform.scale(
    pygame.image.load('graphics/skull.jpg'), (W*0.8, H*0.8))

# buttons and button images
btn_list = ['new game', 'load', 'options', 'exit']
back_btn_img = pygame.image.load(
    'graphics/menu buttons/Large Buttons/Back Button.png')
audio_btn = pygame.transform.scale(pygame.image.load(
    'graphics/menu buttons/Square Buttons/Audio Square Button.png'), (SCALE, SCALE))
music_btn = pygame.transform.scale(pygame.image.load(
    'graphics/menu buttons/Square Buttons/Music Square Button.png'), (SCALE, SCALE))
exit_img = pygame.image.load(
    'graphics/menu buttons/Square Buttons/X Square Button.png')
resume_img = pygame.image.load(
    'graphics/menu buttons/Square Buttons/Play Square Button.png')
e_btn = Button(W*0.65, H*0.8, exit_img, 0.4)  # exit button
r_btn = Button(W*0.2, H*0.8, resume_img, 0.4)  # resume button

screen = pygame.display.set_mode((W, H))
clock = pygame.time.Clock()

# game conditions
display_menu = True
start_game = False
show_settings = False
show_levels = False
run = True
character_select = False
character = 0
loaded = False
lvl_num = 1
game_over = False
level_select = False
game_start_timer = 0
click_timer = 0  # click timer controls the rate of increase of volume in menu

while run:
    clock.tick(FPS)
    click_timer += 1
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            run = False

        # if m is pressed while in game, pause the game
        if event.type == pygame.KEYDOWN and start_game:
            if event.key == pygame.K_m:
                pause(clock, screen, r_btn, e_btn, ui_font_2)

    # main menu buttons and background image
    screen.blit(menu_img, (0, 0))

    # main menu
    if display_menu:
        for count, btn in enumerate(btn_list):
            btn_img = pygame.image.load(
                f'graphics/menu buttons/Large Buttons/{btn_list[count]}.png')
            btn = Button(W//2-(btn_img.get_width()/(SCALE/10)),
                         H//4+(1.5*SCALE*count), btn_img, SCALE/200)
            if btn.draw(screen):
                nav.play()
                if count == 0:  # new game button
                    display_menu = False
                    character_select = True
                if count == 1:  # load button to select the levels
                    display_menu = False
                    level_select = True
                if count == 2:  # settings button
                    display_menu = False
                    show_settings = True
                if count == 3:  # exit button
                    run = False

    # character select screen
    if character_select:
        buttons = []
        for x in range(1, 4):
            buttons.append(
                Button(W/4.5*x, H/2, pygame.image.load(f'graphics/menu buttons/char {x}.png'), 4))
            pos = pygame.mouse.get_pos()  # get mouse position on screen
            draw_text(60, 150, 'red', 'SELECT A CHARACTER...',
                      screen, ui_font_2)

            # if the mouse hovers over the button, draw a red rectangle
            if buttons[x-1].rect.collidepoint(pos):
                pygame.draw.rect(screen, 'red', buttons[x-1].rect, 6)
            if buttons[x-1].draw(screen):
                nav.play()
                character = x
                start_game = True
                character_select = False

    if show_settings:
        screen.blit(music_btn, (W/6, H/3))  # music icon
        screen.blit(audio_btn, (W/6, H/3+120))  # audio icon

        # on screen text
        draw_text(W*0.4, H*0.55, 'blue',
                  f'{str(int(vol*100))}%', screen, ui_font_2)
        draw_text(W*0.4, H*0.36, 'blue',
                  f'{str(int(music_vol*100))}%', screen, ui_font_2)

        # volume is increased or decreased based on the click_timer
        if Button(W*0.8, H*0.53, up_img, 4).draw(screen) and click_timer >= 25:
            nav.play()
            if vol < 1:
                vol += 0.05
            click_timer = 0
            change_audio_volume(vol)

        if Button(W*0.8, H*0.34, up_img, 4).draw(screen) and click_timer >= 25:
            nav.play()
            if music_vol < 1:
                music_vol += 0.05
            click_timer = 0
            change_music_volume(music_vol)

        if Button(W*0.7, H*0.53, down_img, 4).draw(screen) and click_timer >= 25:
            nav.play()
            if vol > 0:
                vol -= 0.05
            click_timer = 0
            change_audio_volume(vol)

        if Button(W*0.7, H*0.34, down_img, 4).draw(screen) and click_timer >= 25:
            nav.play()
            if music_vol > 0:
                music_vol -= 0.05
            click_timer = 0
            change_music_volume(music_vol)

        # back button
        if Button(W*0.35, H*0.8, back_btn_img, SCALE/200).draw(screen):
            nav.play()
            show_settings = False
            display_menu = True

    # game over screen
    if game_over:
        loaded = False
        start_game = False
        screen.fill('black')
        screen.blit(game_over_img, (W/10, 0))
        buttons = ['X', 'Home', 'Return']  # buttons that will be displayed
        for count, btn in enumerate(buttons):
            btn_img = pygame.image.load(
                f'graphics/menu buttons/Square Buttons/{buttons[count]} Square Button.png')
            b = Button(W/8 + (192 * count), H*0.8, btn_img, 0.3)
            if b.draw(screen):
                if count == 0:  # exit
                    run = False
                if count == 1:  # go to main menu
                    # reset these variables
                    display_menu = True
                    game_over = False
                    lvl_num = 1
                if count == 2:  # restart
                    game_over = False
                    start_game = True

    # level select screen
    if level_select:
        buttons = []
        loaded = False
        pos = pygame.mouse.get_pos()
        for x in range(1, 5):
            buttons.append(
                Button(W*0.38, H*0.18*x, ui_font_2.render(f'LEVEL {x}', True, 'black'), 1))
            # if the mouse hovers over the text, change the colour
            if buttons[x-1].rect.collidepoint(pos):
                buttons[x -
                        1].image = ui_font_2.render(f'LEVEL {x}', True, 'red')
            # load the level for which the button has been clicked
            if buttons[x-1].draw(screen):
                nav.play()
                lvl_num = x
                level_select = False
                character_select = True
        # back button
        if Button(W*0.37, H*0.8, back_btn_img, SCALE/200).draw(screen):
            nav.play()
            level_select = False
            display_menu = True

    # start game
    if start_game:
        # if the level has not been loaded, reset the timer and load in the level
        if not loaded:
            wrld = World(select_level(lvl_num), character)
            game_start_timer = pygame.time.get_ticks()
            loaded = True
        else:
            # game over if the player dies
            # next level if the player reaches the end
            for pl in wrld.player:
                if pl.next_level and lvl_num < 4:
                    lvl_num += 1
                    pl.next_level = False
                    loaded = False

                if pl.alive is False:
                    start_game = False
                    game_over = True
            wrld.run(screen, ui_font)
        timer = pygame.time.get_ticks()
        screen.blit(timer_img, (W*0.44+4, 10))  # timer

        # format the timer correctly
        if (timer-game_start_timer)/1000 < 10:
            draw_text(W*0.46, 20, 'grey',
                      f'0{str(int((timer-game_start_timer)/1000))}', screen, ui_font)
        else:
            draw_text(W*0.46, 20, 'grey',
                      str(int((timer-game_start_timer)/1000)), screen, ui_font)
        draw_text(W*0.7, 10, 'white', 'Press M to Pause', screen, ui_font_3)

    # reset the click timer so that it doesn't get too big while doing nothing
    if click_timer >= 1000:
        click_timer = 0

    pygame.display.update()
