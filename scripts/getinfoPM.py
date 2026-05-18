from pathlib import Path
import requests
import pandas as pd

ROOT = Path(__file__).parent.parent

OUT_DIR = ROOT / "data" / "pm"
OUT_DIR.mkdir(parents=True, exist_ok=True)

dataGermany = ROOT / "data" / "urls" / "GermanyUrls.csv"
dataPoland = ROOT / "data" / "urls" / "PolandUrls.csv"


def download_parquet(url, out_path):
    resp = requests.get(url, stream=True, timeout=60)
    resp.raise_for_status()

    with out_path.open("wb") as f:
        for chunk in resp.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)


def process_country(url_csv_path, country_code):
    out_country = OUT_DIR / country_code
    out_country.mkdir(parents=True, exist_ok=True)

    urls = pd.read_csv(url_csv_path).iloc[:, 0].dropna().tolist()

    for u in urls:
        fname = Path(u).name
        out_path = out_country / fname

        try:
            print(f"Downloading {u}")
            download_parquet(u, out_path)

        except Exception as e:
            print(f"Failed {u}: {e}")


def main():
    process_country(dataPoland, "Poland")
    process_country(dataGermany, "Germany")


if __name__ == "__main__":
    main()
