import json
import sys
import os
import pygame

from classes.Spritesheet import Spritesheet


class Menu:
    def __init__(self, screen, dashboard, level, sound, equipment, selectedSkin="red"):
        self.screen = screen
        self.sound = sound
        self.start = False
        self.inSettings = False
        self.inChoosingSkin = False
        self.state = 0
        self.level = level
        self.equipment = equipment
        self.music = True
        self.sfx = True
        self.currSelectedLevel = 1
        self.levelNames = []
        self.inChoosingLevel = False
        self.inChoosingEquipment = False
        self.currSelectedEquipment = 0
        self.equipmentOptions = ["none", "shield", "sword"]
        self.dashboard = dashboard
        self.selectedSkin = selectedSkin
        self.level.sprites.setMarioSkin(self.selectedSkin)
        self.levelCount = 0
        self.spritesheet = Spritesheet("./img/title_screen.png")
        self.menu_banner = self.spritesheet.image_at(
            0,
            60,
            2,
            colorkey=[255, 0, 220],
            ignoreTileSize=True,
            xTileSize=180,
            yTileSize=88,
        )
        self.menu_dot = self.spritesheet.image_at(
            0, 150, 2, colorkey=[255, 0, 220], ignoreTileSize=True
        )
        self.menu_dot2 = self.spritesheet.image_at(
            20, 150, 2, colorkey=[255, 0, 220], ignoreTileSize=True
        )
        self.loadSettings("./settings.json")

    def update(self):
        self.checkInput()
        if self.inChoosingLevel or self.inChoosingEquipment or self.inChoosingSkin:
            return

        self.drawMenuBackground()
        self.dashboard.update()

        if not self.inSettings:
            self.drawMenu()
        else:
            self.drawSettings()

    def drawDot(self):
        positions = (273, 313, 353) if self.inSettings else (243, 283, 323, 363, 403)
        for index, y in enumerate(positions):
            dot = self.menu_dot if self.state == index else self.menu_dot2
            self.screen.blit(dot, (145, y))

    def loadSettings(self, url):
        try:
            with open(url) as jsonData:
                data = json.load(jsonData)
                if data["sound"]:
                    self.music = True
                    self.sound.music_channel.play(self.sound.soundtrack, loops=-1)
                else:
                    self.music = False
                if data["sfx"]:
                    self.sfx = True
                    self.sound.allowSFX = True
                else:
                    self.sound.allowSFX = False
                    self.sfx = False
        except (IOError, OSError):
            self.music = False
            self.sound.allowSFX = False
            self.sfx = False
            self.saveSettings("./settings.json")

    def saveSettings(self, url):
        data = {"sound": self.music, "sfx": self.sfx}
        with open(url, "w") as outfile:
            json.dump(data, outfile)

    def drawMenu(self):
        self.drawDot()
        self.dashboard.drawText("CHOOSE LEVEL", 180, 250, 24)
        self.dashboard.drawText("EQUIPMENT", 180, 290, 24)
        self.dashboard.drawText("SKIN", 180, 330, 24)
        self.dashboard.drawText("SETTINGS", 180, 370, 24)
        self.dashboard.drawText("EXIT", 180, 410, 24)

    def chooseSkin(self):
        self.inChoosingSkin = True
        self.drawMenuBackground(False)
        self.drawSkinChooser()

    def drawSkinChooser(self):
        skins = ("red", "green", "yellow")
        labels = ("RED", "GREEN", "YELLOW")
        positions = (85, 255, 425)
        self.dashboard.drawText("CHOOSE MARIO SKIN", 145, 205, 18)
        for skin, label, x in zip(skins, labels, positions):
            color = (255, 255, 255) if skin == self.selectedSkin else (150, 150, 150)
            pygame.draw.rect(self.screen, color, (x, 260, 130, 70), 4)
            self.dashboard.drawText(label, x + 18, 283, 18)
        self.dashboard.drawText("LEFT / RIGHT: SELECT", 165, 365, 14)
        self.dashboard.drawText("ENTER: BACK", 205, 390, 14)

    def drawMenuBackground(self, withBanner=True):
        for y in range(0, 13):
            for x in range(0, 20):
                self.screen.blit(
                    self.level.sprites.spriteCollection.get("sky").image,
                    (x * 32, y * 32),
                )
        for y in range(13, 15):
            for x in range(0, 20):
                self.screen.blit(
                    self.level.sprites.spriteCollection.get("ground").image,
                    (x * 32, y * 32),
                )
        if withBanner:
            self.screen.blit(self.menu_banner, (150, 80))
        self.screen.blit(
            self.level.sprites.spriteCollection.get("mario_idle").image,
            (2 * 32, 12 * 32),
        )
        self.screen.blit(
            self.level.sprites.spriteCollection.get("bush_1").image, (14 * 32, 12 * 32)
        )
        self.screen.blit(
            self.level.sprites.spriteCollection.get("bush_2").image, (15 * 32, 12 * 32)
        )
        self.screen.blit(
            self.level.sprites.spriteCollection.get("bush_2").image, (16 * 32, 12 * 32)
        )
        self.screen.blit(
            self.level.sprites.spriteCollection.get("bush_2").image, (17 * 32, 12 * 32)
        )
        self.screen.blit(
            self.level.sprites.spriteCollection.get("bush_3").image, (18 * 32, 12 * 32)
        )
        self.screen.blit(self.level.sprites.spriteCollection.get("goomba-1").image, (18.5*32, 12*32))

    def drawSettings(self):
        self.drawDot()
        self.dashboard.drawText("MUSIC", 180, 280, 24)
        if self.music:
            self.dashboard.drawText("ON", 340, 280, 24)
        else:
            self.dashboard.drawText("OFF", 340, 280, 24)
        self.dashboard.drawText("SFX", 180, 320, 24)
        if self.sfx:
            self.dashboard.drawText("ON", 340, 320, 24)
        else:
            self.dashboard.drawText("OFF", 340, 320, 24)
        self.dashboard.drawText("BACK", 180, 360, 24)

    def chooseLevel(self):
        self.drawMenuBackground(False)
        self.inChoosingLevel = True
        self.levelNames = self.loadLevelNames()
        self.drawLevelChooser()

    def chooseEquipment(self):
        self.inChoosingEquipment = True
        self.currSelectedEquipment = self.equipmentOptions.index(self.equipment.selected)
        self.drawEquipmentChooser()

    def drawEquipmentChooser(self):
        self.drawMenuBackground(False)
        self.dashboard.drawText("CHOOSE EQUIPMENT", 150, 115, 20)
        labels = ("NONE", "SHIELD", "SWORD")
        for index, label in enumerate(labels):
            color = (255, 255, 255) if index == self.currSelectedEquipment else (150, 150, 150)
            self.dashboard.drawText(label, 95 + index * 155, 180, 16)
            pygame.draw.rect(self.screen, color, (80 + index * 155, 170, 125, 35), 2)

        # Preview the selected gear on the original Mario sprite.
        preview_x, preview_y = 300, 245
        mario = self.level.sprites.spriteCollection.get("mario_idle").image
        self.screen.blit(mario, (preview_x, preview_y))
        selected = self.equipmentOptions[self.currSelectedEquipment]
        original = self.equipment.selected
        self.equipment.selected = selected
        self.equipment.draw(self.screen, (preview_x, preview_y), 1)
        self.equipment.selected = original
        self.dashboard.drawText("LEFT/RIGHT: SELECT", 205, 355, 12)
        self.dashboard.drawText("ENTER: EQUIP   ESC: BACK", 170, 375, 12)

    def drawBorder(self, x, y, width, height, color, thickness):
        pygame.draw.rect(self.screen, color, (x, y, width, thickness))
        pygame.draw.rect(self.screen, color, (x, y+width, width, thickness))
        pygame.draw.rect(self.screen, color, (x, y, thickness, width))
        pygame.draw.rect(self.screen, color, (x+width, y, thickness, width+thickness))

    def drawLevelChooser(self):
        j = 0
        offset = 75
        textOffset = 90
        for i, levelName in enumerate(self.loadLevelNames()):
            if self.currSelectedLevel == i+1:
                color = (255, 255, 255)
            else:
                color = (150, 150, 150)
            if i < 3:
                self.dashboard.drawText(levelName, 175*i+textOffset, 100, 12)
                self.drawBorder(175*i+offset, 55, 125, 75, color, 5)
            else:
                self.dashboard.drawText(levelName, 175*j+textOffset, 250, 12)
                self.drawBorder(175*j+offset, 210, 125, 75, color, 5)
                j += 1

    def loadLevelNames(self):
        files = []
        res = []
        for r, d, f in os.walk("./levels"):
            for file in f:
                files.append(os.path.join(r, file))
        for f in files:
            res.append(os.path.split(f)[1].split(".")[0])
        self.levelCount = len(res)
        return res

    def checkInput(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.inChoosingSkin:
                        self.inChoosingSkin = False
                        self.state = 2
                    elif self.inChoosingEquipment:
                        self.inChoosingEquipment = False
                        self.state = 1
                    elif self.inChoosingLevel:
                        self.inChoosingLevel = False
                        self.state = 0
                    elif self.inSettings:
                        self.inSettings = False
                        self.state = 3
                    else:
                        pygame.quit()
                        sys.exit()
                elif event.key == pygame.K_UP or event.key == pygame.K_k:
                    if self.inChoosingLevel:
                        if self.currSelectedLevel > 3:
                            self.currSelectedLevel -= 3
                            self.drawLevelChooser()
                    elif not self.inChoosingEquipment and not self.inChoosingSkin and self.state > 0:
                        self.state -= 1
                elif event.key == pygame.K_DOWN or event.key == pygame.K_j:
                    if self.inChoosingLevel:
                        if self.currSelectedLevel+3 <= self.levelCount:
                            self.currSelectedLevel += 3
                            self.drawLevelChooser()
                    elif not self.inChoosingEquipment and not self.inChoosingSkin and self.state < (2 if self.inSettings else 4):
                        self.state += 1
                elif event.key == pygame.K_LEFT or event.key == pygame.K_h:
                    if self.inChoosingEquipment:
                        self.currSelectedEquipment = (self.currSelectedEquipment - 1) % len(self.equipmentOptions)
                        self.drawEquipmentChooser()
                        continue
                    elif self.inChoosingSkin:
                        self.changeSkin(-1)
                        continue
                    elif self.inChoosingLevel and self.currSelectedLevel > 1:
                        self.currSelectedLevel -= 1
                        self.drawLevelChooser()
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_l:
                    if self.inChoosingEquipment:
                        self.currSelectedEquipment = (self.currSelectedEquipment + 1) % len(self.equipmentOptions)
                        self.drawEquipmentChooser()
                        continue
                    elif self.inChoosingSkin:
                        self.changeSkin(1)
                        continue
                    elif self.inChoosingLevel and self.currSelectedLevel < self.levelCount:
                        self.currSelectedLevel += 1
                        self.drawLevelChooser()
                elif event.key == pygame.K_RETURN:
                    if self.inChoosingEquipment:
                        self.equipment.selected = self.equipmentOptions[self.currSelectedEquipment]
                        self.inChoosingEquipment = False
                        continue
                    if self.inChoosingSkin:
                        self.inChoosingSkin = False
                        self.state = 2
                        continue
                    if self.inChoosingLevel:
                        self.inChoosingLevel = False
                        self.dashboard.state = "start"
                        self.dashboard.time = 0
                        self.level.loadLevel(self.levelNames[self.currSelectedLevel-1])
                        self.dashboard.levelName = self.levelNames[self.currSelectedLevel-1].split("Level")[1]
                        self.start = True
                        return
                    if not self.inSettings:
                        if self.state == 0:
                            self.chooseLevel()
                        elif self.state == 1:
                            self.chooseEquipment()
                        elif self.state == 2:
                            self.chooseSkin()
                        elif self.state == 3:
                            self.inSettings = True
                            self.state = 0
                        elif self.state == 4:
                            pygame.quit()
                            sys.exit()
                    else:
                        if self.state == 0:
                            if self.music:
                                self.sound.music_channel.stop()
                                self.music = False
                            else:
                                self.sound.music_channel.play(self.sound.soundtrack, loops=-1)
                                self.music = True
                            self.saveSettings("./settings.json")
                        elif self.state == 1:
                            if self.sfx:
                                self.sound.allowSFX = False
                                self.sfx = False
                            else:
                                self.sound.allowSFX = True
                                self.sfx = True
                            self.saveSettings("./settings.json")
                        elif self.state == 2:
                            self.inSettings = False
        pygame.display.update()

    def changeSkin(self, direction):
        skins = ("red", "green", "yellow")
        index = skins.index(self.selectedSkin)
        self.selectedSkin = skins[(index + direction) % len(skins)]
        self.level.sprites.setMarioSkin(self.selectedSkin)
        self.drawMenuBackground(False)
        self.drawSkinChooser()
