import pygame
import os,sys
import threading
import random
import pickle
pygame.init()
def ls2img(index,dic):
    return pygame.image.fromstring(dic[index][0],dic[index][1],"RGBA").convert_alpha()
def init():
    global imgls,angls,sidls,bgm,star
    with open("main.pdb","rb") as file:
        tmp = pickle.load(file)
    star4 = ls2img("4.png",tmp)
    star5 = ls2img("5.png",tmp)
    star6 = ls2img("6.png",tmp)
    star = [star4,star5,star6]
    bgm = pygame.mixer.Sound(tmp["夜空中最亮的星.ogg"])
    imgls = {}
    angls = {}
    sidls = {}
    cont = tmp["星座/星座.txt"]
    lines = cont.strip("\n").split("\n")
    screensize = screen.get_size()
    for i in lines:
        name = i.strip(" ").split(" ")[0]
        imgls[name] = []
        angls[name] = []
        temp = [j.split(",") for j in i.strip(" ").split(" ")[1:]]
        temp = [[int(int(j[0])/1536*screensize[0]),int(int(j[1])/864*screensize[1]),int(j[2])] for j in temp]
        k = 0
        for j in temp:
            if j[2] == 1:
                k += 1
                select = ls2img(f"星座/{name}/{k}.jpg",tmp).convert()
                if screen.get_size()[0] / select.get_size()[0] > screen.get_size()[1] / select.get_size()[1]:
                    key = screen.get_size()[1] / select.get_size()[1]
                else:
                    key = screen.get_size()[0] / select.get_size()[0]
                image = pygame.transform.smoothscale(select,[select.get_size()[0]*key,select.get_size()[1]*key])
                imgls[name].append([image,j[0],j[1],random.choice(star),random.choice([1,-1])])
                angls[name].append(random.randint(0,359))
        sidls[name] = [j[:-1] for j in temp]
screen = pygame.display.set_mode([0,0],pygame.DOUBLEBUF|pygame.FULLSCREEN|pygame.HWSURFACE,8)
pygame.event.set_allowed([pygame.KEYDOWN,pygame.KEYUP,pygame.MOUSEBUTTONDOWN])
keepgoing = True
first = True
alpha = 0
asp = 3
with open("logo.pdb","rb") as file:
    temp = pickle.load(file)
logo2 = ls2img("logo2.png",temp).convert_alpha()
logo = ls2img("logo.png",temp).convert_alpha()
clock = pygame.time.Clock()
initd = threading.Thread(target=init)
logo2loc = [(screen.get_size()[0]-logo2.get_size()[0])/2,(screen.get_size()[1]+logo.get_size()[1])/2]
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
                logo2.set_alpha(alpha)
                screen.blit(logo,logoloc)
                screen.blit(logo2,logo2loc)
                pygame.display.update()
                clock.tick(60)
            break
    alpha += asp
    logo.set_alpha(alpha)
    logo2.set_alpha(alpha)
    screen.blit(logo,logoloc)
    screen.blit(logo2,logo2loc)
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
                loc = [0,0]
                loc[0] = abs(screen.get_size()[0] - select.get_size()[0]) / 2
                loc[1] = abs(screen.get_size()[1] - select.get_size()[1]) / 2
                image = pygame.transform.smoothscale(select,select.get_size())
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
                            img = pygame.transform.rotate(imgls[i][j][3],angls[i][j])
                            img.set_alpha(255 - alpha)
                            angls[i][j] = (angls[i][j] + imgls[i][j][4]) % 360
                            rect = img.get_rect()
                            imgls[i][j][1] += speed
                            rect.center = imgls[i][j][1:3]
                            s.blit(img,rect)
                        for j in sidls[i]:
                            j[0] += speed
                        pygame.draw.lines(s,[255,255,255,255 - alpha],False,sidls[i],3)
                    image.set_alpha(alpha)
                    s.blit(image,loc)
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
                            img = pygame.transform.rotate(imgls[i][j][3],angls[i][j])
                            img.set_alpha(255 - alpha)
                            angls[i][j] = (angls[i][j] + imgls[i][j][4]) % 360
                            rect = img.get_rect()
                            imgls[i][j][1] += speed
                            rect.center = imgls[i][j][1:3]
                            s.blit(img,rect)
                        for j in sidls[i]:
                            j[0] += speed
                        pygame.draw.lines(s,[255,255,255,255 - alpha],False,sidls[i],3)
                    image.set_alpha(alpha)
                    s.blit(image,loc)
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
            img = pygame.transform.rotate(imgls[i][j][3],angls[i][j])
            angls[i][j] = (angls[i][j] + imgls[i][j][4]) % 360
            rect = img.get_rect()
            imgls[i][j][1] += speed
            if imgls[i][j][1] > 0 and imgls[i][j][1] < screen.get_size()[0]:
                in_screen = True
            rect.center = imgls[i][j][1:3]
            if rect.collidepoint(mouse):
                img = pygame.transform.scale2x(img)
                rect = img.get_rect()
                rect.center = imgls[i][j][1:3]
                select = imgls[i][j][0]
            screen.blit(img,rect)
        for j in sidls[i]:
            j[0] += speed
        pygame.draw.lines(screen,[255,255,255],False,sidls[i],3)
        if not in_screen:
            for j in imgls[i]:
                if j[1] > screen.get_size()[0]:
                    j[1] -= screen.get_size()[0] * 2
                elif j[1] < 0:
                    j[1] += screen.get_size()[0] * 2
            for j in sidls[i]:
                if j[0] > screen.get_size()[0]:
                    j[0] -= screen.get_size()[0] * 2
                elif j[0] < 0:
                    j[0] += screen.get_size()[0] * 2
    pygame.display.update()
    clock.tick(60)
pygame.quit()
