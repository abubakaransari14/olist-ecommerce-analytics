from pathlib import Path
import pandas as pd

from config import RAW_DATA_DIR, DATA_FILES

def loadCsv(file_path: Path) -> pd.DataFrame:
    if not file_path.exists():
        raise FileNotFoundError(
            f"File Not Found: {file_path}"
        )
    return pd.read_csv(file_path)

def extractData() -> dict[str, pd.DataFrame]:
    dataset = {}
    for datasetName, fileName in DATA_FILES.items():
        file_path = RAW_DATA_DIR / fileName
        print(f"Loading : {fileName}")

        dataset[datasetName] = loadCsv(file_path)
        print(f"{datasetName} Have Rows: {len(dataset[datasetName])}")

    print("All Dataset extracted successfully!!")
    return dataset