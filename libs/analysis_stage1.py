#encoding=utf8
import csv
from os import write
import re
from typing import Tuple
from libs.subset import subset
import string
import pandas as pd


def csvValidCheck(filename):
    rowSize=0
    standardRowSize=0
    with open(filename,'r',encoding="utf-8-sig") as f1:
        index=1
        lines=f1.readlines()
        for line in lines:
            temp=line.strip().split(',')
            if(index==1):
                rowSize=len(temp)
            else:
                standardRowSize=len(temp)
                if(rowSize!=standardRowSize):
                    return False,"csv檔第  "+str(index)+"  行的欄位數與其他行不一致\n"
                if(re.fullmatch(r'(\D*)+(\d*)',temp[-1],flags=0)== None):
                    return False,"csv檔第  "+str(index)+"  行的歸納結果不符合命名規則\n歸納結果的命名規則為:任意字元(不可以穿插數字)+數字\n"
                for item in temp:
                    if(item=="" or item==None):
                        return False,"csv檔第  "+str(index)+"  行有欄位為空\n"
            index+=1
        return True,"csv檔檢查通過,符合格式\n"
    
def sortRuleRow(filename,newOrder):
    theLastone=''
    # print('這裡'+newOrder)
    if(newOrder=="" or newOrder==None):
        with open(filename,'r',encoding="utf-8-sig") as f1:
            header=''
            lines=f1.readlines()
            for line in lines:
                header=','.join(line.strip().split(',')[:-1])
                theLastone=line.split(',').pop()
                break
            returnText='目前規則欄位為:'+header+"\n"+'請輸入新的規則欄位排序,請以逗號(,)分隔\n輸入完畢請按enter\n'
        return False,returnText,"",True
    else:
        header=[]
        with open(filename,'r',encoding="utf-8-sig") as f1:
            header=''
            lines=f1.readlines()
            for line in lines:
                header=line.strip().split(',')[:-1]
                theLastone=line.split(',').pop()
                break
        try:
            newOrder=newOrder.strip().split(',')
        except Exception as err:
            return False,('錯誤:'+err+'\n'),True
        if(len(newOrder)!= len(header)):
            print('舊的==>')
            print(header)
            print('新的==>')
            print(newOrder)
            return False,'新規則數量不對,請確認是否有少輸入\n','無檔案',True
        elif( len(header) != len(set(newOrder))):
            print('舊的==>')
            print(header)
            print('新的==>')
            print(newOrder)
            return False,'重複輸入,請確認是否有重複輸入欄位名\n','無檔案',True
        elif( sorted(newOrder) !=sorted(header) ):
            print('舊的==>')
            print(header)
            print('新的==>')
            print(newOrder)
            return False,'錯誤欄位名,請確認是否有打錯欄位名\n','無檔案',True
        else:
            newOrder.append(theLastone.strip())
            newFileName=filename.replace('.csv','-sorted.csv')
            # print('新規則')
            # print(newOrder)
            # print('新黨名:'+newFileName)
            df = pd.read_csv(filename)
            df_reorder = df[newOrder] # rearrange column here
            df_reorder.to_csv(newFileName, index=False)
            return True,'完成',newFileName,False
        
#分離不相容資料        
def exportUncleanData(sourceFile, tolerance = 0.6):
    header = []
    allSubset=[] #The arrayList to store all the subset
    classSorted={}

    for row in sourceFile:
        header.append(row)

    for idx in range(0, len(sourceFile)):
        # print(sourceFile[idx:idx+1])
        temp = []
        for item in header:
            temp.append(sourceFile[item][idx])
        tempResult=temp.pop()
        if(tempResult not in classSorted):
            classSorted[tempResult]=re.sub(r'\D','',tempResult)
        allSubset.append(subset(temp,tempResult))
    
    classSorted=dict(sorted(classSorted.items(), key=lambda item: item[1])) #sort class name
    test={}
    for data in allSubset:
        if(tuple(data.conditions)  not in test):
            test[tuple(data.conditions)]=data
            data.isHead=True
        else:
            test[tuple(data.conditions)].mergeData(data)
    trueData=[one for one in allSubset if one.isHead==True]


    for data in trueData:
        for cdata in list(trueData):
            while(True):
                if(data==cdata):
                    break
                else:
                    if(set(data.primaryKeys).issubset(set(cdata.conditions))):
                        data.updatePrimaryKeys()
                    else:
                        break

    cleanDatas=[]
    uncleanDatas=[]
    check=1
    for unit in trueData:
        unit.setClassDistribution(classSorted)
        unit.setAllOther()
        cleanData,uncleanData=unit.getUncleanData(tolerance)
        cleanDatas.append(cleanData)
        uncleanDatas.append(uncleanData)
        check+=1

    newCleanData = []
    newUncleanData = []
    cleanDataSum = 0
    uncleanDataSum = 0
    for cleanSet in cleanDatas:
        for oneCleanSet in cleanSet:
            newCleanData.append(oneCleanSet)
            cleanDataSum += 1
    for uncleanSet in uncleanDatas:
        for oneUncleanSet in uncleanSet:
            newUncleanData.append(oneUncleanSet)
            uncleanDataSum += 1
    uncleanRate = uncleanDataSum / (cleanDataSum + uncleanDataSum)
    # print(f'不相容率:{uncleanRate}')
    newCleanData = pd.DataFrame(newCleanData, columns = header)
    newUncleanData = pd.DataFrame(newUncleanData, columns = header)

    return uncleanRate, newCleanData
    

