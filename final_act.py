import pandas as pd
import os

import matplotlib.pyplot as plt
import matplotlib.font_manager as fm


data = pd.read_csv('./formatted_data.csv', encoding='UTF-8')

# 연도, 시간대별로 묶고 교통량 데이터를 합친다
data = data.groupby(['연도', '시간대'])["교통량"].mean()

# 결과 데이터 파일
data.to_csv('final_data.csv', encoding = 'utf-8')


time_define_array = [
    "00시~01시",
    "01시~02시",
    "02시~03시",
    "03시~04시",
    "04시~05시",
    "05시~06시",
    "06시~07시",
    "07시~08시",
    "08시~09시",
    "09시~10시",
    "10시~11시",
    "11시~12시",
    "12시~13시",
    "13시~14시",
    "14시~15시",
    "15시~16시",
    "16시~17시",
    "17시~18시",
    "18시~19시",
    "19시~20시",
    "20시~21시",
    "21시~22시",
    "22시~23시",
    "23시~00시",
]

# array = []
# for k in range(len(data)):
#     array.append()        

data = pd.read_csv('./final_data.csv', encoding='UTF-8')

data_2007 = pd.DataFrame(columns=["시간대", "교통량"])
data_2012 = pd.DataFrame(columns=["시간대", "교통량"])
data_2017 = pd.DataFrame(columns=["시간대", "교통량"])
data_2020 = pd.DataFrame(columns=["시간대", "교통량"])



for i in range(len(data)):
    filtered_data = pd.DataFrame()

    if str(data['연도'].iloc[i]) == "2007":
        filtered_data = pd.DataFrame([[data['시간대'].iloc[i], data['교통량'].iloc[i]]], columns=["시간대", "교통량"])
        data_2007 = pd.concat([data_2007, filtered_data])

    if str(data['연도'].iloc[i]) == "2012":
        filtered_data = pd.DataFrame([[data['시간대'].iloc[i], data['교통량'].iloc[i]]], columns=["시간대", "교통량"])
        data_2012 = pd.concat([data_2012, filtered_data])

    if str(data['연도'].iloc[i]) == "2017":
        filtered_data = pd.DataFrame([[data['시간대'].iloc[i], data['교통량'].iloc[i]]], columns=["시간대", "교통량"])
        data_2017 = pd.concat([data_2017, filtered_data])

    if str(data['연도'].iloc[i]) == "2020":
        filtered_data = pd.DataFrame([[data['시간대'].iloc[i], data['교통량'].iloc[i]]], columns=["시간대", "교통량"])
        data_2020 = pd.concat([data_2020, filtered_data])

# ===== 폰트 설정 =====

# Mac

# plt.tick_params(axis='x', labelsize=10)
# plt.rcParams['font.sans-serif'] = ['Apple SD Gothic Neo']


# Window

font_path = 'C:/Windows/Fonts/malgunsl.ttf'
font_name = fm.FontProperties(fname=font_path).get_name()

plt.rc('font', family=font_name)
plt.rcParams['font.sans-serif'] = [font_name]

# =====================


data_2007 = data_2007.sort_values(by='시간대').reset_index(drop=True)
data_2012 = data_2012.sort_values(by='시간대').reset_index(drop=True)
data_2017 = data_2017.sort_values(by='시간대').reset_index(drop=True)
data_2020 = data_2020.sort_values(by='시간대').reset_index(drop=True)

date_arr = ['2007', '2012', '2017', '2020']


plt.title('교통체증 변동 현황')
# i = 0

for dataFrame in [data_2007, data_2012, data_2017, data_2020]:
    dataFrame['timeline_idx'] = range(24)

    max_y1 = dataFrame['교통량'].max()
    max_y1_index = dataFrame['교통량'].idxmax()
    max_y1_x = dataFrame.loc[max_y1_index, 'timeline_idx']

    plt.scatter([max_y1_x], [max_y1], color='red')
    plt.text(max_y1_x, max_y1, f'{time_define_array[max_y1_x]}, ' + f'{int(max_y1):,}', verticalalignment='bottom', horizontalalignment='left')

# i = i + 1
# print(max_y1_index)
plt.ylabel('교통량(평균)')
plt.plot(time_define_array, data_2007['교통량'], label='2007')
plt.plot(time_define_array, data_2012['교통량'], label='2012')
plt.plot(time_define_array, data_2017['교통량'], label='2017')
plt.plot(time_define_array, data_2020['교통량'], label='2020')

plt.legend()
plt.show()

