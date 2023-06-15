import pygame
import mysql.connector

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

PATH_INDENT = -12

DESCRIPTION_FONT_SIZE = 10

LEVEL_STATUS_FONT_SIZE = 24

db_connection = mysql.connector.connect(
    host='127.0.0.2',
    user='Tremexen',
    passwd='q4h887dm_RN',
    database='grand_battle-info'
)
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
data = info.readlines()
info.close()
info = open('../Other/info-flows/db_info_flow.txt', 'w')
info.seek(0)
info.close()


class Button:
    def __init__(self, image, image_path, pos, difficulty_button=0, level_button=0, endless_button=0):
        self.image = image
        self.image_path = image_path
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.difficulty_button = difficulty_button
        self.level_button = level_button
        self.endless_button = endless_button

    def update(self, screen):
        if self.image is not None:
            screen.blit(self.image, self.rect)

    def update_info(self):
        global data
        db_connection1 = mysql.connector.connect(
            host='127.0.0.2',
            user='Tremexen',
            passwd='q4h887dm_RN',
            database='grand_battle-info'
        )
        info_cleaning1 = open('../Other/info-flows/db_info_flow.txt', 'w')
        info_cleaning1.seek(0)
        info_cleaning1.close()
        info1 = open('../Other/info-flows/db_info_flow.txt', 'w')
        get_info_query11 = "SELECT * FROM `levels-info`"
        with db_connection1.cursor() as cursor1:
            cursor1.execute(get_info_query11)
            result11 = cursor1.fetchall()
            for (id1, difficulty1, level1, stars1, hours1, minutes1, seconds1) in result11:
                info1.write(str(stars1) + '\n')
                if id1 % 9 == 0:
                    info1.write('\n')

        get_info_query21 = "SELECT * FROM `song-volume`"
        with db_connection1.cursor() as cursor1:
            cursor1.execute(get_info_query21)
            result21 = cursor1.fetchall()
            for (volume_level_id1, condition1) in result21:
                info1.write(condition1 + '\n')
        info1.write('\n')
        get_info_query31 = "SELECT * FROM `sounds-volume`"
        with db_connection1.cursor() as cursor1:
            cursor1.execute(get_info_query31)
            result31 = cursor1.fetchall()
            for (volume_level_id1, condition1) in result31:
                info1.write(condition1 + '\n')
        info1.write('\n')

        get_info_query41 = "SELECT * FROM `levels-info`"
        with db_connection1.cursor() as cursor1:
            cursor1.execute(get_info_query41)
            result41 = cursor1.fetchall()
            for (id1, difficulty1, level1, stars1, hours1, minutes1, seconds1) in result41:
                info1.write(hours1 + '\n')
                info1.write(minutes1 + '\n')
                info1.write(seconds1 + '\n')
                info1.write('\n')

        endless_info1 = open('../Other/endless_record.txt')
        record1 = endless_info1.readlines()
        endless_info1.close()
        info1.write(record1[0])
        info1.close()
        info1 = open('../Other/info-flows/db_info_flow.txt')
        data = info1.readlines()
        info1.close()
        info1 = open('../Other/info-flows/db_info_flow.txt', 'w')
        info1.seek(0)
        info1.close()

    def checkForInput(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top,
                                                                                          self.rect.bottom):
            return True
        return False

    def changeCondition(self, position, CHOSEN_DIFFICULTY='beginner'):
        c_d = 0
        if CHOSEN_DIFFICULTY == 'medium':
            c_d = 1
        if CHOSEN_DIFFICULTY == 'hard':
            c_d = 2
        if CHOSEN_DIFFICULTY == 'insane':
            c_d = 3
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top,
                                                                                          self.rect.bottom):
            self.image_path = self.image_path[:PATH_INDENT] + "_enabled.png"
            self.image = pygame.image.load(self.image_path)
        else:
            self.image_path = self.image_path[:PATH_INDENT] + "disabled.png"
            self.image = pygame.image.load(self.image_path)
        if self.endless_button:
            if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top,
                                                                                              self.rect.bottom):
                personal_best_text = get_font(LEVEL_STATUS_FONT_SIZE).render("Personal best: " + data[len(data) - 1] + " metres",
                                                                             True, "#b68f40")
                personal_best_rect = personal_best_text.get_rect(center=(1000, 900))
                SCREEN.blit(personal_best_text, personal_best_rect)

        if self.level_button:
            if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top,
                                                                                              self.rect.bottom):
                l_b = self.level_button - 1
                status = data[c_d * 10 + l_b][0] + " stars"
                time = data[62 + c_d * 36 + l_b * 4][:2] + " hr " + data[63 + c_d * 36 + l_b * 4][:2] + " min " + \
                       data[64 + c_d * 36 + l_b * 4][:2] + " sec"
                if data[c_d * 10 + l_b][0] == '0':
                    status = "not completed"
                if data[62 + c_d * 36 + l_b * 4][:2] == "00" and data[63 + c_d * 36 + l_b * 4][:2] == "00" and \
                        data[64 + c_d * 36 + l_b * 4][:2] == "00":
                    time = "-"
                level_status_text = get_font(LEVEL_STATUS_FONT_SIZE).render("Status: " + status, True, "#b68f40")
                level_status_rect = level_status_text.get_rect(center=(1000, 840))
                level_time_text = get_font(LEVEL_STATUS_FONT_SIZE).render("Time: " + time, True, "#b68f40")
                level_time_rect = level_time_text.get_rect(center=(1000, 870))
                SCREEN.blit(level_status_text, level_status_rect)
                SCREEN.blit(level_time_text, level_time_rect)
        if self.difficulty_button:
            if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top,
                                                                                              self.rect.bottom):
                level01_icon_path = "../Textures/Level buttons/level01_button_stars-" + \
                                    data[(self.difficulty_button - 1) * 10][0] + "_disabled.png"
                level02_icon_path = "../Textures/Level buttons/level02_button_stars-" + \
                                    data[(self.difficulty_button - 1) * 10 + 1][0] + "_disabled.png"
                level03_icon_path = "../Textures/Level buttons/level03_button_stars-" + \
                                    data[(self.difficulty_button - 1) * 10 + 2][0] + "_disabled.png"
                level04_icon_path = "../Textures/Level buttons/level04_button_stars-" + \
                                    data[(self.difficulty_button - 1) * 10 + 3][0] + "_disabled.png"
                level05_icon_path = "../Textures/Level buttons/level05_button_stars-" + \
                                    data[(self.difficulty_button - 1) * 10 + 4][0] + "_disabled.png"
                level06_icon_path = "../Textures/Level buttons/level06_button_stars-" + \
                                    data[(self.difficulty_button - 1) * 10 + 5][0] + "_disabled.png"
                level07_icon_path = "../Textures/Level buttons/level01_button_stars-" + \
                                    data[(self.difficulty_button - 1) * 9 + 6][0] + "_disabled.png"
                level08_icon_path = "../Textures/Level buttons/level02_button_stars-" + \
                                    data[(self.difficulty_button - 1) * 9 + 7][0] + "_disabled.png"
                level09_icon_path = "../Textures/Level buttons/level03_button_stars-" + \
                                    data[(self.difficulty_button - 1) * 9 + 8][0] + "_disabled.png"
                level01_icon = pygame.image.load(level01_icon_path)
                level02_icon = pygame.image.load(level02_icon_path)
                level03_icon = pygame.image.load(level03_icon_path)
                level04_icon = pygame.image.load(level04_icon_path)
                level05_icon = pygame.image.load(level05_icon_path)
                level06_icon = pygame.image.load(level06_icon_path)
                level07_icon = pygame.image.load(level07_icon_path)
                level08_icon = pygame.image.load(level08_icon_path)
                level09_icon = pygame.image.load(level09_icon_path)
                SCREEN.blit(level01_icon, (250, 150))
                SCREEN.blit(level02_icon, (600, 150))
                SCREEN.blit(level03_icon, (950, 150))
                SCREEN.blit(level04_icon, (250, 500))
                SCREEN.blit(level05_icon, (600, 500))
                SCREEN.blit(level06_icon, (950, 500))
                SCREEN.blit(level07_icon, (250, 150))
                SCREEN.blit(level08_icon, (600, 150))
                SCREEN.blit(level09_icon, (950, 150))
                difficulty_description = pygame.image.load("../Textures/difficulty_description_label.png")
                SCREEN.blit(difficulty_description, (400, 500))
                if self.difficulty_button == 1:
                    description_text_part01 = get_font(DESCRIPTION_FONT_SIZE).render(
                        "Beginner difficulty (I'm Too Young to Die):", True, "#605b00")
                    description_rect_part01 = description_text_part01.get_rect(center=(672, 518))
                    SCREEN.blit(description_text_part01, description_rect_part01)
                    description_text_part02 = get_font(DESCRIPTION_FONT_SIZE).render(
                        "- Guaranteed drop from every enemy", True, "#605b00")
                    description_rect_part02 = description_text_part02.get_rect(center=(710, 550))
                    SCREEN.blit(description_text_part02, description_rect_part02)
                    description_text_part03 = get_font(DESCRIPTION_FONT_SIZE).render(
                        "   - 3 additional lifes in every attempt", True, "#605b00")
                    description_rect_part03 = description_text_part03.get_rect(center=(710, 585))
                    SCREEN.blit(description_text_part03, description_rect_part03)
                    description_text_part04 = get_font(DESCRIPTION_FONT_SIZE).render("   - Slow turrets and bullets",
                                                                                     True, "#605b00")
                    description_rect_part04 = description_text_part04.get_rect(center=(655, 620))
                    SCREEN.blit(description_text_part04, description_rect_part04)
                    beginner_difficulty = pygame.image.load("../Textures/beginner_difficulty_icon.png")
                    SCREEN.blit(beginner_difficulty, (420, 550))
                if self.difficulty_button == 2:
                    description_text_part01 = get_font(DESCRIPTION_FONT_SIZE).render(
                        "Medium difficulty (Hurt Me Plenty):", True, "#605b00")
                    description_rect_part01 = description_text_part01.get_rect(center=(672, 518))
                    SCREEN.blit(description_text_part01, description_rect_part01)
                    description_text_part02 = get_font(DESCRIPTION_FONT_SIZE).render(
                        "- 70% chance of drop from every enemy", True, "#605b00")
                    description_rect_part02 = description_text_part02.get_rect(center=(725, 550))
                    SCREEN.blit(description_text_part02, description_rect_part02)
                    description_text_part03 = get_font(DESCRIPTION_FONT_SIZE).render(
                        "   - 2 additional lifes in every attempt", True, "#605b00")
                    description_rect_part03 = description_text_part03.get_rect(center=(710, 585))
                    SCREEN.blit(description_text_part03, description_rect_part03)
                    description_text_part04 = get_font(DESCRIPTION_FONT_SIZE).render("   - Normal reaction of", True,
                                                                                     "#605b00")
                    description_rect_part04 = description_text_part04.get_rect(center=(625, 620))
                    SCREEN.blit(description_text_part04, description_rect_part04)
                    description_text_part05 = get_font(DESCRIPTION_FONT_SIZE).render("turrets and bullets speed", True,
                                                                                     "#605b00")
                    description_rect_part05 = description_text_part05.get_rect(center=(665, 655))
                    SCREEN.blit(description_text_part05, description_rect_part05)
                    medium_difficulty = pygame.image.load("../Textures/medium_difficulty_icon.png")
                    SCREEN.blit(medium_difficulty, (420, 550))
                if self.difficulty_button == 3:
                    description_text_part01 = get_font(DESCRIPTION_FONT_SIZE).render(
                        "Hard difficulty (Ultra Violence):", True, "#605b00")
                    description_rect_part01 = description_text_part01.get_rect(center=(672, 518))
                    SCREEN.blit(description_text_part01, description_rect_part01)
                    description_text_part02 = get_font(DESCRIPTION_FONT_SIZE).render(
                        "- 30% chance of drop from every enemy", True, "#605b00")
                    description_rect_part02 = description_text_part02.get_rect(center=(725, 550))
                    SCREEN.blit(description_text_part02, description_rect_part02)
                    description_text_part03 = get_font(DESCRIPTION_FONT_SIZE).render(
                        "   - 1 additional lifes in every attempt", True, "#605b00")
                    description_rect_part03 = description_text_part03.get_rect(center=(710, 585))
                    SCREEN.blit(description_text_part03, description_rect_part03)
                    description_text_part04 = get_font(DESCRIPTION_FONT_SIZE).render("   - Very fast reaction of", True,
                                                                                     "#605b00")
                    description_rect_part04 = description_text_part04.get_rect(center=(640, 620))
                    SCREEN.blit(description_text_part04, description_rect_part04)
                    description_text_part05 = get_font(DESCRIPTION_FONT_SIZE).render("turrets and bullets speed", True,
                                                                                     "#605b00")
                    description_rect_part05 = description_text_part05.get_rect(center=(665, 655))
                    SCREEN.blit(description_text_part05, description_rect_part05)
                    hard_difficulty = pygame.image.load("../Textures/hard_difficulty_icon.png")
                    SCREEN.blit(hard_difficulty, (420, 550))
                if self.difficulty_button == 4:
                    description_text_part01 = get_font(DESCRIPTION_FONT_SIZE).render("Insane difficulty (Nightmare):",
                                                                                     True, "#605b00")
                    description_rect_part01 = description_text_part01.get_rect(center=(672, 518))
                    SCREEN.blit(description_text_part01, description_rect_part01)
                    description_text_part02 = get_font(DESCRIPTION_FONT_SIZE).render(
                        "- No drop from enemies", True, "#605b00")
                    description_rect_part02 = description_text_part02.get_rect(center=(650, 550))
                    SCREEN.blit(description_text_part02, description_rect_part02)
                    description_text_part03 = get_font(DESCRIPTION_FONT_SIZE).render("   - Additional lifes is absent",
                                                                                     True, "#605b00")
                    description_rect_part03 = description_text_part03.get_rect(center=(665, 580))
                    SCREEN.blit(description_text_part03, description_rect_part03)
                    description_text_part04 = get_font(DESCRIPTION_FONT_SIZE).render("   - Perfect reaction of", True,
                                                                                     "#605b00")
                    description_rect_part04 = description_text_part04.get_rect(center=(630, 610))
                    SCREEN.blit(description_text_part04, description_rect_part04)
                    description_text_part05 = get_font(DESCRIPTION_FONT_SIZE).render("turrets and bullets speed", True,
                                                                                     "#605b00")
                    description_rect_part05 = description_text_part05.get_rect(center=(665, 640))
                    SCREEN.blit(description_text_part05, description_rect_part05)
                    description_text_part06 = get_font(DESCRIPTION_FONT_SIZE).render("   - No hope...", True, "#605b00")
                    description_rect_part06 = description_text_part06.get_rect(center=(585, 670))
                    SCREEN.blit(description_text_part06, description_rect_part06)
                    insane_difficulty = pygame.image.load("../Textures/insane_difficulty_icon.png")
                    SCREEN.blit(insane_difficulty, (420, 550))
            else:
                self.image_path = self.image_path[:PATH_INDENT] + "disabled.png"
                self.image = pygame.image.load(self.image_path)


def get_font(size):
    return pygame.font.Font("../Textures/font.ttf", size)
