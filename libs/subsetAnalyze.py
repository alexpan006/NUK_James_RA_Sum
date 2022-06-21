#encoding=utf8
class subset:
    isHead=False    #是否是代表
    deep=0  #深度
    support=0   #支持比數
    reliabilty=0    #可信度
    reliabiltyDisplay=""
    classDistribution={} #dictionary version of class Distribution
    classDistributionOutput=""
    finalClass=""
    simplicity=0
    simplicityDisplay=""
    

    # primaryKeys=[]  
    def __init__(self,conditions,result):
        self.conditions=conditions
        self.result={result:1}
        self.iniResult=result
        self.primaryKeys=[self.conditions[0]]
    def __lt__(self, other):
         return self.deep < other.deep
    def mergeData(self,anotherData):
        if(self.conditions==anotherData.conditions):
            if(anotherData.iniResult in self.result):
                self.result[anotherData.iniResult]+=1
            else:
                self.result[anotherData.iniResult]=1
            return True
        else:
            return False
    def updatePrimaryKeys(self):
        self.primaryKeys=self.conditions[:(self.conditions.index(self.primaryKeys[-1])+2)] 
    def setClassDistribution(self,order):
        for key in order:
            order[key]=0
        self.classDistribution=order
        for resultKey in self.result:
            self.classDistribution[resultKey]=self.result[resultKey]
    def setAllOther(self):
        self.deep=len(self.primaryKeys) 
        bigger=0
        allPos=0
        for sKey in self.result:
            allPos+=self.result[sKey]
            if(self.result[sKey]>bigger):
                bigger=self.result[sKey]
                self.support=bigger
                self.finalClass=str(sKey)
        self.reliabilty=self.support/allPos
        for cd in self.classDistribution:
            self.classDistributionOutput+=str(self.classDistribution[cd])+"," 
        self.classDistributionOutput=self.classDistributionOutput[:-1]
        self.simplicity=(1/self.deep)*self.support
        self.reliabiltyDisplay=format(round(self.reliabilty,4),'.4f')
        self.simplicityDisplay=format(round(self.simplicity,2),'.2f') 
    
    def getUncleanData(self,tolerance=0.7):
        # print('conditions--',self.conditions)
        uncleanData=[]
        cleanData=[]
        try:
            if(self.reliabilty>=tolerance): #當tolerance 小於 reliability
                for k,v in self.classDistribution.items():
                    if(v<self.support and v>0):
                        uncleantemp=list(self.conditions)
                        uncleantemp.append(k)
                        for _ in range(v):
                            uncleanData.append(uncleantemp)
                    elif(v>=self.support):
                        cleantemp=list(self.conditions)
                        cleantemp.append(k)
                        for _ in range(v):
                            cleanData.append(cleantemp)
            else:   #當tolerance 大於 reliability
                for k,v in self.classDistribution.items():
                    if(v>0):
                        uncleantemp=list(self.conditions)
                        uncleantemp.append(k)
                        for _ in range(v):
                            uncleanData.append(uncleantemp)
        except Exception as err:
            print('出錯了',err)
            return cleanData,uncleanData
        # print(cleanData)
        # print(uncleanData)
        return cleanData,uncleanData
        
        
    def getResult(self):
        print("primary keys ==>",self.primaryKeys)
        print('final class ==>',self.finalClass)
        print('deep ==>',self.deep)
        print('support ==>',self.support)
        print('reliability ==>',self.reliabilty)
        print('class distribution ==>',self.classDistribution)
        print('condition ==>',self.conditions)
        