from chi_square_module import raw_data
def test():
    data = raw_data(file_path = 'F:/NUK/建新RA/卡方/James_RA_NEW/10-EWI-8.csv')
    
    for feature in data.data_features.values():
        if(feature.feature_con_domain==None):
            print("值域:"+feature.feature_name+",值域出現值,機率分配,,")
            for k in feature.feature_domain.keys():
                print(feature.feature_name+","+str(feature.feature_domain[k])+","+str(feature.prob[k])+",,")
        else:
            print("值域:"+feature.feature_name+",,值域卡方值,特徵值域合計卡方值,")
            for k,v in feature.feature_con_domain.items():
                print(str(k)+","+str(v.domain_appear)+","+str(v.chi_square)+",")
            print(",,,"+str(feature.feature_chi_square)+",")
            
def exportChiSquareCsvFile(inputFilePath,outputFilePath):
    try:
        with open(file=outputFilePath,encoding='utf-8-sig',newline='',mode='w')as out :
            data = raw_data(file_path = inputFilePath)
            total_chi_square=0.0
            for feature in data.data_features.values():
                if(feature.feature_con_domain==None):
                    out.write("值域:"+feature.feature_name+",值域出現值,機率分配,特徵值域合計卡方值,\n")
                    for k in feature.feature_domain.keys():
                        out.write(k+","+str(feature.feature_domain[k])+","+str(feature.prob[k])+",,\n")
                else:
                    out.write("值域:"+feature.feature_name+",,值域卡方值,,\n")
                    for k,v in feature.feature_con_domain.items():
                        out.write(str(k)+","+str(v.domain_appear)+","+str(v.chi_square)+",\n")
                    out.write(",,,"+str(feature.feature_chi_square)+",\n")
                    total_chi_square+=feature.feature_chi_square
            out.write(",,,,\n")       
            out.write(",,,特徵卡方值,\n")
            out.write(",,,"+str(total_chi_square)+",\n")
        return True,outputFilePath
    except Exception as  err:
        return False,err
    


if __name__ == "__main__":
    # exportChiSquareCsvFile(inputFilePath='F:/NUK/建新RA/卡方/James_RA_NEW/Weather-排序.csv',outputFilePath='F:/NUK/建新RA/卡方/James_RA_NEW/Weather-排序-結果.csv')
    test()
