from tkinter import *
from math import floor, sqrt
import pickle
from random import randint, uniform
import time
import os

### these arrays are global variables that house
### the objects for enemies and for towers
towers = []
enemies = []

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
		# windows.gameCanvas.create_rectangle(self.drawX,self.drawY,self.drawX+windows.w,self.drawY+windows.w)
		if self.wall == True:
			windows.gameCanvas.create_rectangle(self.drawX,self.drawY,self.drawX+windows.w,self.drawY+windows.w,fill="black")
		# if self.X == True:
			# drawnStuff.append(canvas.create_text(self.drawX+(w/2),self.drawY+(w/2),text="X"))
		# if self.pathRight == True:
			# drawnStuff.append(canvas.create_text(self.drawX+(w/2),self.drawY+(w/2),text="-->"))
		# if self.pathUp == True:
			# drawnStuff.append(canvas.create_text(self.drawX+(w/2),self.drawY+(w/2),text="^^^"))
		# if self.pathDown == True:
			# drawnStuff.append(canvas.create_text(self.drawX+(w/2),self.drawY+(w/2),text="vvv"))
		# if self.start == True:
			# drawnStuff.append(canvas.create_text(self.drawX+(w/2),self.drawY+(w/2),text="BEG"))
		# if self.end == True:
			# drawnStuff.append(canvas.create_text(self.drawX+(w/2),self.drawY+(w/2),text="END"))

def dist(x1,y1,x2,y2):
	###### d = sqr((x2-x1)^2 + (y2-y1)^2)
	firstPart = (x2-x1)**2
	secondPart = (y2-y1)**2
	d = sqrt(firstPart+secondPart)
	return(d)

def keyPress(event):
	if event.char == 'p':
		windows.gameWindow.destroy()

def placeTower(x,y):
	global towers
	towers.append(Tower(x,y))
	towers[len(towers)-1].draw()
	player.gold -= 250
	player.currentSelection = 'none'
	windows.updateGoldLabel()

def findCellByXY(x,y):
	for cell in cells:
		if cell.x == x and cell.y == y:
			return(cells.index(cell))

def roundToInterval(x,interval):
	return((floor(x/interval)))

def isSuitableLocationForTower(x,y):
	x = roundToInterval(x,50)
	y = roundToInterval(y,50)
	if cells[findCellByXY(x,y)].wall == True:
		return(True)
	else:
		return(False)

def leftClick(event):
	if event.x < 500 and event.y < 500 and player.currentSelection =='buy tower' and player.gold>249 and event.widget == windows.gameCanvas:
		if isSuitableLocationForTower(event.x,event.y) == True:
			placeTower(event.x,event.y)

def createEnemies(amount):
	global enemies
	### first, pick a random starting cell from list of cells
	startingCells = getStartingCells()
	### then spawn it somewhere in that cell
	for enemy in range(amount):
		whichOne = randint(0,len(startingCells)-1)
		x = (startingCells[whichOne].x * windows.w)+randint(10,40)
		y = (startingCells[whichOne].y * windows.w)+randint(10,40)
		enemies.append(Enemy(x,y))

def getStartingCells():
	listOfStartCells = []
	for cell in cells:
		if cell.start == True:
			listOfStartCells.append(cell)
	return(listOfStartCells)

def drawEnemies():
	for enemy in enemies:
		if enemy.active == False:
			enemy.draw()

def moveEnemies():
	for enemy in enemies:
		enemy.moveForward()
		enemy.active = True

def getEndingCells():
	listofEndingCells = []
	for cell in cells:
		if cell.end == True:
			listofEndingCells.append(cell)
	return(listofEndingCells)

def checkForRunawayEnemies():
	doIt = False
	for enemy in enemies:
		if enemy.x > 400:
			doIt = True
			break
	### enemies that make it to the end of the screen
	if doIt == True:
		endingCells = getEndingCells()
		listOfCoordsToCheck = []
		for cell in endingCells:
			x = (cell.x*windows.w)+(windows.w/2)+15
			y = (cell.y*windows.w)+(windows.w/2)
			listOfCoordsToCheck.append((x,y))

		for enemy in enemies:
			for coords in listOfCoordsToCheck:
				if dist(enemy.x,enemy.y,coords[0],coords[1])<25:
					removeEnemy(enemy)
					player.deleteHealth()
					player.health -= 1
					player.drawHealth()
					break

