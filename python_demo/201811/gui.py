# tkinter 图形库
from tkinter import *
import tkinter.simpledialog as dl
import tkinter.messagebox as mb



root=Tk()
w=Label(root, text="Label Title")
w.pack()

#输入
mb.showinfo('welcome', 'welcome message')
guess=dl.askinteger('number', 'enter a number')

#输出
output='This is output message'
mb.showinfo('output:', output)