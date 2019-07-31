import random
import pygame
import sys
from pygame.locals import *
FPS=30   #Frames per second, the general speed of program
win_width=640
win_height=480
revelspeed=8 #speed box sliding revels and covers
boxsize=40 # size of box height and width in pixels
gapsize=10 #size of gap between boxes in pixels
col=10
row=7
assert (row * col)%2 == 0, 'Board needs to ave an even number of boxes for pairs of mathches.'
xmargin=int((win_width-(col*(boxsize+gapsize)))/2)
ymargin=int((win_height-(row*(boxsize+gapsize)))/2)
gray=(100,100,100)
navyblue=(60,60,100)
white=(255,255,255)
red=(255,0,0)
green=(0,255,0)
blue=(0,0,255)
yellow=(255,255,0)
orange=(255,128,0)
purple=(255,0,255)
cyan=(0,255,255)
bgcolor=navyblue
lightbgcolor=gray
boxcolor=white
highlightcolor=blue
DONUT='donut'
SQUARE='square'
DIAMOND='diamond'
LINES='lines'
OVAL='oval'
allcolors=(red,green,blue,yellow,orange,purple,cyan)
allshapes=(DONUT,SQUARE,DIAMOND,LINES,OVAL)
assert len(allcolors)*len(allshapes)*2 >=col*row,"Board is too big for the number of shapes/colors defined."
def main():
    global FPSCLOCK,Displaysurf
    pygame.init()
    FPSCLOCK=pygame.time.Clock()
    Displaysurf=pygame.display.set_mode((win_width,win_height))
    mousex=0
    mousey=0
    pygame.display.set_caption('Memory Game')
    mainBoard = getRandomsizedBoard()
    revealedBoxes=generateRevealedBoxesData(False)
    firstSelection=None
    Displaysurf.fill(bgcolor)
    startGameAnimation(mainBoard)
    while True:
        mouseClicked=False

        Displaysurf.fill(bgcolor)
        drawBoard(mainBoard,revealedBoxes)

        for event in pygame.event.get():
            if event.type == QUIT or (event.type==KEYUP and event.key==K_SPACE):
                pygame.quit()
                sys.exit()
            elif event.type== MOUSEMOTION:
                mousex,mousey=event.pos
            elif event.type==MOUSEBUTTONUP:
                mousex,mousey=event.pos
                mouseClicked=True

        boxx,boxy=getBoxAtPixel(mousex,mousey)
        if boxx !=None and boxy != None:
            if not revealedBoxes[boxx][boxy]:
                drawHighlightBox(boxx,boxy)
            if not revealedBoxes[boxx][boxy] and mouseClicked:
                revealBoxesAnimation(mainBoard,[(boxx,boxy)])
                revealedBoxes[boxx][boxy]=True
                if firstSelection==None:
                    firstSelection=(boxx,boxy)
                else:
                    icon1shape,icon1color=getShapeAndColor(mainBoard,firstSelection[0],firstSelection[1])
                    icon2shape,icon2color=getShapeAndColor(mainBoard,boxx,boxy)
                    if icon1shape!=icon2shape or icon1color != icon2color:
                        pygame.time.wait(1000)
                        coverBoxesAnimation(mainBoard,[(firstSelection[0],firstSelection[1]),(boxx,boxy)])
                        revealedBoxes[firstSelection[0]][firstSelection[1]]=False
                        revealedBoxes[boxx][boxy]=False
                    elif hasWon(revealedBoxes):
                        gameWonAnimation(mainBoard)
                        pygame.time.wait(2000)
                        mainBoard=getRandomsizedBoard()
                        revealedBoxes=generateRevealedBoxesData(False)
                        drawBoard(mainBoard,revealedBoxes)
                        pygame.display.update()
                        pygame.time.wait(1000)
                        startGameAnimation(mainBoard)
                    firstSelection = None
        pygame.display.update()
        FPSCLOCK.tick(FPS)
def generateRevealedBoxesData(val):
    revealedBoxes=[]
    for i in range(col):
        revealedBoxes.append([val]*row)
    return revealedBoxes
def getRandomsizedBoard():
    icons=[]
    for color in allcolors:
        for shape in allshapes:
            icons.append((shape,color))
    random.shuffle(icons)
    numIconsUsed=int(col *row/2)
    icons=icons[:numIconsUsed]*2
    random.shuffle(icons)
    board=[]
    for x in range(col):
        column=[]
        for y in range(row):
            column.append(icons[0])
            del icons[0]
        board.append(column)
    return board
