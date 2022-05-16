#Developed by u/Jumping_Pig, Steam: Piggy
import os
import ctypes
from PIL import Image, ImageOps
from numpy import asarray
import cv2 as cv
import easyocr

debug = False


os.chdir(os.path.split(__file__)[0])

#custom errors
def throw(e, s):
    try: f.close()
    finally:
        os.remove(os.path.join(os.getcwd(), 'temp.txt'))
        ctypes.windll.user32.MessageBoxW(0, e, s, 0)
        exit()



#read the screenshot directory location
configFile = open(r'config.txt', 'r')
scDirectory = configFile.readline().split('=')[1].strip()

#if first stat for the file then don't preface with newline
first = True
#if no files were worked on
noFiles = True

#reset the temporary stats file, or create it if not there
f = open('temp.txt', 'w')
f.write("")
f.close()

#if the completed screenshot folder DNE, create it
if(not os.path.exists(os.path.join(scDirectory, 'Completed'))): os.mkdir(os.path.join(scDirectory, 'Completed'))

#sort the directory for ordering screenshots by timestamp
dirList = sorted(os.listdir(scDirectory))

#create easyOCR reader object, for english.
reader = easyocr.Reader(['en'])

#for each file in the directory...
for i in range(0, len(dirList), 2):
    #if file 1&2 isn't jpg... or file 3&4... etc. then skip
    if(not dirList[i].endswith('.jpg') and not dirList[i+1].endswith('.jpg')): continue
    #get summary screenshot path
    summary = os.path.join(scDirectory, dirList[i])
    
    #black background, white text
    bwSummary = cv.cvtColor(cv.imread(summary), cv.COLOR_RGB2GRAY)
    #black text on white background is best for OCR
    bwSummary = ImageOps.invert(Image.fromarray(bwSummary))
    
    #determine the pixel locations based on ratio of resolutions (16:9 aspect ratio ONLY)
    w, h = bwSummary.size
    xRatio = w/1920
    yRatio = h/1080
    xOffset = xRatio*145 #1920x1080 145pixel offset to capture K/A/N values and damage values
    xStart1 = xRatio*131 #^ 131 pixel start x position for Player 1 ^
    xStart2 = xRatio*731 #^ 731 pixel start x position for self ^
    xStart3 = xRatio*1331 #^ 1331 pixel start x position for Player 2 ^
    xEnd1 = xStart1+xOffset
    xEnd2 = xStart2+xOffset
    xEnd3 = xStart3+xOffset
    yOffset = yRatio*35 # ^ 35 pixel start y position for K/A/N values
    yNext = yRatio*75 # ^ 75 pixel offset between K/A/N values and damage values
    yStartKDA = yRatio*400 # ^ 400 pixel start y position for K/A/N values
    yEndKDA = yStartKDA+yOffset
    yStartDmg = yStartKDA+yNext
    yEndDmg = yStartDmg+yOffset

    #create list for K/A/N crops ordered as Player 1, Self, Player 2
    KDA = list()
    KDA.append(bwSummary.crop((xStart1, yStartKDA, xEnd1, yEndKDA)))
    KDA.append(bwSummary.crop((xStart2, yStartKDA, xEnd2, yEndKDA)))
    KDA.append(bwSummary.crop((xStart3, yStartKDA, xEnd3, yEndKDA)))
    
    #create list for damage crops ordered as Player 1, Self, Player 2
    dmg = list()
    dmg.append(bwSummary.crop((xStart1, yStartDmg, xEnd1, yEndDmg)))
    dmg.append(bwSummary.crop((xStart2, yStartDmg, xEnd2, yEndDmg)))
    dmg.append(bwSummary.crop((xStart3, yStartDmg, xEnd3, yEndDmg)))

    #create list for placement crop samples (many different game factors can alter the positioning of this)
    placement = list()
    #each crop is shifted right 20 pixels in 1920x1080 format
    placement.append(bwSummary.crop((xRatio*1450, yRatio*125, xRatio*1580, yRatio*180)))
    placement.append(bwSummary.crop((xRatio*1470, yRatio*125, xRatio*1580, yRatio*180)))
    placement.append(bwSummary.crop((xRatio*1490, yRatio*125, xRatio*1580, yRatio*180)))
    
    #create list for total team kill crop samples (see above)
    totalKill = list()
    #pixel 1920x1080 shifts
    totalKill.append(bwSummary.crop((xRatio*1720, yRatio*125, xRatio*1825, yRatio*180)))
    totalKill.append(bwSummary.crop((xRatio*1750, yRatio*125, xRatio*1825, yRatio*180)))
    totalKill.append(bwSummary.crop((xRatio*1760, yRatio*125, xRatio*1825, yRatio*180)))



    #open temporary stats file for transfer to Excel
    f = open('temp.txt', 'a')
    
    #write the K/A/N as without / and each per line
    for x in KDA:
        text = reader.readtext(asarray(x), allowlist=r'/0123456789') #only read digits and /
        try: text = text[0][1]
        except: throw("K/A/N reading error", "OCR Error")
        if(debug): 
            print(text)
            x.show()
        #if OCR did not read 2 slashes, try to fix it
        if(text.count('/') != 2):
            if(text.count('/') == 0 and len(text) == 3): #read as ###
                text = text[0]+'/'+text[1]+'/'+text[2]
                    
            elif text.count('/') == 1: #had mirsread a single /
                if(len(text) == 5): text = text[0]+'/'+text[2]+'/'+text[4] #has read as #/#_# or #_#/#
                elif(len(text) == 4): #did not read a /
                    if(text[1] == '/'): text = text[:3]+'/'+text[3] #read as #/##
                    elif(text[2] == '/'): text = text[0]+'/'+text[1:] #read as ##/#
                else: throw("Missing one \'/ \'") #this is extreme edge case where misread a / and is not single digits. generally if more than #/#/# then OCR has relative data to work with
            
            else: 
                #experimental...
                text = text[0]+text[1:len(text)-1].replace('1', '/')+text[len(text)-1]
                if(debug): print(text)
                #idk what to do, so just throw an error
                if(text.count('/')!=2): throw("EXPERIMENTAL: K/A/N not enough \' / \'", "OCR/Fix Error, EXPERIMENTAL")      
           
        #after fixing the input, replace / with newlines for writing
        if(debug): print("Fixed Text: "+text)
        text = text.replace('/', '\n')
        #special case of first write to file
        if first:
            f.write(text)
            first = False
        else: f.write('\n'+text)
        
    #write damage to file
    for x in dmg:
        text = reader.readtext(asarray(x), allowlist=r'0123456789') #only read digits
        try: text = text[0][1] #if OCR does not pick up any characters, assume it is 0 damage (this has happened in cases of 0 damage)
        except: text = '0'
        f.write('\n'+text)
        
        
    #comparison of confidences
    confidence = [[None,None,0]] #format of readtext
    for x in placement:
        text = reader.readtext(asarray(x), allowlist=r'0123456789#') #only read in digits and '#'
        if(len(text)==0): continue #if we couldn't read the crop then try another
        if(text[0][2] > confidence[0][2]): confidence = text #keep track of the best reading
        
    if(confidence[0][1] is None): throw("Placement misreading", "OCR Error")
    if(confidence[0][1][0]=='#'): text = confidence[0][1][1:] #take digits after the '#' if read 
    else: text = confidence[0][1]
    f.write('\n'+text)
    
    #comparison of confidences
    confidence = [[None, None, 0]]
    for x in totalKill:
        text = reader.readtext(asarray(x), allowlist=r'0123456789') #only read in digits
        if(len(text)==0): continue #if we couldn't read the crop then try another
        if(text[0][2] > confidence[0][2]): confidence = text #keep track of the best reading
    
    if(confidence[0][1] is None): throw("Total Kill misreading", "OCR Error")
    text = confidence[0][1]
    f.write('\n'+text)
    
    #attempt post-game summary photo
    results = os.path.join(scDirectory, dirList[i+1])
    #this screen uses different colors and as such rgb to gray changes can have issues. use original photo and an inverted
    standard = Image.fromarray(cv.imread(results))
    bw2 = ImageOps.invert(standard)
    
    #create list for rp crops
    rp = list()
    #each crop is different colorations
    rp.append(standard.crop((xRatio*970, yRatio*644, xRatio*1117, yRatio*700)))
    rp.append(bw2.crop((xRatio*970, yRatio*644, xRatio*1117, yRatio*700)))
    
    #create list for participation crops
    participation = list()
    #each crop is different colorations
    participation.append(standard.crop((xRatio*775, yRatio*470, xRatio*930, yRatio*500)))
    participation.append(bw2.crop((xRatio*775, yRatio*490, xRatio*930, yRatio*520)))
    participation.append(bw2.crop((xRatio*775, yRatio*510, xRatio*930, yRatio*540)))
    
    
    #comparison of confidences
    confidence = [[None, None, 0]]
    for x in rp:
        text = reader.readtext(asarray(x), allowlist=r'-+0123456789') #only read in digits and - or +
        if(len(text)==0): continue #if we couldn't read the crop then try another
        if(text[0][2] > confidence[0][2]): confidence = text #keep track of the best reading
    
    if(confidence[0][1] is None): throw("RP misreading", "OCR Error")
    text = confidence[0][1]
    if(text.isdigit()): text = '-'+text #no + or - sign, set a - sign because this is misread often (+ doesn't have issues so far)
    f.write('\n'+text)
    
    #comparison of confidences
    confidence = [[None, None, 0]]
    for x in participation:
        text = reader.readtext(asarray(x), allowlist=r'Particpon:0123456789') #only read Participation:##
        if(len(text)==0): continue #if we couldn't read the crop then try another
        if(debug):
            x.show()
            print(text[0][1])
        if(text[0][2] > confidence[0][2]): confidence = text #keep track of the best reading
    
    if(confidence[0][1] is None): throw("Participation misreading", "OCR Error")
    text = confidence[0][1]
    f.write('\n'+text[14:]) #write the number after "Participation:" 
    
    #move the files to the "Completed" folder
    if(not debug): os.rename(summary, os.path.join(scDirectory, os.path.join('Completed', dirList[i])))
    if(not debug): os.rename(results, os.path.join(scDirectory, os.path.join('Completed', dirList[i+1])))
    
    noFiles = False
    #Continue onto the next pair of photos available
if(noFiles): throw("No Image Pairs Found In: "+scDirectory, "No Images Found")