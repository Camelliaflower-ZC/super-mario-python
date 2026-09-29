import json

from classes.Animation import Animation
from classes.Sprite import Sprite
from classes.Spritesheet import Spritesheet


class Sprites:
    def __init__(self):
        self.spriteCollection = self.loadSprites(
            [
                "./sprites/Mario.json",
                "./sprites/Goomba.json",
                "./sprites/Koopa.json",
                "./sprites/Animations.json",
                "./sprites/BackgroundSprites.json",
                "./sprites/ItemAnimations.json",
                "./sprites/RedMushroom.json"
            ]
        )
        self.marioOriginalImages = {
            name: sprite.image.copy()
            for name, sprite in self.spriteCollection.items()
            if name.startswith("mario_")
        }
        self.marioSkin = "red"

    def setMarioSkin(self, skin):
        if skin not in ("red", "green", "yellow"):
            skin = "red"

        replacementColors = {
            "red": None,
            "green": (0, 190, 0),
            "yellow": (255, 220, 0),
        }
        replacement = replacementColors[skin]

        for name, original in self.marioOriginalImages.items():
            image = original.copy()
            if replacement is not None:
                for y in range(image.get_height()):
                    for x in range(image.get_width()):
                        color = image.get_at((x, y))
                        if color.r == 255 and color.g == 49 and color.b == 24:
                            image.set_at((x, y), (*replacement, color.a))
            self.spriteCollection[name].image = image

        self.marioSkin = skin
        #给mario服装换颜色且保证人物不变

    def loadSprites(self, urlList):
        resDict = {}
        for url in urlList:
            with open(url) as jsonData:
                data = json.load(jsonData)
                mySpritesheet = Spritesheet(data["spriteSheetURL"])
                dic = {}
                if data["type"] == "background":
                    for sprite in data["sprites"]:
                        try:
                            colorkey = sprite["colorKey"]
                        except KeyError:
                            colorkey = None
                        dic[sprite["name"]] = Sprite(
                            mySpritesheet.image_at(
                                sprite["x"],
                                sprite["y"],
                                sprite["scalefactor"],
                                colorkey,
                            ),
                            sprite["collision"],
                            None,
                            sprite["redrawBg"],
                        )
                    resDict.update(dic)
                    continue
                elif data["type"] == "animation":
                    for sprite in data["sprites"]:
                        images = []
                        for image in sprite["images"]:
                            images.append(
                                mySpritesheet.image_at(
                                    image["x"],
                                    image["y"],
                                    image["scale"],
                                    colorkey=sprite["colorKey"],
                                )
                            )
                        dic[sprite["name"]] = Sprite(
                            None,
                            None,
                            animation=Animation(images, deltaTime=sprite["deltaTime"]),
                        )
                    resDict.update(dic)
                    continue
                elif data["type"] == "character" or data["type"] == "item":
                    for sprite in data["sprites"]:
                        try:
                            colorkey = sprite["colorKey"]
                        except KeyError:
                            colorkey = None
                        try:
                            xSize = sprite['xsize']
                            ySize = sprite['ysize']
                        except KeyError:
                            xSize, ySize = data['size']
                        dic[sprite["name"]] = Sprite(
                            mySpritesheet.image_at(
                                sprite["x"],
                                sprite["y"],
                                sprite["scalefactor"],
                                colorkey,
                                True,
                                xTileSize=xSize,
                                yTileSize=ySize,
                            ),
                            sprite["collision"],
                        )
                    resDict.update(dic)
                    continue
        return resDict
