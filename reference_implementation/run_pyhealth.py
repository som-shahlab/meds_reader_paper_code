import pyhealth
import pyhealth.data
from pyhealth.datasets import MIMIC3Dataset

import itertools
import pickle

data = MIMIC3Dataset(
    root="datasets/mimiciii/1.4",
    tables=[
        "DIAGNOSES_ICD",
        "PROCEDURES_ICD",
        "PRESCRIPTIONS",
        "LABEVENTS",
    ]
)

def length_of_stay_prediction_mimic3_fn(patient: pyhealth.data.Patient):
    samples = []

    for visit in patient:

        conditions = visit.get_code_list(table="DIAGNOSES_ICD")
        procedures = visit.get_code_list(table="PROCEDURES_ICD")
        drugs = visit.get_code_list(table="PRESCRIPTIONS")
        labs = visit.get_code_list(table="LABEVENTS")

        features = list(itertools.chain((conditions, procedures, drugs, labs)))

        los_days = (visit.discharge_time - visit.encounter_time).days

        samples.append(
            {
                "visit_id": visit.visit_id,
                "patient_id": patient.patient_id,
                "features": features,
                "label": los_days,
            }
        )
    return samples

task_mimic3_ds = data.set_task(task_fn=length_of_stay_prediction_mimic3_fn)

with open('pyhealth_result.pkl', 'wb') as f:
    pickle.dump(task_mimic3_ds.samples, f)