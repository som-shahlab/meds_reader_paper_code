#!/usr/bin/env python
# coding: utf-8

# In[1]:

def display(a):
    pass


import ipywidgets as widgets
import sys
from pathlib import Path
import os
import importlib


module_path='preprocessing/day_intervals_preproc'
if module_path not in sys.path:
    sys.path.append(module_path)

module_path='utils'
if module_path not in sys.path:
    sys.path.append(module_path)
    
module_path='preprocessing/hosp_module_preproc'
if module_path not in sys.path:
    sys.path.append(module_path)
    
module_path='model'
if module_path not in sys.path:
    sys.path.append(module_path)
#print(sys.path)
root_dir = os.path.dirname(os.path.abspath('UserInterface.ipynb'))
import day_intervals_cohort
from day_intervals_cohort import *

import day_intervals_cohort_v2
from day_intervals_cohort_v2 import *

import data_generation_icu

import data_generation
# import evaluation

import feature_selection_hosp
from feature_selection_hosp import *

# import train
# from train import *


# import ml_models
# from ml_models import *

# import dl_train
# from dl_train import *

# import tokenization
# from tokenization import *


# import behrt_train
# from behrt_train import *

import feature_selection_icu
from feature_selection_icu import *
# import fairness
# import callibrate_output


# In[41]:


importlib.reload(day_intervals_cohort)
import day_intervals_cohort
from day_intervals_cohort import *

importlib.reload(day_intervals_cohort_v2)
import day_intervals_cohort_v2
from day_intervals_cohort_v2 import *

importlib.reload(data_generation_icu)
import data_generation_icu
importlib.reload(data_generation)
import data_generation

importlib.reload(feature_selection_hosp)
import feature_selection_hosp
from feature_selection_hosp import *

importlib.reload(feature_selection_icu)
import feature_selection_icu
from feature_selection_icu import *


# # Welcome to your MIMIC-IV Project

# This repository explains the steps to download and clean MIMIC-IV dataset for analysis.
# The repository is compatible with MIMIC-IV v1.0 and MIMIC-IV v2.0
# 
# Please go to:
# - https://physionet.org/content/mimiciv/1.0/ for v1.0
# - https://physionet.org/content/mimiciv/2.0/ for v2.0
# 
# Follow instructions to get access to MIMIC-IV dataset.
# 
# Download the files using your terminal: 
# - wget -r -N -c -np --user mehakg --ask-password https://physionet.org/files/mimiciv/1.0/ or
# - wget -r -N -c -np --user mehakg --ask-password https://physionet.org/files/mimiciv/2.0/
#         
# 
# Save downloaded files in the parent directory of this github repo. 
# 
# The structure should look like below for v1.0-
# - mimiciv/1.0/core
# - mimiciv/1.0/hosp
# - mimiciv/1.0/icu
# 
# The structure should look like below for v2.0-
# - mimiciv/2.0/hosp
# - mimiciv/2.0/icu

# ## 1. DATA EXTRACTION
# Please run below cell to select option for cohort selection.
# The cohort will be svaed in **./data/cohort/**

# In[3]:


print("Please select the approriate version of MIMIC-IV for which you have downloaded data ?")
version = widgets.RadioButtons(options=['Version 1','Version 2'],value='Version 2')
display(version)

print("Please select what prediction task you want to perform ?")
radio_input4 = widgets.RadioButtons(options=['Mortality','Length of Stay','Readmission','Phenotype'],value='Length of Stay')
display(radio_input4)


# ### Refining Cohort and Prediction Task Definition
# 
# Based on your current selection following block will provide option to further refine prediction task and cohort associated with it:
# 
# - First you will refine the prediction task choosing from following options -
#     - **length of Stay** - You can select from two predefined options or enter custom number of days to predict length os stay greater than number of days.
# 
#     - **Readmission** - You can select from two predefined options or enter custom number of days to predict readmission after "number of days" after previous admission.
# 
#     - **Phenotype Prediction** - You can select from four major chronic diseases to predict its future outcome
# 
#         - Heart failure
#         - CAD (Coronary Artery Disease)
#         - CKD (Chronic Kidney Disease)
#         - COPD (Chronic obstructive pulmonary disease)
# 
# - Second, you will choode whether to perfom above task using ICU or non-ICU admissions data
# 
# - Third, you can refine the refine the cohort selection for any of the above choosen prediction tasks by including the admission samples admitted with particular chronic disease - 
#     - Heart failure
#     - CAD (Coronary Artery Disease)
#     - CKD (Chronic Kidney Disease)
#     - COPD (Chronic obstructive pulmonary disease)
#     
# print("**Please run below cell to extract the cohort for selected options**")

