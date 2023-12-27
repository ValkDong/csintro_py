import pygame


class EventHandler:
    def__init__() -> None:
        EventHandler.events = pygame.event.get()
    def poll_events():
        EventHandler.events = pygame.event.get()
    def keydown(key):
        for event in EventHandler.events:
            if event.type == pygame.KEYDOWN:
                if event.key == key:
                    return True
        return False
    def clicked(leftright = 1) -> bool:
        for event in EventHandler.events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == leftright:
                    return True
        return False
    def clicked_any() -> bool:
        for event in EventHandler.events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                return True
        return False
