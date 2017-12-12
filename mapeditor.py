from tkinter import *
from math import floor
import pickle
import os

window = Tk()
window.title('Map Editor')
w = 50
col = 10
row = 10

screenWidth = window.winfo_screenwidth()
screenHeight = window.winfo_screenheight()

print(screenWidth,screenHeight)

windowHeightFromScreenEdge = 100
windowWidthFromScreenEdge = 400

windowString = str((col*w)+5) + "x" + str((row*w)+5) + "+" + str(windowWidthFromScreenEdge) +"+" +str(windowHeightFromScreenEdge)

window.geometry(windowString)

canvas = Canvas(window,width=(col*w)+5,height=(row*w)+5)
canvas.pack()

toggles = Tk()
toggles.title('Options')

togglesWidth = 100
togglesHeight = 300

togglesString = str(togglesWidth)+"x"+str(togglesHeight)+"+"+str(windowWidthFromScreenEdge-120)+"+"+str(windowHeightFromScreenEdge)

toggles.geometry(togglesString)

drawnStuff = []

currentSelection = 0

def saveFile2():
	global inputWindow, fileNameEntry
	fileName = fileNameEntry.get()
	path = os.path.abspath("")
	path = path+"\\savefiles\\"+str(fileName)
	f = open(path,'wb')
	pickle.dump(cells,f)
	f.close()
	inputWindow.destroy()

def saveFile():
	global fileNameEntry, inputWindow
	inputWindow = Tk()
	inputWindow.geometry(str(150)+"x"+str(200)+"+"+str(windowWidthFromScreenEdge+100)+"+"+str(windowHeightFromScreenEdge+100))
	fileNameEntry = Entry(inputWindow)
	fileNameEntry.pack(fill="x", side='bottom')
	fileEntryButton = Button(inputWindow,width=10,height=1,command=saveFile2,text="Enter Filename")
	fileEntryButton.pack(side='bottom')
	inputWindow.mainloop()
def drawX():
	global currentSelection
	currentSelection = 1

def drawPathRight():
	global currentSelection
	currentSelection = 2

def drawPathUp():
	global currentSelection
	currentSelection = 3

def drawPathDown():
	global currentSelection
	currentSelection = 4

def drawStarting():
	global currentSelection
	currentSelection = 5

def drawEnding():
	global currentSelection
	currentSelection = 6

def drawBox():
	global currentSelection
	currentSelection = 0

toggleBlack = Button(toggles,text='Black Box',command=drawBox,width=10,height=1)
toggleBlack.pack(fill='both')

toggleX = Button(toggles,text='Draw X',command=drawX,width=10,height=1)
toggleX.pack(fill='both')

togglePathRight = Button(toggles,text="Path ->",command=drawPathRight,width=10,height=1)
togglePathRight.pack(fill='both')

togglePathUp = Button(toggles,text='Path ^',command=drawPathUp,width=10,height=1)
togglePathUp.pack(fill='both')

togglePathDown = Button(toggles,text='Path v',command=drawPathDown,width=10,height=1)
togglePathDown.pack(fill='both')

toggleBeginning = Button(toggles,text='BEG',command=drawStarting,width=10,height=1)
toggleBeginning.pack(fill='both')

toggleEnding = Button(toggles,text='END',command=drawEnding,width=10,height=1)
toggleEnding.pack(fill='both')

saveButton = Button(toggles, text="Save File",command=saveFile,width=10,height=1)
saveButton.pack(fill='both',side='bottom')

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



cells = []

for x in range(col):
	for y in range(row):
		cells.append(Cell(x,y))

for cell in cells:
	cell.drawGrid()

def findCellByXY(x,y):
	for cell in cells:
		if cell.x == x and cell.y == y:
			return(cells.index(cell))


def keyEvent(event):
	if event.char == 'p':
		window.destroy()
		toggles.destroy()

def mouseClick(event):
	x2 = roundToInterval(event.x,w)
	y2 = roundToInterval(event.y,w)
	print(x2,y2)
	if currentSelection == 0:
		cells[findCellByXY(x2,y2)].wall = True
	if currentSelection == 1:
		cells[findCellByXY(x2,y2)].X = True
	if currentSelection == 2:
		cells[findCellByXY(x2,y2)].pathRight = True
	if currentSelection == 3:
		cells[findCellByXY(x2,y2)].pathUp = True
	if currentSelection == 4:
		cells[findCellByXY(x2,y2)].pathDown = True
	if currentSelection == 5:
		cells[findCellByXY(x2,y2)].start = True
	if currentSelection == 6:
		cells[findCellByXY(x2,y2)].end = True
	drawGrid()

def roundToInterval(x,interval):
	return((floor(x/interval)))

def rightClick(event):
	global drawnStuff
	x = roundToInterval(event.x,w)
	y = roundToInterval(event.y,w)
	cells[findCellByXY(x,y)].wall = False
	cells[findCellByXY(x,y)].X = False
	cells[findCellByXY(x,y)].pathRight = False
	cells[findCellByXY(x,y)].pathUp = False
	cells[findCellByXY(x,y)].pathDown = False
	cells[findCellByXY(x,y)].start = False
	cells[findCellByXY(x,y)].end = False
	for thing in drawnStuff:
		canvas.delete(thing)
	drawnStuff = []
	drawGrid()



window.bind("<Key>",keyEvent)
toggles.bind("<Key>",keyEvent)
window.bind("<Button-1>",mouseClick)
window.bind("<Button-3>",rightClick)


def drawGrid():	
	for cell in cells:
		cell.drawGrid()


while True:
	window.update()
	window.update_idletasks()
	toggles.update()
	toggles.update_idletasks()