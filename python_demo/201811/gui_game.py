# tkinter 图形库
from tkinter import *
import tkinter.simpledialog as dl
import tkinter.messagebox as mb


#设置GUI
root=Tk()
w=Label(root, text="Guess Number Game")
w.pack()

#欢迎消息
mb.showinfo('welcome', 'welcome message')
#处理信息
number=59
while True:
	#让用户验证信息
	guess=dl.askinteger('Number', "what's you guess?")
	if guess == number:
		output='Bingo! you guessed it right, but you do not win any prizes!'
		mb.showinfo('Hint:', output)
		break
	elif guess < number:
		output = 'No, the number is a higer than that'
		mb.showinfo('Hint', output)
	else:
		output = 'No, the number is a lower than that'
		mb.showinfo('Hint', output)
print('Done')