# In[21]:


if radio_input4.value=='Length of Stay':
    radio_input2 = widgets.RadioButtons(options=['Length of Stay ge 3','Length of Stay ge 7','Custom'],value='Length of Stay ge 3')
    display(radio_input2)
    text1=widgets.IntSlider(
    value=3,
    min=1,
    max=10,
    step=1,
    disabled=False,
    continuous_update=False,
    orientation='horizontal',
    readout=True,
    readout_format='d'
)
    display(widgets.HBox([widgets.Label('Length of stay ge (in days)',layout={'width': '180px'}), text1]))
elif radio_input4.value=='Readmission':
    radio_input2 = widgets.RadioButtons(options=['30 Day Readmission','60 Day Readmission','90 Day Readmission','120 Day Readmission','Custom'],value='30 Day Readmission')
    display(radio_input2)
    text1=widgets.IntSlider(
    value=30,
    min=10,
    max=150,
    step=10,
    disabled=False
    )
    display(widgets.HBox([widgets.Label('Readmission after (in days)',layout={'width': '180px'}), text1]))
elif radio_input4.value=='Phenotype':
    radio_input2 = widgets.RadioButtons(options=['Heart Failure in 30 days','CAD in 30 days','CKD in 30 days','COPD in 30 days'],value='Heart Failure in 30 days')
    display(radio_input2)
elif radio_input4.value=='Mortality':
    radio_input2 = widgets.RadioButtons(options=['Mortality'],value='Mortality')
    #display(radio_input2)

print("Extract Data")
print("Please select below if you want to work with ICU or Non-ICU data ?")
radio_input1 = widgets.RadioButtons(options=['ICU', 'Non-ICU'],value='Non-ICU')
display(radio_input1)

print("Please select if you want to perform choosen prediction task for a specific disease.")
radio_input3 = widgets.RadioButtons(options=['No Disease Filter','Heart Failure','CKD','CAD','COPD'],value='No Disease Filter')
display(radio_input3)


# In[22]:


disease_label=""
time=0
label=radio_input4.value

if label=='Readmission':
    if radio_input2.value=='Custom':
        time=text1.value
    else:
        time=int(radio_input2.value.split()[0])
elif label=='Length of Stay':
    if radio_input2.value=='Custom':
        time=text1.value
    else:
        time=int(radio_input2.value.split()[4])

if label=='Phenotype':    
    if radio_input2.value=='Heart Failure in 30 days':
        label='Readmission'
        time=30
        disease_label='I50'
    elif radio_input2.value=='CAD in 30 days':
        label='Readmission'
        time=30
        disease_label='I25'
    elif radio_input2.value=='CKD in 30 days':
        label='Readmission'
        time=30
        disease_label='N18'
    elif radio_input2.value=='COPD in 30 days':
        label='Readmission'
        time=30
        disease_label='J44'
    
data_icu=radio_input1.value=="ICU"
data_mort=label=="Mortality"
data_admn=label=='Readmission'
data_los=label=='Length of Stay'
        

if (radio_input3.value=="Heart Failure"):
    icd_code='I50'
elif (radio_input3.value=="CKD"):
    icd_code='N18'
elif (radio_input3.value=="COPD"):
    icd_code='J44'
elif (radio_input3.value=="CAD"):
    icd_code='I25'
else:
    icd_code='No Disease Filter'

if version.value=='Version 1':
    version_path="../mimiciv/1.0"
    cohort_output = day_intervals_cohort.extract_data(radio_input1.value,label,time,icd_code, root_dir,disease_label)
elif version.value=='Version 2':
    version_path="../datasets/raw_mimiciv/2.2"
    cohort_output = day_intervals_cohort_v2.extract_data(radio_input1.value,label,time,icd_code, root_dir,disease_label)


