from numpy import source
import pandas as pd
from libs.chi_square_module import raw_data
from libs.ID3 import exportUncleanDataNew as exportUnclean
from libs.analysis_stage1 import csvAnalyzeData as csvAnalyze
from libs.ID3 import raw_data as ID3_raw_data
from operator import itemgetter





"""
分工

part1 : getImcomRatio + getRuleNum +getSimplicity

part2 : 其他ㄉmethod + gui + 打包


"""




"""
範例CSV

Weather,Temperature,Humidity,Wind,Go-on-a-picnic
Cloud,Hot,High,No,Good
Cloud,Hot,Normal,No,Good
Cloud,Hot,Normal,No,Good
Cloud,Moderate,High,Yes,Good
Rainy,Hot,Normal,No,Good
Rainy,Hot,Normal,Yes,No
Rainy,Moderate,High,No,Good
Rainy,Moderate,High,Yes,No
Rainy,Moderate,Normal,No,Good
Sunny,Hot,High,No,No
Sunny,Hot,High,Yes,No
Sunny,Hot,Normal,No,Good
Sunny,Moderate,High,No,No
Sunny,Moderate,Normal,Yes,Good

"""

"""
_summary_
    
    class variable : 
        sourceCsv -- (pd.DataFrame)
            -都用這個來讀原始資料,減少IO時間
        dataNums  -- (int)
            -資料筆數
        attrNums  -- (int)
            -特徵數
        
"""


#測試執行ㄉ地方
def main():
    sum=summary("./Weather-MoreData.csv")
    sum.exportResult("./Weather-MoreData-Summary-test.csv")
    # sum.getOtherNums()
    # print(sum.getImcomRatio) #測試印出不相容率
    
    pass


