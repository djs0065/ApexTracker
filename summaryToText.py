#Developed by u/Jumping_Pig, Steam: Piggy
import os
from PIL import Image, ImageOps
from numpy import asarray
import cv2 as cv
import easyocr


configFile = open(r'config.txt', 'r')
scDirectory = configFile.readline().split('=')[1].strip()
first = True
f = open('temp.txt', 'w')
f.write("")
f.close()
if(not os.path.exists(os.path.join(scDirectory, 'Completed'))):
    os.mkdir(os.path.join(scDirectory, 'Completed'))
dirList = sorted(os.listdir(scDirectory))
for i in range(len(dirList)):
    if(len(dirList) < 3): exit()
    if(not dirList[i].endswith('.jpg') and not dirList[i+1].endswith('.jpg')):
        continue
    sc = os.path.join(scDirectory, dirList[i])
    gray = cv.imread(sc)
    gray = cv.cvtColor(gray, cv.COLOR_RGB2GRAY)
    im = Image.fromarray(gray)
    im = ImageOps.invert(im)
    reader = easyocr.Reader(['en'])
    w, h = im.size
    xRatio = w/1920
    yRatio = h/1080
    xOffset = xRatio*145
    xStart1 = xRatio*131
    xStart2 = xRatio*731
    xStart3 = xRatio*1331
    xEnd1 = xStart1+xOffset
    xEnd2 = xStart2+xOffset
    xEnd3 = xStart3+xOffset

    yOffset = yRatio*35
    yNext = yRatio*75
    yStartKDA = yRatio*400
    yEndKDA = yStartKDA+yOffset
    yStartDmg = yStartKDA+yNext
    yEndDmg = yStartDmg+yOffset


    KDA = list()
    KDA.append(im.crop((xStart1, yStartKDA, xEnd1, yEndKDA)))
    KDA.append(im.crop((xStart2, yStartKDA, xEnd2, yEndKDA)))
    KDA.append(im.crop((xStart3, yStartKDA, xEnd3, yEndKDA)))

    dmg = list()
    dmg.append(im.crop((xStart1, yStartDmg, xEnd1, yEndDmg)))
    dmg.append(im.crop((xStart2, yStartDmg, xEnd2, yEndDmg)))
    dmg.append(im.crop((xStart3, yStartDmg, xEnd3, yEndDmg)))


    placement = im.crop((xRatio*1450, yRatio*125, xRatio*1580, yRatio*180))
    placement2 = im.crop((xRatio*1470, yRatio*125, xRatio*1580, yRatio*180))
    placement3 = im.crop((xRatio*1490, yRatio*125, xRatio*1580, yRatio*180))
#placement.show()
#placement2.show()
#placement3.show()
    totalKill = im.crop((xRatio*1720, yRatio*125, xRatio*1825, yRatio*180))
    totalKill2 = im.crop((xRatio*1760, yRatio*125, xRatio*1825, yRatio*180))
#totalKill.show()
#totalKill2.show()



    f = open('temp.txt', 'a')
    for x in KDA:
        text = reader.readtext(asarray(x), allowlist=r'/0123456789')
#print(text)
        text = text[0][1]
        if text.count('/') == 1: #had mirsread a /
            if(len(text) == 5): #has read / as _
                text = text[0]+'/'+text[2]+'/'+text[4] #has read as #/#_# or #_#/#
            elif(len(text) == 4): #did not read /
                if(text[1] == '/'): #read as #/##
                    text = text[:3]+'/'+text[3]
                elif(text[2] == '/'): #read as ##/#
                    text = text[0]+'/'+text[1:]
            elif(len(text) == 3): #did not read ANY /
                text = text[0]+'/'+text[1]+'/'+text[2]
            else: #this is extreme edge case where misread a / and is not single digits
                print("Double Digit Error 1")
                break
        elif(text.count('/') == 0): #had misread both /
            if(len(text) == 3): #read as ###
                text = text[0]+'/'+text[1]+'/'+text[2]
            else: #no idea what it should be, has double digits somewhere
                print("Double Digit Error 2")
                break
        elif(text.count('/') > 2): #has too many /, digit is unknown.
            print(str(text.count('/'))+' Slash Error')
        text = text.replace('/', '\n')
        if first:
            f.write(text)
            first = False
        else:
            f.write('\n'+text)
    for x in dmg:
        text = reader.readtext(asarray(x), allowlist=r'0123456789')
