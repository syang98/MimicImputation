import pyodbc
import pandas as pd
import sqlite3
import re
import pickle


def parse_sql(query, db, filename):
    print("connecting")
    connection = sqlite3.connect(db)
    print("connected! Executing query")
    df = pd.read_sql_query(query, connection)
    print("saving to csv")
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

    mapping =  {
        228640:	"EtCO2",
        228641:	"EtCO2 Clinical indication",
        224166:	"Doppler BP",
        224167:	"Manual Blood Pressure Systolic Left",
        224192:	"Pulsus Paradoxus",
        227242:	"Manual Blood Pressure Diastolic Right",
        227243:	"Manual Blood Pressure Systolic Right",
        224359:	"QTc",
        227630:	"Arctic Sun Temp #1 Location",
        227631:	"Arctic Sun Temp #2 Location",
        227632:	"Arctic Sun/Alsius Temp #1 C",
        227634:	"Arctic Sun/Alsius Temp #2 C",
        224642:	"Temperature Site",
        224643:	"Manual Blood Pressure Diastolic Left",
        224645:	"Orthostatic BPs lying",
        224646:	"Orthostatic BPs sitting",
        224647:	"Orthostatic HR standing",
        224650:	"Ectopy Type 1",
        224651:	"Ectopy Frequency 1",
        226096:	"Orthostatic BPd standing",
        228229:	"PAR-Activity",
        228230:	"PAR-Circulation",
        228231:	"PAR-Consciousness",
        228232:	"PAR-Oxygen saturation",
        228233:	"PAR-Remain sedated",
        228234:	"PAR-Respiration",
        220045:	"Heart Rate",
        220048:	"Heart Rhythm",
        220050:	"Arterial Blood Pressure systolic",
        220051:	"Arterial Blood Pressure diastolic",
        220052:	"Arterial Blood Pressure mean",
        220179:	"Non Invasive Blood Pressure systolic",
        220180:	"Non Invasive Blood Pressure diastoli",
        220181:	"Non Invasive Blood Pressure mean",
        226092:	"Orthostatic BPd lying",
        226094:	"Orthostatic BPd sitting",
        226329:	"Blood Temperature CCO (C)",
        226479:	"Ectopy Type 2",
        226480:	"Ectopy Frequency 2",
        223761:	"Temperature Fahrenheit",
        223762:	"Temperature Celsius",
        223763:	"Bladder Pressure",
        223764:	"Orthostatic HR lying",
        223765:	"Orthostatic HR sitting",
        223766:	"Orthostatic BPs standing",
        225309:	"ART BP Systolic",
        225310:	"ART BP Diastolic",
        225312:	"ART BP mean"
    }


    filt = """
    select * from d_items where 
            (d_items.ITEMID == 220045 or d_items.ITEMID == 223761 or 
             d_items.ITEMID == 223762 or d_items.ITEMID == 223835 or 
             d_items.ITEMID == 220179 or d_items.ITEMID == 220050)
            """
    
    script = """
    SELECT * from chartevents
    WHERE ( chartevents.ITEMID == 228640 or
            chartevents.ITEMID == 228641 or
            chartevents.ITEMID == 224166 or
            chartevents.ITEMID == 224167 or
            chartevents.ITEMID == 224192 or
            chartevents.ITEMID == 227242 or
            chartevents.ITEMID == 227243 or
            chartevents.ITEMID == 224359 or
            chartevents.ITEMID == 227630 or
            chartevents.ITEMID == 227631 or
            chartevents.ITEMID == 227632 or
            chartevents.ITEMID == 227634 or
            chartevents.ITEMID == 224642 or
            chartevents.ITEMID == 224643 or
            chartevents.ITEMID == 224645 or
            chartevents.ITEMID == 224646 or
            chartevents.ITEMID == 224647 or
            chartevents.ITEMID == 224650 or
            chartevents.ITEMID == 224651 or
            chartevents.ITEMID == 226096 or
            chartevents.ITEMID == 228229 or
            chartevents.ITEMID == 228230 or
            chartevents.ITEMID == 228231 or
            chartevents.ITEMID == 228232 or
            chartevents.ITEMID == 228233 or
            chartevents.ITEMID == 228234 or
            chartevents.ITEMID == 220045 or
            chartevents.ITEMID == 220048 or
            chartevents.ITEMID == 220050 or
            chartevents.ITEMID == 220051 or
            chartevents.ITEMID == 220052 or
            chartevents.ITEMID == 220179 or
            chartevents.ITEMID == 220180 or
            chartevents.ITEMID == 220181 or
            chartevents.ITEMID == 226092 or
            chartevents.ITEMID == 226094 or
            chartevents.ITEMID == 226329 or
            chartevents.ITEMID == 226479 or
            chartevents.ITEMID == 226480 or
            chartevents.ITEMID == 223761 or
            chartevents.ITEMID == 223762 or
            chartevents.ITEMID == 223763 or
            chartevents.ITEMID == 223764 or
            chartevents.ITEMID == 223765 or
            chartevents.ITEMID == 223766 or
            chartevents.ITEMID == 225309 or
            chartevents.ITEMID == 225310 or
            chartevents.ITEMID == 225312 )
    ORDER BY chartevents.ICUSTAY_ID DESC

    """
    #parse_sql(script, 'mimic3.db', 'chartevents_all_vitals.csv')

    labels = {
        220045: "Heart Rate",
        220050: "Arterial Blood Pressure systolic",
        220051: "Arterial Blood Pressure diastolic",
        223761: "Temperature Fahrenheit",
        224166: "Doppler BP"
    }

    sql = """
    SELECT * from chartevents
    WHERE ( chartevents.ITEMID == 220045 or
            chartevents.ITEMID == 220179 or
            chartevents.ITEMID == 220180 or
            chartevents.ITEMID == 220181 or
            chartevents.ITEMID == 223761 or
            chartevents.ITEMID == 220050 or
            chartevents.ITEMID == 220051 or
            chartevents.ITEMID == 220052 
            )
    ORDER BY chartevents.ICUSTAY_ID DESC

    """
    good = "(220045, 220179, 220180, 220181, 223761, 220050, 220051, 220052)"
    csv = 'chartevents_vitals.csv'
    parse_sql(sql, 'mimic3.db', csv)



    