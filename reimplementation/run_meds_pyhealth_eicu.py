import meds_reader

from typing import Iterator
import collections

def get_samples(subjects: Iterator[meds_reader.Subject]):
    samples = []
    for subject in subjects: 

        visit_features = collections.defaultdict(set)

        for event in subject.events:
            visit_features[event.visit_id].add(event.code)

        for event in subject.events:
            if event.code == "Visit":
                los_days = (event.discharge_time - event.time).days

                samples.append(
                    {
                        "visit_id": event.visit_id,
                        "patient_id": subject.subject_id,
                        "features": visit_features[event.visit_id],
                        "label": los_days,
                    }
                )

    return samples

if __name__ == "__main__":
    samples = []

    with meds_reader.SubjectDatabase('../datasets/pyhealth_eicu_meds_reader', num_threads=12) as database:
        for s in database.map(get_samples):
            samples.extend(s)

    print(len(samples))