class summary:
    
    def __init__(self,filePath) ->None:
        self.sourceCsv=pd.read_csv(filePath)
        self.dataNums=0
        self.attrNums=0
        self.classNums={}
        self.cleanDatas = []
        self.header = []
        self.simplicity = {}
        self.subsetDataNums = {} # 資料筆數
        self.extractRate = {} # 萃取率
        self.ruleSimplicityRate = {} # 規則精簡率
        pass
    
    
    def getImcomRatio(self,sortedCol) -> dict:
        """
        算不相容率
        
        return : (dict) 
        
        e.g: { "Weather-clean" : 0.11, "Weather/Temperature-clean" : 0.22, ... , "Weather/Temperature/Humidity/Wind-clean" : 0.55 }
        
        """
        imcomRatioDict = {}
        header = []
        # for row in self.sourceCsv:
        #     self.header.append(row)
        
        for row in sortedCol:
            self.header.append(row)
        self.header.append(self.sourceCsv.columns[-1])
            
        # print(self.sourceCsv[[header[0],header[-1]]])
        for col in range(0,len(self.header) - 1):
            tempList = self.header[0:col+1]
            tempList.append(self.header[-1])
            # print(tempList)
            uncleanRate, cleanData = exportUnclean(self.sourceCsv[tempList])
            self.cleanDatas.append(cleanData)
            tempStr = ''
            for item in self.header[0:col+1]:
                tempStr += item + '/'
            tempStr = tempStr.rstrip('/') + '-clean'
            imcomRatioDict[tempStr] = uncleanRate
            # print(f'{tempStr}:{uncleanRate}')
        # uncleanRate, cleanData = exportUnclean(self.sourceCsv)
        # print(imcomRatioDict)
        return imcomRatioDict
        
        # return { "Weather-clean" : 0.13, "Weather/Temperature-clean" : 0.15,"Weather/Temperature/Humidity/Wind-clean" : 0.16 }
    
    def getRuleNum(self) -> dict:
        """
        算規則數
        
        return : (dict) 
        
        e.g: { "Weather-clean" : 3, "Weather/Temperature-clean" : 5, ... , "Weather/Temperature/Humidity/Wind-clean" : 6 }
        
        """
        ruleNumDict = {}
        for cleanData in self.cleanDatas:
            result = ID3_raw_data(dataframe = cleanData, first = True)
            result.export_result('')
            ruleSum, sim = result.get_ruleSum_sim()
            # ruleSum, sim = csvAnalyze(cleanData)
            tempStr = ''
            for item in cleanData:
                if item == self.header[-1]:
                    break
                tempStr += item + '/'
            tempStr = tempStr.rstrip('/') + '-clean'
            ruleNumDict[tempStr] = ruleSum
            self.simplicity[tempStr] = sim
            self.subsetDataNums[tempStr] = len(cleanData)
            self.extractRate[tempStr] = len(cleanData) / ruleSum
            self.ruleSimplicityRate[tempStr] = sim / ruleSum
            
        return ruleNumDict
        # return { "Weather-clean" : 3, "Weather/Temperature-clean" : 5,"Weather/Temperature/Humidity/Wind-clean" : 6 }
    
    def getSimplicity(self) -> dict:
        """
        算Simplicity
        
        return : (dict) 
        
        e.g: { "Weather-clean" : 13, "Weather/Temperature-clean" : 15, ... , "Weather/Temperature/Humidity/Wind-clean" : 16 }
        
        """
        return self.simplicity
        # return { "Weather-clean" : 13, "Weather/Temperature-clean" : 15,"Weather/Temperature/Humidity/Wind-clean" : 16 }
    
    def getChiSquareList(self) -> list:
        """
        依照特徵卡方值排序
        
        return : (list) (已經排好的大盜小)
        
        e.g: [ ["Weather",5],["Temperature",4],["Humidity",3],["Wind",2] ]
        
        """
        
        sortedList=[]
        data = raw_data(sourceFile=self.sourceCsv)
        for feature in data.data_features.values():
            if(feature.feature_con_domain==None):
                pass
            else:
                sortedList.append([feature.feature_name,feature.feature_chi_square])
        
        sortedList= sorted(sortedList, key=itemgetter(1),reverse=True)

        sortedCol=[x[0] for x in sortedList]

        return sortedList,sortedCol
    
    def getOtherNums(self) :
        """
        算資料筆數，不用回傳
        """
        self.dataNums=len(self.sourceCsv.index) 
        self.attrNums=len(self.sourceCsv.columns)-1
        for one in self.sourceCsv[self.sourceCsv.columns[-1]]:
            if one not in self.classNums:
                self.classNums[one]=1
            else:
                self.classNums[one]+=1
        
        tempTotal=0
        for v in self.classNums.values():
            tempTotal+=v
        for key in self.classNums.keys():
            self.classNums[key]=tuple([self.classNums[key],self.classNums[key]/tempTotal])
        # print(self.classNums)
        # return self.dataNums,self.attrNums

    
    def exportResult(self,exportFileName) -> None:
        """
        輸出output
        檔名 = 舊黨名_Summary.csv
        """
        
        with open(exportFileName,encoding='utf-8-sig',newline='',mode='w')as out:
            # imcomRatio={ "Weather-clean" : 13, "Weather/Temperature-clean" : 15,  "Weather/Temperature/Humidity/Wind-clean" : 16 }
            # ruleNum={ "Weather-clean" : 3, "Weather/Temperature-clean" : 5,  "Weather/Temperature/Humidity/Wind-clean" : 6 }
            # simplicity={ "Weather-clean" : 30, "Weather/Temperature-clean" : 54,  "Weather/Temperature/Humidity/Wind-clean" : 60 }
            try:
                self.getOtherNums()
                sortedList,sortedCol=self.getChiSquareList()
                imcomRatio=self.getImcomRatio(sortedCol=sortedCol)
                ruleNum=self.getRuleNum()
                simplicity=self.getSimplicity()
            except Exception as err:
                err.with_traceback
            out.write("資料筆數,"+str(self.dataNums)+"\n")
            out.write("特徵數,"+str(self.attrNums)+"\n")
            out.write("Class分配")
            for k,v in self.classNums.items():
                out.write(","+str(k)+","+str(v[0])+","+str(v[1])+"\n")
            out.write("特徵卡方值與排序(大到小)")
            for one in sortedList:
                out.write(","+one[0]+"-clean-"+str(one[1])+"\n")
            out.write(",不相容率,規則數,精簡度,資料筆數,萃取率,規則精簡率\n")
            
            for key in imcomRatio.keys():
                out.write(key+","+str(imcomRatio[key])+","+str(ruleNum[key])+","+str(simplicity[key])+","+str(self.subsetDataNums[key])+","+str(self.extractRate[key])+","+str(self.ruleSimplicityRate[key])+"\n")

            
        
    
    
    
if __name__ == "__main__":
    main()