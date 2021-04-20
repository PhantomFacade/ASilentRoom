#################################################

#################################################
from cmu_112_graphics import *
import random
if not (LAST_UPDATED.month == 7 and LAST_UPDATED.day == 27):
    raise Exception("Please download the new version of the animation framework from the hw13 page")
import math


class Pages():
    def __init__(self,words=""):
        """create Pages that have content on them"""
        self.words=words
        self.copy=copy.deepcopy(self.words)
        
    def __repr__(self):
        """returns a string of words"""
        return f"{self.words}"
        
    def lines(self,num):
        """splits page contents by number of characters.
        If a word will not fit on the line,
        it is added to the next line instead"""
        self.splitLine = []
        self.copy=self.words.split(" ")
        string=""
        for i in range(len(self.copy)):
            if len(string)+len(self.copy[i])-1<num:
                string+=str(self.copy[i])+" "
            elif len(string)+len(self.copy[i])-1>=num:
                self.splitLine.append(string[:len(string)-1])
                string=""+str(self.copy[i])+" "
            if i==len(self.copy)-1:
                self.splitLine.append(string[:len(string)-1])
        return self.splitLine
class Book(Pages):
    def __init__(self,title,List):
        """create Books that have content on them"""
        self.title=title
        self.list=List
        self.pages=List
        self.pages=Pages(self)
        self.numPage=0
    def __len__(self):
        """returns length of Pages"""
        return len(self.list)
    def getCurrentPage(self):
        """returns current Page number"""
        return self.list[self.numPage]
    def flipForward(self):
        """flip one Page forward"""
        if self.numPage<len(self.list)-1:
            self.numPage+=1
            return True
        if self.numPage==len(self.list)-1:
            return False
    def flipBackward(self):
        """flip one Page backward"""
        if self.numPage==0:
            return False
        else:
            self.numPage-=1
            return True
class Cover(Pages): 
    def __init__(self,title,words=""):
        """creates a cover with title and words"""
        self.title=title
        self.words=words
        self.pages=Pages(self)
    def __repr__(self):
        """returns a string with title"""
        return f"{self.title}"

####################################
class HelpMode(Mode):
    def appStarted(self):
        """When user press h, help mode initialize Pages"""
        P1=Pages("Eyy Welcome to Budget Agar io! Press right to flip!")
        P2=Pages("Press Up Down left right to move :)")
        P3=Pages("Have fun!:)")
        self.b = Book("Instructions", [P1, P2, P3])

    def modeActivated(self):
        """When Help mode activates, print In Help Mode"""
        print("In Help Mode")

    def keyPressed(self, event):
        if event.key=="Space":
            self.app.setActiveMode("play")
        if event.key =="Right":
            self.b.flipForward() 

    def redrawAll(self, canvas):
        canvas.create_text(self.width//2,self.height//2,
        text=self.b.getCurrentPage())

class GameOver(Mode):
    def appStarted(self):
        """Gameover mode initialize
        """
        self.highScore=0

    def modeActivated(self):
        """When Gameover mode activates, 
        print In GameOver Mode"""
        print("In GameOver Mode")

    def keyPressed(self, event):
        if event.key == "r":
            self.app.setActiveMode("play")

    def redrawAll(self, canvas):
        gameMode=self.getMode("play")
        best=gameMode.maxScore
        canvas.create_rectangle(0,0,self.width,self.height,
                                fill="black",width=0)
        canvas.create_text(self.width/2,self.height/2,
                text="Game Over",font=f"Arial {25} bold",fill="gold")
        canvas.create_text(self.width/2,self.height*3/5,
                text=f"bestscore={best}",
                font=f"Arial {15} bold",fill="gold")
        canvas.create_text(self.width/2,self.height*2/3,
                text="press 'r' to start over",
                font=f"Arial {10} bold",fill="gold")


class Food(object):
    def __init__(self,x,y,r):
        self.x=x
        self.y=y
        self.r=r
        if self.r==15:
            self.score=1
        elif self.r==25:
            self.score=2
        self.color=random.choice(["red","orange","green","blue","cyan","magenta"])

    def onClick(self):
        """when a food is clicked, its score increase by 1"""
        self.score+=1

    def render(self,mode,canvas):
        """draws a cicle on the canvas based on its local coordinates"""
        viewCx=self.x-mode.scrollX
        viewCy=self.y-mode.scrollY
        canvas.create_oval(viewCx-self.r, viewCy-self.r,
                           viewCx+self.r, viewCy+self.r,
                           onClick=self.onClick,fill=self.color,width=0)

