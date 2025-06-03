import sys
import os
import numpy as np
import pandas as pd
from sklearn.impute import KNNImputer
from sklearn.pipeline import Pipeline
from networksecurity.constant.training_pipeline import TARGET_COLUMN
from networksecurity.constant.training_pipeline import DATA_TRANSFORMATION_IMPUTER_PARAMS

from networksecurity.entity.artifact_entity import (DataTransformationArtifact,DataValidationArtifact)
from networksecurity.entity.config_entity import DataTransformationConfig
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.utils.main_utils.utils import save_numpy_array_data, save_object


class DataTransformation:
    def __init__(self, data_validation_artifact: DataValidationArtifact,data_transformation_config: DataTransformationConfig):
        """
        Initializes the DataTransformation class with the provided artifacts.

        :param data_validation_artifact: Artifact containing validation data paths.
        :param data_transformation_config: Configuration for data transformation.
        """
        try:
            self.data_validation_artifact = data_validation_artifact
            self.data_transformation_config = data_transformation_config

        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    @staticmethod
    def read_data(file_path: str) -> pd.DataFrame:
        """
        Reads data from a CSV file and returns it as a DataFrame.

        :param file_path: Path to the CSV file.
        :return: DataFrame containing the data.
        """
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    def get_data_transformer_object(self) -> Pipeline:
        """
        Creates a data transformation pipeline with KNN imputer.
        :return: A Pipeline object with KNN imputer.
        """
        logging.info("Entered get_data_transformer_object method of DataTransformation class")
        try:
            imputer:KNNImputer = KNNImputer(**DATA_TRANSFORMATION_IMPUTER_PARAMS)
            logging.info("KNNImputer created with parameters: %s", DATA_TRANSFORMATION_IMPUTER_PARAMS)
            processor:Pipeline = Pipeline(steps=[("imputer", imputer)])
            return processor

        except Exception as e:
            raise NetworkSecurityException(e, sys)


    def initiate_data_transformation(self) -> DataTransformationArtifact:
        """
        Initiates the data transformation process.

        :return: DataTransformationArtifact containing paths to transformed data.
        """
        logging.info("Initiating data transformation process.")
        try:
            logging.info("Starting data transformation process.")

            # Load training and testing data
            train_df = DataTransformation.read_data(self.data_validation_artifact.valid_train_file_path)
            test_df = DataTransformation.read_data(self.data_validation_artifact.valid_test_file_path)

            #taining dataframe
            input_feature_train_df = train_df.drop(columns=[TARGET_COLUMN],axis=1)
            target_feature_train_df = train_df[TARGET_COLUMN]
            target_feature_train_df = target_feature_train_df.replace(-1,0)

            #testing dataframe
            input_feature_test_df = test_df.drop(columns=[TARGET_COLUMN],axis=1)
            target_feature_test_df = test_df[TARGET_COLUMN]
            target_feature_test_df = target_feature_test_df.replace(-1,0)

            # Create a KNN imputer
            preprocessor = self.get_data_transformer_object()
            preprocessor_object = preprocessor.fit(input_feature_train_df)
            transformed_input_feature_train_df = preprocessor_object.transform(input_feature_train_df)
            transformed_input_feature_test_df = preprocessor_object.transform(input_feature_test_df)

            train_array = np.c_[transformed_input_feature_train_df, target_feature_train_df.to_numpy()]
            test_array = np.c_[transformed_input_feature_test_df, target_feature_test_df.to_numpy()]

            #save numpy array data
            save_numpy_array_data(self.data_transformation_config.transformed_train_file_path, train_array)
            save_numpy_array_data(self.data_transformation_config.transformed_test_file_path, test_array)
            save_object(self.data_transformation_config.transformed_object_file_path, preprocessor_object)

            #preparing artifacts
            data_transformation_artifact = DataTransformationArtifact(
                transformed_object_file_path=self.data_transformation_config.transformed_object_file_path,
                transformed_train_file_path=self.data_transformation_config.transformed_train_file_path,
                transformed_test_file_path=self.data_transformation_config.transformed_test_file_path)
            

            # Save the transformed data
            save_numpy_array_data(self.data_transformation_config.transformed_train_file_path, train_array)
            save_numpy_array_data(self.data_transformation_config.transformed_test_file_path, test_array)

            # Save the imputer object
            save_object(self.data_transformation_config.transformed_object_file_path, preprocessor_object)

            logging.info("Data transformation completed successfully.")

            return DataTransformationArtifact

        except Exception as e:
            logging.error(f"Error during data transformation: {e}")
            raise NetworkSecurityException(e, sys)