def quitGame():
	messageBox.quit()
	messageBox.destroy()
	windows.gameWindow.quit()
	windows.gameWindow.destroy()


def checkForDefeat():
	global messageBox
	if player.health < 1:
		messageBox = Tk()
		messageBox.title('Game Over!')
		##### fix this later
		messageBox.geometry('300x65+300+300')
		labelText = "Your Score: "+str(player.score)
		label = Label(messageBox,text=labelText,font='Helvetica 16 bold',bg='black',fg='white')
		label.pack(fill='both')
		button = Button(messageBox,text='Ok',command=quitGame,bg='black',fg='white',height=3)
		button.pack(fill='both')
		messageBox.mainloop()



def removeEnemy(enemy):
	enemy.delete()
	enemies.pop(enemies.index(enemy))

def towerLogic():
	for tower in towers:
		tower.getEnemiesInRange()
		tower.updateTick()
		tower.shouldIDelete()
		tower.shouldIShoot()
		tower.checkLockedOnRange()

class Enemy():
	def __init__(self,x,y):
		self.x = x
		self.y = y
		self.direction = 'right'
		self.speed = uniform(.05,.1)
		self.active = False

	def draw(self):
		self.drawnImage = windows.gameCanvas.create_text(self.x,self.y,text="X")

	def delete(self):
		windows.gameCanvas.delete(self.drawnImage)

	def moveForward(self):
		self.delete()
		if self.direction == 'right':
			self.x += self.speed
		if self.direction == 'up':
			self.y -= self.speed
		if self.direction == 'down':
			self.y += self.speed
		self.draw()

class Player():
	def __init__(self):
		self.gold = 500
		self.score = 0
		self.currentSelection = "none"
		self.health = 5
		self.healthImages = []

	def drawHealth(self):
		x = 410
		y = 10
		for z in range(self.health):
			newX = x+((z+1)*15)
			self.healthImages.append(windows.gameCanvas.create_rectangle(newX,y,(newX+10),(y+10),fill='red'))

	def deleteHealth(self):
		for image in self.healthImages:
			windows.gameCanvas.delete(self.healthImages)
		##### need to redraw top right hand corner cell(8,0) and cell(9,0)
		cells[findCellByXY(8,0)].drawGrid()
		cells[findCellByXY(9,0)].drawGrid()
		self.healthImages = []

class Tower():
	def __init__(self,x,y):
		self.x = x-7
		self.y = y-7
		self.lockedOn = False
		self.reloadRate = 600
		self.currentRate = 0
		self.bulletRate = 0
		self.bulletImages = []

	def draw(self):
		self.drawnImage = windows.gameCanvas.create_oval(self.x,self.y,self.x+15,self.y+15,fill='blue')

	def getEnemiesInRange(self):
		for enemy in enemies:
			if dist(enemy.x,enemy.y,self.x,self.y)<75:
				self.lockedOn = enemy
				break

	def checkLockedOnRange(self):
		if self.lockedOn != False:
			if dist(self.x,self.y,self.lockedOn.x,self.lockedOn.y)>75:
					self.lockedOn = False
					print('enemy got away')

	def updateTick(self):
		self.currentRate += 1
		self.bulletRate += .3

	def shouldIDelete(self):
		if self.bulletRate > self.reloadRate:
			if len(self.bulletImages)>0:
				self.deleteBullet()
			self.bulletRate = 0

	def shouldIShoot(self):
		if self.lockedOn != False:
			print(self.bulletRate)
			if self.currentRate > self.reloadRate:
				self.shoot()
				self.currentRate = 0

	def shoot(self):
		self.drawBullet(self.lockedOn.x,self.lockedOn.y)
		if self.lockedOn in enemies:
			removeEnemy(self.lockedOn)
			self.lockedOn = False
			player.score += 10
			player.gold += 25
			windows.updateLabels()

	def drawBullet(self,x,y):
		self.bulletImages.append(windows.gameCanvas.create_line(self.x,self.y,x,y,width=2))
		print(self.bulletImages)

	def deleteBullet(self):
		for bullet in self.bulletImages:
			windows.gameCanvas.delete(bullet)
		self.bulletImages = []

