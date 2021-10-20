import threading
from tkinter.font import Font
from tkinter import ttk
from numpy.core.fromnumeric import size
from numpy.lib.utils import info
import yfinance
import plotly.express as ex
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
    def information():
        text_1 = tab1.create_text(100,20,text="please wait....",font=("Arial",15))
        data = yfinance.Ticker(company)
        inf = data.info
        df_inf = pd.DataFrame().from_dict(inf,orient='index')
        desc = df_inf.iloc[3]
        with open("file.txt","w") as f:
            f.write(desc[0])
            f.close()
        txt = []
        with open("file.txt","r") as f:
            for line in f:
                for word in line.split():
                    txt.append(word)
            f.close()
        try:
            del ff
        except:
            pass
        finally:
            with open("real.txt","w") as ff:
                ff.write("")
                ff.close()
            with open("real.txt","a") as ff:
                ind = 0
                for i in txt:
                    if ind%15==0:
                        ff.write("\n")
                    ff.write(i+" ")
                    ind+=1
                ff.close()
        del ff
        Canvas.delete(tab1,text_1)
        del f
        f = open("real.txt","r")
        tab1.create_text(20,0,anchor="nw",text=f.read(),font=("Comic Sans MS",15))
        f.close()

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

        text_2 = tab2.create_text(50,10,anchor='nw',text="please wait....",font=("Arial",15))
        stock = {"name":company,"feature":"sentiment analysis"}
        r = requests.post("http://127.0.0.1:8000/",data=stock)
        data = json.loads(r.content)
        news = data['news']
        table = data['table']
        sentiment = data['mean sentiment']
        Canvas.delete(tab2, text_2)
        w = 10
        for i in news:
            tab2.create_text(20,w,text="➡"+i[0] + "  ( "+i[2]+" )",anchor='nw',font=("Comic Sans MS",15))
            w += 30
        tab2.create_text(50,180,anchor="nw",text="News Sentiment Analysis: "+ str(sentiment['Mean Sentiment'][0]),font=("Comic Sans MS",15),fill='red')        
        tv_btn = Button(tab2,text="click here for full details",command=tv_win,width=20,height =2,font=("Arial",10),border=10,borderwidth=5)
        tv_btn.pack(pady=70,padx=10,side=LEFT)

    def stock_prediction():
        global img
        text_3 = tab3.create_text(50,10,anchor='nw',text="please wait....",font=("Arial",15))
        stock = {"name":company,"feature":"stock prediction"}
        r = requests.post("http://127.0.0.1:8000/",data=stock)
        r = r.content
        r = json.loads(r)

        Canvas.delete(tab3,text_3)
        text_3 = tab3.create_text(50,10,anchor='nw',text="Loading graphs....",font=("Arial",15))

        if "saved_graphs" not in os.listdir():
            os.mkdir("saved_graphs")
        df = r["output"]
        df = pd.DataFrame(df)
        fig = ex.line(df)
        graph_path = os.path.join("saved_graphs","plot.png")
        fig.write_image(graph_path)
        img = ImageTk.PhotoImage(Image.open(r"{0}".format(graph_path)))
        Canvas.delete(tab3, text_3)
        tab3.create_image(0,0,anchor="nw",image=img)
        
    t1 = Thread(target=information)
    t2 = Thread(target=sentiment_analysis)
    t3 = Thread(target=stock_prediction)
    t1.start()
    t2.start()
    t3.start()

def restart_program():
    """Restarts the current program.
    Note: this function does not return. Any cleanup action (like
    saving data) must be done before calling this function."""
    python = sys.executable
    os.execl(python, python, * sys.argv)


root = Tk()
root.title("Stock Projection")
root.geometry('700x400')
root.config(bg='#429ef5')

style = ttk.Style()

menubar = Menu(root)
option = Menu(menubar,tearoff=0)
option.add_command(label="Restart",command=restart_program)
option.add_command(label="Exit",command=root.quit)
menubar.add_cascade(label="options",menu=option)
root.config(menu=menubar)

name = Label(root,text="Stock Projection")
name.configure(font=('Arial',20),fg='Black',bg='lightgrey',width=200)
name.pack()

label1 = Label(root,text="Enter the stock symbol",border=5)
label1.pack(side='left',anchor='n',pady=20)
symbol_input = Text(root)
symbol_input.config(height=1,width=13,border=3,borderwidth=5)
symbol_input.place(x=5,y=100)
btn = Button(root,text='okay',command=start,width=10,border=5,borderwidth=5,bg='lightgreen')
btn.place(x=10,y=140)

TabControl = ttk.Notebook(root)
tab1 = Canvas(TabControl,bg='lightgrey')
tab2 = Canvas(TabControl,bg='lightgrey')
tab3 = Canvas(TabControl,bg='lightgrey')
TabControl.add(tab1,text='Description')
TabControl.add(tab2,text='News Sentiment Analysis')
TabControl.add(tab3,text='Stock Price Forecast')
TabControl.pack(expand=True,fill='both')

root.mainloop()
