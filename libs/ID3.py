# -*- coding: utf-8 -*-
import re
import pandas as pd
import math
import json
import csv
import os
from libs.subset import subset
'''
0209 -- CCC 各種暴力解orz
>RID解決完了
>中繼資料要去掉要能讀到-分析後.csv那個file_path line73-75那邊
>subset輸出解決了，但是出來之後有中括號跟引號，我暫時去不掉，寫在analyze-qui-stage2.py line42-47
'''

'''
2022.02.07--Pan 開工大吉
1.我在每一個class的建構子都加了重設所有參數的method,如果後來你有加新的class variable,
  記得要加到resest_all函示裡.
2.解決了之前怪怪ㄉ部分惹,現在要用遞迴的方式才能取出所有的priamry_keys了,拿gain也是用遞迴去
unclean_subsets裡面拿raw_data class 的東東.
3.阿你要用的部分就是:   
    (1)RID處理一下
    (2)中繼資料.csv看可不可以用掉
    (3)等建興說每個分離前的gainA要以啥樣子的csv匯出,你再用個ㄅㄟ

'''

'''
2022.01.25--Pan
1.read_in_csv那個函數要用self去拿class級別的variable,這樣才其他地方才吃的到
2.阿然後你先改read_in_csv好惹
3.clean data 可以用 raw_data().export_result()拿到所有的primary_key.你可以看一夏#遞迴的部分
  現在變成最一開始的raw_data裡面有所有的clean跟unclean資料,分別在clean_subsets跟unclean_subsets李
Noted:
-->然後我發現最好在建構子的地方都把會出錯的variable都clear一下,這樣好像才不會出事,我也不知為啥
-->上面那件事好像又有機會出事,我也不知道為啥
-->然後我有加一個三種結論ㄉcsv,你可以試試看      >> test過了基本上是對的我沒發現啥錯啦
-->阿png那個有分類的過程,attribute排序的部分我都是預設的,紅線部分是分出來clean,藍線分出來是unclean
-->阿你可以直接run,看個結果
'''
class attr_gaiaA():
    gainA_list = pd.DataFrame()
    file_path = ''

    def export(self, file_path):
        print(self.gainA_list)
        # 判斷是否第一次讀寫
        if self.file_path != file_path:
            self.file_path = file_path
            self.gainA_list.to_csv(file_path, index = False, encoding='utf-8-sig')
            self.gainA_list = pd.DataFrame() #reset
        #如果該子集是空的不寫<<不知道為啥有空的
        elif not self.gainA_list.empty:
            self.gainA_list.to_csv(file_path, mode = 'a', index = False, header= False, encoding='utf-8')
            self.gainA_list = pd.DataFrame() #reset


