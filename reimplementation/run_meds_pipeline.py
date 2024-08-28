import meds_reader
import collections
import datetime

from typing import Iterator

def get_samples(subjects: Iterator[meds_reader.Subject]):
    samples = []
    for subject in subjects:
        
        admission_data = {}

        for event in subject.events:
            if event.code == "Visit/":
                los_days = (event.dischtime - event.time).days
                label = los_days > 3

                features = collections.defaultdict(list)
                features[event.gender].append(None)
                features[event.ethnicity].append(None)
                features[event.insurance].append(None)
                features['age'].append(event.age)

                admission_data[event.hadm_id] = {
                    'start': event.time,
                    'label': label, 
                    'features': features,
                }


        for event in subject.events:
            if event.hadm_id in admission_data: 
                if event.time is not None and ((event.time - admission_data[event.hadm_id]['start']) > datetime.timedelta(days=1)):
                    continue
                admission_data[event.hadm_id]['features'][event.code].append(event.valuenum or event.dose_val_rx)
    
        for hadm_id, v in admission_data.items():
            features = []

            for code, values in v['features'].items():
                valid_values = [a for a in values if a is not None]
                if len(valid_values) == 0:
                    value = None
                else:
                    value = sum(valid_values) / len(valid_values)
                features.append((code, value))

            samples.append({
                'hadm_id': hadm_id,
                'label': v['label'],
                'features': features
            })

            if hadm_id == 24975173:
                print(samples[-1])

    return samples

if __name__ == "__main__":
    samples = []

    with meds_reader.SubjectDatabase('datasets/pipeline_meds_reader', num_threads=24) as database:
        for s in database.map(get_samples):
            samples.extend(s)

    print(len(samples))
    print(samples[0])