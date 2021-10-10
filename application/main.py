from requests.api import options
from pandastable import Table, TableModel
from tkinter.font import Font
from tkinter import ttk
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from threading import *
from tkinter import *
from PIL import Image, ImageTk
import pandas as pd
import requests
import json
import sys
import os


def start():
    company = symbol_input.get("1.0",END)
    def sentiment_analysis_thread():
        t2 = Thread(target=sentiment_analysis)
        t2.start()

    def sentiment_analysis():
        def tv_win():
            tv_page = Toplevel(root)
            tv_page.title("table view")
            df = pd.DataFrame(table)
            tv = ttk.Treeview(tv_page)
            cols = []
            for i in df.columns:
                cols.append(i)
            tv['columns']= tuple(cols)
            tv['show'] = 'headings'
            tv.column('#0', width=0, stretch=NO)
            tv.column('0', anchor=CENTER, width=80)
            tv.column('1', anchor=CENTER, width=80)
            tv.column('2', anchor=CENTER, width=80)
            tv.column('3', anchor=CENTER, width=80)
            tv.column('4', anchor=CENTER, width=80)
            tv.column('5', anchor=CENTER, width=80)

            tv.heading('#0', text='', anchor=CENTER)
            tv.heading('0', text=cols[0], anchor=CENTER)
            tv.heading('1', text=cols[1], anchor=CENTER)
            tv.heading('2', text=cols[2], anchor=CENTER)
            tv.heading('3', text=cols[3], anchor=CENTER)
            tv.heading('4', text=cols[4], anchor=CENTER)
            tv.heading('5', text=cols[5], anchor=CENTER)

            for i in range(len(df)):
                t = df.iloc[i].values.tolist()
                tv.insert('','end',text='l1',values=(t))
            tv.pack()

        text_1 = tab2.create_text(50,10,anchor='nw',text="please wait....")
        stock = {"name":company,"feature":"sentiment analysis"}
        r = requests.post("http://127.0.0.1:8000/",data=stock)
        data = json.loads(r.content)
        news = data['news']
        table = data['table']
        sentiment = data['mean sentiment']
        Canvas.delete(tab2, text_1)

        w = 10
        for i in news:
            tab2.create_text(50,w,text=i[0] + "  ( "+i[2]+" )",anchor='nw')
            w += 20
        
        tab2.create_text(50,100,anchor="nw",text="News Sentiment Analyis: "+ str(sentiment['Mean Sentiment'][0]))        
        tv_btn = Button(tab2,text="click here to full details",command=tv_win)
        tv_btn.pack(pady=70,padx=10,side=LEFT)

    def stock_prediction():
        text_2 = tab3.create_text(50,10,anchor='nw',text="please wait....")
        stock = {"name":company,"feature":"stock prediction"}
        r = requests.post("http://127.0.0.1:8000/",data=stock)
        r = r.content
        r = json.loads(r)
        Canvas.delete(tab3, text_2)

        if "saved_graphs" not in os.listdir():
            os.mkdir("saved_graphs")
        df = r["output"]
        df = pd.DataFrame(df)

        plt.plot(df) # This gives warning and gui freezes
        graph_path = os.path.join("saved_graphs","image.png")
        plt.savefig(graph_path)
        img = ImageTk.PhotoImage(Image.open(graph_path))
        tab3.create_image(20,20,anchor='nw',image=img)
        

        #tab3.create_text(50,10,text=df,anchor='nw')

    def stock_prediction_thread():
        t1 = Thread(target=stock_prediction)
        t1.start()
        
    sentiment_analysis_thread()
    stock_prediction_thread()

def restart_program():
    """Restarts the current program.
    Note: this function does not return. Any cleanup action (like
    saving data) must be done before calling this function."""
    python = sys.executable
    os.execl(python, python, * sys.argv)


root = Tk()
root.title("Stock Projection")
root.geometry('700x400')
root.config(bg='grey')

menubar = Menu(root)
option = Menu(menubar,tearoff=0)
option.add_command(label="Restart",command=restart_program)
option.add_command(label="Exit",command=root.quit)

menubar.add_cascade(label="File",menu=option)
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
