#encoding=utf8
import csv
from os import write
import re
from typing import Tuple
from libs.subsetExport import subset as exportsubset
from libs.subsetAnalyze import subset as analyzesubset
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
    
def sortRuleRow(filename, newOrder):

    theLastone=''
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
            df = pd.read_csv(filename)
            df_reorder = df[newOrder] # rearrange column here
            df_reorder.to_csv(newFileName, index=False)
            return True,'完成',newFileName,False

def exportUncleanDataNew(sourceFile, tolerance = 0.6):
    classSorted={} # { ['晴朗','炎熱','高','無'] : subset(..), ['晴朗','炎熱','高','有'] : subset(..) }
    header=[] # [ '天氣','氣溫','濕度','風','結論' ]
    for row in sourceFile:
        header.append(row)
    for idx in range(0, len(sourceFile)):
        tempRow = []
        for item in header:
            tempRow.append(sourceFile[item][idx])
        if (tuple(tempRow[:-1]) not in classSorted):
            tempSubset = exportsubset(tempRow, tolerance)
            classSorted[tuple(tempRow[:-1])] = tempSubset
        else:
            classSorted[tuple(tempRow[:-1])].addData(tempRow)
    # with open(sourceFile,'r',encoding="utf-8-sig") as f1:
    #     index=0
    #     lines=f1.readlines()
    #     for line in lines:
    #         if(index==0):
    #             header=line.strip().split(',')
    #         else:
    #             oneRow=line.strip().split(',')
    #             if( tuple(oneRow[:-1]) not in classSorted):
    #                 tempSubset=subset(oneRow,tolerance)
    #                 classSorted[tuple(oneRow[:-1])]=tempSubset
    #             else:
    #                 classSorted[tuple(oneRow[:-1])].addData(oneRow)
    #         index+=1

    # cleanDataFileName=sourceFile.replace('.csv','-clean.csv')
    # uncleanDataFileName=sourceFile.replace('.csv','-unclean.csv')
    
    #輸出檔案
    newCleanData = []
    newUncleanData = []
    cleanDataSum = 0
    uncleanDataSum = 0
    for oneSubset in classSorted.values():
        cleanData, uncleanData = oneSubset.exportCleanAndUncleanData()
        if(cleanData != None):
            # cleanWriter.writerows(cleanData)
            for cData in cleanData:
                if type(cData) == list:
                    newCleanData.append(cData)
                    cleanDataSum += 1
                else:
                    newCleanData.append(cleanData)
                    cleanDataSum += len(cleanData)        
                    break
            # cleanDataSum += 1
        if(uncleanData!= None):
            # uncleanWriter.writerows(uncleanData)
            for ucData in uncleanData:
                if type(ucData) == list:
                    newUncleanData.append(ucData)
                    uncleanDataSum += 1
                else:
                    newUncleanData.append(uncleanData)
                    uncleanDataSum += len(uncleanData)        
                    break
            # newUncleanData.append(uncleanData)
            # uncleanDataSum += 1
    uncleanRate = uncleanDataSum / (cleanDataSum + uncleanDataSum)

    newCleanData = pd.DataFrame(newCleanData, columns = header)
    newUncleanData  = pd.DataFrame(newUncleanData, columns = header)
    return uncleanRate, newCleanData
    # with open(cleanDataFileName,'w',encoding='utf-8-sig',newline='') as cleanF,open(uncleanDataFileName,'w',encoding='utf-8-sig',newline='') as uncleanF:
    #     cleanWriter=csv.writer(cleanF)
    #     uncleanWriter=csv.writer(uncleanF)
    #     #先寫表頭
    #     cleanWriter.writerow(header)
    #     uncleanWriter.writerow(header)
        
    #     for oneSubset in classSorted.values():
    #         cleanData, uncleanData = oneSubset.exportCleanAndUncleanData()
    #         if(cleanData !=None):
    #             cleanWriter.writerows(cleanData)
    #         if(uncleanData!=None):
    #             uncleanWriter.writerows(uncleanData)
    # return cleanDataFileName, uncleanDataFileName, '', True

        
#分離不相容資料        
def exportUncleanData(filename,tolerance):
    allSubset=[] #The arrayList to store all the subset
    classSorted={}
    header=[]
    with open(filename,'r',encoding="utf-8-sig") as f1:
        index=0
        lines=f1.readlines()
        for line in lines:
            if(index==0):
                header=line.strip().split(',')
            else:
                temp=line.strip().split(',')
                tempResult=temp.pop()
                if(tempResult not in classSorted):
                    classSorted[tempResult]=re.sub(r'\D','',tempResult)
                allSubset.append(exportsubset(temp,tempResult))
            index+=1
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
    cleanFileName=filename.replace('.csv','-clean.csv')
    uncleanFileName=filename.replace('.csv','-unclean.csv')
    try:
        with open(cleanFileName,'w',encoding='utf-8-sig',newline='') as cleanf, open(uncleanFileName,'w',encoding='utf-8-sig',newline='') as uncleanf:
            
            cleanCount=0
            uncleanCount=0
            #先寫 clean data
            writer1=csv.writer(cleanf)
            writer1.writerow(header)
            if(len(cleanDatas)!=0):
                for oneCleanSet in cleanDatas:
                    for one1 in oneCleanSet:
                        writer1.writerow(one1)
                        cleanCount+=1
                
            #在寫 unclean data
            writer2=csv.writer(uncleanf)
            writer2.writerow(header)
            if(len(uncleanDatas)!=0):
                for oneUncleanSet in uncleanDatas:
                    for one2 in oneUncleanSet:
                        writer2.writerow(one2)
                        uncleanCount+=1
    except Exception as err:
        print('出錯',err)
        return cleanFileName,uncleanFileName,'出錯'+err,False
    return cleanFileName,uncleanFileName,'',True
    

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
        allSubset.append(analyzesubset(temp,tempResult))
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
    
    