# ## 2. FEATURE SELECTION
# Features available for ICU data -
# - Diagnosis (https://mimic.mit.edu/docs/iv/modules/hosp/diagnoses_icd/)
# - Procedures (https://mimic.mit.edu/docs/iv/modules/icu/procedureevents/)
# - Medications (https://mimic.mit.edu/docs/iv/modules/icu/inputevents/)
# - Output Events (https://mimic.mit.edu/docs/iv/modules/icu/outputevents/)
# - Chart Events (https://mimic.mit.edu/docs/iv/modules/icu/chartevents/)
# 
# Features available for ICU data -
# - Diagnosis (https://mimic.mit.edu/docs/iv/modules/hosp/diagnoses_icd/)
# - Procedures (https://mimic.mit.edu/docs/iv/modules/hosp/procedures_icd/)
# - Medications (https://mimic.mit.edu/docs/iv/modules/hosp/prescriptions/)
# - Lab Events (https://mimic.mit.edu/docs/iv/modules/hosp/labevents/)
# 
# All features will be saved in **./data/features/**
# 
# **Please run below cell to select features**

# In[19]:


print("Feature Selection")
if data_icu:
    print("Which Features you want to include for cohort?")
    check_input1 = widgets.Checkbox(description='Diagnosis')
    display(check_input1)
    check_input2 = widgets.Checkbox(description='Output Events')
    display(check_input2)
    check_input3 = widgets.Checkbox(description='Chart Events(Labs and Vitals)')
    display(check_input3)
    check_input4 = widgets.Checkbox(description='Procedures')
    display(check_input4)
    check_input5 = widgets.Checkbox(description='Medications')
    display(check_input5)
else:
    print("Which Features you want to include for cohort?")
    check_input1 = widgets.Checkbox(description='Diagnosis', value=True)
    display(check_input1)
    check_input2 = widgets.Checkbox(description='Labs', value=True)
    display(check_input2)
    check_input3 = widgets.Checkbox(description='Procedures', value=True)
    display(check_input3)
    check_input4 = widgets.Checkbox(description='Medications', value=True)
    display(check_input4)
print("**Please run below cell to extract selected features**")


# In[25]:


import time

start = time.time()

print(start)

if data_icu:
    diag_flag=check_input1.value
    out_flag=check_input2.value
    chart_flag=check_input3.value
    proc_flag=check_input4.value
    med_flag=check_input5.value
    if False:
        feature_icu(cohort_output, version_path,diag_flag,out_flag,chart_flag,proc_flag,med_flag)
else:
    diag_flag=check_input1.value
    lab_flag=check_input2.value
    proc_flag=check_input3.value
    med_flag=check_input4.value
    if False:
        feature_nonicu(cohort_output, version_path,diag_flag,lab_flag,proc_flag,med_flag)


end = time.time()

print(start, end)
print(end - start)


# ## 3. CLINICAL GROUPING
# Below you will have option to clinically group diagnosis and medications.
# Grouping medical codes will reduce dimensional space of features.
# 
# Default options selected below will group medical codes to reduce feature dimension space.
# 
# **Please run below cell to select preprocessing for diferent features**

# In[26]:


if data_icu:
    if diag_flag:
        print("Do you want to group ICD 10 DIAG codes ?")
        radio_input4 = widgets.RadioButtons(options=['Keep both ICD-9 and ICD-10 codes','Convert ICD-9 to ICD-10 codes','Convert ICD-9 to ICD-10 and group ICD-10 codes'],value='Keep both ICD-9 and ICD-10 codes',layout={'width': '100%'})
        display(radio_input4)   
    
else:
    if diag_flag:
        print("Do you want to group ICD 10 DIAG codes ?")
        radio_input4 = widgets.RadioButtons(options=['Keep both ICD-9 and ICD-10 codes','Convert ICD-9 to ICD-10 codes','Convert ICD-9 to ICD-10 and group ICD-10 codes'],value='Keep both ICD-9 and ICD-10 codes',layout={'width': '100%'})
        display(radio_input4)     
    if med_flag:
        print("Do you want to group Medication codes to use Non propietary names?")
        radio_input5 = widgets.RadioButtons(options=['Yes','No'],value='No',layout={'width': '100%'})
        display(radio_input5)
    if proc_flag:
        print("Which ICD codes for Procedures you want to keep in data?")
        radio_input6 = widgets.RadioButtons(options=['ICD-9 and ICD-10','ICD-10'],value='ICD-9 and ICD-10',layout={'width': '100%'})
        display(radio_input6)
print("**Please run below cell to perform feature preprocessing**")


# In[27]:


group_diag=False
group_med=False
group_proc=False
if data_icu:
    if diag_flag:
        group_diag=radio_input4.value
    preprocess_features_icu(cohort_output, diag_flag, group_diag,False,False,False,0,0)
