import sys
from random import randint as rdint
from random import randrange as rd

import mysql.connector
import pygame
from mysql.connector import Error

from Button import Button
from Character import Character
from DropCrate import DropCrate
from EnemyBullet import EnemyBullet
from Portal import Portal
from Turret import Turret

# db connection password: q4h887dm_RN

pygame.init()

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

CANVAS = pygame.Surface((6000, 1080))

PATH_INDENT = -12

DESCRIPTION_FONT_SIZE = 10

LEVEL_STATUS_FONT_SIZE = 24

clock = pygame.time.Clock()
FPS = 60
G = 0.5

OOB = (10000, 10000)

GLOBAL_X = -500

CHARACTER_SPEED = 5

TURRETS_DESTROYED = 0

screen_scroll = 0

levels_page = 1

background_theme = pygame.mixer.Sound("../Sounds/background_theme.mp3")
button_click_sound = pygame.mixer.Sound("../Sounds/button_click_sound.mp3")
destruction_sound = pygame.mixer.Sound("../Sounds/destruction_sound.mp3")
game_over_sound = pygame.mixer.Sound("../Sounds/game_over_sound.mp3")
jump_sound = pygame.mixer.Sound("../Sounds/jump_sound.mp3")
shot_sound = pygame.mixer.Sound("../Sounds/shot_sound.mp3")
victory_sound = pygame.mixer.Sound("../Sounds/victory_sound.mp3")

wall_image = pygame.image.load("../Textures/ground_texture.png")
ladder_image = pygame.image.load('../Textures/ladder.png')
turret_image = pygame.image.load('../Textures/turret.png')

l_1 = pygame.image.load('../Textures/1_lives.png')
l_2 = pygame.image.load('../Textures/2_lives.png')
l_3 = pygame.image.load('../Textures/3_lives.png')
l_4 = pygame.image.load('../Textures/4_lives.png')

data = ['-' for i in range(207)]

CHOSEN_DIFFICULTY = 'beginner'

SONG_VOLUME = 0
SOUNDS_VOLUME = 0

MAP_MATRIX = []
for i in range(18):
    MAP_MATRIX.append([])
    for j in range(120):
        if i == 0 or i == 17 or j == 0 or j == 119:
            MAP_MATRIX[len(MAP_MATRIX) - 1].append('P')
        else:
            MAP_MATRIX[len(MAP_MATRIX) - 1].append('0')

background_theme.play(-1)
background_theme.set_volume(SONG_VOLUME / 100)

MAP_MATRIX = []
for i in range(18):
    MAP_MATRIX.append([])
    for j in range(120):
        if i == 0 or i == 17 or j == 0 or j == 119:
            MAP_MATRIX[len(MAP_MATRIX) - 1].append('P')
        else:
            MAP_MATRIX[len(MAP_MATRIX) - 1].append('0')
MAP_SEGMENTS = []

MAP_SEGMENTS_NUMS = [rd(0, 12), rd(0, 12), rd(0, 12)]

map_segments_loaded = []

for i in range(12):
    num = '0' * int(i < 9) + str(i + 1)
    map_segment = open('../Other/endless-map-segments/endless_map_segment' + num + '.txt')
    map_segments_loaded.append(map_segment.readlines())
    map_segment.close()

for k in range(12):
    MAP_SEGMENTS.append([])
    for i in range(18):
        MAP_SEGMENTS[k].append([])
        for j in range(24):
            MAP_SEGMENTS[k][i].append(map_segments_loaded[k][i][j])

bullet_group = pygame.sprite.Group()
enemy_bullet_group = pygame.sprite.Group()
turret_group = pygame.sprite.Group()
drop_crate_group = pygame.sprite.Group()


def create_connection():
    connection = None
    try:
        connection = mysql.connector.connect(
            host='127.0.0.2',
            user='Tremexen',
            passwd='q4h887dm_RN',
            database='grand_battle-info'
        )
    except Error:
        print(f"The error '{Error}' occurred")
    return connection


def update_db():
    db_connection = create_connection()
    global data
    for i in range(9):
        update_query = "UPDATE `levels-info` SET stars=" + data[
            i] + " WHERE difficulty=\"beginner\" AND level=" + str((i % 10) + 1)
        with db_connection.cursor() as cursor:
            cursor.execute(update_query)
            db_connection.commit()
    for i in range(10, 19):
        update_query = "UPDATE `levels-info` SET stars=" + data[i] + " WHERE difficulty=\"medium\" AND level=" + str(
            (i % 10) + 1)
        with db_connection.cursor() as cursor:
            cursor.execute(update_query)
            db_connection.commit()
    for i in range(20, 29):
        update_query = "UPDATE `levels-info` SET stars=" + data[i] + " WHERE difficulty=\"hard\" AND level=" + str(
            (i % 10) + 1)
        with db_connection.cursor() as cursor:
            cursor.execute(update_query)
            db_connection.commit()
    for i in range(30, 39):
        update_query = "UPDATE `levels-info` SET stars=" + data[i] + " WHERE difficulty=\"insane\" AND level=" + str(
            (i % 10) + 1)
        with db_connection.cursor() as cursor:
            cursor.execute(update_query)
            db_connection.commit()

    for i in range(40, 50):
        update_query = "UPDATE `song-volume` SET `condition`=\'" + data[i][:-1] + "\' WHERE volume_level_id=" + str(
            (i % 10) + 1)
        with db_connection.cursor() as cursor:
            cursor.execute(update_query)
            db_connection.commit()

    for i in range(51, 61):
        update_query = "UPDATE `sounds-volume` SET `condition`=\'" + data[i][:-1] + "\' WHERE volume_level_id=" + str(
            i - 50)
        with db_connection.cursor() as cursor:
            cursor.execute(update_query)
            db_connection.commit()

    for i in range(62, 97, 4):
        update_query1 = "UPDATE `levels-info` SET hours=\'" + data[
            i] + "\' WHERE difficulty=\"beginner\" AND level=" + str((i - 62) / 4 + 1)
        update_query2 = "UPDATE `levels-info` SET minutes=\'" + data[
            i + 1] + "\' WHERE difficulty=\"beginner\" AND level=" + str((i - 62) / 4 + 1)
        update_query3 = "UPDATE `levels-info` SET seconds=\'" + data[
            i + 2] + "\' WHERE difficulty=\"beginner\" AND level=" + str((i - 62) / 4 + 1)
        with db_connection.cursor() as cursor:
            cursor.execute(update_query1)
            db_connection.commit()
        with db_connection.cursor() as cursor:
            cursor.execute(update_query2)
            db_connection.commit()
        with db_connection.cursor() as cursor:
            cursor.execute(update_query3)
            db_connection.commit()
    for i in range(98, 133, 4):
        update_query1 = "UPDATE `levels-info` SET hours=\'" + data[
            i] + "\' WHERE difficulty=\"medium\" AND level=" + str((i - 98) / 4 + 1)
        update_query2 = "UPDATE `levels-info` SET minutes=\'" + data[
            i + 1] + "\' WHERE difficulty=\"medium\" AND level=" + str((i - 98) / 4 + 1)
        update_query3 = "UPDATE `levels-info` SET seconds=\'" + data[
            i + 2] + "\' WHERE difficulty=\"medium\" AND level=" + str((i - 98) / 4 + 1)
        with db_connection.cursor() as cursor:
            cursor.execute(update_query1)
            db_connection.commit()
        with db_connection.cursor() as cursor:
            cursor.execute(update_query2)
            db_connection.commit()
        with db_connection.cursor() as cursor:
            cursor.execute(update_query3)
            db_connection.commit()
    for i in range(134, 169, 4):
        update_query1 = "UPDATE `levels-info` SET hours=\'" + data[
            i] + "\' WHERE difficulty=\"hard\" AND level=" + str((i - 134) / 4 + 1)
        update_query2 = "UPDATE `levels-info` SET minutes=\'" + data[
            i + 1] + "\' WHERE difficulty=\"hard\" AND level=" + str((i - 134) / 4 + 1)
        update_query3 = "UPDATE `levels-info` SET seconds=\'" + data[
            i + 2] + "\' WHERE difficulty=\"hard\" AND level=" + str((i - 134) / 4 + 1)
        with db_connection.cursor() as cursor:
            cursor.execute(update_query1)
            db_connection.commit()
        with db_connection.cursor() as cursor:
            cursor.execute(update_query2)
            db_connection.commit()
        with db_connection.cursor() as cursor:
            cursor.execute(update_query3)
            db_connection.commit()
    for i in range(170, 205, 4):
        update_query1 = "UPDATE `levels-info` SET hours=\'" + data[
            i] + "\' WHERE difficulty=\"insane\" AND level=" + str((i - 170) / 4 + 1)
        update_query2 = "UPDATE `levels-info` SET minutes=\'" + data[
            i + 1] + "\' WHERE difficulty=\"insane\" AND level=" + str((i - 170) / 4 + 1)
        update_query3 = "UPDATE `levels-info` SET seconds=\'" + data[
            i + 2] + "\' WHERE difficulty=\"insane\" AND level=" + str((i - 170) / 4 + 1)
        with db_connection.cursor() as cursor:
            cursor.execute(update_query1)
            db_connection.commit()
        with db_connection.cursor() as cursor:
            cursor.execute(update_query2)
            db_connection.commit()
        with db_connection.cursor() as cursor:
            cursor.execute(update_query3)
            db_connection.commit()


