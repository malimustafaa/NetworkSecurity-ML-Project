import sys
import os
import numpy as np
import pandas as pd
from sklearn.impute import KNNImputer
from sklearn.pipeline import Pipeline
from networksecurity.constant.training_pipeline import TARGET_COLUMN
from networksecurity.constant.training_pipeline import DATA_TRANSFORMATION_IMPUTER_PARAMS
from networksecurity.entity.artifact_entity import (
    DataTransformationArtifact,
    DataValidationArtifact
)
from networksecurity.utils.main_utils.utils import save_numpy_array_data,save_object
##from utils.main_utils.utils import save_numpy_array_data,save_object
from networksecurity.entity.config_entity import DataTransformationConfig
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

class DataTransformation:
    def __init__(self,data_validation_artifact:DataValidationArtifact,data_transformation_config:DataTransformationConfig):
        try:
            self.data_validation_artifact = data_validation_artifact
            self.data_transformation_config = data_transformation_config


        except Exception as e:
            raise NetworkSecurityException(e,sys)
    @staticmethod # static method doesnt require a object to be called, you can directly call with class name
    def read_data(file_path)->pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    def get_data_transformer_object(cls)->Pipeline:
        '''
        it initialises a knn imputer object with the parameters specified
        in the training pipeline.py file and returns a Pipeline oject with the
        KNNImputer object as the first step.

        Args:DataTransformation

        returns:
        A pipeline object

        '''
        try:
           '''
           When you write KNNImputer(**DATA_TRANSFORMATION_IMPUTER_PARAMS), it is equivalent to:
           KNNImputer(n_neighbors=5, weights="uniform", missing_values=None)

           '''
           imputer:KNNImputer= KNNImputer(**DATA_TRANSFORMATION_IMPUTER_PARAMS) # ** considers that given parameter is in key:value pair
           logging.info(f"initialize knn imputer with {DATA_TRANSFORMATION_IMPUTER_PARAMS}")
           processor:Pipeline = Pipeline([("imputer",imputer)])
           return processor

        except Exception as e:
            raise NetworkSecurityException(e,sys)
    def initiate_data_transformation(self)->DataTransformationArtifact:
        logging.info("entered initiate data transformation method of DataTransformation class")
        try:
            logging.info("starting data transformation")
            train_df = DataTransformation.read_data(self.data_validation_artifact.valid_train_file_path)
            test_df = DataTransformation.read_data(self.data_validation_artifact.valid_test_file_path)
            #training dataframe 
            input_feature_train_df = train_df.drop(columns=[TARGET_COLUMN],axis=1)
            target_feature_train_df = train_df[TARGET_COLUMN]
            target_feature_train_df = target_feature_train_df.replace(-1,0) # target column has -1 and 0, so converting -1 to 0, so that
            #we have 1 and 0, easy to differentiate


            #testing dataframe
            input_feature_test_df = test_df.drop(columns = [TARGET_COLUMN],axis=1)
            target_feature_test_df = test_df[TARGET_COLUMN]
            target_feature_test_df = target_feature_test_df.replace(-1,0)
            preprocessor = self.get_data_transformer_object()
            preprocessor_obj = preprocessor.fit(input_feature_train_df)
            transformed_input_train_features = preprocessor_obj.transform(input_feature_train_df)
            transformed_input_test_features = preprocessor_obj.transform(input_feature_test_df)

            train_arr = np.c_[transformed_input_train_features,np.array(target_feature_train_df)]
            test_arr = np.c_[transformed_input_test_features,np.array(target_feature_test_df)]

            #save numpy arrays
            save_numpy_array_data(self.data_transformation_config.transformed_train_file_path,train_arr)
            save_numpy_array_data(self.data_transformation_config.transformed_test_file_path,test_arr)
            save_object(self.data_transformation_config.transformed_object_file_path,preprocessor_obj)
            save_object("final_models/preprocessor.pkl",preprocessor_obj)


            data_transformation_artifact = DataTransformationArtifact(self.data_transformation_config.transformed_object_file_path,self.data_transformation_config.transformed_train_file_path,self.data_transformation_config.transformed_test_file_path)
            return data_transformation_artifact



        



        except Exception as e:
            raise NetworkSecurityException(e,sys)