class clean_data:
    '''
    只記錄primary keys，然後會丟conclusion，用來算class distribution
    阿conclusion你在自己用ㄍ
    '''
    original_header=list()
    primary_keys=dict() #主key
    conclusions=list()  #結論
    support=0.0 #
    reliability=0.0
    class_distribution="" #ex: "4,0"
    simplicity=0.0
    deep=0.0
    clean_data=pd.DataFrame()
    result={} #最終輸出dict 藥用dict to 
    policy = pd.DataFrame()
    output = pd.DataFrame()

    def __init__(self,primary_keys=None,clean_data=None,original_header=None,conclusions=None,support=None,output = None):
        self.reset_all()
        self.policy= pd.DataFrame()
        self.clean_data=pd.DataFrame()
        self.primary_keys=primary_keys #傳入primary key會是dict
        self.original_header=original_header
        self.clean_data=clean_data #是pd.DataFrame()
        self.conclusions=conclusions
        self.support=support #Support
        self.output = output
        
        '''
        要去掉中繼資料ㄉ話這裡可以讀到-分析後.csv那個file_path就行ㄌ，直接弄掉就好
        '''    
        # for col in output: 
        #     self.policy[col] = [""]
        
    #Reset所有參數
    def reset_all(self):
        self.original_header=list()
        self.primary_keys=dict() #主key
        self.conclusions=list()  #結論
        self.support=0.0 #
        self.reliability=0.0
        self.class_distribution="" #ex: "4,0"
        self.simplicity=0.0
        self.deep=0.0
        self.clean_data=pd.DataFrame()
        self.result={} #最終輸出dict 藥用dict to 
        self.policy = pd.DataFrame()
        self.output = pd.DataFrame()
        

    def cal_all(self, output):
        #處理最後輸出位置
        # new_path=result_filepath.replace('.csv','-分析後.csv')
        
        self.deep=len(self.primary_keys)-1 #Deep
        self.simplicity=self.support/self.deep #Simplicity
        
        #處理class distribution的部分
        #先sort self.conclusion確保都是['不好', '好']      
        self.conclusions.sort()
        class_d=list()
        for one_conclusion in self.conclusions: #初始化class_d
            class_d.append(0)
            
        for index,v in self.clean_data.iterrows():
            temp_a=list()
            for one_conclusion in self.conclusions:
                if(one_conclusion == v[-1]):
                    temp_a.append(1)
                else:
                    temp_a.append(0)
            class_d=[a+b for a,b in zip(class_d,temp_a)]
        # print('class_d',class_d) #class_d [0, 4]
        self.class_distribution=",".join(list([str(class_d_str) for class_d_str in class_d]))
        
        
        self.reliability=self.support/sum(class_d)#Reliability的部分
        count = 1
        for k,v in self.primary_keys.items():
            if count == len(self.primary_keys):
                self.result['Class']=v
            else:
                self.result[k]=v
            count+=1
        # 全部加到 result dict李
        self.result["Deep"]=self.deep
        self.result["Support"]=self.support
        self.result["Reliability"]=self.reliability
        self.result["Class Distribution"]=self.class_distribution
        self.result["Simplicity"]=self.simplicity
        self.result["RID"] = self.output.shape[0] + 1
        # for key in self.result.keys():
        #     self.policy[key] = self.result[key]
        self.output.loc[self.output.shape[0]] = self.result
        # print(self.output)
        # self.policy.to_csv(new_path, mode = 'a', header = False, index = False,encoding='utf-8-sig') #輸出用append的方式家道csv

        
    def export_result(self,result_filepath):
        #處理最後輸出位置
        new_path = result_filepath.replace('.csv','-分析後.csv')
        self.cal_all(self.output)
        # print(self.primary_keys,'===>',self.class_distribution)

