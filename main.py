import pygame, sys
from button import Button
from main_chess_engine import Start_game_events
import multiprocessing

main_game = Start_game_events()

pygame.init()

SCREEN = pygame.display.set_mode((1024, 700))
pygame.display.set_caption("Menu")

BG = pygame.image.load("assets/Background.jpg")

def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("assets/font.ttf", size)

def play():

    while True:
        PLAY_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill("black")


        # PLAY_TEXT = get_font(20).render("This is the PLAY screen.", True, "White")
        # PLAY_RECT = PLAY_TEXT.get_rect(center=(1000, 260))
        # SCREEN.blit(PLAY_TEXT, PLAY_RECT)

        PLAY_BACK = Button(image=None, pos=(870, 600),
                            text_input="BACK", font=get_font(30), base_color="White", hovering_color="Green")

        PLAY_BACK.changeColor(PLAY_MOUSE_POS)
        PLAY_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BACK.checkForInput(PLAY_MOUSE_POS):
                    main_menu()

        pygame.display.update()
    
def options():
    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill("grey")

        OPTIONS_TEXT1 = get_font(60).render("GAME OPTIONS", True, "Black")
        OPTIONS_RECT1 = OPTIONS_TEXT1.get_rect(center=(510, 100))
        SCREEN.blit(OPTIONS_TEXT1, OPTIONS_RECT1)
        OPTIONS_TEXT2 = get_font(40).render("Difficulty", True, "Black")
        OPTIONS_RECT2 = OPTIONS_TEXT2.get_rect(center=(300, 250))
        SCREEN.blit(OPTIONS_TEXT2, OPTIONS_RECT2)
        OPTIONS_TEXT3 = get_font(40).render("Volume", True, "Black")
        OPTIONS_RECT3 = OPTIONS_TEXT3.get_rect(center=(220, 320))
        SCREEN.blit(OPTIONS_TEXT3, OPTIONS_RECT3)
        OPTIONS_TEXT4 = get_font(40).render("Music", True, "Black")
        OPTIONS_RECT4 = OPTIONS_TEXT4.get_rect(center=(210, 390))
        SCREEN.blit(OPTIONS_TEXT4, OPTIONS_RECT4)
        OPTIONS_TEXT5 = get_font(40).render("Resolution", True, "Black")
        OPTIONS_RECT5 = OPTIONS_TEXT5.get_rect(center=(310, 460))
        SCREEN.blit(OPTIONS_TEXT5, OPTIONS_RECT5)
        OPTIONS_TEXT6 = get_font(35).render("Amateur", True, "Black")
        OPTIONS_RECT6 = OPTIONS_TEXT6.get_rect(center=(800, 250))
        SCREEN.blit(OPTIONS_TEXT6, OPTIONS_RECT6)
        OPTIONS_TEXT7 = get_font(40).render("75%", True, "Black")
        OPTIONS_RECT7 = OPTIONS_TEXT7.get_rect(center=(800, 320))
        SCREEN.blit(OPTIONS_TEXT7, OPTIONS_RECT7)
        OPTIONS_TEXT8 = get_font(40).render("ON/OFF", True, "Black")
        OPTIONS_RECT8 = OPTIONS_TEXT8.get_rect(center=(800, 390))
        SCREEN.blit(OPTIONS_TEXT8, OPTIONS_RECT8)
        OPTIONS_TEXT9 = get_font(40).render("700 x 700", True, "Black")
        OPTIONS_RECT9 = OPTIONS_TEXT9.get_rect(center=(800, 460))
        SCREEN.blit(OPTIONS_TEXT9, OPTIONS_RECT9)


        OPTIONS_BACK = Button(image=None, pos=(530, 630),
                            text_input="BACK", font=get_font(45), base_color="Black", hovering_color="White")

        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    main_menu()

        pygame.display.update()

def main_menu():
    while True:
        SCREEN.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(60).render("CHESS CHAMPION", True, "#d8db30")
        MENU_RECT = MENU_TEXT.get_rect(center=(550, 60))

        PLAY_BUTTON = Button(image=None, pos=(530, 320),
                            text_input="PLAY", font=get_font(55), base_color="#F0F8FF", hovering_color="White")
        OPTIONS_BUTTON = Button(image=None, pos=(530, 400),
                            text_input="SETTINGS", font=get_font(55), base_color="#F0F8FF", hovering_color="White")
        QUIT_BUTTON = Button(image=None, pos=(530, 480),
                            text_input="QUIT", font=get_font(55), base_color="#F0F8FF", hovering_color="White")

        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    # p1 = multiprocessing.Process(target=play())
                    # if __name__ == "__main__":
                    #     p1.start()
                    #     p1.join()
                    SCREEN.fill("Black")
                    PLAY_MOUSE_POS = pygame.mouse.get_pos()
                    PLAY_BACK = Button(image=None, pos=(870, 600), text_input="MAIN MENU", font=get_font(30), base_color="White", hovering_color="Green")
                    PLAY_BACK.changeColor(PLAY_MOUSE_POS)
                    PLAY_BACK.update(SCREEN)

            #         p1 = Process(target=play())
            #         p2 = Process(target=main_game.main_events())
            #         p2.start()
            #         p1.start()
                    main_game.main_events()
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    options()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

main_menu()