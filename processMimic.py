import csv 
import pandas as pd
import numpy as np
from sklearn.impute import KNNImputer
import re
filename = "mimic-data/chartevents_filtered.csv"


def filter_items(row, indicator):
    if row["ITEMID"] == indicator:
        return row["VALUENUM"]
    else:
        return np.NaN

def parse_date(date):
    try:
        return int(''.join(re.split("[-:/ ]", date)))
    except TypeError:
        # handle blank vals for DOD
        return date

def get_age(row):
    try:
        curr = parse_date(row["CHARTTIME"])
        dob = parse_date(row["DOB"])
        #convert to yrs?
        return curr - dob

    except:
        dob = parse_date(row["DOB"])
        dod = parse_date(row["DOD"])
        #print(dod, dob)
        return dod - dob

def load_label(file = filename, rows = 10000):

    df = pd.read_csv(filename, nrows = rows)

    c_drop = ["RESULTSTATUS", "STOPPED", "ROW_ID","ROW_ID.1",'SUBJECT_ID.1']
    df = df.drop(columns = c_drop)

    df['FEMALE'] = df['GENDER'] == 'F'
    df['FEMALE'] = df["FEMALE"].astype(int)
    
    df["AGE"] = df.apply(lambda row: get_age(row), axis=1)


    labels = {
    220045: "HR",
    211: "HR",
    220050: "ABP_s",
    220051: "ABP_d",
    223761: "TEMP_f",
    678: "TEMP_f",
    }
    #224166: "BP" // no vals?

    for ind in labels.keys():
        label = labels[ind] 
        df[label] = df.apply(lambda row: filter_items(row,ind), axis=1)
        #print(label, "missing", np.count_nonzero(df[label].isna().values))


    second_drop = ['ITEMID', 'DOD_HOSP', 'DOD_SSN', 'VALUE', 'VALUENUM', "GENDER"] #keeping only DOD as ground truth ?
    df = df.drop(columns = second_drop)

    # print("Num of Subjects:", len(df.SUBJECT_ID.value_counts()))
    print("Num of ICU Stays:", len(df.ICUSTAY_ID.value_counts()))

    #ADD DUMMIES ?
    # icustay_df = pd.get_dummies(df.ICUSTAY_ID)
    # subject_df = pd.get_dummies(df.SUBJECT_ID)
    # unit_df = pd.get_dummies(df.VALUEUOM)

    return df

def check_missing(df):

    df_missing = df.isna()
    print('Col Percents Missing \n', (df_missing.sum()/ len(df_missing)).round(2))
    

if __name__ == "__main__":
    df = load_label()
    print(df.head())
    print(df.describe())
    #print(df.columns)


