from src.mlProject.config.configuration import ConfigurationManager
from src.mlProject import logger
from src.mlProject.components.data_validation import DataValiadtion

STAGE_NAME = "Data Ingestion stage"


class DataValiadtionTrainingPipeline:
    def __init__(self):
        pass

    def main(self):
        try:
            config = ConfigurationManager()
            data_validation_config = config.get_data_validation_config()
            data_validation = DataValiadtion(config=data_validation_config)
            data_validation.validate_all_columns()
        except Exception as e:
            raise e
        
if __name__ == "__main__":
    try:
        logger.info(f"*******************")
        logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
        obj = DataValiadtionTrainingPipeline()
        obj.main()
        logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
    except Exception as e:
        logger.exception(e)
        raise e