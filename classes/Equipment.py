import pygame


class Equipment:
    """Session equipment choice and its pixel-art rendering."""

    def __init__(self):
        # A new process starts without equipment. This object is shared by the
        # menu and each Mario instance so the choice survives a death/restart.
        self.selected = "none"
        self._images = {}

    def image(self, kind, big=False, heading=1):
        if kind not in ("shield", "sword"):
            return None
        key = (kind, big)
        if key not in self._images:
            self._images[key] = self._create_image(kind, big)
        image = self._images[key]
        if heading < 0:
            return pygame.transform.flip(image, True, False)
        return image

    def draw(self, screen, mario_pos, heading, big=False):
        image = self.image(self.selected, big, heading)
        if image is None:
            return

        x, y = mario_pos
        scale = 4 if big else 2
        # Anchor the grip at Mario's outer hand, then mirror that anchor when
        # he turns. The grip and hand stay connected at both character sizes.
        hand_x = 29 if heading >= 0 else 3
        hand_y = 31 if big else 21
        grip_x, grip_y = (5, 8) if self.selected == "shield" else (5, 10)
        if heading < 0:
            grip_x = 16 - grip_x
        x += hand_x - grip_x * scale
        y += hand_y - grip_y * scale
        screen.blit(image, (x, y))

    def _create_image(self, kind, big):
        # Draw at a small logical resolution, then scale with nearest-neighbour
        # pixels. Big Mario receives a 2x equipment size.
        scale = 4 if big else 2
        surface = pygame.Surface((16, 16), pygame.SRCALPHA)

        if kind == "shield":
            # The handle sits at the inner edge, where Mario's hand meets the
            # shield. The body tapers toward the bottom like a small buckler.
            pygame.draw.rect(surface, (110, 65, 35), (3, 6, 3, 5))
            pygame.draw.polygon(surface, (55, 25, 22), [(5, 2), (13, 2), (14, 3), (14, 9), (10, 13), (5, 10)])
            # Dark outer plane gives the shield a slight turned profile.
            pygame.draw.polygon(surface, (105, 30, 28), [(12, 3), (14, 3), (14, 9), (10, 13), (10, 11), (12, 8)])
            pygame.draw.polygon(surface, (205, 48, 42), [(6, 4), (12, 4), (12, 8), (9, 11), (6, 9)])
            pygame.draw.line(surface, (245, 105, 78), (7, 5), (7, 8), 1)
            pygame.draw.rect(surface, (245, 205, 75), (9, 5, 2, 4))
            pygame.draw.rect(surface, (245, 205, 75), (8, 6, 4, 2))
        else:
            # Handle at lower-left, blade extending up-right. The compact
            # crossguard sits at the blade root, perpendicular to its axis.
            pygame.draw.line(surface, (55, 45, 35), (5, 10), (2, 13), 3)
            pygame.draw.line(surface, (115, 65, 35), (5, 10), (2, 13), 1)
            pygame.draw.line(surface, (55, 45, 35), (7, 8), (15, 0), 3)
            pygame.draw.line(surface, (225, 235, 240), (8, 7), (15, 0), 1)
            pygame.draw.line(surface, (55, 45, 35), (4, 7), (8, 11), 3)
            pygame.draw.line(surface, (235, 185, 55), (4, 7), (8, 11), 1)

        return pygame.transform.scale(surface, (16 * scale, 16 * scale))
