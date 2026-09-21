from tkinter import *
import os

import matplotlib
import pandas as pd
import numpy as np
import ctypes
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
except Exception:
    pass
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import scipy.stats as stat
from sklearn.metrics import r2_score
import statsmodels.api as sm

data = pd.read_csv("Advertising.csv")
data.drop(['Unnamed: 0'], axis=1)

# plt.figure(figsize=(16, 8))

X = data['SN']
y = data['sales']
X2 = sm.add_constant(X)
est = sm.OLS(y, X2)
est2 = est.fit()
print(est2.summary())

Xs = data.drop(['sales', 'Unnamed: 0','views_SN','views_YT','views_TV'], axis=1)
y = data['sales'].values.reshape(-1,1)
reg = LinearRegression()
reg.fit(Xs, y)
print(reg.coef_)
print(reg.intercept_)
print("The linear model is: Y = {:.5} + {:.5}*SN + {:.5}*YT + {:.5}*TV".format(reg.intercept_[0], reg.coef_[0][0], reg.coef_[0][1], reg.coef_[0][2]))

reg.score(Xs, y)

X = np.column_stack((data['SN'], data['YT'], data['TV']))
y = data['sales']
X2 = sm.add_constant(X)
est = sm.OLS(y, X2)
est2 = est.fit()
print(est2.summary())

N = len(data)
k = round(N**0.5)

coef = pd.DataFrame({'coef': [reg.coef_[0][0], reg.coef_[0][1], reg.coef_[0][2]], 'name': ['sn', 'yt', 'tv']})
coef = coef.sort_values(by='coef', ignore_index=True)

CostByView = [round(data["SN"]*1000/data["views_SN"],2),round(data["YT"]*1000/data["views_YT"],2),round(data["TV"]*1000/data["views_TV"],2)]
AvgCost = [round(np.average(CostByView[0]),2),round(np.average(CostByView[1]),2),round(np.average(CostByView[2]),2)]
AvgViews = [round(np.average(data['views_SN']),0), round(np.average(data['views_YT']),0), round(np.average(data['views_TV']),0)]

root = Tk()
root.title("Main")
root.geometry('400x300+100+50')
button1 = Button(text="Calculate ad revenue")
button1.place(x=125, y=50, width=150)
button2 = Button(text="Auto Assistant")
button2.place(x=125, y=130, width=150)
button3 = Button(text="Add new data")
button3.place(x=125, y=210, width=150)

