from dataclasses import dataclass
@dataclass
class DataIngestionArtifact:
    trained_file_path:str
    tested_file_path:str
@dataclass
class DataVAlidationArtifact:
    validation_report_file_path:str
    