from pymongo.database import Database
from typing import List
from models.response_model import UnemploymentRateResponse
from config.settings import MONGODB_DB
from utils.logger import get_logger
from utils.mongo_client import get_mongo_client
from concurrent.futures import ThreadPoolExecutor
import re

logger = get_logger(__name__)

def get_unemployment_data(year: int, month: int) -> List[UnemploymentRateResponse]:
    logger.info(f"Fetching unemployment data for {year}-{month}")

    client = get_mongo_client()
    db = client[MONGODB_DB]

    try:
        basic_info_cursor = db.basic_info.find(
            {
                "area_code": {"$regex": "^ST[0-9]{13}$"},
                "area_text": {"$ne": None}
            }
        )

        state_mappings = {}
        for doc in basic_info_cursor:
            area_code = doc["area_code"]
            area_text = doc["area_text"]

            area_code_digits = area_code[2:]
            state_mappings[area_code_digits] = area_text

        logger.debug(f"Loaded {len(state_mappings)} state mappings")

        if not state_mappings:
            logger.warning("No state mappings found")
            return []
        
        results = []

        def query_state(state_name: str, area_code_digits: str, db: Database):
            collection_name = f"states_{state_name.replace(' ', '')}"
            try:
                doc = db[collection_name].find_one(
                    {
                        "year": year,
                        "period": f"M{month:02}",
                        "series_id": {"$regex": "^LASST.*03$"}
                    }
                )

                if not doc:
                    logger.debug(f"No data found for {state_name} in {year}-{month}")
                    return None
                
                series_id = doc["series_id"]
                match = re.match(r"LASST([0-9]{13})03$", series_id)
                if not match:
                    logger.warning(f"Series ID {series_id} does not match expected format")
                    return None
                
                doc_area_code_digits = match.group(1)

                if doc_area_code_digits != area_code_digits:
                    logger.info(f"Area code digits mismatch: {doc_area_code_digits} != {area_code_digits}")
                    return None
                
                return UnemploymentRateResponse(
                    state=state_name,
                    value=float(doc["value"])
                )
            except Exception as e:
                logger.warning(f"Error querying state {state_name}: {e}")
                return None
            
        with ThreadPoolExecutor() as executor:
            futures = [
                executor.submit(query_state, state_name, area_code_digits, db)
                for area_code_digits, state_name in state_mappings.items()
            ]
            for future in futures:
                result = future.result()
                if result:
                    results.append(result)

        logger.info(f"Fetched unemployment data for {len(results)} states")
        return results
    except Exception as e:
        logger.error(f"Error fetching unemployment data: {e}")
        raise