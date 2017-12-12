from tkinter import *
from math import floor, sqrt
import pickle
from random import randint, uniform
import time
import os

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
	path = os.path.abspath("")
	path = path+"\\savefiles\\"+fileName
	cells = pickle.load(open(path,'rb'))
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

def drawMap():
	for cell in cells:
		cell.drawGrid()

drawMap()

enemyDrawnList = []

def distanceTwoPoints(x1,y1,x2,y2):
	###### d = sqr((x2-x1)^2 + (y2-y1)^2)
	firstPart = (x2-x1)**2
	secondPart = (y2-y1)**2
	d = sqrt(firstPart+secondPart)
	return(d)

class tower():
	def __init__(self,x,y):
		self.x = x
		self.y = y
		self.lockedOn = False
		self.bullets = []
		self.reloadRate = 500
		self.currentRate = 0
		self.currentBulRate = 0


	def draw(self):
		self.drawnImage = canvas.create_oval(self.x,self.y,self.x+15,self.y+15,fill="blue")

	def shoot(self):
		global enemyList
		if self.currentRate > 500:
			self.currentRate = randint(0,400)
		if self.currentBulRate > 500:
			self.currentBulRate = 0
		self.currentRate += 1
		if len(self.bullets) >0:
			self.currentBulRate += 4
		if self.currentBulRate == self.reloadRate:
			for bullet in self.bullets:
				canvas.delete(bullet)
				self.bullets = []
				self.currentBulRate = 0
		self.checkLockedOn()
		if self.lockedOn == False:
			self.pickEnemy()
		else:
			if self.currentRate == self.reloadRate:
				self.bullets.append(canvas.create_line(self.x,self.y,self.lockedOn.x,self.lockedOn.y,width=2))
				if self.lockedOn in enemyList:
					canvas.delete(enemyList[enemyList.index(self.lockedOn)].drawnImage)
					enemyList.pop(enemyList.index(self.lockedOn))
				self.lockedOn = False
				self.currentRate = 0

	def pickEnemy(self):
		global enemyList
		enemiesInRange = []
		enemyListy = enemyList
		for enemy in enemyListy:
			distance = distanceTwoPoints(self.x,self.y,enemy.x,enemy.y)
			if distance < 60:
				enemiesInRange.append(enemy)
		if len(enemiesInRange) > 0:
			whichOne = randint(0,len(enemiesInRange)-1)
			self.lockedOn = enemiesInRange[whichOne]

	def checkLockedOn(self):
		if self.lockedOn != False:
			if distanceTwoPoints(self.x,self.y,self.lockedOn.x,self.lockedOn.y) > 70:
				self.lockedOn = False



def getPathChanges():
	pathRight = []
	pathUp = []
	pathDown = []
	for cell in cells:
		if cell.pathRight == True:
			pathRight.append((cell.drawX,cell.drawY))
		if cell.pathUp == True:
			pathUp.append((cell.drawX,cell.drawY))
		if cell.pathDown == True:
			pathDown.append((cell.drawX,cell.drawY))
	allPaths = [pathRight,pathUp,pathDown]
	return(allPaths)

pathChanges = getPathChanges()


def getEndCell():
	for cell in cells:
		if cell.end == True:
			return((cell.drawX,cell.drawY))

endCoords = getEndCell()


def fifty50():
	#### returns True one half of the time.. returns False the other half

	number = randint(0,1)
	if number == 0:
		return True
	else:
		return False

def thirty33():
	#### returns True 1/3 of the time.. returns False 2/3
	number = randint(0,2)
	if number == 0:
		return True
	else:
		return False


class enemyX():
	def __init__(self,x,y):
		self.x = x
		self.y = y
		# self.speed = uniform(.01,.03)
		self.speed = uniform(.15,.25)
		self.direction = "right"

	def draw(self):
		self.drawnImage = canvas.create_text(self.x,self.y,text="X")

	def move(self):
		self.checkMovement()
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

	def destroy(self):
		whereAreWe = enemyList.index(self)
		enemyList.pop(whereAreWe)
		print(enemyList)


	def checkMovement(self):
		if distanceTwoPoints(self.x,self.y,endCoords[0]+74,endCoords[1]+24) < 20:
			print('another one bites the dust')
			self.delete()
			self.destroy()

		for x,coords in enumerate(pathChanges):
			for y,coord in enumerate(coords):
				coordMidX = coord[0]+24
				coordMidY = coord[1]+24
				if distanceTwoPoints(self.x,self.y,coordMidX,coordMidY) < 20:
					if x == 0:
						if thirty33():
							self.direction = 'right'
					if x ==1:
						if thirty33():
							self.direction = 'up'
					if x == 2:
						if thirty33():
							self.direction = 'down'

enemyList = []

towerList = []


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
	global enemyList
	startingRanges = getStartingCoords()
	print(startingRanges)
	startingX = startingRanges[0]
	startingY = startingRanges[1]
	for x in range(10):
		randomX = randint(startingX[0],startingX[1])
		randomY = randint(startingY[0],startingY[1])
		enemyList.append(enemyX(randomX,randomY))

createEnemies()

def deleteEnemies():
	global enemyDrawnList
	for enemy in enemyDrawnList:
		canvas.delete(enemy)
	enemyDrawnList = []
	drawMap()
	drawTowers()

for enemy in enemyList:
	enemy.draw()


def leftClick(event):
	print(event.x,event.y)
	towerList.append(tower(event.x,event.y))
	towerList[len(towerList)-1].draw()

def drawTowers():
	for towers in towerList:
		towers.draw()

def keyPress(event):
	global enemyList
	if event.char == 'q':
		createEnemies()
		deleteEnemies()
		for enemy in enemyList:
			enemy.draw()
		drawMap()
		for towers in towerList:
			towers.draw()
			towers.currentRate = randint(0,400)

window.bind("<Button-1>",leftClick)
window.bind("<Key>",keyPress)

while True:
	window.update()
	window.update_idletasks()
	for enemy in enemyList:
		enemy.move()
	for towers in towerList:
		towers.shoot()
	# deleteEnemies()
