import pandas as pd
import os

from normalize import normalize

file_list = os.listdir("./data")

# 결과 데이터프레임 정의
final = pd.DataFrame(columns=["연도", "시간대", "교통량"])

time_define_obj = {
    1: "01시~02시",
    2: "02시~03시",
    3: "03시~04시",
    4: "04시~05시",
    5: "05시~06시",
    6: "06시~07시",
    7: "07시~08시",
    8: "08시~09시",
    9: "09시~10시",
    10: "10시~11시",
    11: "11시~12시",
    12: "12시~13시",
    13: "13시~14시",
    14: "14시~15시",
    15: "15시~16시",
    16: "16시~17시",
    17: "17시~18시",
    18: "18시~19시",
    19: "19시~20시",
    20: "20시~21시",
    21: "21시~22시",
    22: "22시~23시",
    23: "23시~24시",
    24: "00시~01시"
}

for path in file_list:
    year = str(path.split("_")[0])


    
    # 이름이 .csv 로 끝나는 파일만 허용
    if path.endswith('.csv') == False:
        continue
    # 넣을 데이터를 담아둘 데이터프레임 정의
    filtered_data = pd.DataFrame()

    data = pd.read_csv('./data/{}'.format(path), encoding='UTF-8')

    


    # normalize로 인코딩 방식을 통일함 (통일하지 않았더니 인코딩 방식이 달라 조건문에서 감지하지 못하는 경우가 있음)

    # 수집 데이터 정의에 있던 column 필터링

    default_column_name = ['시간', '계', '방향']
    unique_number_column_name = ""


    if normalize("2020_수시교통량.csv") == normalize(path):
        data = data[["지점번호", '호선구분', '시간대', '교통량', "차종", "방향"]]
        unique_number_column_name = "지점번호"

    elif normalize("2007_수시교통량.csv") == normalize(path) or \
        normalize("2012_수시교통량.csv") == normalize(path):
        data = data[default_column_name + ["지점번호"]]
        unique_number_column_name = "지점번호"

    elif normalize("2017_수시교통량.csv") == normalize(path):
        data = data[default_column_name + ["조사지점"]]
        unique_number_column_name = "조사지점"
    

    
    # 결과 데이터프레임에 저장할 데어터들의 column 정의
    columns = ["연도", "시간대", "교통량"]


    count = 0
    # 데이터의 길이만큼 반복
    for k in range(len(data)):
        
        unique_number_column = str(data[unique_number_column_name].iloc[k])
        
        if normalize("2020_수시교통량.csv") == normalize(path):
            
            # 수집 데이터 정의의 조건 작성

            if str(data['방향'].iloc[k]) != "양방향":
                continue
                

            if str(data['호선구분'].iloc[k]) == "고속국도" and data['차종'].iloc[k] == "합계":
                
                if unique_number_column.startswith("0013") or (unique_number_column.startswith("13") and len(str(unique_number_column)) == 3):
                        
                    if str(data['시간대'].iloc[k]) not in ["주간", "전일"]:
                        filtered_data = pd.DataFrame([[year, data['시간대'].iloc[k], data['교통량'].iloc[k]]], columns=["연도", "시간대", "교통량"])
                        final = pd.concat([final, filtered_data])

                
        
        elif normalize(path) in [normalize("2012_수시교통량.csv"), normalize("2017_수시교통량.csv"), normalize("2007_수시교통량.csv")]:
            if str(data['시간'].iloc[k]) not in ["25", "26", "주간", "전일"]:
                if unique_number_column.startswith("0013") or (unique_number_column.startswith("13") and len(str(unique_number_column)) == 3): 
                    time = data['시간'].iloc[k]
                    if normalize(path) == normalize("2017_수시교통량.csv"):
                        if str(data['방향'].iloc[k]) != "0":
                            continue

                    
                    if normalize(path) == [normalize("2007_수시교통량.csv"), normalize("2012_수시교통량.csv")]:
                        if str(data['방향'].iloc[k]) != "0":
                            continue
                    
                    if normalize(path) in [normalize("2007_수시교통량.csv"), normalize("2017_수시교통량.csv")]:
                        time = time_define_obj[int(time)]
                    if normalize(path) == normalize("2012_수시교통량.csv"):
                        time = time.split("~")
                        if(int(time[0]) < 10):
                            time[0] = "0" + time[0]
                        if(int(time[1]) < 10):
                            time[1] = "0" + time[1]
                        
                        print(data.iloc[k])
                        
                        time = time[0] + "시~" + time[1] + "시"

                    # if normalize(path) in [normalize("2007_수시교통량.csv"), normalize("2017_수시교통량.csv")]:

                    #     filtered_data = pd.DataFrame([[year, time, data['계'].iloc[k]]], columns=["연도", "시간대", "교통량"])
                    #     final = pd.concat([final, filtered_data])
                    # else:
                            
                    filtered_data = pd.DataFrame([[year, time, data['계'].iloc[k]]], columns=["연도", "시간대", "교통량"])
                    final = pd.concat([final, filtered_data])
        
        else: 
            continue
        
            
# 결과 데이터프레임를 csv로 변환

final.to_csv('formatted_data.csv', encoding = 'utf-8', index=False)