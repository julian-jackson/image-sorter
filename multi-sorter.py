import pygame, os
from shutil import copyfile

class InputBox:
    def __init__(self, x=0, y=0, width=256, height=64,active=False, passive_colour=(207, 207, 207), active_colour=(79, 79, 79), tag="default"):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.active = active
        self.box = pygame.Rect(self.x, self.y, self.width, self.height)

        self.active_colour = active_colour
        self.passive_colour = passive_colour
        self.colour = self.passive_colour

        self.font = pygame.font.Font(None, 48)
        self.text = ""
        self.state = ""
        self.dynamicLogging = False
        self.doubleTypedBlock = False
        self.tag = tag

    def update(self, event, keydown):
        self.surface = pygame.Surface((self.width, self.height))
        self.surface.fill((255, 255, 255))

        click = pygame.mouse.get_pressed()
        mouse = pygame.mouse.get_pos()

        if click[0]:
            if self.box.collidepoint(mouse):
                self.active = True
            else:
                self.active = False

        if self.active and keydown == True:
            self.colour = self.active_colour

            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif event.key == pygame.K_RETURN:
                self.state = self.text
                self.text = ""
                
            elif event.key == pygame.K_e and pygame.key.get_mods() & pygame.KMOD_SHIFT:
                self.text = ""
            else:
                self.text += event.unicode 

            if self.dynamicLogging:
                self.state = self.text

        else:
            self.colour = self.passive_colour

        pygame.draw.rect(self.surface, self.colour, self.box, 3)
        text_surface = self.font.render(self.text, True, (0, 0, 0))
        self.surface.blit(text_surface, (5, 5))

        self.data = {
            "surface": self.surface,
            "state": self.state,
            "tag": self.tag,
            "pos": [self.x, self.y]
        }

        return self.data

class TextBox:
    def __init__(self, x = 0, y= 0, font_size = 64, font_colour = (0, 0, 0), text="Placeholder"):
        self.x = x
        self.y = y
        self.text = text
        self.font_size = font_size
        self.font_colour = font_colour
    def update(self, event, keydown):
        self.surface = pygame.font.Font(None, self.font_size).render(self.text, True, self.font_colour)
    
        self.data = {
            "surface": self.surface,
            "pos": [self.x, self.y],
            "tag": "",
            "state": ""
        }

        return self.data

class InputboxWrapper:
    def __init__(self, data, width, height):
        self.data = data
        self.width = width
        self.height = height

    def splitList(self, l):
        x = []
        y = []
        z = 0

        for item in l:
            if z < 2:
                x.append(item)
                z += 1
            else:
                y.append(x)
                x = []
                x.append(item)
                z = 1
        y.append(x)
        
        return y

    def update(self, event, keydown):
        self.surface = pygame.Surface((self.width, self.height))
        self.subSurfaces = []
        self.subSurfacesPos = []
        self.subSurfacesRaw = []
        self.subSurfacesData = []

        self.surface.fill((200,200,200))

        for subSurface in self.data:
            self.subSurfacesRaw.append(subSurface.update(event=event, keydown=keydown))
        
        for tempSubsurface in self.subSurfacesRaw:
            self.subSurfaces.append(tempSubsurface["surface"])
            self.subSurfacesPos.append(tempSubsurface["pos"])

            self.subSurfacesData.append(tempSubsurface["tag"])
            self.subSurfacesData.append(tempSubsurface["state"])

        self.subSurfacesData = self.splitList(self.subSurfacesData)

        for i, sub in enumerate(self.subSurfaces):
            self.surface.blit(sub, (self.subSurfacesPos[i][0],self.subSurfacesPos[i][1]))

        self.finalSurface = {
            "surface": self.surface,
            "state": self.subSurfacesData,
        }

        return self.finalSurface

class Listener:
    def __init__(self, return_code):
        self.return_code = return_code
    def update(self, event):
        if event.key == pygame.K_RETURN:
            return "submit"
        elif event.key == pygame.K_RIGHT:
            return "next"
        elif event.key == pygame.K_LEFT:
            return "prev"

pygame.init()
pygame.key.set_repeat(200)
clock = pygame.time.Clock()

win = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Cell Image Sorter")

mainPath = os.path.dirname(os.path.realpath(__file__))
rawImagesPath = mainPath + "/Raw Images"
processedImagePath = mainPath + "/Processed Images"

dirList = os.listdir(path=rawImagesPath) 
imgTypes = [".png", ".jpeg", ".jpg"]
imgDirList = []

for item in dirList:
    for image_type in imgTypes:
        if image_type in item:
            if not "health-" in item:
                imgDirList.append(item)

run = True
reRenderImage = True
imageIndex = 0

sortingAttributes = InputboxWrapper(data=[
# TextBox(x=25, y=100, text="Cell Health"), 
# InputBox(x=25, y=200, tag="health"), 
TextBox(x=25, y=100, text="Bacteria Type"), 
InputBox(x=25, y=200, tag="bacteria", active=True)], width=1280, height=720)

submitListener = Listener(return_code="submit")

listenerQueue = [submitListener]

while run:
    renderQueue = []
    stateQueue = []
    logicQueue = []
    listenerResponseQueue = []
    win.fill((255,255,255))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.KEYDOWN:
            sortingAttributes.update(event=event, keydown=True)

            for i in listenerQueue:
                listenerResponseQueue.append(i.update(event=event))

        ## Object Rendering ##

        rawBlitData = sortingAttributes.update(event=event, keydown=False)

        renderQueue.append(rawBlitData["surface"])
        logicQueue.append(rawBlitData["state"])

        for surface in renderQueue:
            win.blit(surface, (0,0))

        ## Listerner keywords ##

        if "submit" in listenerResponseQueue:
            tags = []
            tagsData = []
            attString = ""
            print(logicQueue[0])
            for att in logicQueue[0]:
                if att[0] not in tags:
                    tags.append(att[0])
                    tagsData.append(att[1])

            for x in range(len(tags)):
                attString = attString + tags[x] + "-" + tagsData[x] + "-"  

            copyfile(f"{rawImagesPath}/{imgDirList[imageIndex]}", f"{processedImagePath}/{attString}{imgDirList[imageIndex]}")      

            imageIndex += 1
            reRenderImage = True
        
        if "next" in listenerResponseQueue:
            if len(imgDirList) != imageIndex + 1:
                imageIndex += 1
                reRenderImage = True

        if "prev" in listenerResponseQueue and imageIndex > 0:
            imageIndex += -1
            reRenderImage = True

        if len(imgDirList) > 0:
            if reRenderImage:
                currentImage = pygame.image.load(f"{rawImagesPath}/{imgDirList[imageIndex]}")
                scaledCurrentImage = pygame.transform.scale(currentImage, (768 , 432))
                reRenderImage = False
            else:
                win.blit(scaledCurrentImage, (430, 80))

        pygame.display.update()
