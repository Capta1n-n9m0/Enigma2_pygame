import pygame
import time
import sys
import random
import string


KEY_BG = pygame.image.load("key1.png")
KEY_BG = pygame.transform.scale(KEY_BG, (100, 100))

class Rotor:
    def __init__(self, outputs: list[str]):
        if len(outputs) != 26:
            raise IndexError("Wrong rotor alphabet")
        self.outputs = outputs
        self.shift = 0

    def turn(self, n=1):
        self.outputs = self.outputs[n:] + self.outputs[:n]
        if self.shift == 26:
            self.shift = 0
        else:
            self.shift += 1

    def encode(self, letter: str):
        if len(letter) != 1:
            raise IndexError("Cannot encode more that one letter at a time")
        res = self.outputs[ord(letter.lower()) - ord("a")]
        self.turn()
        return res


class Key:
    def __init__(self, key, posx, posy):
        global KEY_BG
        self.posx = posx
        self.posy = posy
        self.key = KEY_BG.copy()
        self.font_ = pygame.font.SysFont("timesnewroman", 20)
        self.letter = self.font_.render(key, True, pygame.color.Color(0, 0, 0, 255))
        self.key.blit(self.letter, (0, 0))

        pass

    def press(self):
        ...

    def unpress(self):
        ...

class Board:
    def __init__(self, posx, posy):
        self.posx = posx
        self.posy = posy

        pass

class Enigma:

    @staticmethod
    def setup():
        pygame_status = pygame.init()
        print(pygame_status)

    def __init__(self):
        resolution = (1000, 720)
        self.screen = pygame.display.set_mode(resolution, pygame.DOUBLEBUF | pygame.RESIZABLE)

        # keys
        self.set1 = ['c', 'p', 'w', 'z', 's', 'o', 'd', 'y', 'g', 'm', 'x', 'k', 'j', 'u', 'h', 'e', 'l', 'n', 'i', 'a', 't', 'f', 'b', 'q', 'v', 'r']
        self.set2 = ['u', 's', 'y', 'q', 'd', 'c', 'b', 'i', 'k', 'l', 'n', 'e', 't', 'w', 'f', 'g', 'h', 'r', 'o', 'm', 'z', 'a', 'v', 'j', 'p', 'x']
        self.set3 = ['m', 't', 'z', 'r', 'j', 'x', 'o', 's', 'n', 'w', 'h', 'l', 'f', 'y', 'd', 'v', 'b', 'g', 'u', 'q', 'c', 'e', 'a', 'k', 'p', 'i']

        # rotors
        self.rotor1 = Rotor(self.set1)
        self.rotor2 = Rotor(self.set2)
        self.rotor3 = Rotor(self.set3)

        # decoration
        pygame.display.set_caption("Enigma machine")
        icon = pygame.image.load("icon.jpg")
        pygame.display.set_icon(icon)

        # display
        self.lampboard_img = pygame.image.load("enigma-lampboard.jpg")
        self.lampboard_img = pygame.transform.scale(self.lampboard_img, (990, 300))
        self.keyboard_img  = pygame.image.load("enigma-keyboard.jpg")
        self.keyboard_img  = pygame.transform.scale(self.keyboard_img, (990, 339))

        # sound
        self.keypress_sound = pygame.mixer.Sound("Keypress-sound2.wav")
        self.keypress_sound.set_volume(0.3)

        # variables
        self.ii = 0
        self.frame_start = time.time_ns()
        self.frames = 0

    def run(self):
        while True:
            event = pygame.event.wait()
            if event.type == pygame.QUIT:
                print("quiting")
                sys.exit(0)
            if event.type == pygame.KEYDOWN:
                self.keydown_handle(event.key)
            if event.type == pygame.KEYUP:
                self.keyup_handle(event.key)
            self.screen.fill((232, 172, 132))
            self.frame()
            pygame.display.update()
            self.framerate()

    def keydown_handle(self, event):
        self.keypress_sound.play()
        print(f"{chr(self.key_filter(event))}", end="")

    def keyup_handle(self, event):
        pressed_key = chr(self.key_filter(event))
        rotor1_res = self.rotor1.encode(pressed_key)
        rotor2_res = self.rotor2.encode(rotor1_res)
        rotor3_res = self.rotor3.encode(rotor2_res)
        print(rotor3_res, end="")


    def key_filter(self, key):
        if pygame.K_a <= key <= pygame.K_z or pygame.K_0 <= key <= pygame.K_9:
            return key
        else:
            return ord("?")

    def highlight_key(self, key):
        ...

    def frame(self):
        self.screen.blit(self.lampboard_img, (5, 5))
        self.screen.blit(self.keyboard_img, (5, 355))

    def framerate(self):
        if time.time_ns() - self.frame_start > 10**9:
            # print(f"Framerate: {self.frames} FPS; Frametime: {1000/self.frames:.2f}ms")
            self.frame_start = time.time_ns()
            self.frames = 0
        else:
            self.frames += 1

def main():
    Enigma.setup()
    e = Enigma()
    e.run()

def test():
    alphabet = [i for i in string.ascii_lowercase]
    random.shuffle(alphabet)
    print(alphabet)




if __name__ == '__main__':
    main()
    # test()
    ...
