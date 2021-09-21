from pandastable import Table, TableModel
from tkinter import *
from tkinter.font import Font
from tkinter import ttk
import pandas as pd
import requests
import json
import os

def start():
    def sentiment_analysis(company):
        stock = {"name":company,"feature":"sentiment analysis"}

        #r = requests.post("http://127.0.0.1:8000/",data=stock)
        f = open(os.getcwd()+"/new/sentiment_analysis.json","r")
        data = json.loads(f.read())

        news = data['news']
        table = data['table']
        sentiment = data['mean sentiment']
        #for sentiment analysis
        w = 10
        for i in news:
            tab2.create_text(50,w,text=i[0] + "  ( "+i[2]+" )",anchor='nw')
            w += 20
        tab1.create_text(50,10,table,anchor='nw')
        
        
    company = symbol_input.get("1.0",END)
    sentiment_analysis(company)


root = Tk()
root.title("Stock Projection")
root.geometry('700x400')
root.config(bg='grey')

menubar = Menu(root)
file_menu = Menu(menubar,tearoff=0)
file_menu.add_command(label="Help")
file_menu.add_command(label="Exit",command=root.quit)
file_menu.add_separator()

menubar.add_cascade(label="File",menu=file_menu)
root.config(menu=menubar)

name = Label(root,text="Stock Projection")
name.configure(font=('Arial',20),fg='Black',bg='lightgrey')
name.pack()

label1 = Label(root,text="Enter the symbol of any stock")
label1.pack(side='left',anchor='n',pady=20)

symbol_input = Text(root)
symbol_input.config(height=1,width=10,border=3)
symbol_input.pack(padx=5,anchor='n',side=LEFT,pady=20)

btn = Button(root,text="Okay",command=start)
btn.pack(anchor='n',side=LEFT,pady=20)

TabControl = ttk.Notebook(root)
tab1 = Canvas(TabControl,bg='lightgrey')
tab2 = Canvas(TabControl)
tab3 = Canvas(TabControl)

TabControl.add(tab1,text='Description')
TabControl.add(tab2,text='News Sentiment Analysis')
TabControl.add(tab3,text='Stock Price Forecast')
TabControl.pack(expand=True,fill='both')



root.mainloop()