def csvAnalyzeData(sourceFile):
    conditionCount=0    #Condition count
    conditionNames=[]   #Condition name
    allSubset=[] #The arrayList to store all the subset
    classSorted={}
    header=[]

    for row in sourceFile:
        header.append(row)
    conditionCount = len(header)
    conditionNames = header[0:-1]
    for idx in range(0, len(sourceFile)):
        # print(sourceFile[idx:idx+1])
        temp = []
        for item in header:
            temp.append(sourceFile[item][idx])
        tempResult=temp.pop()
        if(tempResult not in classSorted):
            classSorted[tempResult]=re.sub(r'\D','',tempResult)
        allSubset.append(subset(temp,tempResult))
    # with open(sourceFile,'r',encoding="utf-8-sig") as f1:
    #     index=0
    #     lines=f1.readlines()
    #     for line in lines:
    #         if(index==0):
    #             conditionCount=len(line.strip().split(','))-1
    #             conditionNames=line.strip().split(',')
    #             conditionNames.pop()
    #         else:
    #             temp=line.strip().split(',')
    #             tempResult=temp.pop()
    #             if(tempResult not in classSorted):
    #                 classSorted[tempResult]=re.sub(r'\D','',tempResult)
    #             allSubset.append(subset(temp,tempResult))
    #         index+=1
    
    classSorted=dict(sorted(classSorted.items(), key=lambda item: item[1])) #sort class name
    test={}
    for data in allSubset:
        if(tuple(data.conditions)  not in test):
            test[tuple(data.conditions)]=data
            data.isHead=True
        else:
            test[tuple(data.conditions)].mergeData(data)
    trueData=[one for one in allSubset if one.isHead==True]


    for data in trueData:
        for cdata in list(trueData):
            while(True):
                if(data==cdata):
                    break
                else:
                    if(set(data.primaryKeys).issubset(set(cdata.conditions))):
                        data.updatePrimaryKeys()
                    else:
                        break



    for unit in trueData:
        unit.setClassDistribution(classSorted)
        unit.setAllOther()
        unit.getResult()
        # print('---------------')
    
    trueData.sort() #Sort data 
    header=[]
    #Header treatment
    header.append("ID")
    alphabet=list(string.ascii_uppercase)
    for i in range(0,conditionCount):
        header.append(alphabet.pop(0))
    header.append("Class")
    header.append("Deep")
    header.append("Support")
    header.append("Reliability")
    header.append("Class Distribution")
    header.append("Simplicity")
    #End of Header treatment#
    # newFileName='./hahahahahatest.csv'
    # with open(newFileName,'w',encoding='utf-8-sig',newline="") as f1:
        # writer=csv.writer(f1)
        # writer.writerow(header)
    ruleIndex=1
    avgSupport=0
    avgReliability=0
    totalSim=0
    for unit in trueData:
        ruleCount="R"+str(ruleIndex)
        oneRow=[]
        oneRow.append(ruleCount)
        for i in unit.primaryKeys:
            oneRow.append(str(i))
        for x in range(0,conditionCount-len(unit.primaryKeys)):
            oneRow.append("")
        oneRow.append(unit.finalClass)
        oneRow.append(unit.deep)
        oneRow.append(unit.support)
        oneRow.append(unit.reliabiltyDisplay)
        oneRow.append(unit.classDistributionOutput)
        oneRow.append(unit.simplicityDisplay)
        totalSim+=unit.simplicity
        avgSupport+=unit.support
        avgReliability+=unit.reliabilty
        # writer.writerow(oneRow)
        ruleIndex+=1
    avgSupport/=len(trueData)
    avgReliability/=len(trueData)
    avgSupport=round(avgSupport,4)
    avgReliability=round(avgReliability,4)
    lastRow=[]
    for i in range(0,conditionCount+3):
        lastRow.append("")
    lastRow.append(format(avgSupport,'.4f'))
    lastRow.append(format(avgReliability,'.4f'))
    lastRow.append("")
    lastRow.append(format(totalSim,'.4f') )
    # writer.writerow(lastRow)
    return ruleIndex, totalSim


if __name__=='__main__':
    pass
    # print('ha')
    csvAnalyzeData('F:/NUK/CSVanaly/dataSet1.csv')
    # token,result=sortRuleRow('F:/NUK/CSVanaly/dataSet1.csv','')
    # print(token+','+result)
    
    

