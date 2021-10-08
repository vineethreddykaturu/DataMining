import pandas as pd
import datetime

# mydateparser = lambda x: datetime.strptime(x, '%m/%d/%Y')
# CGM_DATA = pd.read_csv('CGMData.csv', parse_dates=['Date'], date_parser=mydateparser)
CGM_DATA = pd.read_csv('CGMData.csv')
CGM_DATA['Date']=pd.to_datetime(CGM_DATA['Date'], format="%m/%d/%Y")
CGM_DATA = CGM_DATA[["Date", "Time", "Sensor Glucose (mg/dL)","ISIG Value"]]
CGM_DATA.rename({'Sensor Glucose (mg/dL)': 'Glucose'}, axis=1, inplace=True)
CGM_DATA['Time'] = pd.to_timedelta(CGM_DATA['Time'])

# Insulin = pd.read_csv('InsulinData.csv', parse_dates=['Date'], date_parser=mydateparser)
Insulin = pd.read_csv("InsulinData.csv")
Insulin['Date']=pd.to_datetime(Insulin['Date'], format="%m/%d/%Y")
Insulin = Insulin[["Date", "Time", "Alarm"]]
Insulin['Time'] = pd.to_timedelta(Insulin['Time'])

Midnight = datetime.timedelta(hours=0, minutes=0, seconds=0)
EarlyDay = datetime.timedelta(hours=6, minutes=0, seconds=0)
BeforeEarlyDay = datetime.timedelta(hours=5, minutes=59, seconds=59)
EndOfTheDay = datetime.timedelta(hours=23, minutes=59, seconds=59)

NewTable = pd.DataFrame((Insulin.loc[Insulin['Alarm'] == 'AUTO MODE ACTIVE PLGM OFF']))
Auto_Mode_Active_Plgm_Off = NewTable.iloc[-1]["Date"]
Auto_Mode_Active_Plgm_Off_time = NewTable.iloc[-1]["Time"]

CGM_Manual_Mode = CGM_DATA[(CGM_DATA["Date"] < Auto_Mode_Active_Plgm_Off) | ((CGM_DATA["Date"] == Auto_Mode_Active_Plgm_Off) & (CGM_DATA["Time"] < Auto_Mode_Active_Plgm_Off_time))]

CGM_Auto_Mode = CGM_DATA[(CGM_DATA["Date"] > Auto_Mode_Active_Plgm_Off) | ((CGM_DATA["Date"] == Auto_Mode_Active_Plgm_Off) & (CGM_DATA["Time"] >= Auto_Mode_Active_Plgm_Off_time))]

manualdateList = CGM_Manual_Mode["Date"].unique()
autodatelist = CGM_Auto_Mode["Date"].unique()
d = 0
Manual_List = []
Auto_List = []
mode = ['manual','auto']
Glucose_Levels = ['hyperglycemia','hyperglycemia critical','range','range secondary','hypoglycemia level 1','hypoglycemia level 2']
Time_Streams = ['OverNight','DayTime','WholeDay']
for x in mode:
    if x == 'auto':
        Final_Data = CGM_Auto_Mode
        dateList = autodatelist
    else:
        Final_Data = CGM_Manual_Mode
        dateList = manualdateList
    for i in Time_Streams:
        if i == 'OverNight':
            CGM_Final_Time_Based = Final_Data[(Final_Data['Time']>=Midnight) & (Final_Data['Time']<= EarlyDay)]
        if i == 'DayTime':
            CGM_Final_Time_Based = Final_Data[(Final_Data['Time']>EarlyDay) & (Final_Data['Time']<= EndOfTheDay)]
            
        if i == 'WholeDay':
            CGM_Final_Time_Based = Final_Data
        for i in Glucose_Levels:
            d = 0
            if i == 'hyperglycemia':
                for j in dateList:
                    dayresult = CGM_Final_Time_Based[CGM_Final_Time_Based["Date"] == j]
                    d = d + (dayresult[dayresult["Glucose"] > 180].shape[0]/float(288))*100
                d = d/(float(dateList.shape[0])*1.0)
                if x == 'manual':
                    Manual_List.append(d)
                elif x == 'auto':
                    Auto_List.append(d)
            elif i == 'hyperglycemia critical':
                for j in dateList:
                    dayresult = CGM_Final_Time_Based[CGM_Final_Time_Based["Date"] == j]
                    d = d + (dayresult[dayresult["Glucose"] > 250].shape[0]/float(288))*100
                d = d/(float(dateList.shape[0])*1.0)
                if x == 'manual':
                    Manual_List.append(d)
                else:
                    Auto_List.append(d)
            elif i == 'range':
                for j in dateList:
                    dayresult = CGM_Final_Time_Based[CGM_Final_Time_Based["Date"] == j]
                    d = d+(dayresult[(dayresult["Glucose"] >= 70) & (dayresult["Glucose"] <= 180)].shape[0]/float(288))*100
                d = d/(float(dateList.shape[0])*1.0)
                if x == 'manual':
                    Manual_List.append(d)
                elif x == 'auto':
                    Auto_List.append(d)
            elif i == 'range secondary':
                for j in dateList:
                    dayresult = CGM_Final_Time_Based[CGM_Final_Time_Based["Date"] == j]
                    d = d+(dayresult[(dayresult["Glucose"] >= 70) & (dayresult["Glucose"] <= 150)].shape[0]/float(288))*100
                d = d/(float(dateList.shape[0])*1.0)
                if x == 'manual':
                    Manual_List.append(d)
                elif x == 'auto':
                    Auto_List.append(d)
            elif i == 'hypoglycemia level 1':
                for j in dateList:
                    dayresult = CGM_Final_Time_Based[CGM_Final_Time_Based["Date"] == j]
                    d = d+(dayresult[dayresult["Glucose"] < 70].shape[0]/float(288))*100
                d = d/(float(dateList.shape[0])*1.0)
                if x == 'manual':
                    Manual_List.append(d)
                elif x == 'auto':
                    Auto_List.append(d)
            elif i == 'hypoglycemia level 2':
                for j in dateList:
                    dayresult = CGM_Final_Time_Based[CGM_Final_Time_Based["Date"] == j]
                    d = d+(dayresult[dayresult["Glucose"] < 54].shape[0]/float(288))*100
                d = d/(float(dateList.shape[0])*1.0)
                if x == 'manual':
                    Manual_List.append(d)
                elif x == 'auto':
                    Auto_List.append(d)
Results = pd.DataFrame()
Manual_List.append(1.1)
Auto_List.append(1.1)
Results['Manual'] = Manual_List
Results['Auto'] = Auto_List
Results = Results.transpose()
Results.to_csv("Results.csv",index=False,header=False)