else:
    if diag_flag:
        group_diag=radio_input4.value
    if med_flag:
        group_med=radio_input5.value
    if proc_flag:
        group_proc=radio_input6.value
    preprocess_features_hosp(cohort_output, diag_flag,proc_flag,med_flag,False,group_diag,group_med,group_proc,False,False,0,0)


# ### 4. SUMMARY OF FEATURES
# 
# This step will generate summary of all features extracted so far.<br>
# It will save summary files in **./data/summary/**<br>
# - These files provide summary about **mean frequency** of medical codes per admission.<br>
# - It also provides **total occurrence count** of each medical code.<br>
# - For labs and chart events it will also provide <br>**missing %** which tells how many rows for a certain medical code has missing value.
# 
# Please use this information to further refine your cohort by selecting <br>which medical codes in each feature you want to keep and <br>which codes you would like to remove for downstream analysis tasks.
# 
# **Please run below cell to generate summary files**

# ## 5. Feature Selection
# 
# based on the files generated in previous step and other infromation gathered by you,<br>
# Please select which medical codes you want to include in this study.
# 
# Please run below cell to to select options for which features you want to perform feature selection.
# 
# - Select **Yes** if you want to select a subset of medical codes for that feature and<br> **edit** the corresponding feature file for it.
# - Select **No** if you want to keep all the codes in a feature.

# In[29]:


if data_icu:
    if diag_flag:
        print("Do you want to do Feature Selection for Diagnosis \n (If yes, please edit list of codes in ./data/summary/diag_features.csv)")
        radio_input4 = widgets.RadioButtons(options=['Yes','No'],value='No')
        display(radio_input4)       
    if med_flag:
        print("Do you want to do Feature Selection for Medication \n (If yes, please edit list of codes in ./data/summary/med_features.csv)")
        radio_input5 = widgets.RadioButtons(options=['Yes','No'],value='No')
        display(radio_input5)   
    if proc_flag:
        print("Do you want to do Feature Selection for Procedures \n (If yes, please edit list of codes in ./data/summary/proc_features.csv)")
        radio_input6 = widgets.RadioButtons(options=['Yes','No'],value='No')
        display(radio_input6)   
    if out_flag:
        print("Do you want to do Feature Selection for Output event \n (If yes, please edit list of codes in ./data/summary/out_features.csv)")
        radio_input7 = widgets.RadioButtons(options=['Yes','No'],value='No')
        display(radio_input7)  
    if chart_flag:
        print("Do you want to do Feature Selection for Chart events \n (If yes, please edit list of codes in ./data/summary/chart_features.csv)")
        radio_input8 = widgets.RadioButtons(options=['Yes','No'],value='No')
        display(radio_input8)  
else:
    if diag_flag:
        print("Do you want to do Feature Selection for Diagnosis \n (If yes, please edit list of codes in ./data/summary/diag_features.csv)")
        radio_input4 = widgets.RadioButtons(options=['Yes','No'],value='No')
        display(radio_input4)         
    if med_flag:
        print("Do you want to do Feature Selection for Medication \n (If yes, please edit list of codes in ./data/summary/med_features.csv)")
        radio_input5 = widgets.RadioButtons(options=['Yes','No'],value='No')
        display(radio_input5)   
    if proc_flag:
        print("Do you want to do Feature Selection for Procedures \n (If yes, please edit list of codes in ./data/summary/proc_features.csv)")
        radio_input6 = widgets.RadioButtons(options=['Yes','No'],value='No')
        display(radio_input6)   
    if lab_flag:
        print("Do you want to do Feature Selection for Labs \n (If yes, please edit list of codes in ./data/summary/lab_features.csv)")
        radio_input7 = widgets.RadioButtons(options=['Yes','No'],value='No')
        display(radio_input7)   
print("**Please run below cell to perform feature selection**")


# In[30]:


select_diag=False
select_med=False
select_proc=False
select_lab=False
select_out=False
select_chart=False

if data_icu:
    if diag_flag:
        select_diag=radio_input4.value == 'Yes'
    if med_flag:
        select_med=radio_input5.value == 'Yes'
    if proc_flag:
        select_proc=radio_input6.value == 'Yes'
    if out_flag:
        select_out=radio_input7.value == 'Yes'
    if chart_flag:
        select_chart=radio_input8.value == 'Yes'
    features_selection_icu(cohort_output, diag_flag,proc_flag,med_flag,out_flag, chart_flag,select_diag,select_med,select_proc,select_out,select_chart)