class raw_data:
    conclusions = {} #結論 ex: {好:2,不好:5}
    conclusion_col = ""
    raw_source=pd.DataFrame()
    class_info=0.0  #類別訊息獲取量
    attributes={}  #建字典對到 effect attribute
    original_header=list()
    '''
    attributes['天氣']=effect_attribute('天氣')
    '''
    primary_keys=dict() #唯一分辨的key
    clean_subsets=[] #其他的clean subset 裡面存 clean_data class
    unclean_subsets=[]  #其他的unclean subset 裡面存raw_data class
    is_Head=False #是否是開頭
    outputData = pd.DataFrame() # 存放output
    
    export_gainA = attr_gaiaA()
    #建構子
    def __init__(self,file_path=None,dataframe=None,primary_keys=None,is_Head=False,first = False, oldPolicy = None):
        '''
        先判定是否需要讀csv,若不用就直接用現有dataframe建立
        之後就先建立attri字典
        '''
        self.reset_all()
        if first:
            self.outputData = pd.DataFrame() # reset output data
        #直接相等會讓primary_keys的型態變成None
        if(primary_keys!=None):
            self.primary_keys=primary_keys #傳入primary key會是dict
        self.is_Head=is_Head
        self.load_data(file_path=file_path,data=dataframe,first=first, oldPolicy = oldPolicy)
        self.sort_attri_order() #排序gainA
        self.reorder_raw_source() #依照attribute的gainA去重新排列data
        self.extract_to_subsets()  #分離clean與unclean資料
        
    #Reset所有參數
    def reset_all(self):
        # self.conclusions = {} #結論 ex: {好:2,不好:5}
        self.conclusion_col = ""
        self.raw_source=pd.DataFrame()
        self.class_info=0.0  #類別訊息獲取量
        self.attributes={}  #建字典對到 effect attribute
        self.original_header=list()
        self.primary_keys=dict() #唯一分辨的key
        self.clean_subsets=[] #其他的clean subset 裡面存 clean_data class
        self.unclean_subsets=[]  #其他的unclean subset 裡面存raw_data class
        self.export_gainA.file_path = ''
        is_Head=False #是否是開頭
        
    def get_ruleSum_sim(self):
        self.outputData.drop_duplicates(subset = self.outputData.columns[1:-5], keep = 'first', inplace = True)
        return self.outputData['RID'].shape[0], self.outputData['Simplicity'].sum()
    #分離unclean跟clean資料
    def extract_to_subsets(self):
        '''
        分離unclean跟clean資料
        '''
        temp_dict_to_check={}
        temp_dict_to_cast={}
        temp_dict_series_dataframe_clean={}
        temp_dict_series_dataframe_unclean={}

        for index,row in self.raw_source.iterrows(): #先檢查
            if(row[0] not in temp_dict_to_check):#第一次被讀到
                temp_dict_to_check[row[0]]=True #True 代表是clean data, False代表是 unclean data
                temp_dict_to_cast[row[0]]=row[-1]
                continue
            if(row[-1]!=temp_dict_to_cast[row[0]]):#不等於
                temp_dict_to_check[row[0]]=False
        for index,row in self.raw_source.iterrows(): #分類
            if(temp_dict_to_check[row[0]]): #clean data 丟到clean data
                if(row[0] not in temp_dict_series_dataframe_clean):
                    temp_dict_series_dataframe_clean[row[0]]=row.to_frame(0).T
                else:
                    temp_dict_series_dataframe_clean[row[0]]=temp_dict_series_dataframe_clean[row[0]].append(row.to_frame(0).T,ignore_index=True)
            else: #unclean data 把unclean丟到unclean data
                if(row[0] not in temp_dict_series_dataframe_unclean):
                    temp_dict_series_dataframe_unclean[row[0]]=row.to_frame(0).T
                else:
                    temp_dict_series_dataframe_unclean[row[0]]=temp_dict_series_dataframe_unclean[row[0]].append(row.to_frame(0).T,ignore_index=True)
        
        '''
        下面是可以用來測試,分別看現在乾淨資料與不乾淨資料
        print('乾淨')
        for clean in temp_dict_series_dataframe_clean.values():
            print(clean)        
        print('不乾淨')
        for unclean in temp_dict_series_dataframe_unclean.values():
            print(unclean)        
        '''
        
        if(len(temp_dict_series_dataframe_clean) != 0):
            for clean in dict(temp_dict_series_dataframe_clean).values():
                temp_primary_k_clean=dict(self.primary_keys)    #處理primary key
                temp_primary_k_clean[clean.columns[0]]=(clean[clean.columns[0]][0])
                temp_primary_k_clean[clean.columns[-1]]=(clean[clean.columns[-1]][0])
                self.clean_subsets.append(clean_data(primary_keys=temp_primary_k_clean,original_header=self.original_header,clean_data=clean,conclusions=list(self.conclusions.keys()),support=clean.shape[0], output = self.outputData))
                    
        if(len(temp_dict_series_dataframe_unclean) != 0):
            for unclean in dict(temp_dict_series_dataframe_unclean).values(): #匯出unclean data,記得刪除第一航並加primary key(一個list)
                temp_primary_k_unclean=dict(self.primary_keys)  #處理primary key
                temp_primary_k_unclean[unclean.columns[0]]=(unclean[unclean.columns[0]][0])
                tempOutput = raw_data(file_path=None,dataframe=(unclean.drop(columns=unclean.columns[0])),primary_keys=temp_primary_k_unclean, first = 'unclean', oldPolicy = self.outputData)

                self.unclean_subsets.append(tempOutput)
                tempOutput.export_result('')
        
    #排序gainA
    def sort_attri_order(self):
        self.attributes=dict(sorted(self.attributes.items(), key=lambda item: item[1].gainA,reverse=True)) #照gainA升冪排序
        
    def reorder_raw_source(self):
        newOrder=list(self.attributes.keys())
        newOrder.append(self.raw_source.columns[-1]) #加上結論
        self.raw_source=self.raw_source[newOrder]
        self.raw_source=self.raw_source.sort_values(self.raw_source.columns[0],ascending=True)
    
    #載入df回傳effect_attributes
    def load_data(self, file_path = None, data = None, first = False, oldPolicy = None):
        self.raw_source = data
        if first == True:
            policy = pd.DataFrame()
            policy['RID'] = []
            for effect in self.raw_source.columns[:-1]:
                policy[effect] = []
            policy['Class'] = []
            policy['Deep'] = []
            policy['Support'] = []
            policy['Reliability'] = []
            policy['Class Distribution'] = []
            policy['Simplicity'] = []
            self.outputData = policy
        elif first == 'unclean':
            self.outputData = oldPolicy

        # if file_path == None: #不用讀csv
        #     self.raw_source = data
        # else:
        #     self.raw_source = pd.read_csv(file_path,encoding='utf-8-sig') #讀檔
        #     policy = pd.DataFrame()
        #     # 設定clean_data的data
        #     # clean_data.data = self.raw_source
        #     # 初始化policy(export)的dataframe
            # policy['RID'] = []
            # for effect in self.raw_source.columns[:-1]:
            #     policy[effect] = []
            # policy['Class'] = []
            # policy['Deep'] = []
            # policy['Support'] = []
            # policy['Reliability'] = []
            # policy['Class Distribution'] = []
            # policy['Simplicity'] = []
            
            # output_filename = file_path.replace('.csv','-分析後.csv')
            # policy.to_csv(output_filename, index = False,encoding='utf-8-sig')
            # policy.to_csv('中繼資料.csv', index = False,encoding='utf-8-sig')

        self.original_header=self.raw_source.columns
        self.s_col = self.raw_source.columns[-1] #直接這樣就好惹  記錄結論的欄位名
        counter=0 #用來算資料總數
        for index,one in self.raw_source[self.s_col].iteritems():
            if(one not in self.conclusions):
                self.conclusions[one]=1
            else:
                self.conclusions[one]+=1
            counter+=1
        data_sum=counter #資料總數
        # print(list(self.conclusions.values()))
        self.class_info=self.cal_i(list(self.conclusions.values())) #算類別訊息輛
        for col in self.raw_source.columns[:-1]:
            self.attributes[col]=effect_attribute(name=col,conclusion=list(self.conclusions.keys()),gainA=self.class_info,dataframe=self.raw_source[[col,self.raw_source.columns[-1]]])
    #遞迴的部分
    def export_result(self,result_filepath):
        # print('乾淨節點數:',len(self.clean_subsets),"不乾淨節點數:",len(self.unclean_subsets))
        for unclean_subset in self.unclean_subsets:
            unclean_subset.export_result(result_filepath)
        for clean_subset in self.clean_subsets:
            clean_subset.export_result(result_filepath)
        result_filepath=result_filepath.replace('.csv','-分析後.csv')
        return result_filepath
    
    def get_all_gainA_test(self,result_filepath):
        words_to_write=list() #準備被寫入的list
        if( self.is_Head ):
            words_to_write.append(['Title==>',json.dumps(self.primary_keys,ensure_ascii=False).encode('utf8').decode()])
            words_to_write.append(['屬性','','Gain(A)'])
            words_to_write.append(['結論',str(self.class_info),''])
            for attr in self.attributes.values():
                words_to_write.append([attr.effect_attr_name,attr.attr_info,attr.gainA])
                
            with open(result_filepath,'a',encoding='utf-8-sig',newline='') as f:
                writer=csv.writer(f)
                writer.writerows(words_to_write)
            words_to_write.clear()
            
        for unclean_subset in self.unclean_subsets:
            words_to_write.append(['Title==>',json.dumps(unclean_subset.primary_keys,ensure_ascii=False).encode('utf8').decode()])
            words_to_write.append(['屬性','','Gain(A)'])
            words_to_write.append(['結論',str(unclean_subset.class_info),''])
            for attr in unclean_subset.attributes.values():
                words_to_write.append([attr.effect_attr_name,attr.attr_info,attr.gainA])
            with open(result_filepath,'a',encoding='utf-8-sig',newline='') as f:
                writer=csv.writer(f)
                writer.writerows(words_to_write)
            words_to_write.clear()
            
        for unclean_subset in self.unclean_subsets:
            unclean_subset.get_all_gainA_test(result_filepath)
                
            
        return result_filepath
    
    def reset_all_subsets_file(self,filepath):
        try:
            os.remove(filepath)
        except:
            pass
        
    def cal_i(self,x):
        '''
        用來算 I( X , Y )
        x=[5,9],x是list 
        '''
        total_count=0
        for one in x:
            total_count+=one
        sum=0.0
        for one in x:
            if(one==0):
                continue
            temp=(-one/total_count)*math.log2((one/total_count))
            sum+=temp
        return sum
                
    
