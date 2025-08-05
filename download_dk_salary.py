import requests
import pandas as pd
from pathlib import Path

# Constants
CSV_URL = "https://www.draftkings.com/lineup/getavailableplayerscsv?contestTypeId=21&draftGroupId=131064"
OUTPUT_DIR = Path(__file__).resolve().parent / "data"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_PATH = OUTPUT_DIR / "dk_salaries_week1_2024.csv"


def download_csv(url: str, output_path: Path) -> None:
    """Download a CSV file from a URL and save it to the given path."""
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    output_path.write_bytes(response.content)
    print(f"Downloaded CSV to {output_path}")


def load_salaries(csv_path: Path) -> pd.DataFrame:
    """Load the salaries CSV into a DataFrame with cleaned column names."""
    df = pd.read_csv(csv_path)
    # Clean up column names: strip whitespace and lower case with underscores
    df.columns = (
        df.columns.str.strip()
        .str.lower()
        .str.replace("/", "_", regex=False)
        .str.replace(" ", "_", regex=False)
    )
    return df


def main() -> None:
    download_csv(CSV_URL, OUTPUT_PATH)
    df = load_salaries(OUTPUT_PATH)
    print(df.head())


if __name__ == "__main__":
    main()