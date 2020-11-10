csv = 'chartevents_actual.csv'
import pandas as pd

def count_missing(csv):
    df = pd.read_csv(csv)
    missing = 0
    cols = 0

    for val in df["VALUENUM"]:
        cols += 1
        try:
            hi = float(val)
        except:
            missing += 1
    return missing/cols

stays = 4000

def number_of_stays(csv):
    stays = set()
    df = pd.read_csv(csv)
    for index, row in df.iterrows():
        if row["ICUSTAY_ID"] not in stays:
            stays.add(row["ICUSTAY_ID"])
    return len(stays)

labels = {
    220045: "Heart Rate",
    220050: "Arterial Blood Pressure systolic",
    220051: "Arterial Blood Pressure diastolic",
    223761: "Temperature Fahrenheit",
    224166: "Doppler BP"

}

measurements = ["Heart Rate",
    "Arterial Blood Pressure systolic",
    "Arterial Blood Pressure diastolic",
    "Temperature Fahrenheit",
    "Doppler BP"]

def create_data_set(csv):
    stays = {}
    df = pd.read_csv(csv)
    print("finding stays")
    for index, row in df.iterrows():
        if len(stays) < 5000:
            stays.setdefault(row['ICUSTAY_ID'], {})
            item = labels[row["ITEMID"]]
            stays[row['ICUSTAY_ID']].setdefault(item , [0,0])
            stays[row['ICUSTAY_ID']][item][0] += 1
            stays[row['ICUSTAY_ID']][item][1] = (stays[row['ICUSTAY_ID']][item][1] + row['VALUENUM']) / stays[row['ICUSTAY_ID']][item][0]
        else:
            break
    
    valid_stays = {}

    print("finding valid stays")
    for stay in stays:
        if len(stays[stay]) == len(labels):
            valid_stays[stay] = stays[stay]
    
    data_set = pd.DataFrame(columns=['STAY', "Heart Rate",
    "Arterial Blood Pressure systolic",
    "Arterial Blood Pressure diastolic",
    "Temperature Fahrenheit",
    "Doppler BP"], index=[i for i in range(len(valid_stays))])

    print("Building dataset dataframe")
    location = 0
    for stay in valid_stays:
        rows = [None]* 6
        rows[0] = stay
        for i in range(len(measurements)):
            rows[i+1] = valid_stays[stay][measurements[i]]

        data_set[location] = rows
        location += 1

    print("Saving dataset to csv")
    data_set.to_csv("first_data_set_not_normalized.csv")

create_data_set(csv)