def get_db_info():
    db_connection = create_connection()
    global data
    info_cleaning = open('../Other/info-flows/db_info_flow.txt', 'w')
    info_cleaning.seek(0)
    info_cleaning.close()
    info = open('../Other/info-flows/db_info_flow.txt', 'w')
    get_info_query1 = "SELECT * FROM `levels-info`"
    with db_connection.cursor() as cursor:
        cursor.execute(get_info_query1)
        result1 = cursor.fetchall()
        for (id, difficulty, level, stars, hours, minutes, seconds) in result1:
            info.write(str(stars) + '\n')
            if id % 9 == 0:
                info.write('\n')

    get_info_query2 = "SELECT * FROM `song-volume`"
    with db_connection.cursor() as cursor:
        cursor.execute(get_info_query2)
        result2 = cursor.fetchall()
        for (volume_level_id, condition) in result2:
            info.write(condition + '\n')
    info.write('\n')
    get_info_query3 = "SELECT * FROM `sounds-volume`"
    with db_connection.cursor() as cursor:
        cursor.execute(get_info_query3)
        result3 = cursor.fetchall()
        for (volume_level_id, condition) in result3:
            info.write(condition + '\n')
    info.write('\n')

    get_info_query4 = "SELECT * FROM `levels-info`"
    with db_connection.cursor() as cursor:
        cursor.execute(get_info_query4)
        result4 = cursor.fetchall()
        for (id, difficulty, level, stars, hours, minutes, seconds) in result4:
            info.write(hours + '\n')
            info.write(minutes + '\n')
            info.write(seconds + '\n')
            info.write('\n')

    endless_info = open('../Other/endless_record.txt')
    record = endless_info.readlines()
    endless_info.close()
    info.write(record[0])
    info.close()
    info = open('../Other/info-flows/db_info_flow.txt')
    data = []
    data = info.readlines()
    info.close()
    info = open('../Other/info-flows/db_info_flow.txt', 'w')
    info.seek(0)
    info.close()


def endless_map_update():
    global MAP_MATRIX
    global MAP_SEGMENTS
    global MAP_SEGMENTS_NUMS
    for k in range(len(MAP_SEGMENTS_NUMS) - 3, len(MAP_SEGMENTS_NUMS)):
        new_segment = MAP_SEGMENTS_NUMS[k]
        for i in range(18):
            for j in range(24):
                MAP_MATRIX[i].append(MAP_SEGMENTS[new_segment][i][j])


def get_font(size):
    return pygame.font.Font("../Textures/font.ttf", size)


def load_map(level):
    global MAP_MATRIX
    Map = open('../Other/level-maps/level0' + level + 'map.txt')
    map_matrix = Map.readlines()
    for i in range(18):
        MAP_MATRIX.append([])
        for j in range(120):
            MAP_MATRIX[i].append(map_matrix[i][j])
    Map.close()


