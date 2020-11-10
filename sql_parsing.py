import pyodbc
import pandas as pd
import sqlite3
import re


def parse_sql(query, db, filename):
    connection = sqlite3.connect(db)
    df = pd.read_sql_query(query, connection)
    df.to_csv(filename)


def parse_date(date):
    try:
        return int(''.join(re.split("[-:/ ]", date)))
    except TypeError:
        # handle blank vals for DOD
        return date

def parse_dates(csv, columns, csv_name):
    df = pd.read_csv(csv)
    for col in columns:
        print("processing column: %s" %col)
        df[col] = df[col].apply(parse_date)
    df.to_csv(csv_name)

if __name__ == "__main__":
    # select * from d_items where d_items.CATEGORY == "Routine Vital Signs" and d_items.DBSOURCE == "metavision"
    # query for items that are routine vital signs # tele ICU

    filt = """
    select * from d_items where 
            (d_items.ITEMID == 220045 or d_items.ITEMID == 223761 or 
             d_items.ITEMID == 223762 or d_items.ITEMID == 223835 or 
             d_items.ITEMID == 220179 or d_items.ITEMID == 220050)
            """
    
    script = """
    SELECT * from chartevents
    LEFT JOIN patients
    ON patients.SUBJECT_ID = chartevents.SUBJECT_ID
    WHERE (chartevents.ITEMID == 220045 or chartevents.ITEMID == 223761 or 
             chartevents.ITEMID == 224166  or 
             chartevents.ITEMID == 220051 or chartevents.ITEMID == 220050)

    """
    parse_sql(script, 'mimic3.db', 'chartevents_actual.csv')

    labels = {
        220045: "Heart Rate",
        220050: "Arterial Blood Pressure systolic",
        220051: "Arterial Blood Pressure diastolic",
        223761: "Temperature Fahrenheit",
        224166: "Doppler BP"

    }



    # csv = 'input_events_join_patients.csv'
    # columns = ["STARTTIME", "ENDTIME", "DOB", "DOD"]
    # new_csv = 'input_events_patients_clean.csv'
    # parse_dates(csv, columns, new_csv)
    pass