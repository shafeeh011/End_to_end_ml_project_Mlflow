import os
import dagshub
import pandas as pd
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import numpy as np
import joblib
import mlflow
import mlflow.sklearn
from urllib.parse import urlparse
from src.mlProject.entity.config_entity import ModelEvaluationConfig
from src.mlProject.utils.common import save_json
from pathlib import Path
from src.mlProject import logger

class ModelEvaluation:
    def __init__(self, config: ModelEvaluationConfig):
        self.config = config
        
    def eval_metrics(self, actual, pred):
        rmse = np.sqrt(mean_squared_error(actual, pred))
        mae = mean_absolute_error(actual, pred)
        r2 = r2_score(actual, pred)
        return rmse, mae, r2
    
    def log_into_mlflow(self):
        try:
            # Initialize DAGshub tracking
            dagshub.init(repo_owner='shafeeh011', repo_name='my-first-repo', mlflow=True)
            
            logger.info("Model Evaluation started")
            test_data = pd.read_csv(self.config.test_file_path)
            logger.info("Test data loaded successfully")

            model = joblib.load(self.config.model_path)
            logger.info("Model loaded successfully")

            test_x = test_data.drop([self.config.target_column], axis=1)
            test_y = test_data[[self.config.target_column]]

            mlflow.set_registry_uri(self.config.mlflow_uri)
            tracking_url_type_store = urlparse(mlflow.get_tracking_uri()).scheme

            with mlflow.start_run():
                logger.info("MLflow run started")

                predicted_qualities = model.predict(test_x)
                logger.info("Predictions made successfully")

                (rmse, mae, r2) = self.eval_metrics(test_y, predicted_qualities)
                logger.info("Metrics calculated successfully")

                # Saving metrics as local
                scores = {"rmse": rmse, "mae": mae, "r2": r2}
                save_json(path=Path(self.config.metric_file_name), data=scores)
                logger.info("Metrics saved locally")

                mlflow.log_params(self.config.all_params)
                logger.info("Hyperparameters logged")

                mlflow.log_metric("rmse", rmse)
                mlflow.log_metric("r2", r2)
                mlflow.log_metric("mae", mae)
                logger.info("Metrics logged")

                # Model registry does not work with file store
                if tracking_url_type_store != "file":
                    mlflow.sklearn.log_model(model, "model", registered_model_name="ElasticnetModel")
                    logger.info("Model registered")
                else:
                    mlflow.sklearn.log_model(model, "model")
                    logger.info("Model logged")

            logger.info("Model Evaluation completed")
        except Exception as e:
            logger.exception(e)
            raise e