def difficulty_list(return_to_main_menu_P):
    global SOUNDS_VOLUME
    global SONG_VOLUME
    global CHOSEN_DIFFICULTY
    global OOB

    get_db_info()

    while True:
        diffculty_list_mouse_pos = pygame.mouse.get_pos()

        return_to_main_menu_P.changeCondition(diffculty_list_mouse_pos)
        return_to_main_menu_P.update(SCREEN)

        beginner_difficulty = Button(
            image=pygame.image.load("../Textures/Difficulty buttons/beginner_difficulty_button_disabled.png"),
            image_path="../Textures/Difficulty buttons/beginner_difficulty_button_disabled.png", pos=(1500, 300),
            difficulty_button=1)

        beginner_difficulty.changeCondition(diffculty_list_mouse_pos)
        beginner_difficulty.update(SCREEN)

        medium_difficulty = Button(
            image=pygame.image.load("../Textures/Difficulty buttons/medium_difficulty_button_disabled.png"),
            image_path="../Textures/Difficulty buttons/medium_difficulty_button_disabled.png", pos=(1500, 400),
            difficulty_button=2)

        medium_difficulty.changeCondition(diffculty_list_mouse_pos)
        medium_difficulty.update(SCREEN)

        hard_difficulty = Button(
            image=pygame.image.load("../Textures/Difficulty buttons/hard_difficulty_button_disabled.png"),
            image_path="../Textures/Difficulty buttons/hard_difficulty_button_disabled.png", pos=(1500, 500),
            difficulty_button=3)

        hard_difficulty.changeCondition(diffculty_list_mouse_pos)
        hard_difficulty.update(SCREEN)

        insane_difficulty = Button(
            image=pygame.image.load("../Textures/Difficulty buttons/insane_difficulty_button_disabled.png"),
            image_path="../Textures/Difficulty buttons/insane_difficulty_button_disabled.png", pos=(1500, 600),
            difficulty_button=4)

        insane_difficulty.changeCondition(diffculty_list_mouse_pos)
        insane_difficulty.update(SCREEN)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if return_to_main_menu_P.checkForInput(diffculty_list_mouse_pos):
                    button_click_sound.play()
                    main_menu()
                if beginner_difficulty.checkForInput(diffculty_list_mouse_pos):
                    button_click_sound.play()
                    button_click_sound.set_volume(SOUNDS_VOLUME / 100)
                    return 'beginner'
                if medium_difficulty.checkForInput(diffculty_list_mouse_pos):
                    button_click_sound.play()
                    button_click_sound.set_volume(SOUNDS_VOLUME / 100)
                    return 'medium'
                if hard_difficulty.checkForInput(diffculty_list_mouse_pos):
                    button_click_sound.play()
                    button_click_sound.set_volume(SOUNDS_VOLUME / 100)
                    return 'hard'
                if insane_difficulty.checkForInput(diffculty_list_mouse_pos):
                    button_click_sound.play()
                    button_click_sound.set_volume(SOUNDS_VOLUME / 100)
                    return 'insane'
        pygame.display.update()