class effect_attribute:
    con_num = 0 #存結論數量
    ss = []   #結論
    attr_subset = {}  #屬性對應結論
    parent_gainA = 0.0   #上層屬性訊息獲取量
    attr_info = 0.0  #屬性訊息量
    effect_attr_name = ""    #屬性名稱
    attr_data=pd.DataFrame() 
    gainA=0.0
    
    '''
    attr_subset={}
    conclusions=["不好","好"]

    ====>晴朗,炎熱,高,無,不好
    讀一行原始資料，讀到一個結論(當作 a="不好")

    for one_conclusion in conclusions:
        if(a == one_conclusion):
            attr_subset[ one_conclusion ] += 1
        else:
            pass

    attr_subset=>
    {"晴朗" : [1,0],
    "陰天" : [1,1],
    "雨天" : [0,2]}

    '''
    def __init__(self, name, conclusion, gainA, dataframe):
        
        self.attr_subset.clear() #0207
        
        self.reset_all() 
        
        
        self.effect_attr_name = name
        self.ss = conclusion
        self.parent_gainA = gainA
        self.con_num = len(conclusion)
        self.attr_data=dataframe

        self.caculate_attr()
    
    def reset_all(self):
        self.con_num = 0 #存結論數量
        self.ss = []   #結論
        self.attr_subset = {}  #屬性對應結論
        self.parent_gainA = 0.0   #上層屬性訊息獲取量
        self.attr_info = 0.0  #屬性訊息量
        self.effect_attr_name = ""    #屬性名稱
        self.attr_data=pd.DataFrame() 
        self.gainA=0.0
    
        
    def cal_i(self,x):
        '''
        用來算 I( X , Y )
        x=[5,9],x是list 
        '''
        total_count=0
        for one in x:
            total_count+=one
        sum=0.0
        for one in x:
            if(one==0):
                continue
            temp=(-one/total_count)*math.log2((one/total_count))
            sum+=temp
        return sum
    def caculate_attr(self):
        for index,raw in self.attr_data.iterrows(): #設定attr_subset
            if(raw[0] not in self.attr_subset): #第一次讀到
                temp_list=list()
                for one_conclusion in self.ss:
                    if(raw[1] == one_conclusion):
                        temp_list.append(1)
                    else:
                        temp_list.append(0)
                self.attr_subset[raw[0]]=temp_list
            else: #不是第一次讀到
                temp_list=list()
                for one_conclusion in self.ss:
                    if(raw[1] == one_conclusion):
                        temp_list.append(1)
                    else:
                        temp_list.append(0)
                self.attr_subset[raw[0]]=[a+b for a,b in zip(list(self.attr_subset[raw[0]]),temp_list)] 
        #算gain A
        for one in self.attr_subset.values():
            self.attr_info+=(sum(one)/self.attr_data.shape[0])*self.cal_i(one)
        self.gainA=self.parent_gainA-self.attr_info #結論-自己的屬性訊息量=GainA    
        
        

