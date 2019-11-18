# Overview
__*Towards Semi-Automatic Embedded Data Type Inferencing*__ is a project that expands on the 3rd phase of an existing project known as the [ML Data Prep Zoo](https://github.com/pvn25/ML-Data-Prep-Zoo). Our work is an approach using machine learning models to classify contextual data that requires further extraction. We have created our own dictionary for the data to be labelled by and is as follows:
1. Numbers
2. List
3. Datetime
4. Sentence
5. URL
6. Custom Object

The current dataset and results include ~541 datapoints with our best accuracy (~86%) coming from Random Forest. All scripts to help labelling have been written in Python and all model testing has been used in Jupyter Notebooks. Oue models come from using the Python library, scikit-learn, and have been validated using *k*-fold cross validation.

# Scripts
NOTE: All scripts have been moved into the *Preprocessing_Scripts* folder, however the paths to data have been hardcoded. To execute the script without error, move the files outside of the folder. The following section gives a brief summary of each script and it's usage. Order listed is the expected order of execution
1. ```tobelabelled_list_creator.py``` : Short script file that creates two CSV's needed for the project. This script specifically looks through our original data file (not included in this repository) and looks for rows that have been labelled *'Usable with Extraction.'* The two CSV's include: 
    - *needs_extraction.csv* : Contains the original base featurization data of each row.
    - *record_ids.csv* : Contains the `Record_id` and `Attribute_name` of each row.
2. ```labeller_cli_tool.py``` : CLI script that helped the manual labelling process of the project. The script would first display meaningful features of the row, ask the user what is the appropriate label, the specific reason (also part of a list detailed in our technical report), and document these results in `labelled_data.csv.`
3. ```rulebased_auto_labeller.py``` : Rulebased approach we've created. A small portion is dependent on `pandas.Timestamp` object for recognizing *Datetime* rows. Details about our rulebased approach can be found in our technical report. The return CSV for the rulebased approach is found at *rulebook_labelled.csv.*
4. ```add_features.py``` : This script was made after our initial featurization in order to test new features that may improve our models. The return CSV is found at *labelled_added.csv.* This script adds the features related to *stopword_total, whitespace_count, char_count, delim_count, has_url, has_date,* and *has_email.*

# Jupyter Notebooks
NOTE: All notebooks have been moved into the *Jupyter_Notebooks* folder, however the paths to data have been hardcoded. To execute the notebook without error, move the files outside of the folder.
+ ```Model Comparison.ipynb``` : Primary notebook for viewing best performing models in a single notebook
+ ```Feature Testing.ipynb``` :Extra notebook for a closer view of a models' misclassifications.
+ ```knn.ipynb, Logistic Regression.ipynb, RBF-SVM.ipynb, RandomForest.ipynb``` : Models used. Included are ablation results, *k* fold cross validation results, and best performing model with its predictions.