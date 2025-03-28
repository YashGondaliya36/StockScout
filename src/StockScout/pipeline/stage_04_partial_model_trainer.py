from src.StockScout.config.configuration import ConfigurationManager
from src.StockScout.components.partial_model_trainer import PartialModelTrainer
from src.StockScout  import logger
from pathlib import Path


STAGE_NAME = "Partial Model Training  stage"

class PartialModelTrainingPipeline:
    def __init__(self):
        pass


    def main(self):
        try:
            
            config = ConfigurationManager()
            partial_model_trainer_config = config.get_partial_model_trainer_config()
            partial_model_trainer_config = PartialModelTrainer(partial_model_trainer_config)
            partial_model_trainer_config.partial_train()

        except Exception as e:
            print(e)


if __name__ == '__main__':
    try:
        logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
        obj = PartialModelTrainingPipeline()
        obj.main()
        logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\n{'-' * 100}")
    except Exception as e:
        logger.exception(e)
        raise e