class PlayMode(Mode):
    def appStarted(self):
        """Play mode initialize, player's position
        initialize, canvas resets"""
        print("W=, H=",self.width,self.height)
        #set x,y coord for self
        self.x=1000
        self.y=1000
        self.lightx=random.randint(0,600)
        self.lighty=random.randint(0,600)
        #set initial scrollX,scrollY
        self.scrollX = self.x - self.width//2
        self.scrollY = self.y - self.height//2
        self.scrollspd=40
        self.imagesize=80
        self.image=self.loadImage('bug.png')
        w,h=self.image.size
        self.image=self.scaleImage(self.image,self.imagesize/w)
        self.imageW,self.imageH=self.image.size

        self.imasize=2000
        self.ima=self.loadImage('BED.jpg')
        wid,hei=self.ima.size
        self.ima=self.scaleImage(self.ima,self.imasize/wid)
        self.imaW,self.imaH=self.image.size

        self.imsize=150
        self.im=self.loadImage('light.png')
        wi,hi=self.im.size
        self.im=self.scaleImage(self.im,self.imsize/wi)
        #set global bounds
        self.xlbounds=0
        self.xrbounds=2000
        self.ylbounds=0
        self.yrbounds=2000
        #set other variables
        self.food=[]
        self.timer=0
        self.score=self.maxScore=5
        self.counter=0
    

    def keyPressed(self, event):
        if event.key=="h":
            self.setActiveMode("help")
        if event.key=="Right":
            self.move(self.scrollspd,0)
        elif event.key=="Left":
            self.move(-self.scrollspd,0)
        elif event.key=="Up":
            self.move(0,-self.scrollspd)
        elif event.key=="Down":
            self.move(0,self.scrollspd)

    def modeActivated(self):
        """when first activated, 
        call appstarted"""
        self.appStarted()
        print("In Play Mode")

    def move(self,dx,dy):
        """takes in dx, dy, change self.x and self.y"""
        self.scrollX+=dx
        self.scrollY+=dy
        self.lightx+=dx
        self.lighty+=dx
        self.x+=dx
        self.y+=dy
        if self.x-600<self.xlbounds or self.x+600>self.xrbounds: 
            #checks global x Boundary
            self.scrollX-=dx
            self.x-=dx
            self.lightx-=dx
        if self.y-600<self.ylbounds or self.y+600>self.yrbounds:
            #checks global y Boundary
            self.scrollY-=dy
            self.y-=dy
            self.lighty-=dy
        self.updateFood()

    def getFood(self):
        """returns a list of tuples with the x and y coord
        of each food, and the score it holds"""
        return[(food.x, food.y, food.score) for food in self.food]

    def mousePressed(self, event):
        x,y=event.x,event.y
        print(x,y)
        self.food.append(Food(x+self.scrollX,y+self.scrollY,15))

    def updateFood(self):
        distance=((self.x-self.lightx)**2+(self.y-self.lighty)**2)**0.5
        if distance<=60:
            self.setActiveMode("gameOver")


    def timerFired(self):
        self.counter+=1
        randnum=random.randint(-19,19)
        pos=random.randint(0,1)
        if pos==1:
            self.move(randnum,0)
        if pos==0:
            self.move(0,randnum)
        if self.counter%2==0:
            self.imagesize=60
            self.image=self.loadImage('bug.png')
            w,h=self.image.size
            self.image=self.scaleImage(self.image,self.imagesize/w)
        if self.counter%2==1:
            self.imagesize=80
            self.image=self.loadImage('bug1.png')
            w,h=self.image.size
            self.image=self.scaleImage(self.image,self.imagesize/w)
    

    def redrawAll(self, canvas):
        for food in self.food:
            food.render(self,canvas)
        x0=self.xlbounds-self.scrollX
        y0=self.ylbounds-self.scrollY
        x1=self.xrbounds-self.scrollX
        y1=self.yrbounds-self.scrollY
        canvas.create_rectangle(x0, y0,x1,y1,width=10)
        canvas.create_image(1000-self.scrollX,1000-self.scrollY,image=ImageTk.PhotoImage(self.ima))

        r=40
        viewCx=self.x-self.scrollX
        viewCy=self.y-self.scrollY
           #canvas.create_oval(viewCx-r, viewCy-r,
                           #viewCx+r, viewCy+r,
                           #fill='black')
        canvas.create_image(viewCx,viewCy,image=ImageTk.PhotoImage(self.image))
        viewx=self.lightx-self.scrollX
        viewy=self.lighty-self.scrollY
        canvas.create_image(viewx,viewy,image=ImageTk.PhotoImage(self.im))



class AgarGame(ModalApp):
    def appStarted(self):
        """Add all three modes to the Agar Game,
        set inital mode to play mode"""
        self.addMode(PlayMode(name="play"))
        self.addMode(HelpMode(name="help"))
        self.addMode(GameOver(name="gameOver"))
        
        self.setActiveMode("play")

    def getState(self):
        """returns a tuple of the player's current x,y
        coord, remaining food, the player's current
        and max score"""
        mode = self.getMode("play") # this gets the instance of your play mode
        # if you have a variable you set in play's appStarted named "foo"
        # you can access it using mode.foo
        # TODO: get these
        x, y = mode.x, mode.y
        food=mode.getFood()
        score = mode.score
        maxScore=mode.maxScore
        return ((x, y), food, score, maxScore)




def main():
    AgarGame(width=1200, height=1200)
    testAll()


if __name__ == "__main__":
    main()