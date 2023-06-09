import pygame
import os,sys
import threading
import random
pygame.init()
def init():
    global imgls,angls,bgm,star
    star = pygame.image.load("star.png")
    bgm = pygame.mixer.Sound("夜空中最亮的星.ogg")
    imgls = {}
    angls = {}
    with open("星座/星座.txt",encoding="UTF-8") as file:
        cont = file.read()
    lines = cont.strip("\n").split("\n")
    
    for i in lines:
        name,num = i.strip(" ").split(" ")[0].split(",")
        num = int(num)
        imgls[name] = []
        angls[name] = []
        temp = [j.split(",") for j in i.strip(" ").split(" ")[1:]]
        temp = [[int(j[0]),int(j[1])] for j in temp]
        for i in range(num):
            imgls[name].append([pygame.image.load(f"星座/{name}/{i+1}.jpg"),temp[i][0],temp[i][1]])
            angls[name].append(random.randint(0,359))
screen = pygame.display.set_mode()
keepgoing = True
first = True
alpha = 0
asp = 3
logo = pygame.image.load("logo.png")
clock = pygame.time.Clock()
initd = threading.Thread(target=init)
logoloc = [(screen.get_size()[0]-logo.get_size()[0])/2,(screen.get_size()[1]-logo.get_size()[1])/2]
while True:
    screen.fill([0,0,0])
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
    if alpha >= 253:
        if first:
            asp = 0
            initd.start()
            first = False
        if not initd.is_alive():
            asp = -3
            while alpha > 2:
                screen.fill([0,0,0])
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            pygame.quit()
                            sys.exit()
                alpha += asp
                logo.set_alpha(alpha)
                screen.blit(logo,logoloc)
                pygame.display.update()
                clock.tick(60)
            break
    alpha += asp
    logo.set_alpha(alpha)
    screen.blit(logo,logoloc)
    pygame.display.update()
    clock.tick(60)
del init,first,alpha,asp,logo,initd,logoloc

speed = 0
kdl = kdr = False
showing = False
select = False
bgm.play(-1)
while keepgoing:
    screen.fill([0,0,0])
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                keepgoing = False
            elif event.key == pygame.K_LEFT:
                kdl = True
            elif event.key == pygame.K_RIGHT:
                kdr = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                kdl = False
            elif event.key == pygame.K_RIGHT:
                kdr = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if select:
                showing = True
                image = pygame.transform.smoothscale(select,screen.get_size())
            if showing:
                showing = False
                kg = True
                kdl = kdr = False
                alpha = 0
                while kg:
                    screen.fill([0,0,0])
                    s = screen.convert_alpha()
                    for event in pygame.event.get():
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_ESCAPE:
                                kg = False
                                keepgoing = False
                                alpha = -3
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            kg = False
                    if alpha < 253:
                        alpha += 3
                    else:
                        alpha = 255
                    speed += kdl
                    speed -= kdr
                    speed = round(speed*0.95,5)
                    for i in imgls:
                        for j in range(len(imgls[i])):
                            img = pygame.transform.rotate(star,angls[i][j])
                            img.set_alpha(255 - alpha)
                            angls[i][j] = (angls[i][j] + 1) % 360
                            rect = img.get_rect()
                            imgls[i][j][1] += speed
                            rect.center = imgls[i][j][1:]
                            s.blit(img,rect)
                        pygame.draw.lines(s,[255,255,255,255 - alpha],False,[k[1:] for k in imgls[i]],3)
                    image.set_alpha(alpha)
                    s.blit(image,[0,0])
                    screen.blit(s,[0,0])
                    pygame.display.update()
                    clock.tick(60)
                while alpha > 0:
                    screen.fill([0,0,0])
                    s = screen.convert_alpha()
                    for event in pygame.event.get():
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_ESCAPE:
                                keepgoing = False
                                alpha = 3
                    alpha -= 3
                    speed += kdl
                    speed -= kdr
                    speed = round(speed*0.95,5)
                    for i in imgls:
                        for j in range(len(imgls[i])):
                            img = pygame.transform.rotate(star,angls[i][j])
                            img.set_alpha(255 - alpha)
                            angls[i][j] = (angls[i][j] + 1) % 360
                            rect = img.get_rect()
                            imgls[i][j][1] += speed
                            rect.center = imgls[i][j][1:]
                            s.blit(img,rect)
                        pygame.draw.lines(s,[255,255,255,255 - alpha],False,[k[1:] for k in imgls[i]],3)
                    image.set_alpha(alpha)
                    s.blit(image,[0,0])
                    screen.blit(s,[0,0])
                    pygame.display.update()
                    clock.tick(60)
    speed += kdl
    speed -= kdr
    speed = round(speed*0.95,5)
    mouse = pygame.mouse.get_pos()
    select = False
    for i in imgls:
        in_screen = False
        for j in range(len(imgls[i])):
            img = pygame.transform.rotate(star,angls[i][j])
            angls[i][j] = (angls[i][j] + 1) % 360
            rect = img.get_rect()
            imgls[i][j][1] += speed
            if imgls[i][j][1] > 0 and imgls[i][j][1] < screen.get_size()[0]:
                in_screen = True
            rect.center = imgls[i][j][1:]
            if rect.collidepoint(mouse):
                img = pygame.transform.scale2x(img)
                rect = img.get_rect()
                rect.center = imgls[i][j][1:]
                select = imgls[i][j][0]
            screen.blit(img,rect)
        pygame.draw.lines(screen,[255,255,255],False,[k[1:] for k in imgls[i]],3)
        if not in_screen:
            for j in imgls[i]:
                if j[1] > screen.get_size()[0]:
                    j[1] -= screen.get_size()[0] * 2
                elif j[1] < 0:
                    j[1] += screen.get_size()[0] * 2
    pygame.display.update()
    clock.tick(60)
pygame.quit()
