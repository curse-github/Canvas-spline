from tkinter import *
from math import *

#go to end of file

def lerp(a,b,t):
    return [(1 - t) * a[0] + t * b[0],(1 - t) * a[1] + t * b[1]]

def drawcircle(v,color,radius,Type,index):
    value = False
    color1 = color
    if Type == 1:
        value = pointsSelected[index]
    elif Type == 2:
        value = pointModifiersSelected[index[0]][index[1]]
    if value:
        color1 = "red"
    v1 = [v[0] + screensize[0] / 2,v[1] + screensize[1] / 2]
    C.create_oval(v1[0]-radius, v1[1]-radius, v1[0]+radius, v1[1]+radius,fill=color1,outline=color1)

def drawline(v1,v2,color):
    global screensize
    line = C.create_line(v1[0] + screensize[0] / 2,v1[1] + screensize[1] / 2,v2[0] + screensize[0] / 2,v2[1] + screensize[1] / 2,fill=color)
    C.pack()

def drawrec(v1,v2,color):
    C.create_rectangle(v1[0],v1[1], v2[0],v2[1], fill=color, outline = color)
    C.pack()

def clear():
    C.delete("all")

def recalculate():
    global running
    global needs_to_be_called
    if running:
        needs_to_be_called = True
        return
    running = True
    #draw button in top right
    global screensize
    drawrec([screensize[0] - 51, 2],[screensize[0] + 1, 52],"black")
    #draw lines used for editing but only if they are enabled
    global show_lines
    if show_lines:
        i = 0
        while i < len(points) - 1:
            #lines amd dots
            drawcircle(pointModifiers[i][0],"black",5,2,[i,0])
            drawline(pointModifiers[i][0],points[i],"black")
            if i % 2 == 0:
                drawcircle(points[i],"blue",5,1,i)
            drawline(points[i],points[i + 1],"blue")
            if i == len(points) or i % 2 == 0:
                drawcircle(points[i + 1],"blue",5,1,i + 1)
            drawline(points[i + 1],pointModifiers[i][1],"black")
            drawcircle(pointModifiers[i][1],"black",5,2,[i,1])
            i = i + 1
    #check if screen needs to be refreshed again
    if needs_to_be_called:
        running = False
        needs_to_be_called = False
        clear()
        recalculate()
    #spline
    i = 0
    lastpoint = points[0]
    while i < len(points) - 1:
        for l in range(steps):
            t = (1 / steps) * (l + 1)
            lerp1 = lerp(points[i],pointModifiers[i][0],t)
            lerp2 = lerp(pointModifiers[i][0],pointModifiers[i][1],t)
            lerp3 = lerp(pointModifiers[i][1],points[i + 1],t)
            lerp4 = lerp(lerp1,lerp2,t)
            lerp5 = lerp(lerp2,lerp3,t)
            output = lerp(lerp4,lerp5,t)
            drawline([lastpoint[0],lastpoint[1]],[output[0],output[1]],"red")
            lastpoint = output
        i = i + 1
    running = False
    #check if screen needs to be refreshed again
    if needs_to_be_called:
        needs_to_be_called = False
        clear()
        recalculate()

