from src.mlProject.config.configuration import ConfigurationManager
from src.mlProject.components.model_evaluation import ModelEvaluation
from src.mlProject import logger

STAGE_NAME = "Model Evaluation stage"

class ModelEvaluationTrainingPipeline:  
    def __init__(self):
        pass

    def main(self):
        config = ConfigurationManager()
        model_eval_config = config.get_model_evaluatiion_config()
        model_eval_config = ModelEvaluation(config=model_eval_config)
        model_eval_config.log_into_mlflow()
        
if __name__ == "__main__":
    try:
        logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
        obj = ModelEvaluationTrainingPipeline()
        obj.main()  
        logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx===========x")
    except Exception as e:    
        raise e
    