else:
    if diag_flag:
        select_diag=radio_input4.value == 'Yes'
    if med_flag:
        select_med=radio_input5.value == 'Yes'
    if proc_flag:
        select_proc=radio_input6.value == 'Yes'
    if lab_flag:
        select_lab=radio_input7.value == 'Yes'
    features_selection_hosp(cohort_output, diag_flag,proc_flag,med_flag,lab_flag,select_diag,select_med,select_proc,select_lab)


# ## 6. CLEANING OF FEATURES
# Below you will have option to to clean lab and chart events by performing outlier removal and unit conversion.
# 
# Outlier removal is performed to remove values higher than selected **right threshold** percentile and lower than selected **left threshold** percentile among all values for each itemid. 
# 
# **Please run below cell to select preprocessing for diferent features**

# In[31]:


if data_icu:
    if chart_flag:
        print("Outlier removal in values of chart events ?")
        layout = widgets.Layout(width='100%', height='40px') #set width and height

        radio_input5 = widgets.RadioButtons(options=['No outlier detection','Impute Outlier (default:98)','Remove outliers (default:98)'],value='No outlier detection',layout=layout)
        display(radio_input5)
        outlier=widgets.IntSlider(
        value=98,
        min=90,
        max=99,
        step=1,
        disabled=False,layout={'width': '100%'}
        )
        left_outlier=widgets.IntSlider(
        value=0,
        min=0,
        max=10,
        step=1,
        disabled=False,layout={'width': '100%'}
        )
        #display(oulier)
        display(widgets.HBox([widgets.Label('Right Outlier Threshold',layout={'width': '150px'}), outlier]))
        display(widgets.HBox([widgets.Label('Left Outlier Threshold',layout={'width': '150px'}), left_outlier]))
    
else:      
    if lab_flag:
        print("Outlier removal in values of lab events ?")
        layout = widgets.Layout(width='100%', height='40px') #set width and height

        radio_input7 = widgets.RadioButtons(options=['No outlier detection','Impute Outlier (default:98)','Remove outliers (default:98)'],value='No outlier detection',layout=layout)
        display(radio_input7)
        outlier=widgets.IntSlider(
        value=98,
        min=90,
        max=99,
        step=1,
        disabled=False,layout={'width': '100%'}
        )
        left_outlier=widgets.IntSlider(
        value=0,
        min=0,
        max=10,
        step=1,
        disabled=False,layout={'width': '100%'}
        )
        #display(oulier)
        display(widgets.HBox([widgets.Label('Right Outlier Threshold',layout={'width': '150px'}), outlier]))
        display(widgets.HBox([widgets.Label('Left Outlier Threshold',layout={'width': '150px'}), left_outlier]))
print("**Please run below cell to perform feature preprocessing**")


# In[32]:


thresh=0
if data_icu:
    if chart_flag:
        clean_chart=radio_input5.value!='No outlier detection'
        impute_outlier_chart=radio_input5.value=='Impute Outlier (default:98)'
        thresh=outlier.value
        left_thresh=left_outlier.value
    preprocess_features_icu(cohort_output, False, False,chart_flag,clean_chart,impute_outlier_chart,thresh,left_thresh)
else:
    if lab_flag:
        clean_lab=radio_input7.value!='No outlier detection'
        impute_outlier=radio_input7.value=='Impute Outlier (default:98)'
        thresh=outlier.value
        left_thresh=left_outlier.value
    preprocess_features_hosp(cohort_output, False,False,False,lab_flag,False,False,False,clean_lab,impute_outlier,thresh,left_thresh)


# ## 7. Time-Series Representation
# In this section, please choose how you want to process and represent time-series data.
# 
# - First option is to select the length of time-series data you want to include for this study. (Default is 72 hours)
# 
# - Second option is to select bucket size which tells in what size time windows you want to divide your time-series.<br>
# For example, if you select **2** bucket size, it wil aggregate data for every 2 hours and <br>a time-series of length 24 hours will be represented as time-series with 12 time-windows <br>where data for every 2 hours is agggregated from original raw time-series.
# 
# During this step, we will also save the time-series data in data dictionaries in the format that can be directly used for following deep learning analysis.
# 
# ### Imputation
# You can also choose if you want to impute lab/chart values. The imputation will be done by froward fill and mean or median imputation.<br>
# Values will be forward fill first and if no value exists for that admission we will use mean or median value for the patient.
# 
# The data dictionaries will be saved in **./data/dict/**
# 
# Please refer the readme to know the structure of data dictionaries.
# 
# **Please run below cell to select time-series representation**

