from extract import extractData
from transfrom import transformAll
from validate import validateAll
from load import loadProcessedData, applyMySQLPrimaryKeys
from sqlalchemy import create_engine

from config import PROCESSED_DATA_DIR

def runPipeline():
    
    print("-" * 30)
    print("OLIST E-COMMERCE DATA PIPELINE")
    print("-" * 30)

    MYSQL_URI = "mysql+pymysql://root:root@127.0.0.1:3306/olist_db"
    
    print("Initializing Database Connection Engine...")
    dbEngine = create_engine(MYSQL_URI)
    
    # 1. EXTRACT
    print("\n[1/4] EXTRACT")

    rawData = extractData()

    # 2. TRANSFORM
    print("\n[2/4] TRANSFORM")

    transformedData = transformAll(rawData)

    # 3. VALIDATE
    print("\n[3/4] VALIDATE")
    validateAll(transformedData)

    # 4. LOAD
    print("\n[4/4] LOAD")

    loadProcessedData(transformedData,PROCESSED_DATA_DIR,dbEngine)

    print("\n--- Phase 5: Enforcing MySQL Schema Constraints ---")
    applyMySQLPrimaryKeys(dbEngine)

    print("\n" + "-" * 70)
    print("PIPELINE COMPLETED SUCCESSFULLY")
    print("-" * 70)

if __name__ == "__main__":
    runPipeline()