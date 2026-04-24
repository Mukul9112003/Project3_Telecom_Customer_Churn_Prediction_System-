from dataclasses import dataclass
@dataclass
class DataIngestionArtifact:
    trained_file_path:str
    tested_file_path:str
    validate_file_path:str
@dataclass
class DataValidationArtifact:
    status:bool
    message:str
    validation_report_file_path:str
@dataclass
class DataTransformationArtifact:
    trained_transformed_filepath:str
    tested_transformed_filepath:str
    validate_transformed_filepath:str
    preprocessing_file_object_filepath:str
@dataclass
class ClassificationMetricArtifact:
    precision:float
    accuracy:float
    recall:float
    f1_score:float
    classification_report:str

@dataclass
class ModelTrainerArtifact:
    trained_model:str
    metric_artifact:ClassificationMetricArtifact
@dataclass
class ModelEvaluationArtifact:
    is_model_accepted:bool
    changed_accuracy:float
    s3_model_path:str 
    trained_model_path:str
@dataclass
class ModelPusherArtifact:
    bucket_name:str
    s3_model_path:str