def AddW1(event):
    f1 = Toplevel()
    f1.title("Count")
    f1.geometry('400x400')
    count_f1 = Label(f1)
    count_f1.place(x=20, y=270)
    def count():
        inv1 = float(invSN.get())
        inv2 = float(invYT.get())
        inv3 = float(invTV.get())
        sales = reg.intercept_[0] + reg.coef_[0][0]*inv1 + reg.coef_[0][1]*inv2 + reg.coef_[0][2]*inv3
        count_f1.config(text="Your earnings will be $"+str(round(sales, 2))+"k.")
    def regr_sn():
        X = data['SN'].values.reshape(-1, 1)
        y = data['sales'].values.reshape(-1, 1)
        reg = LinearRegression()
        reg.fit(X, y)
        predictions = reg.predict(X)
        plt.figure(figsize=(16, 8))
        plt.scatter(
            data['SN'],
            data['sales'],
            c='black'
        )
        plt.plot(
            data['SN'],
            predictions,
            c='blue',
            linewidth=2
        )
        plt.xlabel("Money spent on SN ads ($)")
        plt.ylabel("Sales ($)")
        plt.show()

    def regr_yt():
        X = data['YT'].values.reshape(-1, 1)
        y = data['sales'].values.reshape(-1, 1)
        reg = LinearRegression()
        reg.fit(X, y)
        predictions = reg.predict(X)
        plt.figure(figsize=(16, 8))
        plt.scatter(
            data['YT'],
            data['sales'],
            c='black'
        )
        plt.plot(
            data['YT'],
            predictions,
            c='blue',
            linewidth=2
        )
        plt.xlabel("Money spent on YT ads ($)")
        plt.ylabel("Sales ($)")
        plt.show()

    def regr_tv():
        X = data['TV'].values.reshape(-1, 1)
        y = data['sales'].values.reshape(-1, 1)
        reg = LinearRegression()
        reg.fit(X, y)
        predictions = reg.predict(X)
        plt.figure(figsize=(16, 8))
        plt.scatter(
            data['TV'],
            data['sales'],
            c='black'
        )
        plt.plot(
            data['TV'],
            predictions,
            c='blue',
            linewidth=2
        )
        plt.xlabel("Money spent on TV ads ($)")
        plt.ylabel("Sales ($)")
        plt.show()
    def hist_sn():
        histogr, b = np.histogram(data['SN'], k, density=True)
        plt.hist(data['SN'], bins=b, density=True)

        xx = np.linspace(np.min(data['SN']), np.max(data['SN']), 100)
        Mx = np.average(data['SN'])
        Sx = np.std(data['SN'])
        y = ((1 / (np.sqrt(2 * np.pi) * Sx)) * np.exp(-0.5 * (1 / Sx * (xx - Mx)) ** 2))

        plt.plot(xx, y, '-r')

        a, dd, p = stat.gamma.fit(data['SN'])

        yyy = stat.gamma.pdf(xx, a=a, loc=dd, scale=p)
        plt.plot(xx, yyy, '--c')
        plt.show()

    def hist_yt():
        histogr, b = np.histogram(data['YT'], k, density=True)
        plt.hist(data['YT'], bins=b, density=True)

        xx = np.linspace(np.min(data['YT']), np.max(data['YT']), 100)
        Mx = np.average(data['YT'])
        Sx = np.std(data['YT'])
        y = ((1 / (np.sqrt(2 * np.pi) * Sx)) * np.exp(-0.5 * (1 / Sx * (xx - Mx)) ** 2))

        plt.plot(xx, y, '-r')

        a, dd, p = stat.gamma.fit(data['YT'])

        yyy = stat.gamma.pdf(xx, a=a, loc=dd, scale=p)
        plt.plot(xx, yyy, '--c')
        plt.show()

    def hist_tv():
        histogr, b = np.histogram(data['TV'], k, density=True)
        plt.hist(data['TV'], bins=b, density=True)

        xx = np.linspace(np.min(data['TV']), np.max(data['TV']), 100)
        Mx = np.average(data['TV'])
        Sx = np.std(data['TV'])
        y = ((1 / (np.sqrt(2 * np.pi) * Sx)) * np.exp(-0.5 * (1 / Sx * (xx - Mx)) ** 2))

        plt.plot(xx, y, '-r')

        a, dd, p = stat.gamma.fit(data['TV'])

        yyy = stat.gamma.pdf(xx, a=a, loc=dd, scale=p)
        plt.plot(xx, yyy, '--c')
        plt.show()
    Label(f1, text="Spread the cost of advertising:").place(x=10,y=10)
    Label(f1, text="Social network").place(x=20, y=40)
    invSN = Entry(f1, width=10)
    invSN.place(x=20, y=70)
    Label(f1, text="YouTube").place(x=20, y=110)
    invYT = Entry(f1, width=10)
    invYT.place(x=20, y=150)
    Label(f1, text="TV").place(x=20, y=190)
    invTV = Entry(f1, width=10)
    invTV.place(x=20, y=230)
    Button(f1, text="Count",width=20, command=count).place(x=20,y=310)
    Button(f1, text="上", width=4, command=regr_sn).place(x=250, y=60)
    Button(f1, text="上", width=4, command=regr_yt).place(x=250, y=140)
    Button(f1, text="上", width=4, command=regr_tv).place(x=250, y=220)
    Button(f1, text="日", width=4, command=hist_sn).place(x=300, y=60)
    Button(f1, text="日", width=4, command=hist_yt).place(x=300, y=140)
    Button(f1, text="日", width=4, command=hist_tv).place(x=300, y=220)