def play():
    global CHOSEN_DIFFICULTY
    global SOUNDS_VOLUME
    global SONG_VOLUME
    global levels_page

    get_db_info()

    info_updated = False
    while True:
        chosen_diff = 0
        if CHOSEN_DIFFICULTY == 'beginner':
            chosen_diff = 0
        if CHOSEN_DIFFICULTY == 'medium':
            chosen_diff = 1
        if CHOSEN_DIFFICULTY == 'hard':
            chosen_diff = 2
        if CHOSEN_DIFFICULTY == 'insane':
            chosen_diff = 3

        play_mouse_pos = pygame.mouse.get_pos()

        SCREEN.fill("#121212")
        pygame.draw.rect(SCREEN, (0, 0, 0), pygame.Rect(0, 0, 240, 1080))
        pygame.draw.rect(SCREEN, (0, 0, 0), pygame.Rect(1680, 0, 240, 1080))

        levels_page_forward_button = Button(
            image=pygame.image.load("../Textures/forward_list_button_disabled.png"),
            image_path="../Textures/forward_list_button_disabled.png", pos=OOB)

        levels_page_forward_button.changeCondition(play_mouse_pos)
        levels_page_forward_button.update(SCREEN)

        levels_page_back_button = Button(
            image=pygame.image.load("../Textures/back_list_button_disabled.png"),
            image_path="../Textures/back_list_button_disabled.png", pos=OOB)

        levels_page_back_button.changeCondition(play_mouse_pos)
        levels_page_back_button.update(SCREEN)

        if levels_page == 1:
            levels_page_forward_button = Button(
                image=pygame.image.load("../Textures/forward_list_button_disabled.png"),
                image_path="../Textures/forward_list_button_disabled.png", pos=(1400, 500))

            levels_page_forward_button.changeCondition(play_mouse_pos)
            levels_page_forward_button.update(SCREEN)

        else:
            levels_page_back_button = Button(
                image=pygame.image.load("../Textures/back_list_button_disabled.png"),
                image_path="../Textures/back_list_button_disabled.png", pos=(1320, 500))

            levels_page_back_button.changeCondition(play_mouse_pos)
            levels_page_back_button.update(SCREEN)

        choose_difficulty = Button(
            image=pygame.image.load("../Textures/Difficulty buttons/difficulty_button_disabled.png"),
            image_path="../Textures/Difficulty buttons/difficulty_button_disabled.png", pos=(1500, 200))

        choose_difficulty.changeCondition(play_mouse_pos)
        choose_difficulty.update(SCREEN)

        level01_button_path = "../Textures/Level buttons/level01_button_stars-" + data[chosen_diff * 10][
            0] + "_disabled.png"
        level01_button_pos = OOB
        if levels_page == 1:
            level01_button_pos = (400, 300)
        level01_button = Button(image=pygame.image.load(level01_button_path), image_path=level01_button_path,
                                pos=level01_button_pos, level_button=1)
        if not info_updated:
            level01_button.update_info()

        level01_button.changeCondition(play_mouse_pos, CHOSEN_DIFFICULTY=CHOSEN_DIFFICULTY)
        level01_button.update(SCREEN)

        level02_button_path = "../Textures/Level buttons/level02_button_stars-" + data[chosen_diff * 10 + 1][
            0] + "_disabled.png"
        level02_button_pos = OOB
        if levels_page == 1:
            level02_button_pos = (750, 300)
        level02_button = Button(image=pygame.image.load(level02_button_path), image_path=level02_button_path,
                                pos=level02_button_pos, level_button=2)
        if not info_updated:
            level02_button.update_info()

        level02_button.changeCondition(play_mouse_pos, CHOSEN_DIFFICULTY=CHOSEN_DIFFICULTY)
        level02_button.update(SCREEN)

        level03_button_path = "../Textures/Level buttons/level03_button_stars-" + data[chosen_diff * 10 + 2][
            0] + "_disabled.png"
        level03_button_pos = OOB
        if levels_page == 1:
            level03_button_pos = (1100, 300)
        level03_button = Button(image=pygame.image.load(level03_button_path), image_path=level03_button_path,
                                pos=level03_button_pos, level_button=3)
        if not info_updated:
            level03_button.update_info()

        level03_button.changeCondition(play_mouse_pos, CHOSEN_DIFFICULTY=CHOSEN_DIFFICULTY)
        level03_button.update(SCREEN)

        level04_button_path = "../Textures/Level buttons/level04_button_stars-" + data[chosen_diff * 10 + 3][
            0] + "_disabled.png"
        level04_button_pos = OOB
        if levels_page == 1:
            level04_button_pos = (400, 650)
        level04_button = Button(image=pygame.image.load(level04_button_path), image_path=level04_button_path,
                                pos=level04_button_pos, level_button=4)
        if not info_updated:
            level04_button.update_info()

        level04_button.changeCondition(play_mouse_pos, CHOSEN_DIFFICULTY=CHOSEN_DIFFICULTY)
        level04_button.update(SCREEN)

        level05_button_path = "../Textures/Level buttons/level05_button_stars-" + data[chosen_diff * 10 + 4][
            0] + "_disabled.png"
        level05_button_pos = OOB
        if levels_page == 1:
            level05_button_pos = (750, 650)
        level05_button = Button(image=pygame.image.load(level05_button_path), image_path=level05_button_path,
                                pos=level05_button_pos, level_button=5)
        if not info_updated:
            level05_button.update_info()

        level05_button.changeCondition(play_mouse_pos, CHOSEN_DIFFICULTY=CHOSEN_DIFFICULTY)
        level05_button.update(SCREEN)

        level06_button_path = "../Textures/Level buttons/level06_button_stars-" + data[chosen_diff * 10 + 5][
            0] + "_disabled.png"
        level06_button_pos = OOB
        if levels_page == 1:
            level06_button_pos = (1100, 650)
        level06_button = Button(image=pygame.image.load(level06_button_path), image_path=level06_button_path,
                                pos=level06_button_pos, level_button=6)
        if not info_updated:
            level06_button.update_info()

        level06_button.changeCondition(play_mouse_pos, CHOSEN_DIFFICULTY=CHOSEN_DIFFICULTY)
        level06_button.update(SCREEN)

        level07_button_path = "../Textures/Level buttons/level07_button_stars-" + data[chosen_diff * 10 + 6][
            0] + "_disabled.png"
        level07_button_pos = OOB
        if levels_page == 2:
            level07_button_pos = (400, 300)
        level07_button = Button(image=pygame.image.load(level07_button_path), image_path=level07_button_path,
                                pos=level07_button_pos, level_button=7)
        if not info_updated:
            level07_button.update_info()

        level07_button.changeCondition(play_mouse_pos, CHOSEN_DIFFICULTY=CHOSEN_DIFFICULTY)
        level07_button.update(SCREEN)

        level08_button_path = "../Textures/Level buttons/level08_button_stars-" + data[chosen_diff * 10 + 7][
            0] + "_disabled.png"
        level08_button_pos = OOB
        if levels_page == 2:
            level08_button_pos = (750, 300)
        level08_button = Button(image=pygame.image.load(level08_button_path), image_path=level08_button_path,
                                pos=level08_button_pos, level_button=8)
        if not info_updated:
            level08_button.update_info()

        level08_button.changeCondition(play_mouse_pos, CHOSEN_DIFFICULTY=CHOSEN_DIFFICULTY)
        level08_button.update(SCREEN)

        level09_button_path = "../Textures/Level buttons/level09_button_stars-" + data[chosen_diff * 10 + 8][
            0] + "_disabled.png"
        level09_button_pos = OOB
        if levels_page == 2:
            level09_button_pos = (1100, 300)
        level09_button = Button(image=pygame.image.load(level09_button_path), image_path=level09_button_path,
                                pos=level09_button_pos, level_button=9)

        level09_button.changeCondition(play_mouse_pos, CHOSEN_DIFFICULTY=CHOSEN_DIFFICULTY)
        level09_button.update(SCREEN)
        if not info_updated:
            level09_button.update_info()

        endless_button_path = "../Textures/endless_mode_button_disabled.png"
        endless_button = Button(image=pygame.image.load(endless_button_path), image_path=endless_button_path,
                                pos=(1490, 830), endless_button=1)

        endless_button.changeCondition(play_mouse_pos)
        endless_button.update(SCREEN)

        return_to_main_menu_P = Button(image=pygame.image.load("../Textures/return_button_disabled.png"),
                                       image_path="../Textures/return_button_disabled.png", pos=(310, 900))

        return_to_main_menu_P.changeCondition(play_mouse_pos)
        return_to_main_menu_P.update(SCREEN)

        info_updated = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if return_to_main_menu_P.checkForInput(play_mouse_pos):
                    button_click_sound.play()
                    button_click_sound.set_volume(SOUNDS_VOLUME / 100)
                    main_menu()

                if levels_page_forward_button.checkForInput(play_mouse_pos):
                    button_click_sound.play()
                    button_click_sound.set_volume(SOUNDS_VOLUME / 100)
                    levels_page = 2
                if levels_page_back_button.checkForInput(play_mouse_pos):
                    button_click_sound.play()
                    button_click_sound.set_volume(SOUNDS_VOLUME / 100)
                    levels_page = 1

                if choose_difficulty.checkForInput(play_mouse_pos):
                    button_click_sound.play()
                    button_click_sound.set_volume(SOUNDS_VOLUME / 100)
                    CHOSEN_DIFFICULTY = difficulty_list(return_to_main_menu_P)

                if level01_button.checkForInput(play_mouse_pos):
                    button_click_sound.play()
                    button_click_sound.set_volume(SOUNDS_VOLUME / 100)
                    level_launch('1')
                if level02_button.checkForInput(play_mouse_pos):
                    button_click_sound.play()
                    button_click_sound.set_volume(SOUNDS_VOLUME / 100)
                    level_launch('2')
                if level03_button.checkForInput(play_mouse_pos):
                    button_click_sound.play()
                    button_click_sound.set_volume(SOUNDS_VOLUME / 100)
                    level_launch('3')
                if level04_button.checkForInput(play_mouse_pos):
                    button_click_sound.play()
                    button_click_sound.set_volume(SOUNDS_VOLUME / 100)
                    level_launch('4')
                if level05_button.checkForInput(play_mouse_pos):
                    button_click_sound.play()
                    button_click_sound.set_volume(SOUNDS_VOLUME / 100)
                    level_launch('5')
                if level06_button.checkForInput(play_mouse_pos):
                    button_click_sound.play()
                    button_click_sound.set_volume(SOUNDS_VOLUME / 100)
                    level_launch('6')
                if level07_button.checkForInput(play_mouse_pos):
                    button_click_sound.play()
                    button_click_sound.set_volume(SOUNDS_VOLUME / 100)
                    level_launch('7')
                if level08_button.checkForInput(play_mouse_pos):
                    button_click_sound.play()
                    button_click_sound.set_volume(SOUNDS_VOLUME / 100)
                    level_launch('8')
                if level09_button.checkForInput(play_mouse_pos):
                    button_click_sound.play()
                    button_click_sound.set_volume(SOUNDS_VOLUME / 100)
                    level_launch('9')

                if endless_button.checkForInput(play_mouse_pos):
                    button_click_sound.play()
                    button_click_sound.set_volume(SOUNDS_VOLUME / 100)
                    endless_mode()
        pygame.display.update()


