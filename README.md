This is the code repository for the meds_reader ML4H paper submission.

It consists of four main components, each corresponding to a folder:

1. meds\_reader: Our meds\_reader software package. Install this using pip install -e .

2. reference_implementaion: Reference implementations for length of stay labeling and featurization for both PyHealth and MIMIC-IV-Data Pipeline. Note the README for running against MIMIC-IV Data Pipeline.

3. conversion: Scripts for converting from PyHealth to MIMIC-IV Data Pipeline to MEDS format for use with meds\_reader. 

Make sure to install PyHealth from their Github (https://github.com/sunlabuiuc/PyHealth). Likewise, install MIMIC-IV Data Pipeline using their instructions (https://github.com/healthylaife/MIMIC-IV-Data-Pipeline).

After conversion, make sure to run meds\_reader\_convert on both of the result folders

```bash

meds_reader_convert datasets/pyhealth_meds datasets/pyhealth_meds_reader --num_threads 10
meds_reader_convert datasets/pipeline_meds datasets/pipeline_meds_reader --num_threads 10
```

4. reimplementation: Reimplementations of length of stay labeling and featurization using meds\_reader. Make sure to run the conversion scripts as well as meds\_reader\_convert before running.

In order to run any of these scripts, you must first create a "datasets" folder with downloads of MIMIC-III and MIMIC-IV.