# In[36]:


print("=======Time-series Data Represenation=======")

print("Length of data to be included for time-series prediction ?")
if(data_mort):
    radio_input8 = widgets.RadioButtons(options=['First 72 hours','First 48 hours','First 24 hours','Custom'],value='First 72 hours')
    display(radio_input8)
    text2=widgets.IntSlider(
    value=72,
    min=24,
    max=72,
    step=1,
    description='Fisrt',
    disabled=False
    )
    display(widgets.HBox([widgets.Label('Fisrt (in hours):',layout={'width': '150px'}), text2]))
elif(data_admn):
    radio_input8 = widgets.RadioButtons(options=['Last 72 hours','Last 48 hours','Last 24 hours','Custom'],value='Last 72 hours')
    display(radio_input8)
    text2=widgets.IntSlider(
    value=72,
    min=24,
    max=72,
    step=1,
    description='Last',
    disabled=False
    )
    display(widgets.HBox([widgets.Label('Last (in hours):',layout={'width': '150px'}), text2]))
elif(data_los):
    radio_input8 = widgets.RadioButtons(options=['First 12 hours','First 24 hours','Custom'],value='First 24 hours')
    display(radio_input8)
    text2=widgets.IntSlider(
    value=72,
    min=12,
    max=72,
    step=1,
    description='First',
    disabled=False
    )
    display(widgets.HBox([widgets.Label('Fisrt (in hours):',layout={'width': '150px'}), text2]))
    
    
print("What time bucket size you want to choose ?")
radio_input7 = widgets.RadioButtons(options=['1 hour','2 hour','3 hour','4 hour','5 hour', '24 hour', 'Custom'],value='24 hour')
display(radio_input7)
text1=widgets.IntSlider(
    value=1,
    min=1,
    max=24,
    step=1,
    disabled=False
    )
#display(text1)
display(widgets.HBox([widgets.Label('Bucket Size (in hours):',layout={'width': '150px'}), text1]))
print("Do you want to forward fill and mean or median impute lab/chart values to form continuous data signal?")
radio_impute = widgets.RadioButtons(options=['No Imputation', 'forward fill and mean','forward fill and median'],value='No Imputation')
display(radio_impute)   

radio_input6 = widgets.RadioButtons(options=['0 hours','2 hours','4 hours','6 hours'],value='0 hours')
if(data_mort):
    print("If you have choosen mortality prediction task, then what prediction window length you want to keep?")
    radio_input6 = widgets.RadioButtons(options=['2 hours','4 hours','6 hours','8 hours','Custom'],value='2 hours')
    display(radio_input6)
    text3=widgets.IntSlider(
    value=2,
    min=2,
    max=8,
    step=1,
    disabled=False
    )
    display(widgets.HBox([widgets.Label('Prediction window (in hours)',layout={'width': '180px'}), text3]))
print("**Please run below cell to perform time-series represenation and save in data dictionaries**")


# In[ ]:


if (radio_input6.value=='Custom'):
    predW=int(text3.value)
else:
    predW=int(radio_input6.value[0].strip())
if (radio_input7.value=='Custom'):
    bucket=int(text1.value)
else:
    bucket=int(radio_input7.value.split()[0])
if (radio_input8.value=='Custom'):
    include=int(text2.value)
else:
    include=int(radio_input8.value.split()[1])
if (radio_impute.value=='forward fill and mean'):
    impute='Mean'
elif (radio_impute.value=='forward fill and median'):
    impute='Median'
else:
    impute=False

if data_icu:
    gen=data_generation_icu.Generator(cohort_output,data_mort,data_admn,data_los,diag_flag,proc_flag,out_flag,chart_flag,med_flag,impute,include,bucket,predW)
    #gen=data_generation_icu.Generator(cohort_output,data_mort,diag_flag,False,False,chart_flag,False,impute,include,bucket,predW)
    #if chart_flag:
    #    gen=data_generation_icu.Generator(cohort_output,data_mort,False,False,False,chart_flag,False,impute,include,bucket,predW)
else:
    gen=data_generation.Generator(cohort_output,data_mort,data_admn,data_los,diag_flag,lab_flag,proc_flag,med_flag,impute,include,bucket,predW)

