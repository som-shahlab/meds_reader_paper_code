## meds_reader: A Pythonic interface for MEDS datasets

meds_reader is a fast and easy-to-use library for reading and processing subject data stored in [MEDS (Medical Event Data Standard)](https://github.com/Medical-Event-Data-Standard/) format using a Python-native API.

Inspired by HuggingFace Datasets, meds_reader transforms MEDS datasets into collections of Python objects, that can then be processed using normal Python functions.

### Example

```bash
# First we need to convert to a database
# That requires running the following command in a terminal
$ meds_reader_convert mimic_meds mimic_meds_reader --num_threads 4
```

```python
# Now we can use Python to interact with our data
import meds_reader

# We can now construct a database
database = meds_reader.SubjectDatabase("mimic_meds_reader")

# Databases are dict-like objects that store subject data

# We can iterate through all the subject ids in the database
for subject_id in database:

    # We can retrieve subject data given a subject_id
    subject = database[subject_id]

    # Subject data can be manipulated with normal Python operations
    print(subject.subject_id)
    for event in subject.events:
        print(event.time, event.code)

        # We can also iterate through all properties in a generic manner
        for property_name, property_value in event:
            print(property_name, property_value)
```

### Installation

meds_reader can be installed using pip.

```bash
pip install meds_reader
```