def main():
    panMain()    

def panMain():
    test=raw_data(file_path='./Weather-MoreData.csv',is_Head=True)# pan
    test.export_result("./Weather-MoreData_測試匯出.csv")
    test.reset_all_subsets_file('./Weather-MoreData_分析過程子集.csv')
    test.get_all_gainA_test('./Weather-MoreData_分析過程子集.csv')
    
    pass

if __name__ == "__main__":
    main()

#檢查CSV是否符合規則
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
                    pass
                    # return False,"csv檔第  "+str(index)+"  行的歸納結果不符合命名規則\n歸納結果的命名規則為:任意字元(不可以穿插數字)+數字\n"
                for item in temp:
                    if(item=="" or item==None):
                        return False,"csv檔第  "+str(index)+"  行有欄位為空\n"
            index+=1
        return True,"csv檔檢查通過,符合格式\n"
      
#分離相容與不相容資料    
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
            tempSubset = subset(tempRow, tolerance)
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
    #                 tempSubset=subset(oneRow, tolerance)
    #                 classSorted[tuple(oneRow[:-1])]=tempSubset
    #             else:
    #                 classSorted[tuple(oneRow[:-1])].addData(oneRow)
    #         index+=1
    # cleanDataFileName=filename.replace('.csv','-clean.csv')
    # uncleanDataFileName=filename.replace('.csv','-unclean.csv')
    
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
    #         cleanData,uncleanData=oneSubset.exportCleanAndUncleanData()
    #         if(cleanData !=None):
    #             cleanWriter.writerows(cleanData)
    #         if(uncleanData!=None):
    #             uncleanWriter.writerows(uncleanData)
        
    # return cleanDataFileName,uncleanDataFileName,'',True