def level_background(lvl_n, screen_scroll):
    global MAP_MATRIX
    if lvl_n == 'endless':
        CANVAS.blit(pygame.image.load('../Textures/level_02.png'), (0, 0))
    else:
        CANVAS.blit(pygame.image.load('../Textures/level_0' + str(lvl_n) + '.png'), (0, 0))
        for i in range(22):
            for j in range(1, 8):
                CANVAS.blit(wall_image, (j * - 50 + screen_scroll, i * 50))
        for i in range(22):
            for j in range(1, 8):
                CANVAS.blit(wall_image, (5950 + j * 50 + screen_scroll, i * 50))
    for i in range(18):
        for j in range(len(MAP_MATRIX[i])):
            if MAP_MATRIX[i][j] == 'P' and (j * 50 + screen_scroll) in range(-200, 1800):
                CANVAS.blit(wall_image, (j * 50 + screen_scroll, i * 50))
            elif MAP_MATRIX[i][j] == 'L' and (j * 50 + screen_scroll) in range(-200, 1800):
                CANVAS.blit(ladder_image, (j * 50 + screen_scroll, i * 50))
    for i in range(4):
        for j in range(len(MAP_MATRIX[i])):
            if (j * 50 + screen_scroll) in range(-200, 1800):
                CANVAS.blit(wall_image, (j * 50 + screen_scroll, 900 + i * 50))

    SCREEN.blit(CANVAS, (240, 0))


