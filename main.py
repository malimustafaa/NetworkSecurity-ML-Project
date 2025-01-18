from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.entity.config_entity import DataIngestionConfig,DataTransformationConfig
from networksecurity.entity.config_entity import DataValidationConfig,ModelTrainerConfig
from networksecurity.components.data_validation import DataValidation
from networksecurity.components.data_transformation import DataTransformation
from networksecurity.components.model_trainer import ModelTrainer
from networksecurity.entity.config_entity import TrainingPipelineConfig
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.entity.artifact_entity import DataIngestionArtifact,DataTransformationArtifact
import sys


if __name__ == "__main__":
    try:
        training_pipeline_config = TrainingPipelineConfig()
        data_ingestion_config = DataIngestionConfig(training_pipeline_config)
        data_ingestion = DataIngestion(data_ingestion_config) 
        logging.info("initiate the data ingestion")
        data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
        logging.info("data ingestion completed")
        print(data_ingestion_artifact.trained_file_path)
        data_validation_config = DataValidationConfig(training_pipeline_config)
        data_validation = DataValidation(data_ingestion_artifact,data_validation_config)
        logging.info("initiate the data validation")
        data_validation_artifact = data_validation.initiate_data_validation()
        logging.info("data validation completed")
        print(data_validation_artifact)
        logging.info("initiate data transformation")

        data_transformation_config = DataTransformationConfig(training_pipeline_config)
        data_transformation = DataTransformation(data_validation_artifact,data_transformation_config)
        data_transformation_artifact = data_transformation.initiate_data_transformation()
        print(data_transformation_artifact)
        logging.info("data transformation completed")

        logging.info("Model Training started")
        model_trainer_config = ModelTrainerConfig(training_pipeline_config)
        model_trainer = ModelTrainer(model_trainer_config,data_transformation_artifact)
        model_trainer_artifact = model_trainer.initiate_model_trainer()
        print(model_trainer_artifact)
    except Exception as e:
        raise NetworkSecurityException(e,sys)
    