from pathlib import Path

import pandas as pd

dataGermany = Path(__file__).with_name("data") / "GermanyMap.csv"
dataPoland = Path(__file__).with_name("data") / "PolandMap.csv"


def count_occurance_station_areas(csv_path) -> pd.DataFrame:
    df = pd.read_csv(csv_path)

    res = (
        df[["Air Quality Station Area", "Air Quality Station Nat Code"]]
        .drop_duplicates()
        .groupby("Air Quality Station Area", as_index=False)
        .size()
        .rename(columns={"size": "unique_station_count"})
        .sort_values(
            ["unique_station_count", "Air Quality Station Area"],
            ascending=[False, True],
        )
        .reset_index(drop=True)
    )

    return res


def count_cadence_units(csv_path) -> pd.DataFrame:
    df = pd.read_csv(csv_path)

    res = (
        df[
            [
                "Cadence Unit",
                "Sampling Point Id",
            ]
        ]
        .drop_duplicates()
        .groupby("Cadence Unit", as_index=False)
        .size()
        .rename(columns={"size": "unique_sampling_points"})
        .sort_values(
            ["unique_sampling_points", "Cadence Unit"],
            ascending=[False, True],
        )
        .reset_index(drop=True)
    )

    return res


def count_analytical_techniques(csv_path) -> pd.DataFrame:
    df = pd.read_csv(csv_path)

    res = (
        df[
            [
                "Analytical Technique",
                "Sampling Point Id",
            ]
        ]
        .drop_duplicates()
        .groupby("Analytical Technique", as_index=False)
        .size()
        .rename(columns={"size": "unique_sampling_points"})
        .sort_values(
            ["unique_sampling_points", "Analytical Technique"],
            ascending=[False, True],
        )
        .reset_index(drop=True)
    )

    return res


def main() -> None:
    cosaG = count_occurance_station_areas(dataGermany)
    cosaP = count_occurance_station_areas(dataPoland)
    print("Germany Air Quality Station Areas:")
    print(cosaG.to_string(index=False))
    print("Poland Air Quality Station Areas:")
    print(cosaP.to_string(index=False))

    cdsuG = count_cadence_units(dataGermany)
    cdsuP = count_cadence_units(dataPoland)
    print("Germany Cadence Units:")
    print(cdsuG.to_string(index=False))
    print("Poland Cadence Units:")
    print(cdsuP.to_string(index=False))

    atG = count_analytical_techniques(dataGermany)
    atP = count_analytical_techniques(dataPoland)
    print("Germany Analytical Techniques:")
    print(atG.to_string(index=False))
    print("Poland Analytical Techniques:")
    print(atP.to_string(index=False))


if __name__ == "__main__":
    main()
