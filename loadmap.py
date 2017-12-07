from tkinter import *
from math import floor
import pickle
from random import randint, uniform
import time

class Cell():
	def __init__(self,x,y):
		self.x = x
		self.y = y
		self.drawX = (self.x*w)+4
		self.drawY = (self.y*w)+4
		self.wall = False
		self.X = False
		self.pathRight = False
		self.pathUp = False
		self.pathDown = False
		self.start = False
		self.end = False

	def drawGrid(self):
		canvas.create_rectangle(self.drawX,self.drawY,self.drawX+w,self.drawY+w)

		if self.wall == True:
			drawnStuff.append(canvas.create_rectangle(self.drawX,self.drawY,self.drawX+w,self.drawY+w,fill="black"))
		if self.X == True:
			drawnStuff.append(canvas.create_text(self.drawX+(w/2),self.drawY+(w/2),text="X"))
		if self.pathRight == True:
			drawnStuff.append(canvas.create_text(self.drawX+(w/2),self.drawY+(w/2),text="-->"))
		if self.pathUp == True:
			drawnStuff.append(canvas.create_text(self.drawX+(w/2),self.drawY+(w/2),text="^^^"))
		if self.pathDown == True:
			drawnStuff.append(canvas.create_text(self.drawX+(w/2),self.drawY+(w/2),text="vvv"))
		if self.start == True:
			drawnStuff.append(canvas.create_text(self.drawX+(w/2),self.drawY+(w/2),text="BEG"))
		if self.end == True:
			drawnStuff.append(canvas.create_text(self.drawX+(w/2),self.drawY+(w/2),text="END"))

def loadMap():
	global cells
	fileName = fileNameEntry.get()
	cells = pickle.load(open("C:\\Users\\Gustavo\\Documents\\programming python\\tower defense\\savefiles\\"+str(fileName),'rb'))
	inputWindow.quit()

inputWindow = Tk()
fileNameEntry = Entry(inputWindow)
fileNameEntry.pack()
fileNameEntryButton = Button(inputWindow,text='Enter File Name',command=loadMap)
fileNameEntryButton.pack()
inputWindow.mainloop()

window = Tk()
w = 50
col = 10
row = 10

drawnStuff = []

screenWidth = window.winfo_screenwidth()
screenHeight = window.winfo_screenheight()

print(screenWidth,screenHeight)

windowHeightFromScreenEdge = 100
windowWidthFromScreenEdge = 400

windowString = str((col*w)+5) + "x" + str((row*w)+5) + "+" + str(windowWidthFromScreenEdge) +"+" +str(windowHeightFromScreenEdge)

window.geometry(windowString)

canvas = Canvas(window,width=(col*w)+5,height=(row*w)+5)
canvas.pack()

for cell in cells:
	cell.drawGrid()

enemyDrawnList = []

class enemyX():
	def __init__(self,x,y):
		self.x = x
		self.y = y
		self.speed = uniform(.01,.03)
		self.direction = "right"

	def draw(self):
		self.drawnImage = canvas.create_text(self.x,self.y,text="X")

	def move(self):
		self.delete()
		if self.direction == "right":
			self.x += self.speed
		if self.direction == "up":
			self.y -= self.speed
		if self.direction == "down":
			self.y += self.speed
		self.draw()

	def delete(self):
		canvas.delete(self.drawnImage)

enemyList = []

for cell in cells:
	print(cell.start)

def getStartingCoords():
	global startingCell
	for cell in cells:
		if cell.start == True:
			startingX = cell.drawX
			startingY = cell.drawY
			print(startingX,startingY)
			startingXRange = (startingX+7,startingX+w-7)
			startingYRange = (startingY+7,startingY+w-7)
			return(startingXRange,startingYRange)


def createEnemies():
	startingRanges = getStartingCoords()
	print(startingRanges)
	startingX = startingRanges[0]
	startingY = startingRanges[1]
	for x in range(5):
		randomX = randint(startingX[0],startingX[1])
		randomY = randint(startingY[0],startingY[1])
		enemyList.append(enemyX(randomX,randomY))

createEnemies()

def deleteEnemies():
	global enemyDrawnList
	for enemy in enemyDrawnList:
		canvas.delete(enemy)
	enemyDrawnList = []

for enemy in enemyList:
	enemy.draw()

while True:
	window.update()
	window.update_idletasks()
	for enemy in enemyList:
		enemy.move()
	# deleteEnemies()
