from networksecurity.entity.artifact_entity import DataIngestionArtifact,DataValidationArtifact
from networksecurity.entity.config_entity import DataValidationConfig
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.constant.training_pipeline import SCHEMA_FILE_PATH
from scipy.stats import ks_2samp # for data drift
import pandas as pd
import os,sys
from networksecurity.utils.main_utils.utils import read_yaml_file,write_yaml_file


class DataValidation:
    def __init__(self,data_ingestion_artifact:DataIngestionArtifact,
                 data_validation_config:DataValidationConfig):
        try:
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_config = data_validation_config
            self._schema_config = read_yaml_file(SCHEMA_FILE_PATH)
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    @staticmethod #one time function can be written as staticmethod
    def read_data(file_path) -> pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    def validate_number_of_columns(self,dataframe:pd.DataFrame)->bool:
        try:
            number_of_columns = len(self._schema_config['columns'])
            logging.info(f"required no of columns: {number_of_columns}")
            logging.info(f"Dataframe has columns: {len(dataframe.columns)}")
            if len(dataframe.columns) == number_of_columns:
                return True
            return False
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    def validate_numeric(self,dataframe:pd.DataFrame)->bool:
        try:
         # numeric columns
         numeric_schema = self._schema_config['numerical_columns']
         numeric_df = dataframe.select_dtypes(include = ['int64']).columns
         if set(numeric_schema) != set(numeric_df):
             return False
         return True
        
             
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    def detect_data_drift(self,base_df,current_df,threshold=0.05)->bool:
        try:
            status = True
            report = {}
            for column in base_df.columns:
                d1 = base_df[column]
                d2 = current_df[column] # current df is new data which we will get
                is_sample_dist = ks_2samp(d1,d2) # to compare distribution of 2 data samples
                if threshold < is_sample_dist.pvalue:
                    is_found = False
                else:
                    is_found = True # data drift found between two data 
                    status = False
                report.update({column:{
                    "p_value": float(is_sample_dist.pvalue),
                    "drift_status": is_found
                }})
            drift_report_file_path = self.data_validation_config.data_drift_report_file_path
            # create directory
            dir_path = os.path.dirname(drift_report_file_path)
            os.makedirs(dir_path,exist_ok=True)
            write_yaml_file(drift_report_file_path,report)
            return status
        
        




        except Exception as e:
            raise NetworkSecurityException(e,sys)



        except Exception as e:
            raise NetworkSecurityException(e,sys)

    def initiate_data_validation(self) -> DataValidationArtifact:
        try:
            train_file_path = self.data_ingestion_artifact.trained_file_path
            test_file_path = self.data_ingestion_artifact.test_file_path

            # read the data from train and test
            train_dataframe = DataValidation.read_data(train_file_path)
            test_dataframe = DataValidation.read_data(test_file_path)
            #validate number of columns
            status = self.validate_number_of_columns(train_dataframe)
            if not status:
                error_message = f" Train dataframe does not contain same number of columns "
                raise NetworkSecurityException(error_message, sys)
            status = self.validate_number_of_columns(test_dataframe)
            if not status:
                error_message = f"Test dataframe does not contain same number of columns "
                raise NetworkSecurityException(error_message, sys)
            numeric_data = self.validate_numeric(train_dataframe)
            if not numeric_data:
                 error_message = f"Train dataframe does not contain same numeric columns "
            numeric_data = self.validate_numeric(test_dataframe)
            if not numeric_data:
                error_message = f"Test dataframe does not contain same numeric columns "
            # lets check data drift
            status = self.detect_data_drift(base_df=train_dataframe,current_df=test_dataframe)
            dir_path = os.path.dirname(self.data_validation_config.valid_train_file_path)
            os.makedirs(dir_path,exist_ok=True)
            if status:
                train_dataframe.to_csv(self.data_validation_config.valid_train_file_path,header=True,index=False)
                test_dataframe.to_csv(self.data_validation_config.valid_test_file_path,index=False,header=True)
            else:
                train_dataframe.to_csv(self.data_validation_config.invalid_train_file_path,header=True,index=False)
                test_dataframe.to_csv(self.data_validation_config.invalid_test_file_path,index=False,header=True)

                
            return DataValidationArtifact(status,self.data_validation_config.valid_train_file_path,self.data_validation_config.valid_test_file_path,self.data_validation_config.invalid_train_file_path,self.data_validation_config.invalid_test_file_path,self.data_validation_config.data_drift_report_file_path)
            # return DataValidationArtifact(status,self.data_validation_config.valid_train_file_path,self.data_validation_config.valid_test_file_path,self.data_validation_config.invalid_train_file_path,self.data_validation_config.invalid_test_file_path,self.data_validation_config.data_drift_report_file_path)


    



                



        except Exception as e:
            raise NetworkSecurityException(e,sys)