def level_launch(level_num):

    get_db_info()

    completed = False
    global TURRETS_DESTROYED
    TURRETS_DESTROYED = 0
    global CHOSEN_DIFFICULTY
    global data
    bullet_group.empty()
    enemy_bullet_group.empty()
    turret_group.empty()
    drop_crate_group.empty()
    TURRET_HEALTH = 0
    CHARACTER_HEALTH = 0
    BULLET_SPEED = 0
    c_d = 0
    if CHOSEN_DIFFICULTY == 'beginner':
        TURRET_HEALTH = 1
        CHARACTER_HEALTH = 4
        BULLET_SPEED = 2
    if CHOSEN_DIFFICULTY == 'medium':
        TURRET_HEALTH = 2
        CHARACTER_HEALTH = 3
        BULLET_SPEED = 3
        c_d = 1
    if CHOSEN_DIFFICULTY == 'hard':
        TURRET_HEALTH = 3
        CHARACTER_HEALTH = 2
        BULLET_SPEED = 4
        c_d = 2
    if CHOSEN_DIFFICULTY == 'insane':
        TURRET_HEALTH = 4
        CHARACTER_HEALTH = 1
        BULLET_SPEED = 5
        c_d = 3

    global screen_scroll
    screen_scroll = 0
    playing = True
    move_left = False
    move_right = False

    MAP_MATRIX.clear()

    load_map(level_num)

    player = Character(700, 770, CHARACTER_SPEED, CHARACTER_HEALTH, MAP_MATRIX, screen_scroll)

    portal_y = 0

    for i in range(1, 16):
        if MAP_MATRIX[i + 2][117] == 'P':
            portal_y = i * 50 + 20
            break

    portal = Portal(6150, portal_y, CHOSEN_DIFFICULTY)

    for i in range(18):
        for j in range(120):
            if MAP_MATRIX[i][j] == 'T':
                turret_group.add(Turret(j * 50 + 290, i * 50 + 50, TURRET_HEALTH, BULLET_SPEED, MAP_MATRIX, c_d))

    clock1 = pygame.time.get_ticks()

    while playing:

        clock.tick(FPS)
        level_background(int(level_num), player.get_screen_scroll())
        change = player.move(move_left, move_right)

        for i in turret_group:
            i.update(change, player)

        requests = open('../Other/info-flows/flow_01.txt')
        requests_copy = requests.readlines()
        while len(requests_copy) > 1:
            enemy_bullet_group.add(
                EnemyBullet(int(requests_copy[0][:-1]), int(requests_copy[1][:-1]), int(requests_copy[2][:-1]),
                            int(requests_copy[3]), MAP_MATRIX, screen_scroll))
            requests_copy = requests_copy[4:]
        requests.close()
        requests = open('../Other/info-flows/flow_01.txt', 'w')
        requests.seek(0)
        requests.close()

        requests2 = open('../Other/info-flows/flow_02.txt')
        requests_copy2 = requests2.readlines()
        drop_crates = []
        while len(requests_copy2) > 1:
            drop_crates.append((int(requests_copy2[0][:-1]), int(requests_copy2[1][:-1])))
            requests_copy2 = requests_copy2[2:]
        requests2.close()
        requests2 = open('../Other/info-flows/flow_02.txt', 'w')
        requests2.seek(0)
        requests2.close()

        requests3 = open('../Other/info-flows/flow_03.txt')
        requests_copy3 = requests3.readlines()
        buffs = []
        while len(requests_copy3):
            buffs.append(int(requests_copy3[0][:-1]))
            requests_copy3 = requests_copy3[1:]
        requests3.close()
        requests3 = open('../Other/info-flows/flow_03.txt', 'w')
        requests3.seek(0)
        requests3.close()

        for x, y in drop_crates:
            drop_chance = 0
            if CHOSEN_DIFFICULTY == 'beginner':
                drop_chance = 100
            if CHOSEN_DIFFICULTY == 'medium':
                drop_chance = 70
            if CHOSEN_DIFFICULTY == 'hard':
                drop_chance = 30
            q = rdint(1, 100)
            if q <= drop_chance:
                drop_crate_group.add(DropCrate(x, y, rdint(1, 3), screen_scroll, rdint(1, 2), MAP_MATRIX))

        for i in buffs:
            player.realize_buff(i)

        portal.update(change)
        portal.draw()
        player.draw()
        bullet_group.update(change, turret_group, player, screen_scroll)
        bullet_group.draw(SCREEN)
        enemy_bullet_group.update(change, player, screen_scroll)
        enemy_bullet_group.draw(SCREEN)
        drop_crate_group.update(change, player, screen_scroll)
        drop_crate_group.draw(SCREEN)
        pygame.draw.rect(SCREEN, (0, 0, 0), pygame.Rect(0, 0, 240, 1080))
        pygame.draw.rect(SCREEN, (0, 0, 0), pygame.Rect(1680, 0, 240, 1080))

        if not player.check_alive:
            playing = False

        if portal.check_completion(player):
            playing = False
            completed = True
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    move_left = True
                    move_right = False
                    player.ladder = False
                    player.climbing = False
                if event.key == pygame.K_d:
                    move_right = True
                    move_left = False
                    player.ladder = False
                    player.climbing = False
                if event.key == pygame.K_SPACE and not player.air:
                    jump_sound.play()
                    jump_sound.set_volume(SOUNDS_VOLUME / 100)
                    player.jump = True
                if event.key == pygame.K_ESCAPE:
                    playing = False
                if event.key == pygame.K_w and not move_left and not move_right:
                    player.climbing = True

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    move_left = False
                if event.key == pygame.K_d:
                    move_right = False
                if event.key == pygame.K_w:
                    player.climbing = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if player.cooldown == 0:
                        player.cooldown = 30
                        shot_sound.play()
                        shot_sound.set_volume(SOUNDS_VOLUME / 100)
                        bullet_group.add(player.shoot())

        screen_scroll = player.get_screen_scroll()

        pygame.display.update()

    ticks = pygame.time.get_ticks() - clock1
    seconds = int(ticks / 1000 % 60)
    minutes = int(ticks / 60000 % 60)
    hours = int(ticks / 3600000 % 24)
    if seconds < 10:
        seconds = '0' + str(seconds)
    if minutes < 10:
        minutes = '0' + str(minutes)
    if hours < 10:
        hours = '0' + str(hours)
    c_d = 0
    if CHOSEN_DIFFICULTY == 'medium':
        c_d = 1
    if CHOSEN_DIFFICULTY == 'hard':
        c_d = 2
    if CHOSEN_DIFFICULTY == 'insane':
        c_d = 3
    if completed:
        get_db_info()
        victory_sound.play()
        victory_sound.set_volume(SOUNDS_VOLUME / 100)
        if TURRETS_DESTROYED in range(12, 15):
            if data[c_d * 10 + int(level_num) - 1][0] == '3':
                if int(data[62 + c_d * 36 + (int(level_num) - 1) * 4][:2]) * 3600 + int(
                        data[63 + c_d * 36 + (int(level_num) - 1) * 4][:2]) * 60 + int(
                    data[64 + c_d * 36 + (int(level_num) - 1) * 4][:2]) > ticks / 1000:
                    data[62 + c_d * 36 + (int(level_num) - 1) * 4] = str(hours) + '\n'
                    data[63 + c_d * 36 + (int(level_num) - 1) * 4] = str(minutes) + '\n'
                    data[64 + c_d * 36 + (int(level_num) - 1) * 4] = str(seconds) + '\n'
            else:
                data[62 + c_d * 36 + (int(level_num) - 1) * 4] = str(hours) + '\n'
                data[63 + c_d * 36 + (int(level_num) - 1) * 4] = str(minutes) + '\n'
                data[64 + c_d * 36 + (int(level_num) - 1) * 4] = str(seconds) + '\n'

            data[c_d * 10 + int(level_num) - 1] = '3\n'
        elif TURRETS_DESTROYED in range(8, 12) and data[c_d * 10 + int(level_num) - 1][0] != '3':
            if data[c_d * 10 + int(level_num) - 1][0] == '2':
                if int(data[62 + c_d * 36 + (int(level_num) - 1) * 4][:2]) * 3600 + int(
                        data[63 + c_d * 36 + (int(level_num) - 1) * 4][:2]) * 60 + int(
                    data[64 + c_d * 36 + (int(level_num) - 1) * 4][:2]) > ticks / 1000:
                    data[62 + c_d * 36 + (int(level_num) - 1) * 4] = str(hours) + '\n'
                    data[63 + c_d * 36 + (int(level_num) - 1) * 4] = str(minutes) + '\n'
                    data[64 + c_d * 36 + (int(level_num) - 1) * 4] = str(seconds) + '\n'
            else:
                data[62 + c_d * 36 + (int(level_num) - 1) * 4] = str(hours) + '\n'
                data[63 + c_d * 36 + (int(level_num) - 1) * 4] = str(minutes) + '\n'
                data[64 + c_d * 36 + (int(level_num) - 1) * 4] = str(seconds) + '\n'
            data[c_d * 10 + int(level_num) - 1] = '2\n'
        elif TURRETS_DESTROYED in range(0, 8) and data[c_d * 10 + int(level_num) - 1][0] != '2' and \
                data[c_d * 10 + int(level_num) - 1][0] != '3':
            if data[c_d * 10 + int(level_num) - 1 + int(level_num)][0] == '1':
                if int(data[62 + c_d * 36 + (int(level_num) - 1) * 4][:2]) * 3600 + int(
                        data[63 + c_d * 36 + (int(level_num) - 1) * 4][:2]) * 60 + int(
                    data[64 + c_d * 36 + (int(level_num) - 1) * 4][:2]) > ticks / 1000:
                    data[62 + c_d * 36 + (int(level_num) - 1) * 4] = str(hours) + '\n'
                    data[63 + c_d * 36 + (int(level_num) - 1) * 4] = str(minutes) + '\n'
                    data[64 + c_d * 36 + (int(level_num) - 1) * 4] = str(seconds) + '\n'
            else:
                data[62 + c_d * 36 + (int(level_num) - 1) * 4] = str(hours) + '\n'
                data[63 + c_d * 36 + (int(level_num) - 1) * 4] = str(minutes) + '\n'
                data[64 + c_d * 36 + (int(level_num) - 1) * 4] = str(seconds) + '\n'
            data[c_d * 10 + int(level_num) - 1] = '1\n'
        update_db()
    else:
        game_over_sound.play()
        game_over_sound.set_volume(SOUNDS_VOLUME / 100)


    while True:
        play_mouse_pos = pygame.mouse.get_pos()

        retry_button = Button(image=pygame.image.load("../Textures/restart_button_disabled.png"),
                              image_path="../Textures/restart_button_disabled.png", pos=(790, 700))

        retry_button.changeCondition(play_mouse_pos)
        retry_button.update(SCREEN)

        return_to_level_menu = Button(image=pygame.image.load("../Textures/exit_button_disabled.png"),
                                      image_path="../Textures/exit_button_disabled.png", pos=(1130, 700))

        return_to_level_menu.changeCondition(play_mouse_pos)
        return_to_level_menu.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                victory_sound.stop()
                game_over_sound.stop()
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if return_to_level_menu.checkForInput(play_mouse_pos):
                    button_click_sound.play()
                    button_click_sound.set_volume(SOUNDS_VOLUME / 100)
                    victory_sound.stop()
                    game_over_sound.stop()
                    play()
                if retry_button.checkForInput(play_mouse_pos):
                    button_click_sound.play()
                    button_click_sound.set_volume(SOUNDS_VOLUME / 100)
                    victory_sound.stop()
                    game_over_sound.stop()
                    level_launch(level_num)

        pygame.display.update()


