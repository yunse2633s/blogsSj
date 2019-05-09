# 导入turtle包的所有内容:
from turtle import *

# 设置笔刷宽度:
width(4)

# 前进:
forward(200)
# 右转90度:
right(90)

# 笔刷颜色:
pencolor('red')
forward(100)
right(90)

pencolor('green')
forward(200)
right(90)

pencolor('blue')
forward(100)
right(90)

# 调用done()使得窗口等待被关闭，否则将立刻关闭窗口:
# done()
# 
up()
left(45)
fd(50)

down()

s = Shape("compound")
poly1 = ((0,0),(10,-5),(0,10),(-10,-5))
s.addcomponent(poly1, "red", "blue")
poly2 = ((0,0),(10,-5),(-10,-5))
s.addcomponent(poly2, "blue", "red")

# turtle2 = MyTurtle()
# onclick(turtle2.glow)
# onrealease(turtle2.unglow)

done()