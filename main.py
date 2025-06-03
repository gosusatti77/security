from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.components.data_validation import DataValidation
from networksecurity.components.data_transformation import DataTransformation
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.entity.config_entity import DataIngestionConfig,DataValidationConfig
from networksecurity.entity.config_entity import TrainingPipelineConfig
from networksecurity.entity.config_entity import DataTransformationConfig

import sys
from datetime import datetime


if __name__ == "__main__":
    try:
        training_pipeline_config = TrainingPipelineConfig(datetime.now())
        dataingestionconfig = DataIngestionConfig(training_pipeline_config)
         
        data_ingestion = DataIngestion(dataingestionconfig)
        logging.info(f"Data Ingestion started with config: {dataingestionconfig}")
        data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
        logging.info(f"Data Ingestion completed with artifact: {data_ingestion_artifact}")
        print(data_ingestion_artifact)

        data_validation_config = DataValidationConfig(training_pipeline_config)
        data_validation=DataValidation(data_ingestion_artifact,data_validation_config)
        logging.info(f"Data Validation started with config: {data_validation_config}")
        data_validation_artifact= data_validation.initiate_data_validation()
        logging.info(f"Data Validation completed with artifact: {data_validation_artifact}")
        print(data_validation_artifact)

        data_transformation_config = DataTransformationConfig(training_pipeline_config)
        data_transformation = DataTransformation(data_validation_artifact, data_transformation_config)
        logging.info(f"Data Transformation started with config: {data_transformation_config}")
        data_transformation_artifact = data_transformation.initiate_data_transformation()
        logging.info(f"Data Transformation completed with artifact: {data_transformation_artifact}")
        print(data_transformation_artifact)
        



    except Exception as e:
        raise NetworkSecurityException(e, sys)