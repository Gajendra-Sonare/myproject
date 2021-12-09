from numpy.core.fromnumeric import size
from numpy.lib.utils import info
from bs4 import BeautifulSoup
from PIL import Image, ImageTk
import plotly.express as ex
from tkinter import Canvas, messagebox
from tkinter.font import Font
from tkinter import ttk
from threading import *
import tkinter as tk
import pandas as pd
import requests
import yfinance
import threading
import json
import sys
import os

from plotly.subplots import make_subplots
import plotly.graph_objects as go

def start():
    company = symbol_input.get("1.0",'end-1c')
    def information():
        tab1.delete('all')
        print(var.get())
        text_1 = tab1.create_text(100,20,text="please wait....",font=("Arial",15))

        if var.get() == "IND":
            data = requests.get("https://www.screener.in/company/{0}/".format(company.upper()))
            if data.status_code == 200:
                soup = BeautifulSoup(data.content,"lxml")
                inf = soup.find_all("div",{"class":"sub show-more-box about"})
                txt = ""
                for el in inf:
                    txt += el.get_text()
                txt = txt.split()
            else:
                messagebox.showerror("Error","Cannot collect data at this time. Try again later.")
                tk.Canvas.delete(tab1,text_1)
                tab1.create_text(20,20,anchor="nw",text="try again",font=("Arial,15"))
                return
        
        else:
            data = yfinance.Ticker(company)
            inf = data.info
            df_inf = pd.DataFrame().from_dict(inf,orient='index')
            try:
                desc = df_inf.iloc[3]
            except:
                messagebox.showerror("Error","Cannot collect data at this time. Try again later.")
                tk.Canvas.delete(tab1,text_1)
                tab1.create_text(20,20,anchor="nw",text="try again",font=("Arial,15"))
                return
            with open("file.txt","w") as f:
                f.write(desc[0])
                f.close()
            txt = []
            with open("file.txt","r") as f:
                for line in f:
                    for word in line.split():
                        txt.append(word)
                f.close()

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
        tk.Canvas.delete(tab1,text_1)

        f = open("real.txt","r")
        tab1.create_text(20,0,anchor="nw",text=f.read(),font=("Century Schoolbook",15))
        f.close()

    def sentiment_analysis():

        tab2.delete('all')

        if var.get() == "IND":
            tab2.create_text(20,20,anchor="nw",text="This service is not available for NSE stocks",font=("Arial",15))
            return
        
        def tv_win():
            tv_page = tk.Toplevel(root)
            tv_page.title("table view")
            df = pd.DataFrame(table)
            tv = ttk.Treeview(tv_page)
            cols = []
            for i in df.columns:
                cols.append(i)
            tv['columns']= tuple(cols)
            tv['show'] = 'headings'
            tv.column('#0', width=0, stretch=tk.NO)
            tv.column('0', anchor=tk.CENTER, width=80)
            tv.column('1', anchor=tk.CENTER, width=80)
            tv.column('2', anchor=tk.CENTER, width=80)
            tv.column('3', anchor=tk.CENTER, width=80)
            tv.column('4', anchor=tk.CENTER, width=80)
            tv.column('5', anchor=tk.CENTER, width=80)

            tv.heading('#0', text='', anchor=tk.CENTER)
            tv.heading('0', text=cols[0], anchor=tk.CENTER)
            tv.heading('1', text=cols[1], anchor=tk.CENTER)
            tv.heading('2', text=cols[2], anchor=tk.CENTER)
            tv.heading('3', text=cols[3], anchor=tk.CENTER)
            tv.heading('4', text=cols[4], anchor=tk.CENTER)
            tv.heading('5', text=cols[5], anchor=tk.CENTER)
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
        tk.Canvas.delete(tab2, text_2)
        w = 10
        for i in news:
            tab2.create_text(20,w,text="➡"+i[0] + "  ( "+i[2]+" )",anchor='nw',font=("Century Schoolbook",15))
            w += 40
        tab2.create_text(50,220,anchor="nw",text="News Sentiment Analysis: "+ str(sentiment['Mean Sentiment'][0]),font=("Century Schoolbook",15),fill='red')        
        tv_btn = tk.Button(tab2,text="click here for full details",command=tv_win,width=20,height =2,font=("Arial",10),border=10,borderwidth=5)
        tv_btn.pack(pady=80,padx=10,side=tk.LEFT)

    def stock_prediction():
        tab3.delete('all')
        global img
        text_3 = tab3.create_text(50,10,anchor='nw',text="please wait....",font=("Arial",15))
        stock = {"name":company,"feature":"stock prediction","exchange":var.get()}
        r = requests.post("http://127.0.0.1:8000/",data=stock)
        r = r.content
        r = json.loads(r)

        #check if dictionay is empty
        if not r:
            Canvas.delete(tab3,text_3)
            tab3.create_text(50,10,anchor='nw',text="No data available",font=("Arial",15))
            return

        tk.Canvas.delete(tab3,text_3)
        text_3 = tab3.create_text(50,10,anchor='nw',text="Loading graphs....",font=("Arial",15))

        if "saved_graphs" not in os.listdir():
            os.mkdir("saved_graphs")
        df = pd.DataFrame(r["prediction"])
        df1  = pd.DataFrame(r["output"])
        fig = make_subplots(rows=1,cols=2,subplot_titles=("15 days Prediction","Current values with predicted values"))
        fig.add_trace(go.Scatter(x=df.index,y=df.values.reshape(df.shape[0])),row=1,col=1)
        fig.add_trace(go.Scatter(x=df1.index,y=df1.values.reshape(df1.shape[0])),row=1,col=2)
        fig.update_layout(height=600,width=1000)
        fig.update_xaxes(title_text="Time")
        fig.update_yaxes(title_text="Prediction")
        fig.write_image("saved_graphs/"+"plot.png")
        img = ImageTk.PhotoImage(Image.open("saved_graphs/"+"plot.png"))
        
        tk.Canvas.delete(tab3,text_3)
        
        tab3.create_image(0,0,image=img,anchor="nw")

        vbar = tk.Scrollbar(TabControl,orient=tk.VERTICAL)
        vbar.pack(anchor='e',fill='y',expand=True)
        vbar.config(command=tab3.yview)
        tab3.config(yscrollcommand=vbar.set)
        tab3.config(scrollregion=tab3.bbox("all"))

        print("done")

        
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


