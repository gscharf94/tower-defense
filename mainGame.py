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
	towers = []
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

class Player():
	def __init__(self):
		self.gold = 500
		self.score = 0
		self.currentSelection = "none"

class Tower():
	def __init__(self,x,y):
		self.x = x-7
		self.y = y-7

	def draw(self):
		self.drawnImage = windows.gameCanvas.create_oval(self.x,self.y,self.x+15,self.y+15,fill='blue')


class WindowHandler():
	def __init__(self):
		self.currentLevel = None
		
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
		pass

	def clickedBuyTower(self):
		player.currentSelection = 'buy tower'

	def mainGameLoop(self):
		self.gameWindow.bind("<Key>",keyPress)
		self.gameWindow.bind("<Button-1>",leftClick)

		currentGameTick = 0
		while True:
			currentGameTick += 1
			self.gameWindow.update()
			self.gameWindow.update_idletasks()

	def loadLevel(self):
		### sets up the cells and draws everything once
		for cell in cells:
			cell.drawGrid()
		self.mainGameLoop()


player = Player()
windows = WindowHandler()

windows.startMainMenu()