import pickle
import pygame
pygame.init()
def img2ls(img):
    return [pygame.image.tostring(img,"RGBA"),img.get_size()]
with open("logo.pdb","wb") as file:
    dic = {"logo.png":img2ls(pygame.image.load("logo.png")),
           "logo2.png":img2ls(pygame.image.load("logo2.png"))}
    pickle.dump(dic,file)
with open("main.pdb","wb") as file:
    dic = {}
    print("正在打包:  " + "4.png")
    dic["4.png"] = img2ls(pygame.image.load("4.png"))
    print("正在打包:  " + "5.png")
    dic["5.png"] = img2ls(pygame.image.load("5.png"))
    print("正在打包:  " + "6.png")
    dic["6.png"] = img2ls(pygame.image.load("6.png"))
    print("正在打包:  " + "lock.png")
    dic["lock.png"] = img2ls(pygame.image.load("lock.png"))
    print("正在打包:  " + "夜空中最亮的星.ogg")
    dic["夜空中最亮的星.ogg"] = pygame.mixer.Sound("夜空中最亮的星.ogg").get_raw()
    with open("星座/星座.txt",encoding="UTF-8") as f:
        print("正在打包:  " + "星座/星座.txt")
        dic["星座/星座.txt"] = f.read()
    lines = dic["星座/星座.txt"].strip("\n").split("\n")
    for i in lines:
        name = i.strip(" ").split(" ")[0]
        temp = [j.split(",") for j in i.strip(" ").split(" ")[1:]]
        temp = [[int(j[0]),int(j[1]),int(j[2])] for j in temp]
        k = 0
        for j in temp:
            if j[2] == 1:
                k += 1
                print("正在打包:  " + f"星座/{name}/{k}.jpg")
                try:
                    dic[f"星座/{name}/{k}.jpg"] = img2ls(pygame.image.load(f"星座/{name}/{k}.jpg"))
                except:
                    print(f"警告:无法打包'星座/{name}/{k}.jpg',星图将锁定这颗星")
    pickle.dump(dic,file)
