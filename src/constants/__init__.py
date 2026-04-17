import os
from datetime import date
from from_root import from_root 
DATABASE_NAME="Project"
COLLECTION_NAME="Telco-Customer-Churn"
MONGODB_URL_KEY="MONGODB_URL"
PIPELINE_NAME=""
ARTIFACT_DIR="artifact"
CURRENT_YEAR=date.today().year
FILE_NAME="data.csv"
TRAIN_FILE_NAME="train.csv"
TEST_FILE_NAME="test.csv"
REPORT_FILE_PATH="report.yaml"
SCHEMA_FILE_NAME=from_root("config/Schema.yaml")
DATA_INGESTION_DIR_NAME:str="data_ingestion"
DATA_INGESTION_INGESTED_DIR:str="ingested"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO:float=0.25
DATA_INGESTION_FEATURE_STORE_DIR:str="feature_store"
DATA_INGESTION_COLLECTION_NAME:str="Telco-Customer-Churn"
DATA_VALIDATION_DIR_NAME:str="data_validation"
DATA_VALIDATION_SCHEMA_FILE_PATH:str="config/schema.yaml"
DATA_TRANSFORMATION_DIR_NAME:str="data_transformation"
DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR:str="transformed_data"
DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR:str="object"
PREPROCESSING_OBJECT_FILE_NAME="preprocessing.pkl"
TARGET_COLUMN="Churn"