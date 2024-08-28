import polars as pl
import os
import shutil


a = pl.read_csv('MIMIC-IV-Data-Pipeline/data/features/preproc_diag.csv.gz', infer_schema_length=0)

print(a.schema)
a = a.select(
    subject_id = pl.col('subject_id').cast(pl.Int64()),
    time = pl.lit(None, dtype=pl.Datetime('us')),
    code = 'ICD/' + pl.col('new_icd_code'),
    hadm_id = pl.col('hadm_id').cast(pl.Int64()),
)

print(a.schema)
print(a)

b = pl.read_csv('MIMIC-IV-Data-Pipeline/data/features/preproc_proc.csv.gz', infer_schema_length=0)

print(b.schema)
b = b.select(
    subject_id = pl.col('subject_id').cast(pl.Int64()),
    time = pl.col('chartdate').str.to_datetime(time_unit='us'),
    code = 'Procedure/' + pl.col('icd_code'),
    hadm_id = pl.col('hadm_id').cast(pl.Int64()),
)

print(b.schema)
print(b)


c = pl.read_csv('MIMIC-IV-Data-Pipeline/data/features/preproc_med.csv.gz', infer_schema_length=0)


print(c.schema)

c = c.select(
    subject_id = pl.col('subject_id').cast(pl.Int64()),
    time = pl.col('starttime').str.to_datetime(time_unit='us'),
    code = 'Medication/' + pl.col('drug_name'),
    hadm_id = pl.col('hadm_id').cast(pl.Int64()),
    stoptime = pl.col('stoptime').str.to_datetime(time_unit='us'),
    dose_val_rx = pl.col('dose_val_rx').cast(pl.Float32(), strict=False),
)


print(c.schema)
print(c)


d = pl.read_csv('MIMIC-IV-Data-Pipeline/data/features/preproc_labs.csv.gz', infer_schema_length=0)


d = d.select(
    subject_id = pl.col('subject_id').cast(pl.Int64()),
    time = pl.col('charttime').str.to_datetime(time_unit='us'),
    code = 'Lab/' + pl.col('itemid'),
    hadm_id = pl.col('hadm_id').cast(pl.Float32()).cast(pl.Int64()),
    valuenum = pl.col('valuenum').cast(pl.Float32()),
)

print(d.schema)
print(d)

e = pl.read_csv('MIMIC-IV-Data-Pipeline/data/cohort/cohort_non-icu_length_of_stay_3_.csv.gz', infer_schema_length=0)

print(e.schema)

e = e.select(
    subject_id = pl.col('subject_id').cast(pl.Int64()),
    time = pl.col('admittime').str.to_datetime(time_unit='us'),
    code = pl.lit('Visit/'),


    hadm_id = pl.col('hadm_id').cast(pl.Int64()),
    dischtime = pl.col('dischtime').str.to_datetime(time_unit='us'),
    age = pl.col('Age').cast(pl.Float32()),

    gender = pl.col('gender'),
    ethnicity = pl.col('ethnicity'),
    insurance = pl.col('insurance'),
)


final_result = pl.concat((a, b, c, d, e), how='diagonal')

del a
del b
del c
del d
del e

final_result = final_result.sort(by=(pl.col('subject_id'), pl.col('time')))

num_shards = 100

final_result = final_result.with_columns(shard = pl.col('subject_id').hash() % 100)

parts = final_result.partition_by('shard')

result_dir = 'datasets/pipeline_meds'

if os.path.exists(result_dir):
    shutil.rmtree(result_dir)

os.mkdir(result_dir)

os.mkdir(result_dir + '/metadata')
os.mkdir(result_dir + '/data')

for i, part in enumerate(parts):
    part.write_parquet(result_dir + f'/data/{i}.parquet')

