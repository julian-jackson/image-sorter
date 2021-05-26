import pygame, os, time
from pathlib import Path

pygame.init()
clock = pygame.time.Clock()

win = pygame.display.set_mode((1280, 720), pygame.RESIZABLE)
pygame.display.set_caption("Cell Image Sorter")

main_path = os.path.dirname(os.path.realpath(__file__))
run = True

width_scaler = 0
height_scaler = 0
original_width = 1280
original_height = 720

image_index = 0
dir_list = os.listdir(path=main_path) 
image_dir_list = []
textbox_handler = []
image_types = [".png", ".jpeg", ".jpg"]

for item in dir_list:
    for image_type in image_types:
        if image_type in item:
            if not "health-" in item:
                image_dir_list.append(item)

print(image_dir_list)

class TextBox:
    def __init__(self, x = 0, y= 0, font_size = 64, font_colour = (0, 0, 0), text="Placeholder"):
        self.x = x
        self.y = y
        self.text = text
        self.font_size = font_size
        self.font_colour = font_colour
    def draw(self, win):
        my_surface = pygame.font.Font(None, self.font_size).render(self.text, True, self.font_colour)
        win.blit(my_surface, (self.x, self.y))

class Button:
    def __init__(self, x=0, y=0, width=64, height=64, passive_colour=(255, 255, 255), active_colour=(0, 0, 0), font_size=32, active_font=(255, 255, 255), passive_font=(0, 0, 0), border_width=10, icon_type="Text", icon="Demo", item_id="default"):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.passive_colour = passive_colour
        self.active_colour = active_colour
        self.colour = passive_colour
        self.border_width = border_width

        self.font_size = font_size
        self.active_font = active_font
        self.passive_font = passive_font
        self.font_colour = passive_font
        self.font = pygame.font.Font(None, self.font_size)

        self.icon_type = icon_type
        self.icon = icon
        self.item_id = item_id
        self.active = False

        text_surface = self.font.render(self.icon, True, self.font_colour)
        text_surface_rect = pygame.Surface(text_surface.get_size())
        self.rect = pygame.Rect(self.x, self.y, text_surface_rect.get_width(), text_surface_rect.get_height())

    def draw(self, win):
        click = pygame.mouse.get_pressed()
        mouse = pygame.mouse.get_pos()
        
        if self.rect.collidepoint(mouse):
            self.active = True
        else:
            self.active = False

        if click[0] and self.rect.collidepoint(mouse):
            return self.item_id

        if self.active:
            self.colour = self.active_colour
            self.font_colour = self.active_font
        else:
            self.colour = self.passive_colour
            self.font_colour = self.passive_font

        text_surface = self.font.render(self.icon, True, self.font_colour)

        text_surface_rect = pygame.Surface(text_surface.get_size())
        text_surface_rect.fill(self.colour)
        text_surface_rect.blit(text_surface, (0, 0))
        win.blit(text_surface_rect, (self.x, self.y))

class InputBox:
    def __init__(self, x=0, y=0, width=96, height=32, passive_colour=pygame.Color("gray15"), active_colour=pygame.Color("lightskyblue3")):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.box = pygame.Rect(self.x, self.y, self.width, self.height)
        self.text = "0."
        self.active = True
        self.passive_colour = passive_colour
        self.active_colour =  active_colour
        self.colour = self.passive_colour
        self.font = pygame.font.Font(None, 48)
    
    def reset(self):
        self.text = "0."
            
    def keydown_update(self, event):
        keys = pygame.key.get_pressed()
        if self.active == True:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif event.key == pygame.K_RETURN:
                event_handler.append("submit")

            elif event.key == pygame.K_e and pygame.key.get_mods() & pygame.KMOD_SHIFT:
                self.text = ""
            else:
                self.text += event.unicode 
            return self.text
        
    def draw(self, win):
        click = pygame.mouse.get_pressed()
        mouse = pygame.mouse.get_pos()
        if click[0]:
            if self.box.collidepoint(mouse):
                self.active = True
            else:
                self.active = False
        if self.active:
            self.colour = self.active_colour
        else:
            self.colour = self.passive_colour

        pygame.draw.rect(win, self.colour, self.box, 3)
        text_surface = self.font.render(self.text, True, (0, 0, 0))
        win.blit(text_surface, (self.x + 5, self.y + 5))

title_textbox = TextBox(x=150, y=75, font_size=30, font_colour=(30, 30, 30), text="Image Sorter")
health_button = Button(x=320, y=150, font_size=75, item_id="submit", active_font=(220, 220, 220), passive_colour=(75, 75, 75), active_colour=(38, 38, 38), icon="+")
health_inputbox = InputBox(x=100, y=150, width=200 + width_scaler, height=48, passive_colour=(50, 50, 50), active_colour=(0, 0, 0))

render_queue = (title_textbox, health_button, health_inputbox)

while run:

    event_handler = []
    win.fill((255,255,255))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.VIDEORESIZE:
            win = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
            width_scaler = event.w - original_width
            height_scaler = event.h  - original_height
        if event.type == pygame.KEYDOWN:
            textbox_handler = []
            textbox_handler.append(health_inputbox.keydown_update(event))

    current_image = pygame.image.load(f"{main_path}/{image_dir_list[image_index]}")
    scaled_current_image = pygame.transform.scale(current_image, (768 + width_scaler, 432 + int(height_scaler / 2)))
    win.blit(scaled_current_image, (430, 70))

    for obj in render_queue:
        event_handler.append(obj.draw(win))

    if "submit" in event_handler:
        print(textbox_handler[0])
        os.rename(f"{main_path}/{image_dir_list[image_index]}", f"{main_path}/health-{textbox_handler[0]}-{image_dir_list[image_index]}")
        image_index += 1
        health_inputbox.reset()
        time.sleep(0.1)

    

    clock.tick(60)
    pygame.display.update()
