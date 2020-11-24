import pandas as pd
import json
import pickle
import itertools

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

labels =  {
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



good = sorted([220045, 220179, 220180, 220181, 223761, 220050, 220051, 220052])
measurements = [labels[i] for i in good]


def data_set(csv, need=False):
    if need:
        stays = {}
        df = pd.read_csv(csv)

        
        for index, row in df.iterrows():
            
            stays.setdefault(row['HADM_ID'], {})
            item = labels[row["ITEMID"]]
            stays[row['HADM_ID']].setdefault(item , [0,0])
            stays[row['HADM_ID']][item][0] += 1
            stays[row['HADM_ID']][item][1] += row['VALUENUM']
        
        print("save stays to picket") 
        with open('stays.pickle', 'wb') as handle:
            pickle.dump(stays, handle, protocol=pickle.HIGHEST_PROTOCOL)    
  

    else:
        with open('stays.pickle', 'rb') as handle:
            stays = pickle.load(handle)
    print("Building dataset dataframe")
    

    lengths = {}

    for i in stays:
        lengths.setdefault(len(stays[i]), 0)
        lengths[len(stays[i])] += 1
    

    good_stays = {}
    for i in stays:
        if len(stays[i]) == 8:
            good_stays[i] = stays[i]
    
    stays = good_stays

    column = ["Stay"]+measurements
    data_set = pd.DataFrame(columns=column, index=[i for i in range(len(good))])

    location = 0
    for stay in stays:
        rows = [0]* 9
        rows[0] = stay
        for i in range(len(measurements)):
            rows[i+1] = stays[stay][measurements[i]][1] / stays[stay][measurements[i]][0]
        data_set.loc[location] = rows
        location += 1

    print("Saving dataset to csv")
    data_set.to_csv("good_data_set.csv")

def is_num(num):
    try:
        int(num)
        return True
    except:
        try:
            float(num)
            return True
        except:
            return False



def number_patients(items, mapping):
    current = mapping[items[0]]
    other_sets = [mapping[other] for other in items[1:]]
    return len(current.intersection(*other_sets))

def find_features(csv, need=False):
    print("make df")
    if need:
        df = pd.read_csv(csv)
        # find features that span a lot of icu_stay_ids
        features_icustayid = {}
        # item_id : {stay_id, stay_id, ....}
        print("iterating over df, will take a while")
        for i, row in df.iterrows():
            if is_num(row["VALUE"]):
                features_icustayid.setdefault(row["ITEMID"], set())

                features_icustayid[row["ITEMID"]].add(row["HADM_ID"])
        print("iteration finished, saving json")

        save_json = {
            feature: list(features_icustayid[feature]) for feature in features_icustayid
        }

        with open('features_icustayid.json', 'w') as fp:
            json.dump(save_json, fp)

        with open('features_icustayid.pickle', 'wb') as handle:
            pickle.dump(features_icustayid, handle, protocol=pickle.HIGHEST_PROTOCOL)
    else:
        with open('features_icustayid.pickle', 'rb') as handle:
            features_icustayid = pickle.load(handle)
    # try powerset of patients to see which meet the minimum features required
    print("finding best features")
    tried = set()
    minimum_features = 8
    most_patients = 0
    best_features = None
    maximum_features = 20
    features = list(features_icustayid.keys())
    for length in range(minimum_features, maximum_features):
        print(length)
        for combination in itertools.combinations(features, length):
            if tuple(sorted(combination)) not in tried:
                tried.add(tuple(sorted(combination)))
                current_patients = number_patients(combination, features_icustayid)
                if current_patients > 9000:
                    print("number of patients, please be largish", current_patients)
                    print("On combo: ", combination)
                    if current_patients > most_patients:
                        most_patients = current_patients
                        best_features = combination
    print("done!")

    answer = {
        "patients": most_patients,
        "features": best_features
    }
    with open('best_chart_features.json', 'w') as fp:
        json.dump(answer, fp)

    with open('best_chart_features.pickle', 'wb') as handle:
        pickle.dump(answer, handle, protocol=pickle.HIGHEST_PROTOCOL)    
    return answer

if __name__ == "__main__":
    csv = 'chartevents_all_vitals.csv'
    print(find_features(csv))

    # nice = 'chartevents_vitals.csv'
    # data_set(nice)

