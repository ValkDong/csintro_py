    self scene=Scene(self)
def run(self):
    while self.running:
        self.update()
        self.draw()
    self.close()
def update(self):
    EventHandler.poll_events()
    for event in EventHandler.events:
        if event.type==pygame QUIT:
            self.running=False

    self scene.update()

    pygame.display.update()
    self.clock.tick(FPS)
def draw(self):
    self.scene.draw()
def close(self):
    pygame.quit()
    sys.exit()
