import os
import sys
import numpy as np
import pandas as pd

'''
defining common constant variable for training pipeline
'''
TARGET_COLUMN = "Result"
PIPELINE_NAME:str = "NetworkSecurity"
ARTIFACT_DIR:str = "Artifacts"
FILE_NAME:str = "phisingData.scv"

TRAIN_FILE_NAME: str = "train.csv"
TEST_FILE_NAME:str = "test.csv"
SCHEMA_FILE_PATH = "networksecurity/data_schema/schema.yaml"

MODEL_FILE_NAME = "trained_model.pkl"
SAVED_MODEL_DIR = "savel_models"


#os.path.join("data_schema","schema.yaml")






'''
 Data Ingestion related constants start with DATA_INGESTION VAR NAME

 '''
DATA_INGESTION_COLLECTION_NAME:str = "NetworkData"
DATA_INGESTION_DATABASE_NAME:str = "ALI_AI"
DATA_INGESTION_DIR_NAME :str= "data_ingestion"
DATA_INGESTION_FEATURE_STORE_DIR :str = "feature_store"
DATA_INGESTION_INGESTED_DIR :str= "ingested"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO :float = 0.2

"""
Data Validation related constants
"""
DATA_VALIDATION_DIR_NAME: str = "data_validation"
DATA_VALIDATION_VALID_DIR:str = "valid"
DATA_VALIDATION_INVALID_DIR : str = "invalid"
DATA_VALIDATION_DRIFT_REPORT_DIR:str = "drift_report"
DATA_VALIDATION_DRIFT_REPORT_FILENAME:str = "report.yaml"

"""
Data Transformation related constants
"""
DATA_TRANSFORMATION_DIR_NAME:str = "data_transformation"
DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR:str = "transformed"
DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR:str = "transformed_object"
PRE_PROCESSING_OBJECT_FILE_NAME = "preprocessor.pkl"

#knn imputer for replacing nan values
DATA_TRANSFORMATION_IMPUTER_PARAMS : dict = {
    "missing_values":np.nan,
    "n_neighbors":3, #calculate avg value of 3 nearest neighbor, and replace nan value with that
    "weights":"uniform"
}

"""
Model Trainer related constants
"""

MODEL_TRAINER_DIR_NAME:str = "model_trainer"
MODEL_TRAINER_TRAINED_MODEL_DIR:str= "trained_model"
#MODEL_TRAINER_TRAINED_MODEL_NAME:str= "trained_model.pkl"
MODEL_TRAINER_EXPECTED_SCORE:float = 0.6
MODEL_TRAINER_OVERFITTING_UNDERFITTING_THRESHOLD :float = 0.05
