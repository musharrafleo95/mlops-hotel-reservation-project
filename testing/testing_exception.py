from src.logger import get_logger
from src.custom_exception import CustomException
import sys

logger = get_logger(__name__)

def divide_number(a, b):
    try:
        logger.info("dividing two numbers")
        result = a/b
        return result
    except Exception as e:
        logger.error("Error occurred while dividing two numbers")
        raise CustomException("zero error", e)
    
if __name__ == "__main__":
    try: 
        logger.info("Starting the application")
        print(divide_number(3, 0))
    except CustomException as ce:
        logger.error(str(ce))