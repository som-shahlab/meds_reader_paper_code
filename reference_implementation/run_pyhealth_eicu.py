import pyhealth
import pyhealth.data
from pyhealth.datasets import eICUDataset

import itertools
import pickle

import collections

data = eICUDataset(
    # root directory of the dataset
    root="../datasets/eicu-collaborative-research-database-2.0",
    # raw CSV table name
    tables=["diagnosis", "medication", "physicalExam"]
    # map all NDC codes to CCS codes in these tables
    # code_mapping={"NDC": "CCSCM"},
)

def length_of_stay_prediction_eicu_fn(patient: pyhealth.data.Patient):
    samples = []

    for visit in patient:

        conditions = visit.get_code_list(table="diagnosis")
        procedures = visit.get_code_list(table="physicalExam")
        drugs = visit.get_code_list(table="medication")
        # exclude: visits without condition, procedure, or drug code
        if len(conditions) * len(procedures) * len(drugs) == 0:
            continue


        features = list(itertools.chain((conditions, procedures, drugs)))

        los_days = (visit.discharge_time - visit.encounter_time).days

        # TODO: should also exclude visit with age < 18
        samples.append(
            {
                "visit_id": visit.visit_id,
                "patient_id": patient.patient_id,
                "features": features,
                "label": los_days,
            }
        )
    # no cohort selection
    return samples

task_mimic3_ds = data.set_task(task_fn=length_of_stay_prediction_eicu_fn)

print(len(task_mimic3_ds.samples))
