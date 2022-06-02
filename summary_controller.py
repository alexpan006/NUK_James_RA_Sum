import pandas as pd





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
    sum=summary("./Weather-排序.csv")
    #print(sum.getImcomRatio) #測試印出不相容率
    
    pass


class summary:
    
    def __init__(self,filePath) ->None:
        self.sourceCsv=pd.read_csv(filePath)
        pass
    
    
    def getImcomRatio(self) -> dict:
        """
        算不相容率
        
        return : (dict) 
        
        e.g: { "Weather-clean" : 0.11, "Weather/Temperature-clean" : 0.22, ... , "Weather/Temperature/Humidity/Wind-clean" : 0.55 }
        
        """
        pass
    
    def getRuleNum(self) -> dict:
        """
        算規則數
        
        return : (dict) 
        
        e.g: { "Weather-clean" : 3, "Weather/Temperature-clean" : 5, ... , "Weather/Temperature/Humidity/Wind-clean" : 6 }
        
        """

        pass
    
    def getSimplicity(self) -> dict:
        """
        算Simplicity
        
        return : (dict) 
        
        e.g: { "Weather-clean" : 13, "Weather/Temperature-clean" : 15, ... , "Weather/Temperature/Humidity/Wind-clean" : 16 }
        
        """

        pass
    
    def getChiSquareList(self) -> list:
        """
        依照特徵卡方值排序
        
        return : (list) (已經排好的大盜小)
        
        e.g: ["Weather-5","Temperature-4", "Humidity-3","Wind-2"]
        
        """

        pass
    
    def getOtherNums(self) -> None:
        """
        算資料筆數，不用回傳
        """

        pass
    
    def exportResult(self) -> None:
        """
        輸出output
        檔名 = 舊黨名_Summary.csv
        """
        pass
    
    
    
if __name__ == "__main__":
    main()