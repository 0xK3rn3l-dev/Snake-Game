import pygame
from screens.MenuScreen import MenuScreen
from screens.SettingScreen import SettingScreen
from screens.GameScreen import GameScreen


def RunningProgram(MainScreen):

    screens = {
        "menu": MenuScreen(MainScreen),
        "game": GameScreen(MainScreen),
        "settings": SettingScreen(MainScreen)
    }

    current_screen_key = "menu"
    current = screens[current_screen_key]

    current.on_enter()

    running = True

    while running:

        # EVENTS
        events = pygame.event.get()

        for event in events:
            if event.type == pygame.QUIT:
                running = False

        # LOGIC
        current.handle_events(events)
        current.update()
        current.draw()

        pygame.display.flip()
        current.clock.tick(60)

        # SCREEN SWITCH
        if current.next_screen:

            if current.next_screen == "quit":
                running = False
                continue

            if current.next_screen in screens:

                # exit old
                current.on_exit()

                # switch
                current_screen_key = current.next_screen
                current = screens[current_screen_key]

                current.next_screen = None
                current.running = True

                # enter new
                current.on_enter()

    pygame.quit()