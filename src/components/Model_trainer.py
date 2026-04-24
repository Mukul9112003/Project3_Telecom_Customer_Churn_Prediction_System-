from src.exception import MyException
from src.logger import logging
from src.constants import *
import os
from src.entity.estimator import MyModel
from src.entity.config_entity import ModelTrainerConfig
from src.entity.artifact_entity import ModelTrainerArtifact,ClassificationMetricArtifact,DataTransformationArtifact
from src.utils.main_utils import read_yaml_file,load_numpy_array,save_object,load_object,write_yaml_file
from xgboost import XGBClassifier
import numpy as np
from sklearn.base import BaseEstimator,ClassifierMixin
from sklearn.metrics import precision_score,recall_score,accuracy_score,f1_score,classification_report,precision_recall_curve
class MeraModel(BaseEstimator,ClassifierMixin):
    def __init__(self,sc):
        try:
            self._ModelSchema=read_yaml_file(filepath=MODEL_SCHEMA_FILE_NAME)
            self.threshold= self._ModelSchema.get("threshold", 0.5)
            self.parameter=self._ModelSchema.get("configs", {})
            self.parameter["scale_pos_weight"] = sc
            self.model=XGBClassifier(**self.parameter)
        except Exception as e:
            raise MyException(e) from e
    def fit(self,X,Y):
        self.model.fit(X,Y)
        return self
    def predict_proba(self,X):
        return self.model.predict_proba(X)
    def predict(self,X):
        prob=self.predict_proba(X)[:,1]
        result=(prob>self.threshold).astype(int)
        return result
class ModelTrainer:
    def __init__(self,data_transformation_artifact:DataTransformationArtifact,model_trainer_config:ModelTrainerConfig):
        try:
            self.model_trainer_config=model_trainer_config
            self.data_transformation_artifact=data_transformation_artifact
            self._ModelSchema=read_yaml_file(filepath=MODEL_SCHEMA_FILE_NAME)
        except Exception as e:
            raise MyException(e) from e
    def training_model(self,train,test,val):
        try:
            X_train,Y_train=train[:,:-1],train[:,-1]
            X_test,Y_test=test[:,:-1],test[:,-1]
            X_val,Y_val=val[:,:-1],val[:,-1]
            scale_pos_weight = len(Y_train[Y_train == 0]) / len(Y_train[Y_train == 1])
            model=MeraModel(sc=scale_pos_weight)
            model.fit(X_train,Y_train)
            probs = model.predict_proba(X_val)[:, 1]
            precision, recall, thresholds = precision_recall_curve(Y_val, probs)
            f1 = 2 * (precision * recall) / (precision + recall + 1e-10)
            best_idx = np.argmax(f1)
            best_thresh = thresholds[best_idx]
            model.threshold = best_thresh
            Y_pred=model.predict(X_test)
            precision_val=float(precision_score(Y_test,Y_pred))
            recall_val=float(recall_score(Y_test,Y_pred))
            f1_score_val=float(f1_score(Y_test,Y_pred))
            accuracy_score_val=float(accuracy_score(Y_test,Y_pred))
            classification_reports=str(classification_report(Y_test,Y_pred))
            metric=ClassificationMetricArtifact(precision=precision_val,accuracy=accuracy_score_val,recall=recall_val,f1_score=f1_score_val,classification_report=classification_reports)
            report= {
                "precision": precision_val,
                "recall": recall_val,
                "f1_score": f1_score_val,
                "accuracy": accuracy_score_val,
                "classification_report": classification_reports
            }
            return model,metric,report
        except Exception as e:
            raise MyException(e) from e
    def Iniciate_Model_Trainer(self):
        try:
            train=load_numpy_array(self.data_transformation_artifact.trained_transformed_filepath)
            logging.info("train data loaded successfully")
            test=load_numpy_array(self.data_transformation_artifact.tested_transformed_filepath)
            logging.info("test data loaded successfully")
            val=load_numpy_array(self.data_transformation_artifact.validate_transformed_filepath)
            logging.info("validation data loaded successfully")
            model,metric,report=self.training_model(train,test,val)
            logging.info("model trained successfully")
            preprocessing=load_object(filepath=self.data_transformation_artifact.preprocessing_file_object_filepath)
            real_model=MyModel(preprocessing_object=preprocessing,model=model)
            file=os.path.join(self.model_trainer_config.model_trainer_metric_dir,"metric.yaml")
            dir_name=os.path.dirname(file)
            os.makedirs(dir_name,exist_ok=True)
            write_yaml_file(filepath=file,content=report)
            logging.info("metrics are saved  successfully")
            file=os.path.join(self.model_trainer_config.trained_model_path)
            dir_name=os.path.dirname(file)
            os.makedirs(dir_name,exist_ok=True)
            save_object(filepath=file,content=real_model)
            model_trainer_artifact=ModelTrainerArtifact(trained_model=self.model_trainer_config.trained_model_path,metric_artifact=metric)
            logging.info("model trainer artifact  successfully")
            return model_trainer_artifact
        except Exception as e:
            raise MyException(e) from e