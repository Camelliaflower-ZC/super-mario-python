import pygame
from classes.Equipment import Equipment
from classes.Dashboard import Dashboard
from classes.Level import Level
from classes.Menu import Menu
from classes.Sound import Sound
from entities.Mario import Mario


windowSize = 640, 480
selectedSkin = "red"
#初始颜色为红色


def main(equipment):
    global selectedSkin
    pygame.mixer.pre_init(44100, -16, 2, 4096)
    pygame.init()
    screen = pygame.display.set_mode(windowSize)
    max_frame_rate = 60
    dashboard = Dashboard("./img/font.png", 8, screen)
    sound = Sound()
    level = Level(screen, sound, dashboard)
    menu = Menu(screen, dashboard, level, sound, equipment, selectedSkin=selectedSkin)

    while not menu.start:
        menu.update()
    selectedSkin = menu.selectedSkin

    mario = Mario(0, 0, level, screen, dashboard, sound, equipment)
    clock = pygame.time.Clock()

    while not mario.restart:
        pygame.display.set_caption("Super Mario running with {:d} FPS".format(int(clock.get_fps())))
        if mario.pause:
            mario.pauseObj.update()
        else:
            level.drawLevel(mario.camera)
            dashboard.update()
            mario.update()
        pygame.display.update()
        clock.tick(max_frame_rate)
    return 'restart'


if __name__ == "__main__":
    exitmessage = 'restart'
    equipment = Equipment()
    while exitmessage == 'restart':
        exitmessage = main(equipment)