def endless_mode():

    get_db_info()

    global MAP_MATRIX
    global MAP_SEGMENTS
    global MAP_SEGMENTS_NUMS
    global GLOBAL_X
    GLOBAL_X = -500
    bullet_group.empty()
    enemy_bullet_group.empty()
    turret_group.empty()
    drop_crate_group.empty()
    global screen_scroll
    screen_scroll = 0
    player = Character(700, 770, 5, 4, MAP_MATRIX, screen_scroll)
    playing = True
    move_left = False
    move_right = False
    level_num = 'endless'
    MAP_SEGMENTS_NUMS.clear()
    MAP_SEGMENTS_NUMS = [rd(0, 12), rd(0, 12), rd(0, 12)]
    MAP_MATRIX.clear()
    for i in range(18):
        MAP_MATRIX.append([])
        for j in range(24):
            if i == 0 or i == 17 or j < 8:
                MAP_MATRIX[i].append('P')
            else:
                MAP_MATRIX[i].append('0')
    endless_map_update()

    turrets_update = 0
    for i in range(18):
        for j in range(turrets_update, len(MAP_MATRIX[0])):
            if MAP_MATRIX[i][j] == 'T':
                turret_group.add(Turret(j * 50 + 290 + screen_scroll, i * 50 + 50, 3, 4, MAP_MATRIX, 2))

    map_last_update = GLOBAL_X
    turrets_update += 72

    while playing:
        clock.tick(FPS)
        level_background(level_num, player.get_screen_scroll())
        change = player.move(move_left, move_right)
        for i in turret_group:
            i.update(change, player)
        requests = open('../Other/info-flows/flow_01.txt')
        requests_copy = requests.readlines()
        while len(requests_copy) > 1:
            enemy_bullet_group.add(
                EnemyBullet(int(requests_copy[0][:-1]), int(requests_copy[1][:-1]), int(requests_copy[2][:-1]),
                            int(requests_copy[3][:-1]), MAP_MATRIX, screen_scroll))
            requests_copy = requests_copy[4:]
        requests.close()
        requests = open('../Other/info-flows/flow_01.txt', 'w')
        requests.seek(0)
        requests.close()

        requests2 = open('../Other/info-flows/flow_02.txt')
        requests_copy2 = requests2.readlines()
        drop_crates = []
        while len(requests_copy2) > 1:
            drop_crates.append((int(requests_copy2[0][:-1]), int(requests_copy2[1][:-1])))
            requests_copy2 = requests_copy2[2:]
        requests2.close()
        requests2 = open('../Other/info-flows/flow_02.txt', 'w')
        requests2.seek(0)
        requests2.close()

        requests3 = open('../Other/info-flows/flow_03.txt')
        requests_copy3 = requests3.readlines()
        buffs = []
        while len(requests_copy3):
            buffs.append(int(requests_copy3[0][:-1]))
            requests_copy3 = requests_copy3[1:]
        requests3.close()
        requests3 = open('../Other/info-flows/flow_03.txt', 'w')
        requests3.seek(0)
        requests3.close()

        requests4 = open('../Other/info-flows/flow_04.txt')
        requests_copy4 = requests4.readlines()
        GLOBAL_X = int(requests_copy4[0])
        requests4.close()
        requests4 = open('../Other/info-flows/flow_04.txt', 'w')
        requests4.seek(0)
        requests4.close()

        for x, y in drop_crates:
            q = rdint(1, 100)
            if q <= 70:
                drop_crate_group.add(DropCrate(x, y, rdint(1, 3), screen_scroll, rdint(1, 2), MAP_MATRIX))

        for i in buffs:
            player.realize_buff(i)

        player.draw()
        bullet_group.update(change, turret_group, player, screen_scroll)
        bullet_group.draw(SCREEN)
        enemy_bullet_group.update(change, player, screen_scroll)
        enemy_bullet_group.draw(SCREEN)
        drop_crate_group.update(change, player, screen_scroll)
        drop_crate_group.draw(SCREEN)
        pygame.draw.rect(SCREEN, (0, 0, 0), pygame.Rect(0, 0, 240, 1080))
        pygame.draw.rect(SCREEN, (0, 0, 0), pygame.Rect(1680, 0, 240, 1080))

        if not player.check_alive:
            playing = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    move_right = False
                    move_left = True
                    player.ladder = False
                    player.climbing = False
                if event.key == pygame.K_d:
                    move_left = False
                    move_right = True
                    player.ladder = False
                    player.climbing = False
                if event.key == pygame.K_SPACE and not player.air:
                    jump_sound.play()
                    jump_sound.set_volume(SOUNDS_VOLUME / 100)
                    player.jump = True
                if event.key == pygame.K_ESCAPE:
                    bullet_group.empty()
                    enemy_bullet_group.empty()
                    turret_group.empty()
                    playing = False
                if event.key == pygame.K_w and not move_left and not move_right:
                    player.climbing = True

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    move_left = False
                if event.key == pygame.K_d:
                    move_right = False
                if event.key == pygame.K_w:
                    player.climbing = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if player.cooldown == 0:
                        player.cooldown = 30
                        shot_sound.play()
                        shot_sound.set_volume(SOUNDS_VOLUME / 100)
                        bullet_group.add(player.shoot())

        if GLOBAL_X % 3600 in range(1500, 1600) and GLOBAL_X - map_last_update not in range(0,
                                                                                            100) and GLOBAL_X > map_last_update:
            for i in range(GLOBAL_X, GLOBAL_X + 102):
                if i % 3600 == 1600:
                    map_last_update = i
            endless_map_update()
            for i in range(18):
                for j in range(turrets_update, len(MAP_MATRIX[0])):
                    if MAP_MATRIX[i][j] == 'T':
                        turret_group.add(Turret(j * 50 + 290 + screen_scroll, i * 50 + 50, 3, 4, MAP_MATRIX, 2))
            turrets_update += 72

        screen_scroll = player.get_screen_scroll()

        pygame.display.update()

    game_over_sound.play()
    game_over_sound.set_volume(SOUNDS_VOLUME / 100)
    data[len(data) - 1] = str(max(int(data[len(data) - 1]), (GLOBAL_X + 500) // 50))
    update_db()
    info_copy = open('../Other/endless_record.txt', 'w')
    info_copy.seek(0)
    info_copy.write(data[len(data) - 1])
    info_copy.close()
    while True:
        play_mouse_pos = pygame.mouse.get_pos()

        retry_button = Button(image=pygame.image.load("../Textures/restart_button_disabled.png"),
                              image_path="../Textures/restart_button_disabled.png", pos=(790, 700))

        retry_button.changeCondition(play_mouse_pos)
        retry_button.update(SCREEN)

        return_to_level_menu = Button(image=pygame.image.load("../Textures/exit_button_disabled.png"),
                                      image_path="../Textures/exit_button_disabled.png", pos=(1130, 700))

        return_to_level_menu.changeCondition(play_mouse_pos)
        return_to_level_menu.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over_sound.stop()
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if return_to_level_menu.checkForInput(play_mouse_pos):
                    button_click_sound.play()
                    button_click_sound.set_volume(SOUNDS_VOLUME / 100)
                    game_over_sound.stop()
                    play()
                if retry_button.checkForInput(play_mouse_pos):
                    button_click_sound.play()
                    button_click_sound.set_volume(SOUNDS_VOLUME / 100)
                    game_over_sound.stop()
                    endless_mode()

        pygame.display.update()


def options():

    get_db_info()

    global SOUNDS_VOLUME
    global SONG_VOLUME
    while True:

        options_mouse_pos = pygame.mouse.get_pos()

        SCREEN.fill("#121212")
        pygame.draw.rect(SCREEN, (0, 0, 0), pygame.Rect(0, 0, 240, 1080))
        pygame.draw.rect(SCREEN, (0, 0, 0), pygame.Rect(1680, 0, 240, 1080))
        return_to_main_menu_O = Button(image=pygame.image.load("../Textures/return_button_disabled.png"),
                                       image_path="../Textures/return_button_disabled.png", pos=(310, 900))

        return_to_main_menu_O.changeCondition(options_mouse_pos)
        return_to_main_menu_O.update(SCREEN)

        song_on_off_button = Button(image=pygame.image.load("../Textures/music_en_dis_button_disabled.png"),
                                    image_path="../Textures/music_en_dis_button_disabled.png", pos=(530, 300))
        song_on_off_button.changeCondition(options_mouse_pos)
        song_on_off_button.update(SCREEN)

        sounds_on_off_button = Button(image=pygame.image.load("../Textures/volume_en_dis_button_disabled.png"),
                                      image_path="../Textures/volume_en_dis_button_disabled.png", pos=(530, 600))
        sounds_on_off_button.changeCondition(options_mouse_pos)
        sounds_on_off_button.update(SCREEN)

        song_volume_buttons = []
        for i in range(10):
            song_vol_button_condition = ""
            if data[i + 40][:2] == "of":
                song_vol_button_condition = "off"
            else:
                song_vol_button_condition = "on"
            song_volume_button_path = "../Textures/volume_button_" + song_vol_button_condition + "_disabled.png"
            song_volume_buttons.append(
                Button(image=pygame.image.load(song_volume_button_path), image_path=song_volume_button_path,
                       pos=(800 + i * 70, 300)))
        for i in range(10):
            song_volume_buttons[i].changeCondition(options_mouse_pos)
            song_volume_buttons[i].update(SCREEN)

        sounds_volume_buttons = []
        for i in range(10):
            sounds_vol_button_condition = ""
            if data[i + 51][:2] == "of":
                sounds_vol_button_condition = "off"
            else:
                sounds_vol_button_condition = "on"
            sounds_volume_button_path = "../Textures/volume_button_" + sounds_vol_button_condition + \
                                        "_disabled.png"
            sounds_volume_buttons.append(
                Button(image=pygame.image.load(sounds_volume_button_path), image_path=sounds_volume_button_path,
                       pos=(800 + i * 70, 600)))
        for i in range(10):
            sounds_volume_buttons[i].changeCondition(options_mouse_pos)
            sounds_volume_buttons[i].update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if return_to_main_menu_O.checkForInput(options_mouse_pos):
                    button_click_sound.play()
                    button_click_sound.set_volume(SOUNDS_VOLUME / 100)
                    main_menu()
                if song_on_off_button.checkForInput(options_mouse_pos):
                    button_click_sound.play()
                    button_click_sound.set_volume(SOUNDS_VOLUME / 100)
                    if not SONG_VOLUME:
                        SONG_VOLUME = 10
                        data[40] = "on\n"
                    else:
                        SONG_VOLUME = 0
                    for i in range(40, 50):
                        data[i] = "off\n"

                if sounds_on_off_button.checkForInput(options_mouse_pos):
                    button_click_sound.play()
                    button_click_sound.set_volume(SOUNDS_VOLUME / 100)
                    if not SOUNDS_VOLUME:
                        SOUNDS_VOLUME = 10
                        data[51] = "on\n"
                    else:
                        SOUNDS_VOLUME = 0
                        data[51] = "off\n"
                    for i in range(52, 61):
                        data[i] = "off\n"

                for i in range(10):
                    if song_volume_buttons[i].checkForInput(options_mouse_pos):
                        SONG_VOLUME = i * 10 + 10
                        button_click_sound.play()
                        button_click_sound.set_volume(SOUNDS_VOLUME / 100)
                        for j in range(40, 41 + i):
                            data[j] = "on\n"
                        for j in range(41 + i, 50):
                            data[j] = "off\n"
                update_db()
                background_theme.set_volume(SONG_VOLUME / 100)

                for i in range(10):
                    if sounds_volume_buttons[i].checkForInput(options_mouse_pos):
                        SOUNDS_VOLUME = i * 10 + 10
                        button_click_sound.play()
                        button_click_sound.set_volume(SOUNDS_VOLUME / 100)
                        for j in range(51, 52 + i):
                            data[j] = "on\n"
                        for j in range(52 + i, 61):
                            data[j] = "off\n"
                update_db()

        pygame.display.update()


def main_menu():
    global SOUNDS_VOLUME
    global SONG_VOLUME

    get_db_info()

    for i in range(16, 26):
        if data[i][:2] == "on":
            SONG_VOLUME += 10
    for i in range(51, 61):
        if data[i][:2] == "on":
            SOUNDS_VOLUME += 10

    while True:
        pygame.draw.rect(SCREEN, (0, 0, 0), pygame.Rect(0, 0, 240, 1080))
        pygame.draw.rect(SCREEN, (0, 0, 0), pygame.Rect(1680, 0, 240, 1080))

        SCREEN.fill("#121212")
        pygame.draw.rect(SCREEN, (0, 0, 0), pygame.Rect(0, 0, 240, 1080))
        pygame.draw.rect(SCREEN, (0, 0, 0), pygame.Rect(1680, 0, 240, 1080))

        menu_mouse_pos = pygame.mouse.get_pos()

        menu_text = get_font(100).render("GRAND BATTLE", True, "#b68f40")
        menu_rect = menu_text.get_rect(center=(960, 200))

        play_button = Button(image=pygame.image.load("../Textures/play_button_disabled.png"),
                             image_path="../Textures/play_button_disabled.png", pos=(960, 400))
        options_button = Button(image=pygame.image.load("../Textures/options_button_disabled.png"),
                                image_path="../Textures/options_button_disabled.png", pos=(960, 600))
        quit_button = Button(image=pygame.image.load("../Textures/quit_button_disabled.png"),
                             image_path="../Textures/quit_button_disabled.png", pos=(960, 800))

        SCREEN.blit(menu_text, menu_rect)

        for button in [play_button, options_button, quit_button]:
            button.changeCondition(menu_mouse_pos)
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.checkForInput(menu_mouse_pos):
                    button_click_sound.play()
                    button_click_sound.set_volume(SOUNDS_VOLUME / 100)
                    play()
                if options_button.checkForInput(menu_mouse_pos):
                    button_click_sound.play()
                    button_click_sound.set_volume(SOUNDS_VOLUME / 100)
                    options()
                if quit_button.checkForInput(menu_mouse_pos):
                    button_click_sound.play()
                    button_click_sound.set_volume(SOUNDS_VOLUME / 100)
                    pygame.quit()
                    sys.exit()
        pygame.display.update()


main_menu()
