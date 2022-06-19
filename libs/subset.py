class subset:
    resultDistribution={} #{'好':2 , '不好':1}
    attribution=[] #['晴朗','炎熱','高','無']
    tolerance=0.0
    
    def __init__(self,rowData,tolerance):
        self.resultDistribution={} #{'好':2 , '不好':1}
        self.attribution=[] #['晴朗','炎熱','高','無']
        self.tolerance=tolerance
        
        self.attribution=rowData[:-1]
        self.resultDistribution[rowData[-1]]=1
        
        
    def addData(self,newData):
        if(newData[-1] not in self.resultDistribution):
            self.resultDistribution[newData[-1]]=1
        else:
            self.resultDistribution[newData[-1]]+=1

            
    def exportCleanAndUncleanData(self):
        cleanArray=[]   #放乾淨資料 ex: [ ['晴朗','炎熱','高','無'],['晴朗','炎熱','高','無'] ]
        uncleanArray=[] #放不乾淨資料 ex: [ ['晴朗','炎熱','高','無'],['晴朗','炎熱','高','無'] ]
        
        
        #先判定輸入tolerance值是否有大於現有reliability
        if((max(self.resultDistribution.values()) / sum(self.resultDistribution.values())) >= self.tolerance):
            #大於輸入tolerance值
            for result,times in self.resultDistribution.items():
                #是主要結果
                if(times==max(self.resultDistribution.values())):
                    #有幾個就加幾個回去
                    for _ in range(0,times):
                        tempList=list(self.attribution) #tempList是用來把self.atribution + result用的
                        tempList.append(result)
                        cleanArray.append(tempList)
                #不是主要結果
                else:
                    #有幾個就加幾個回去
                    for _ in range(0,times):
                        tempList=list(self.attribution) #tempList是用來把self.atribution + result用的
                        tempList.append(result)
                        uncleanArray.append(tempList)
        
        else:
            #小於輸入tolerance值
            for result,times in self.resultDistribution.items():
                for _ in range(0,times):
                    tempList=list(self.attribution) #tempList是用來把self.atribution + result用的
                    tempList.append(result)
                    uncleanArray.append(tempList)
        return cleanArray,uncleanArray
                
            