root = tk.Tk()
root.title("Stock Projection")
root.geometry('700x400')
root.config(bg='#429ef5')

var = tk.StringVar()

menubar = tk.Menu(root)
option = tk.Menu(menubar,tearoff=0)
option.add_command(label="Restart",command=restart_program)
option.add_command(label="Exit",command=root.quit)
menubar.add_cascade(label="options",menu=option)
root.config(menu=menubar)

name = tk.Label(root,text="Stock Projection")
name.configure(font=('Arial',20),fg='Black',bg='lightgrey',width=200)
name.pack()

label1 = tk.Label(root,text="Enter the stock symbol",border=5)
label1.pack(side='left',anchor='n',pady=20)
r1 = tk.Radiobutton(root,text="US",variable=var,value="US")
r2 = tk.Radiobutton(root,text="IND",variable=var,value="IND")
r1.place(x=10,y=100)
r2.place(x=10,y=130)
symbol_input = tk.Text(root)
symbol_input.config(height=1,width=13,border=3,borderwidth=5)
symbol_input.place(x=5,y=160)
btn = tk.Button(root,text='okay',command=start,width=10,border=5,borderwidth=5,bg='lightgreen')
btn.place(x=10,y=190)

TabControl = ttk.Notebook(root)
tab1 = tk.Canvas(TabControl,bg='lightgrey')
tab2 = tk.Canvas(TabControl,bg='lightgrey')
tab3 = tk.Canvas(TabControl,bg='lightgrey')



TabControl.add(tab1,text='Description')
TabControl.add(tab2,text='News Sentiment Analysis')
TabControl.add(tab3,text='Stock Price Forecast')
TabControl.pack(side=tk.LEFT,expand=True,fill='both')

root.mainloop()
