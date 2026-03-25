import pygame
from screens import MenuScreen

def RunningProgram(MainScreen):

    screens = {
        "menu": MenuScreen(MainScreen)
        
    }

    current_screen = "menu"
    running = True
    
    while(running):
        current = screens[current_screen]
        current.next_screen = None
        current.running = True

        events = pygame.event.get()
        
        for event in events:
            if event.type == pygame.QUIT:
                running = False

        current.handle_events(events)
        current.update()
        current.draw()

        pygame.display.flip()
        current.clock.tick(60)

        if current.next_screen:
            if current.next_screen == "quit":
                running = False
            elif current.next_screen in screens:
                current_screen = current.next_screen

    pygame.quit()


