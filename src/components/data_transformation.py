import numpy as np
import os
from sklearn.pipeline import Pipeline 
from src.logger import logging
from src.exception import MyException
from sklearn.preprocessing import OneHotEncoder
from src.entity.config_entity import DataTransformationConfig
from src.entity.artifact_entity import DataTransformationArtifact,DataValidationArtifact,DataIngestionArtifact
from src.constants import SCHEMA_FILE_NAME
from src.utils.main_utils import read_yaml_file,save_object,read_csv_file,save_numpy_array
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.base import BaseEstimator,TransformerMixin
from sklearn.impute import SimpleImputer
from src.constants import TARGET_COLUMN
class Mera_Transformer(BaseEstimator,TransformerMixin):
    def __init__(self,services):
        self.services=services
    def fit(self,X,y=None):
        return self
    def transform(self,X,y=None):
        X = X.copy()
        X["tenure"]=pd.to_numeric(X["tenure"],errors="coerce").fillna(0)
        X["tenure_group"]=pd.cut(X["tenure"],bins=[0,12,24,48,100],labels=["High Chances","Chances","low Chances","very low chances"],include_lowest=True)
        X["InternetService_used"]=X["InternetService"].map({"No":"No","Fiber optic":"Yes","DSL":"Yes"})
        X["MultipleLines"]=X["MultipleLines"].map({"No phone service":"No","Yes":"Yes","No":"No"})
        X["number_of_services"]=X[self.services].eq("Yes").sum(axis=1)
        X["Partner"] = X["Partner"].str.strip().str.capitalize()
        X["Dependents"] = X["Dependents"].str.strip().str.capitalize()
        X["is_high_risk"]=((X["Contract"]=="Month-to-month") & (X["tenure_group"]=="High Chances")).astype("bool")
        X["Partner"] = X["Partner"].map({"Yes": 1, "No": 0})
        X["Dependents"] = X["Dependents"].map({"Yes": 1, "No": 0})
        X["family_present"]=(X["SeniorCitizen"]+X["Partner"]+X["Dependents"])
        X=X.drop(columns=["customerID"],errors="ignore")
        return X
    
class DataTransformation:
    def __init__(self,data_transformation_config:DataTransformationConfig,data_validation_artifact:DataValidationArtifact,data_ingestion_artifact:DataIngestionArtifact):
        try:
            self.data_transformation_config=data_transformation_config
            self.data_ingestion_artifact=data_ingestion_artifact
            self.data_validation_artifact=data_validation_artifact
            self._Schema_config=read_yaml_file(filepath=SCHEMA_FILE_NAME)
        except Exception as e:
            raise MyException(e) from e
    def preprocessing_start(self):
        try:
            expected_col=self._Schema_config["services"]
            preprocessing=Pipeline(steps=[
                ("mera",Mera_Transformer(expected_col)),
                ("category_handling",ColumnTransformer(transformers=[("encoding",OneHotEncoder(handle_unknown="ignore",drop="first",sparse_output=False),self._Schema_config["category"]),("total",SimpleImputer(strategy="median"),["TotalCharges"])],remainder="passthrough"
                ))
           ])
            return preprocessing
        except Exception as e:
            raise MyException(e) from e
    def IniciateDataTransformation(self):
        try:
            if self.data_validation_artifact.status:
                train=read_csv_file(self.data_ingestion_artifact.trained_file_path)
                test=read_csv_file(self.data_ingestion_artifact.tested_file_path)
                validate=read_csv_file(self.data_ingestion_artifact.validate_file_path)
                logging.info("train and test data load successfully from data ingestion artifact ")
                X_train,y_train=train.drop(columns=[TARGET_COLUMN],axis=1),train[TARGET_COLUMN]
                X_test,y_test=test.drop(columns=[TARGET_COLUMN],axis=1),test[TARGET_COLUMN]
                X_val,y_val=validate.drop(columns=[TARGET_COLUMN],axis=1),validate[TARGET_COLUMN]
                expected_col = self._Schema_config["services"]
                preprocessing=self.preprocessing_start()
                preprocessing.fit(X_train)
                logging.info("Preprocessing object made successfully")
                y_train=y_train.map({"Yes":1,"No":0}).astype(int)
                y_test=y_test.map({"Yes":1,"No":0}).astype(int)
                y_val=y_val.map({"Yes":1,"No":0}).astype(int)
                X_transformed_train=preprocessing.transform(X_train)
                X_transformed_test=preprocessing.transform(X_test)
                X_transformed_val=preprocessing.transform(X_val)
                transformed_train=np.c_[X_transformed_train,y_train]
                transformed_test=np.c_[X_transformed_test,y_test]
                transformed_val=np.c_[X_transformed_val,y_val]
                dir_name=os.path.dirname(self.data_transformation_config.preprocessing_object_file_path)
                os.makedirs(dir_name,exist_ok=True)
                save_object(filepath=self.data_transformation_config.preprocessing_object_file_path,content=preprocessing)
                logging.info("Preprocessing object is store successfully")
                dir_name=os.path.dirname(self.data_transformation_config.transformed_train_file_path)
                os.makedirs(dir_name,exist_ok=True)
                save_numpy_array(filepath=self.data_transformation_config.transformed_train_file_path,content=transformed_train)
                logging.info("Transformed train array is store successfully")
                save_numpy_array(filepath=self.data_transformation_config.transformed_test_file_path,content=transformed_test)
                logging.info("Transformed test array is store successfully")
                save_numpy_array(filepath=self.data_transformation_config.transformed_validate_file_path,content=transformed_val)
                logging.info("Transformed test array is store successfully")
                data_transformation_artifact=DataTransformationArtifact(trained_transformed_filepath=self.data_transformation_config.transformed_train_file_path,tested_transformed_filepath=self.data_transformation_config.transformed_test_file_path,preprocessing_file_object_filepath=self.data_transformation_config.preprocessing_object_file_path,validate_transformed_filepath=self.data_transformation_config.transformed_validate_file_path)
                return data_transformation_artifact
        except Exception as e:
            raise MyException(e) from e