def splitIntoGroupsOf(groupSize,theList):
    result=[]
    for i in range(0,len(theList),groupSize):
        result.append(theList[i:i+groupSize])
    return result
def leftTopCoordsOfBox(boxx,boxy):
    left=boxx*(boxsize+gapsize)+xmargin
    top=boxy*(boxsize+gapsize)+ymargin
    return (left,top)
def getBoxAtPixel(x,y):
    for boxx in range(col):
        for boxy in range(row):
            left,top = leftTopCoordsOfBox(boxx,boxy)
            boxRect=pygame.Rect(left,top,boxsize,boxsize)
            if boxRect.collidepoint(x,y):
                return (boxx,boxy)
    return (None,None)
def drawIcon(shape,color,boxx,boxy):
    quarter = int(boxsize*0.25)
    half=int(boxsize*0.5)

    left,top=leftTopCoordsOfBox(boxx,boxy)
    if shape==DONUT:
        pygame.draw.circle(Displaysurf,color,(left+half,top+half),half-5)
        pygame.draw.circle(Displaysurf,bgcolor,(left+half,top+half),quarter-5)
    elif shape==SQUARE:
        pygame.draw.rect(Displaysurf,color,(left+quarter,top+quarter,boxsize-half,boxsize-half))
    elif shape==DIAMOND:
        pygame.draw.polygon(Displaysurf,color,((left+half,top),(left+boxsize-1,top+half),(left+half,top+boxsize-1),(left,top+half)))
    elif shape==LINES:
        for i in range(0,boxsize,4):
            pygame.draw.line(Displaysurf,color,(left,top+i),(left+i,top))
            pygame.draw.line(Displaysurf,color,(left+i,top+boxsize-1),(left+boxsize-1,top+i))
    elif shape==OVAL:
        pygame.draw.ellipse(Displaysurf,color,(left,top+quarter,boxsize,half))

def getShapeAndColor(board,boxx,boxy):
    return board[boxx][boxy][0],board[boxx][boxy][1]
def drawBoxCovers(board,boxes,coverage):
    for box in boxes:
        left,top = leftTopCoordsOfBox(box[0],box[1])
        pygame.draw.rect(Displaysurf,bgcolor,(left,top,boxsize,boxsize))
        shape,color=getShapeAndColor(board,box[0],box[1])
        drawIcon(shape,color,box[0],box[1])
        if coverage>0:
            pygame.draw.rect(Displaysurf,boxcolor,(left,top,coverage,boxsize))
    pygame.display.update()
    FPSCLOCK.tick(FPS)

def revealBoxesAnimation(board,boxesToReveal):
    for coverage in range(boxsize,(-revelspeed)-1,-revelspeed):
        drawBoxCovers(board,boxesToReveal,coverage)

def coverBoxesAnimation(board,boxesToCover):
    for coverage in range(0,boxsize+revelspeed,revelspeed):
        drawBoxCovers(board,boxesToCover,coverage)

def drawBoard(board,revealed):
    for boxx in range(col):
        for boxy in range(row):
            left,top=leftTopCoordsOfBox(boxx,boxy)
            if not revealed[boxx][boxy]:
                pygame.draw.rect(Displaysurf,boxcolor,(left,top,boxsize,boxsize))
            else:
                shape,color=getShapeAndColor(board,boxx,boxy)
def drawHighlightBox(boxx,boxy):
    left,top = leftTopCoordsOfBox(boxx,boxy)
    pygame.draw.rect(Displaysurf,highlightcolor,(left-5,top-5,boxsize+19,boxsize+10),4)

def startGameAnimation(board):
    coveredBoxes=generateRevealedBoxesData(False)
    boxes=[]
    for x in range(col):
        for y in range(row):
            boxes.append((x,y))
    random.shuffle(boxes)
    boxGroups=splitIntoGroupsOf(8,boxes)

    drawBoard(board,coveredBoxes)
    for boxGroup in boxGroups:
        revealBoxesAnimation(board,boxGroup)
        coverBoxesAnimation(board,boxGroup)


def gameWonAnimation(board):
    coveredBoxes=generateRevealedBoxesData(True)
    color1=lightbgcolor
    color2=bgcolor
    for i in range(13):
        color1,color2=color2,color1
        Displaysurf.fill(color1)

        drawBoard(board,coveredBoxes)
        pygame.display.update()
        pygame.time.wait(300)
def hasWon(revealedBoxes):
    for i in revealedBoxes:
        if False in i:
            return False
    return True


if __name__=='__main__':
    main()



