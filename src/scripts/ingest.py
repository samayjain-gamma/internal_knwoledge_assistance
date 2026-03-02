from src.core.exception import CustomException
from src.core.logger import logger
from src.ingestion.pipeline import IngestionPipeline

pipeline = IngestionPipeline()
file = "company_policy.txt"
chunk_count = pipeline.ingest_file(file_path=file)

logger.info("ingestion pipeline initiated with")
logger.info(f"Ingested {chunk_count} chunks")
