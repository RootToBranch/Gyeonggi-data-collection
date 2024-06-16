import pandas as pd
import os

from normalize import normalize

file_list = os.listdir("./data/dual_direction_before")

# 결과 데이터프레임 정의
final = pd.DataFrame(columns=["연도", "시간대", "교통량"])

for path in file_list:
    year = str(path.split("_")[0])


    
    # 이름이 .csv 로 끝나는 파일만 허용
    if path.endswith('.csv') == False:
        continue
    # 넣을 데이터를 담아둘 데이터프레임 정의
    filtered_data = pd.DataFrame()

    df = pd.read_csv('./data/dual_direction_before/{}'.format(path), encoding='UTF-8')

    


    # normalize로 인코딩 방식을 통일함 (통일하지 않았더니 인코딩 방식이 달라 조건문에서 감지하지 못하는 경우가 있음)

    # 수집 데이터 정의에 있던 column 필터링

    if normalize(path) not in [normalize("2007_수시교통량.csv"), normalize("2012_수시교통량.csv")]:
        continue
    
    # 방향이 1인 것과 2인 것의 교통량 합치기
    df_combined = df.groupby(['지점번호', '년', '월', '일', '시간']).agg({
        '1종': 'sum', '2종': 'sum', '3종': 'sum', '4종': 'sum', '5종': 'sum', 
        '6종': 'sum', '7종': 'sum', '8종': 'sum', '9종': 'sum', '10종': 'sum', 
        '11종': 'sum', '12종': 'sum', '계': 'sum'
    }).reset_index()

    # 방향을 0으로 설정
    df_combined['방향'] = 0

    # 기존 데이터에서 방향이 1인 것과 2인 것을 제외하고 추출
    df_filtered = df[df['방향'].isin([1, 2])]

    # 방향이 1인 것과 2인 것을 제외한 데이터프레임 생성
    df_rest = df[~df['방향'].isin([1, 2])]

    # 수정된 데이터를 다시 합치기
    final_df = pd.concat([df_rest, df_combined])

    # 결과를 CSV 파일로 저장 (필요시)
    final_df.to_csv("data/"+ path, index=False)