from pathlib import Path
import pandas as pd
from sqlalchemy import text
from sqlalchemy.types import VARCHAR
from sqlalchemy.engine import Engine

def saveDataFrame(df: pd.DataFrame, outputPath: Path) -> None:
    outputPath.parent.mkdir(
        parents = True,
        exist_ok = True
    )

    df.to_csv(
        outputPath,
        index = False
    )
    print(f"Saved: {outputPath}")
    print(f"{len(df)} rows")

def saveToDatabase(df: pd.DataFrame, tableName: str, dbEngine: Engine) -> None:
    # Upload a DATAFRAME into database table
    dtypeMapping = {
        col: VARCHAR(255) 
        for col in df.select_dtypes(include=['object', 'string']).columns
    }
    df.to_sql(
        name= tableName,
        con = dbEngine,
        if_exists= "replace",
        index = False,
        chunksize=100000,
        dtype=dtypeMapping
    )
    print(f"Upload DB Table: {tableName} and {len(df):,} rows")

def loadProcessedData(dataset: dict[str, pd.DataFrame], outputDirectory: Path, dbEngine: Engine = None) -> None:
    outputDirectory.mkdir(
        parents = True,
        exist_ok = True
    )
    for dfName, df in dataset.items():
        outputPath = (outputDirectory / f"{dfName}.csv")
        saveDataFrame(df, outputPath)
        if dbEngine is not None:
            saveToDatabase(df, dfName, dbEngine)
    print("\nAll processed datasets saved successfully csv and MySQL!.")

def applyMySQLPrimaryKeys(dbEngine: Engine) -> None:
    """Apply Primary Key constraints to MySQL tables post-load."""
    pkQueries = [
        "ALTER TABLE orders ADD PRIMARY KEY (order_id(255));",
        "ALTER TABLE customers ADD PRIMARY KEY (customer_id(255));",
        "ALTER TABLE products ADD PRIMARY KEY (product_id(255));",
        "ALTER TABLE sellers ADD PRIMARY KEY (seller_id(255));",
        "ALTER TABLE order_items ADD PRIMARY KEY (order_id(255), order_item_id);",
        "ALTER TABLE order_payments ADD PRIMARY KEY (order_id(255), payment_sequential);",
        "ALTER TABLE order_reviews ADD PRIMARY KEY (order_id(255), review_id(255));",
        "ALTER TABLE category_translation ADD PRIMARY KEY (product_category_name(255));",
        "ALTER TABLE master_orders ADD PRIMARY KEY (order_id(255));",
        "ALTER TABLE master_order_items ADD PRIMARY KEY (order_id(255), order_item_id);"
    ]

    print("\nApplying Primary Keys in MySQL Workbench database...")
    with dbEngine.connect() as conn:
        for query in pkQueries:
            tableName = query.split()[2]
            try:
                conn.execute(text(query))
                conn.commit()
                print(f"  Applied PK constraint on table: {tableName}")
            except Exception as e:
                print(f"  Skipped PK on table {tableName}: {e}")