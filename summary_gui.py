# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter.constants import BOTTOM
from tkinter.filedialog import askopenfilename
from summary_controller import summary

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
        
    def exportChiSquare(self):
        if(self.filename==""):
            self.writeToMiniConsole('還沒有選擇欲彙整總攬的csv檔\n')
            return
        outputFilePath=self.filename.replace('.csv','-Summary.csv')
        sum=summary(self.filename)
        sum.exportResult(outputFilePath)
        self.writeToMiniConsole('彙整總攬輸出至==>'+outputFilePath+'\n')
        self.miniConsole.config(state='disable')
        
        
    def onChange(self,event):
        self.rule.set(event.widget.get("end-1c linestart", "end-1c"))   
    def on_closing(self): 
        self.isOkay=True
        self.window.destroy()
    def __init__(self):
        self.window = tk.Tk()
        self.window.title('計算特徵卡分值')
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
        
        #計算特徵卡分值
        exportUnclean=tk.Button(topFrame,text='彙整總攬',fg='Red',command=self.exportChiSquare)
        exportUnclean.grid(column=0, row=2,pady=10)
        
        
        
        
        #mini console
        self.miniConsole=tk.Text(bottomFrame,fg="Black",state='disable',width=80,height=10,relief='solid',borderwidth=2,font=('Arial', 13))
        self.miniConsole.grid(column=0, row=0)
        self.miniConsole.bind("<Return>",self.onChange)
        
        self.rule=tk.StringVar()
        
        
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.window.mainloop()

if __name__ == '__main__':
    gui=analyzeGui()
    
    