class WindowHandler():
	def __init__(self):
		self.currentLevel = None
		self.numOfEnemies = 5
		
	def startMainMenu(self):
		### starts up the main menu, makes the buttons
		self.mainMenu = Tk()
		self.monitorWidth = self.mainMenu.winfo_screenwidth()
		self.monitorHeight = self.mainMenu.winfo_screenheight()
		self.mainMenu.title('Welcome')
		self.mainMenu.geometry('225x85+'+str(int(self.monitorWidth/2.5))+"+"+str(int(self.monitorHeight/3)))

		self.menuLabel1 = Label(self.mainMenu, text="Welcome to",bg='black',fg='white',font="Helvetica 13 bold")
		self.menuLabel1.pack(fill='x')

		self.menuLabel2 = Label(self.mainMenu, text='pyTower Defense!',bg='black',fg='blue',font='Helvetica 14 bold')
		self.menuLabel2.pack(fill='x')

		self.startGameButton = Button(self.mainMenu,text='Start New Game',bg='black',fg='white',command=self.startGameWindow,width=15)
		self.startGameButton.pack(side='left', fill='both')

		self.loadGameButton = Button(self.mainMenu,text='Load Saved Game',bg='black',fg='white',width=15)
		self.loadGameButton.pack(side='right',fill='both')

		self.mainMenu.mainloop()

	def exitMainMenu(self):
		self.mainMenu.quit()
		self.mainMenu.destroy()

	def levelPicker(self,level):
		### uses pickle to import the level
		global cells
		path = os.path.abspath("")
		path += "\\savefiles\\"+level
		cells = pickle.load(open(path,'rb'))
		self.loadLevel()

	def updateGoldLabel(self):
		labelText = "Gold: "+str(player.gold)+"gp"
		self.goldLabel['text'] = labelText
		if player.gold == 0:
			self.goldLabel['fg'] = 'red'

	def startGameWindow(self):
		### initalize the game window
		self.exitMainMenu()
		self.w = 50
		self.rows = 10
		self.cols = 10

		self.gameWindow = Tk()
		self.gameWindow.title('pyTower Defense')

		self.gameCanvas = Canvas(self.gameWindow,width=((self.w*self.rows)+5),height=((self.w*self.cols)+5))
		self.gameCanvas.pack()

		self.buyTowerButton = Button(self.gameWindow,text='Buy Tower (250g)',font='Helvetica 12 bold',command=self.clickedBuyTower)
		self.buyTowerButton.pack(side='left')

		labelText = "Gold: "+str(player.gold)+"gp"
		self.goldLabel = Label(self.gameWindow,text=labelText,font='Helvetica 12 bold')
		self.goldLabel.pack(side='right',padx=15)

		labelText = "Score: "+str(player.score)
		self.scoreLabel = Label(self.gameWindow,text=labelText,font='Helvetica 12 bold')
		self.scoreLabel.pack(side='right',padx=5)

		self.startWaveButton = Button(self.gameWindow,text='Start Wave',font='Helvetica 12 bold',command=self.startWave)
		self.startWaveButton.pack(side='left')

		self.levelPicker('level 1')

	def startWave(self):
		self.currentSelection = 'none'
		createEnemies(self.numOfEnemies)
		drawEnemies()
		self.numOfEnemies += 1

	def clickedBuyTower(self):
		player.currentSelection = 'buy tower'

	def mainGameLoop(self):
		self.gameWindow.bind("<Key>",keyPress)
		self.gameWindow.bind("<Button-1>",leftClick)

		currentGameTick = 0
		while True:
			currentGameTick += 1
			moveEnemies()
			checkForRunawayEnemies()
			towerLogic()
			checkForDefeat()
			self.gameWindow.update()
			self.gameWindow.update_idletasks()

	def updateLabels(self):
		labelText = "Score: "+str(player.score)
		self.scoreLabel['text'] = labelText
		labelText = "Gold: "+str(player.gold)+'gp'
		self.goldLabel['text'] = labelText
		self.goldLabel['fg'] = 'black'

	def loadLevel(self):
		### sets up the cells and draws everything once
		for cell in cells:
			cell.drawGrid()
		player.drawHealth()
		self.mainGameLoop()


player = Player()
windows = WindowHandler()

windows.startMainMenu()