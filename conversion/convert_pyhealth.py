import pyhealth
import pyhealth.data
from pyhealth.datasets import MIMIC3Dataset

import pyarrow as pa
import pyarrow.compute as pac
import pyarrow.parquet as pq

import os
import shutil
import datetime
import numpy as np
import collections

data = MIMIC3Dataset(
    # root directory of the dataset
    root="mimiciii/1.4",
    # raw CSV table name
    tables=[
        "DIAGNOSES_ICD",
        "PROCEDURES_ICD",
        "PRESCRIPTIONS",
        "LABEVENTS",
    ]
    # map all NDC codes to CCS codes in these tables
    # code_mapping={"NDC": "CCSCM"},
)

results = collections.defaultdict(list)

for patient_id, patient in data.patients.items():
    subject_id = int(patient_id)

    birth_obj = {'subject_id': subject_id, 'code': 'Birth', 'time': patient.birth_datetime}

    birth_obj['gender'] = patient.gender
    birth_obj['ethnicity'] = patient.ethnicity


    for k, v in patient.attr_dict.items():
        if v != v:
            continue
        birth_obj[k] = v

    results[subject_id].append(birth_obj)

    if patient.death_datetime is not None:
        results[subject_id].append({'subject_id': subject_id, 'code': 'Death', 'time': patient.death_datetime})


    visit: pyhealth.data.Visit

    for visit_id, visit in patient.visits.items():
        visit_id = int(visit_id)
        visit_event = {'subject_id': subject_id, 'code': 'Visit', 'time': visit.encounter_time, 'visit_id': visit_id, 'discharge_time': visit.discharge_time, 'discharge_status': visit.discharge_status}

        for k, v in visit.attr_dict.items():
            if v != v:
                continue
            visit_event[k] = v

        results[subject_id].append(visit_event)

        for table in visit.available_tables:
            for event in visit.get_event_list(table):
                event_obj = {'subject_id': subject_id, 'visit_id': visit_id, 'code': event.vocabulary + '/' + event.code, 'time': event.timestamp or visit.discharge_time}

                for k, v in event.attr_dict.items():
                    if v != v:
                        continue
                    event_obj[k] = v

                results[subject_id].append(event_obj)

    results[subject_id].sort(key=lambda a: a['time'])

all_subjects = list(results)

attr_map = {str: pa.string(), int: pa.int64(), np.int64: pa.int64(), datetime.datetime: pa.timestamp('us')}

attr_schema = {(k, attr_map[type(v)]) for subject_values in results.values() for row in subject_values for k, v in row.items() if k not in {'subject_id', 'time', 'numeric_value'}}

print(attr_schema)

# Verify one type per attribute
assert len(attr_schema) == len(set(k for k,_ in attr_schema))

schema = pa.schema([
    ('subject_id', pa.int64()),
    ('time', pa.timestamp('us')),
] + sorted(list(attr_schema)))

print(schema)

result_dir = 'datasets/pyhealth_meds'

if os.path.exists(result_dir):
    shutil.rmtree(result_dir)

os.mkdir(result_dir)

os.mkdir(result_dir + '/metadata')
os.mkdir(result_dir + '/data')


num_shards = 100

subject_ids_per_shard = np.array_split(all_subjects, num_shards)

for i, subject_ids in enumerate(subject_ids_per_shard):
    rows = [v for subject_id in subject_ids for v in results[subject_id]]


    table = pa.Table.from_pylist(rows, schema=schema)

    pq.write_table(table, result_dir + f'/data/{i}.parquet')


