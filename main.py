from src.StockScout import logger
from src.StockScout.pipeline.stage_01_data_ingestion import DataIngestionTrainingPipeline
from src.StockScout.pipeline.stage_02_data_validation import DataValidationTrainingPipeline
from src.StockScout.pipeline.stage_03_data_transformation import DataTransformationTrainingPipeline
from src.StockScout.pipeline.stage_04_partial_model_trainer import PartialModelTrainingPipeline


STAGE_NAME = "Data Ingestion stage"
try:
   logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<") 
   data_ingestion = DataIngestionTrainingPipeline()
   data_ingestion.main()
   logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\n{'-' * 100}")
except Exception as e:
        logger.exception(e)
        raise e


STAGE_NAME = "Data Validation stage"
try:
   logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
   obj = DataValidationTrainingPipeline()
   obj.main()
   logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\n{'-' * 100}")
except Exception as e:
   logger.exception(e)
   raise e

STAGE_NAME = "Data Transformation stage"
try:
   logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<") 
   data_ingestion = DataTransformationTrainingPipeline()
   data_ingestion.main()
   logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\n{'-' * 100}")
except Exception as e:
        logger.exception(e)
        raise e


STAGE_NAME = "Partial Model Training  stage"
try:
   logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<") 
   data_ingestion = PartialModelTrainingPipeline()
   data_ingestion.main()
   logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\n{'-' * 100}")
except Exception as e:
        logger.exception(e)
        raise e