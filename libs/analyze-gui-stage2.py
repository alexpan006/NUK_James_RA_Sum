# -*- coding: utf-8 -*-
from os import error, stat
from time import sleep, time
import tkinter as tk
from tkinter.constants import BOTTOM
from tkinter.filedialog import askopenfilename, test
from tkinter import ttk 
from ID3 import attr_gaiaA, csvValidCheck,exportUncleanDataNew
from ID3 import clean_data
from ID3 import raw_data
import csv
import pandas as pd

class analyzeGui:
    filename=""
    #選檔案
    def showChooseFile(self):
        self.rule.set('')
        self.filename = askopenfilename() # show an "Open" dialog box and return the path to the selected file
        self.writeToMiniConsole("你選擇的檔案路徑為-->"+self.filename+"\n")
    #寫到小panel
    def writeToMiniConsole(self,string):
        self.miniConsole.config(state='normal')
        self.miniConsole.insert('insert',string)
        self.miniConsole.config(state='disable')
        self.miniConsole.see(tk.END)
        
    def exportUnclean(self):
        if(self.filename==""):
            self.writeToMiniConsole('還沒有選擇欲分離不相容資料的csv檔\n')
            return
        self.isOkay=False
        while(not self.isOkay):
            self.writeToMiniConsole('請輸入相容資料的接受等級(一定要大於0.51)，輸入完請按Enter :\n')
            self.miniConsole.config(state='normal')
            self.miniConsole.wait_variable(self.rule)
            if(self.rule.get()==None or self.rule.get()==''):
                continue
            if(float(self.rule.get())<=0.5):
                continue
            clean,unclean,state,self.isOkay=exportUncleanDataNew(self.filename,float(self.rule.get()))
            if(not self.isOkay):
                self.writeToMiniConsole('出錯'+state+"\n")
        self.writeToMiniConsole('相容資料以輸出至==>'+clean+"\n"+'不相容資料以輸出至==>'+unclean+'\n')
        self.miniConsole.config(state='disable')
        
        
    #開始分析
    def startAnalyze(self, sourceFile):
        # source = raw_data(dataframe = sourceFile)
        # result = source.export_result(sourceFile)
        result = raw_data(dataframe = sourceFile).export_result()
        resultToken=False
        if(self.filename==""):
            self.writeToMiniConsole('還沒有選擇欲分析的csv檔\n')
            return
        try:
            resultToken,result=csvValidCheck(self.filename)
        except :
            self.writeToMiniConsole('發生預期外的錯誤1\n')
        if(resultToken):
            try:
                source=raw_data(file_path=self.filename,is_Head=True)
                result=source.export_result(self.filename)
                #處理all subsets部分
                all_subsets_filepath=self.filename.replace('.csv','-分析過程子集.csv')
                source.reset_all_subsets_file(all_subsets_filepath) 
                all_subsets=source.get_all_gainA_test(result_filepath=all_subsets_filepath)
                '''
                寫這 在call個函數ㄅ
                '''    
                # sum
                data = pd.read_csv(result)
                data = data.append({'RID':'','Support':data['Support'].sum(),'Simplicity':data['Simplicity'].sum()}, ignore_index = True)
                data.to_csv(result, index = False,encoding='utf-8-sig')
                self.writeToMiniConsole('分析完成,輸出結果位於-->'+result+'\n')
                self.writeToMiniConsole('分析完成,分析過程子集合位於-->'+all_subsets+'\n')
            except Exception as err:
                self.writeToMiniConsole('發生預期外的錯誤2\n')
                self.writeToMiniConsole(err)
        else:
            self.writeToMiniConsole('原始csv不符合格式:\n'+result)
    def onChange(self,event):
        self.rule.set(event.widget.get("end-1c linestart", "end-1c"))   
    def on_closing(self): 
        self.isOkay=True
        self.window.destroy()
    def __init__(self):
        self.window = tk.Tk()
        self.window.title('ID3決策規則分析')
        self.window.geometry('700x500')
        topFrame=tk.Frame(self.window)
        topFrame.pack()
        bottomFrame=tk.Frame(self.window)
        bottomFrame.pack(side=BOTTOM)
        #檔案路徑label
        lbl_1 = tk.Label(topFrame, text='Csv檔案路徑:', fg='#263238', font=('Arial', 12))
        lbl_1.grid(column=0, row=0,pady=10)

        #選擇button
        chooseCsvFile=tk.Button(topFrame,text='選擇Csv檔案',fg='Green',command=self.showChooseFile)
        chooseCsvFile.grid(column=0, row=1,pady=10)
        
        #分離不相容
        exportUnclean=tk.Button(topFrame,text='分離不相容資料',fg='Green',command=self.exportUnclean)
        exportUnclean.grid(column=0, row=2,pady=10)
        
        
        # #規則欄位排序
        # sortRule=tk.Button(topFrame,text='規則欄位排序',fg='Green',command=self.sortRule)
        # sortRule.grid(column=0, row=3,pady=10)
        
        
        
        
        #開始分析button
        startButton=tk.Button(topFrame,text='產生決策規則',fg='Red',command=self.startAnalyze)
        startButton.grid(column=0, row=4,pady=20)
        
        
        #mini console
        self.miniConsole=tk.Text(bottomFrame,fg="Black",state='disable',width=80,height=10,relief='solid',borderwidth=2,font=('Arial', 13))
        self.miniConsole.grid(column=0, row=0)
        self.miniConsole.bind("<Return>",self.onChange)
        
        self.rule=tk.StringVar()
        
        
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.window.mainloop()

if __name__ == '__main__':
    gui=analyzeGui()
    
    