def move(Type,index,position):
    #honestly im not even really sure how this works
    if Type == 1:
        pointsSelected[index] = False
        index1 = [index - 1,1]
        if index == 0:
            index1 = None
        index2 = [index,0]
        if not index > 0:
            index2 = [0,0]
        elif index == len(points) - 1:
            index2 = None
        if not index1 == None:
            pointModifiers[index1[0]][index1[1]][0] = (pointModifiers[index1[0]][index1[1]][0] - points[index][0]) + position[0]
            pointModifiers[index1[0]][index1[1]][1] = (pointModifiers[index1[0]][index1[1]][1] - points[index][1]) + position[1]
        if not index2 == None:
            pointModifiers[index2[0]][index2[1]][0] = (pointModifiers[index2[0]][index2[1]][0] - points[index][0]) + position[0]
            pointModifiers[index2[0]][index2[1]][1] = (pointModifiers[index2[0]][index2[1]][1] - points[index][1]) + position[1]
        points[index][0] = position[0]
        points[index][1] = position[1]
    elif Type == 2:
        pointModifiersSelected[index[0]][index[1]] = False
        pointModifiers[index[0]][index[1]][0] = position[0]
        pointModifiers[index[0]][index[1]][1] = position[1]
        if index[1] == 0:
            if not index[0] == 0:
                if index[0] > 0:
                    pointModifiers[index[0] - 1][1][0] = (-(position[0] - points[index[0]][0])) + points[index[0]][0]
                    pointModifiers[index[0] - 1][1][1] = (-(position[1] - points[index[0]][1])) + points[index[0]][1]
        elif index[1] == 1:
            index2 = [index[0] + 1,0]
            if not index[0] > -1:
                index2 = [0,0]
            elif index[0] == len(points) - 2:
                index2 = None
            if not index2 == None:
                if index[0] < len(pointModifiers) - 1:
                    pointModifiers[index2[0]][0][0] = (-(position[0] - points[index[0] + 1][0])) + points[index[0] + 1][0]
                    pointModifiers[index2[0]][0][1] = (-(position[1] - points[index[0] + 1][1])) + points[index[0] + 1][1]
    else:
        print("Error1")
    clear()
    recalculate()

def select(event):
    global mousepos
    global screensize
    x,y = mousepos[0] - screensize[0] / 2 + 5,mousepos[1] - screensize[1] / 2
    #check if user click the button to toggle the lines for editing
    global show_lines
    if mousepos[0] >= screensize[0] - 51 and mousepos[1] <= 55:
        show_lines = not show_lines
        clear()
        recalculate()
    elif show_lines: # otherwise check which point is closest to where the player clicks
        closest = 1000000
        Type = 0
        index = 101203
        for i in range(len(points)):
            #if this point is already selected, instead of trying to select a point, return and move the selected point the position of the click
            if pointsSelected[i] == True:
                move(1,i,[x,y])
                return
            else:
                point = points[i]
                distance = sqrt(abs(point[0] - x) ** 2 + abs(point[1] - y) ** 2)
                if distance < closest:
                    closest = distance
                    Type = 1
                    index = i
                elif distance == closest:
                    #there are two or more points with the same distance from the mouse
                    print("Error2")
        for i in range(len(pointModifiers)):
            for l in range(len(pointModifiers[i])):
                #if this point is already selected, instead of trying to select a point, return and move the selected point the position of the click
                if pointModifiersSelected[i][l] == True:
                    move(2,[i,l],[x,y])
                    return
                else:
                    point = points[l]
                    distance = sqrt(abs(pointModifiers[i][l][0] - x) ** 2 + abs(pointModifiers[i][l][1] - y) ** 2)
                    if distance < closest:
                        closest = distance
                        Type = 2
                        index = [i,l]
                    elif distance == closest:
                    #there are two or more points with the same distance from the mouse
                        print("Error3")

        if closest < 25:#if the closest point is also within the range of 25 pixels select it and redraw the screen
            if Type == 1:
                pointsSelected[index] = True
                clear()
                recalculate()
            elif Type == 2:
                pointModifiersSelected[index[0]][index[1]] = True
                clear()
                recalculate()
            else:
                print("Error4")

def updateMouse(event):
    global mousepos
    mousepos = [event.x,event.y]

#settings
steps = 15 # raise or lower this variable to raise or lower the "resolution" of the line
points = [[-225.0,0.0],[-75.0,0.0],[75.0,0.0],[225.0,0.0]]
pointsSelected = [False,False,False,False]
pointModifiers = [[[-225.0,-75.0],[-75.0,75.0]],[[-75.0,-75.0],[75.0,75.0]],[[75.0,-75.0],[225.0,75.0]]]
pointModifiersSelected = [[False,False],[False,False],[False,False]]
speed = 1000 #if you want to see the way its drawing you can turn this variable down

#other variables
running = False
needs_to_be_called = False
show_lines = True
trtLocation = [0,0]
screensize = [600,600]
mousepos = [0,0]

#set settings
root = Tk()
C = Canvas(root,bg="white",height=screensize[0],width=screensize[1])

#call main code
recalculate()
root.bind("<Motion>",updateMouse)
root.bind("<Button-1>",select)

#main loop
try:
    mainloop()
except KeyboardInterrupt:
    print('Interrupted')
    C.destroy()
    root.destroy()