#print(text)
        if len(text) == 0: #could not read damage.... no idea why, only when damage is 0..
            text = '0'
        else: text = text[0][1]
        if first:
            f.write(text)
            first = False
        else:
            f.write('\n'+text)
    #comparison of confidence
    text = reader.readtext(asarray(placement), allowlist=r'0123456789#')
    text2 = reader.readtext(asarray(placement2), allowlist=r'0123456789#')
    text3 = reader.readtext(asarray(placement3), allowlist=r'0123456789#')
#if(len(text)!=0): print('placement1: '+str(text[0][1])+'|'+str(text[0][2]))
    if(len(text2)!=0): 
#print('placement2: '+str(text2[0][1])+'|'+str(text2[0][2]))
        if(len(text)==0): text = text2
#if(len(text3)!=0): print('placement3: '+str(text3[0][1])+'|'+str(text3[0][2]))
    if(len(text)!=0 and len(text2)!=0 and text2[0][2] > text[0][2]): text = text2
    if(len(text)!=0 and len(text3)!=0 and text3[0][2] > text[0][2]): text = text3
    if(text[0][1][0]=='#'): text = text[0][1][1:] #take digits after the '#' (first) character
    else: text = text[0][1]
    f.write('\n'+text)
    #comparison of confidence
    text = reader.readtext(asarray(totalKill), allowlist=r'0123456789')
    text2 = reader.readtext(asarray(totalKill2), allowlist=r'0123456789')
#if(len(text)!=0): print('TK1: '+str(text[0][1])+'|'+str(text[0][2]))
    if(len(text2)!=0):
#print('TK2: '+str(text2[0][1])+'|'+str(text2[0][2]))
        if(len(text)==0): text = text2
    if(len(text)!=0 and len(text2)!=0 and text2[0][2] > text[0][2]): text = text2
    text = text[0][1].strip()
    f.write('\n'+text)
    try:
        sc2 = os.path.join(scDirectory, dirList[i+1])
        gray2 = cv.imread(sc2)
        im2 = Image.fromarray(gray2)
        im3 = ImageOps.invert(im2)
        #comparison of confidence
        rp = im2.crop((xRatio*970, yRatio*644, xRatio*1117, yRatio*700))
        rp2 = im3.crop((xRatio*970, yRatio*644, xRatio*1117, yRatio*700))
        part = im2.crop((xRatio*775, yRatio*470, xRatio*930, yRatio*500))
        part2 = im2.crop((xRatio*775, yRatio*490, xRatio*930, yRatio*520))
#part.show()
#part2.show()
#rp.show()
#rp2.show()
        text = reader.readtext(asarray(rp), allowlist=r'-+0123456789')
        text2 = reader.readtext(asarray(rp2), allowlist=r'-+0123456789')
#if(len(text)!=0): print('rp1: '+str(text[0][1])+'|'+str(text[0][2]))
        if(len(text2)!=0): 
#print('rp2: '+str(text2[0][1])+'|'+str(text2[0][2]))
            if(len(text)==0): text = text2
        if(len(text)!=0 and len(text2)!=0 and text2[0][2] > text[0][2]): text = text2
        text = text[0][1]
        if(text.isdigit()): #no + or - sign
            text = '-'+text #most often can not read a '-'
        f.write('\n'+text)
        text = reader.readtext(asarray(part), allowlist=r'Particpon:0123456789')
        text2 = reader.readtext(asarray(part2), allowlist=r'Particpon:0123456789')
        if(len(text)!=0 and len(text2)!=0):
            if(text2[0][2] > text[0][2]): text = text2
#print('part: '+str(text[0][1])+'|'+str(text[0][2]))
        text = text[0][1]
        f.write('\n'+text[14:])
    except Exception as e:
        print(e)
        os.rename(sc, os.path.join(scDirectory, os.path.join('Completed', dirList[i])))
        break
    else:
        os.rename(sc, os.path.join(scDirectory, os.path.join('Completed', dirList[i])))
        os.rename(sc2, os.path.join(scDirectory, os.path.join('Completed', dirList[i+1])))
        break
