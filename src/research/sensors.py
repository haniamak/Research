from pathlib import Path

import pandas as pd

dataGermany = Path(__file__).parent.parent.parent / "data" / "maps" / "GermanyMap.csv"
dataPoland = Path(__file__).parent.parent.parent / "data" / "maps" / "PolandMap.csv"


def count_occurance_station_areas(csv_path) -> pd.DataFrame:
    df = pd.read_csv(csv_path)

    res = (
        df[["Air Quality Station Area", "Air Quality Station Nat Code"]]
        .drop_duplicates()
        .groupby("Air Quality Station Area")
        .size()
        .reset_index(name="unique_station_count")
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
        .groupby("Cadence Unit")
        .size()
        .reset_index(name="unique_sampling_points")
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
        .groupby("Analytical Technique")
        .size()
        .reset_index(name="unique_sampling_points")
        .sort_values(
            ["unique_sampling_points", "Analytical Technique"],
            ascending=[False, True],
        )
        .reset_index(drop=True)
    )

    return res


def cout_detection_limit(csv_path) -> pd.DataFrame:
    df = pd.read_csv(csv_path)

    res = (
        df[
            [
                "Detection Limit",
                "Sampling Point Id",
            ]
        ]
        .drop_duplicates()
        .groupby("Detection Limit")
        .size()
        .reset_index(name="unique_sampling_points")
        .sort_values(
            ["unique_sampling_points", "Detection Limit"],
            ascending=[False, True],
        )
        .reset_index(drop=True)
    )

    return res


def count_measurement_methods(csv_path) -> pd.DataFrame:
    df = pd.read_csv(csv_path)

    res = (
        df[
            [
                "Measurement Method",
                "Sampling Point Id",
            ]
        ]
        .drop_duplicates()
        .groupby("Measurement Method")
        .size()
        .reset_index(name="unique_sampling_points")
        .sort_values(
            ["unique_sampling_points", "Measurement Method"],
            ascending=[False, True],
        )
        .reset_index(drop=True)
    )

    return res


def group_method_based_on_area(csv_path) -> pd.DataFrame:
    df = pd.read_csv(csv_path)

    res = (
        df[
            [
                "Air Quality Station Area",
                "Measurement Method",
                "Sampling Point Id",
            ]
        ]
        .drop_duplicates()
        .groupby(["Air Quality Station Area", "Measurement Method"])
        .size()
        .reset_index(name="unique_sampling_points")
        .sort_values(
            ["unique_sampling_points", "Air Quality Station Area"],
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

    cdlG = cout_detection_limit(dataGermany)
    cdlP = cout_detection_limit(dataPoland)
    print("Germany Detection Limits:")
    print(cdlG.to_string(index=False))
    print("Poland Detection Limits:")
    print(cdlP.to_string(index=False))

    mmG = count_measurement_methods(dataGermany)
    mmP = count_measurement_methods(dataPoland)
    print("Germany Measurement Methods:")
    print(mmG.to_string(index=False))
    print("Poland Measurement Methods:")
    print(mmP.to_string(index=False))

    gmbA = group_method_based_on_area(dataGermany)
    gmbP = group_method_based_on_area(dataPoland)
    print("Germany Measurement Methods based on Air Quality Station Area:")
    print(gmbA.to_string(index=False))
    print("Poland Measurement Methods based on Air Quality Station Area:")
    print(gmbP.to_string(index=False))


if __name__ == "__main__":
    main()