def AddW2(event):
    f2 = Toplevel()
    f2.title("Assistant")
    f2.geometry('500x250')
    count1_f2 = Label(f2)
    count1_f2.place(x=20, y=90)
    count2_f2 = Label(f2)
    count2_f2.place(x=20, y=130)
    def find_best():
        invest = float(all_inv.get())*1000
        profit_sn = 0.0
        profit_yt = 0.0
        profit_tv = 0.0
        if coef['coef'][2] > 0:
            if coef['name'][2] == 'sn':
                if round(invest / AvgCost[0], 0) <= AvgViews[0]:
                    profit_sn = invest
                    invest = invest - profit_sn
                else:
                    profit_sn = round(AvgViews[0] * AvgCost[0])
                    invest = invest - profit_sn
                    if coef['coef'][1] > 0:
                        if coef['name'][1] == 'yt':
                            if round(invest / AvgCost[1], 0) <= AvgViews[1]:
                                profit_yt = invest
                                invest = invest - profit_yt
                            else:
                                profit_yt = round(AvgViews[1] * AvgCost[1])
                                if coef['coef'][0] > 0:
                                    profit_tv = invest - profit_yt
                                invest = invest - profit_yt - profit_tv
                        else:
                            if round(invest / AvgCost[2], 0) <= AvgViews[2]:
                                profit_tv = invest
                                invest = invest - profit_tv
                            else:
                                profit_tv = round(AvgViews[2] * AvgCost[2])
                                if coef['coef'][0] > 0:
                                    profit_yt = invest - profit_tv
                                invest = invest - profit_tv - profit_yt
            elif coef['name'][2] == 'yt':
                if round(invest / AvgCost[1], 0) <= AvgViews[1]:
                    profit_yt = invest
                    invest = invest - profit_yt
                else:
                    profit_yt = round(AvgViews[1] * AvgCost[1])
                    invest = invest - profit_yt
                    if coef['coef'][1] > 0:
                        if coef['name'][1] == 'sn':
                            if round(invest / AvgCost[0], 0) <= AvgViews[0]:
                                profit_sn = invest
                                invest = invest - profit_sn
                            else:
                                profit_sn = round(AvgViews[0] * AvgCost[0])
                                if coef['coef'][0] > 0:
                                    profit_tv = invest - profit_sn
                                invest = invest - profit_sn - profit_tv
                        else:
                            if round(invest / AvgCost[2], 0) <= AvgViews[2]:
                                profit_tv = invest
                                invest = invest - profit_tv
                            else:
                                profit_tv = round(AvgViews[2] * AvgCost[2])
                                if coef['coef'][0] > 0:
                                    profit_sn = invest - profit_tv
                                invest = invest - profit_tv - profit_sn
            else:
                if round(invest / AvgCost[2], 0) <= AvgViews[2]:
                    profit_tv = invest
                    invest = invest - profit_tv
                else:
                    profit_tv = round(AvgViews[2] * AvgCost[2])
                    invest = invest - profit_tv
                    if coef['coef'][1] > 0:
                        if coef['name'][1] == 'yt':
                            if round(invest / AvgCost[1], 0) <= AvgViews[1]:
                                profit_yt = invest
                                invest = invest - profit_yt
                            else:
                                profit_yt = round(AvgViews[1] * AvgCost[1])
                                if coef['coef'][0] > 0:
                                    profit_sn = invest - profit_yt
                                invest = invest - profit_yt - profit_sn
                        else:
                            if round(invest / AvgCost[0], 0) <= AvgViews[0]:
                                profit_sn = invest
                                invest = invest - profit_sn
                            else:
                                profit_sn = round(AvgViews[0] * AvgCost[0])
                                if coef['coef'][0] > 0:
                                    profit_yt = invest - profit_sn
                                invest = invest - profit_sn - profit_yt

        profit_sn = round(profit_sn / 1000, 1)
        profit_yt = round(profit_yt / 1000, 1)
        profit_tv = round(profit_tv / 1000, 1)
        earnig = reg.intercept_[0] + reg.coef_[0][0] * profit_sn + reg.coef_[0][1] * profit_yt + reg.coef_[0][2] * profit_tv
        count1_f2.config(text="Your earnings will be $" + str(round(earnig, 2))+"k.")
        count2_f2.config(text="Deposits in SN $"+str(profit_sn)+"k, in YT "+str(profit_yt)+"k, in TV $"+str(profit_tv)+"k, and rest $"+str(round(invest/1000,1))+"k.")

    Label(f2, text="Enter your advertising costs:").place(x=10, y=10)
    all_inv = Entry(f2, width=10)
    all_inv.place(x=20, y=50)
    Button(f2, text="Find", width=20, command=find_best).place(x=20, y=170)

def AddW3(event):
    def AddData():
        SN_add = str(dataSN.get())
        YT_add = str(dataYT.get())
        TV_add = str(dataTV.get())
        SNV_add = str(dataVSN.get())
        YTV_add = str(dataVYT.get())
        TVV_add = str(dataVTV.get())
        flen = len(pd.read_csv("Advertising.csv"))
        add_str = '\n' + str(flen+1) + ',' + SN_add + ',' + YT_add + ',' + TV_add + ',' + SNV_add  + ',' + YTV_add  + ',' + TVV_add
        f_add = open("Advertising.csv",'a')
        f_add.write(add_str)
        f_add.close()

    def open_data():
        os.startfile("Advertising.csv")
    f3 = Toplevel()
    f3.title("Data")
    f3.geometry('350x600')
    Label(f3, text="Enter your data:").place(x=10, y=10)
    Label(f3, text="Social network").place(x=20, y=50)
    dataSN = Entry(f3, width=10)
    dataSN.place(x=20, y=90)
    Label(f3, text="YouTube").place(x=20, y=130)
    dataYT = Entry(f3, width=10)
    dataYT.place(x=20, y=170)
    Label(f3, text="TV").place(x=20, y=210)
    dataTV = Entry(f3, width=10)
    dataTV.place(x=20, y=250)
    Label(f3, text="Views on social network").place(x=20, y=290)
    dataVSN = Entry(f3, width=10)
    dataVSN.place(x=20, y=330)
    Label(f3, text="Views on YouTube").place(x=20, y=370)
    dataVYT = Entry(f3, width=10)
    dataVYT.place(x=20, y=410)
    Label(f3, text="Views on TV").place(x=20, y=450)
    dataVTV = Entry(f3, width=10)
    dataVTV.place(x=20, y=490)
    Button(f3, text="Add", width=20, command=AddData).place(x=20, y=530)
    Button(f3, text="三", width=4, command=open_data).place(x=250, y=80)

button1.bind('<Button-1>', AddW1)
button2.bind('<Button-1>', AddW2)
button3.bind('<Button-1>', AddW3)
root.mainloop()