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