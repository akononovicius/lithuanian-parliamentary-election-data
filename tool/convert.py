import polars as pl

from typer import run as cli_run


def read_activity_file(file_name: str) -> pl.DataFrame:
    return (
        pl.read_csv(file_name, columns=[3, 4, 5, 6, 7, 8, 9])
        .rename(
            {
                "Turas": "round",
                "Apygardos Nr.": "major_id",
                "Apygardos pavadinimas": "major_name",
                "Apylinkės Nr.": "minor_id",
                "Apylinkės pavadinimas": "minor_name",
                "Rinkėjų skaičius": "registered_voters",
                "Unikalus apylinkės Nr.": "minor_gid",
            }
        )
        .filter(pl.col("round") == 1)
    )


def read_votes_data_file(file_name: str) -> pl.DataFrame:
    return pl.read_csv(
        file_name,
        skip_rows=7,
        columns=[3, 5, 6, 7, 8, 9],
    ).rename(
        {
            "Apygardos Nr.": "major_id",
            "Apylinkės Nr.": "minor_id",
            "Apylinkės pavadinimas": "minor_name",
            "Org. Nr. ": "org_id",
            "Organizacijos pavadinimas": "org_name",
            "Gauti balsai (iš viso)": "votes",
        }
    )


def write_major(year: int, raw_activity_df: pl.DataFrame) -> pl.DataFrame:
    major_df = (
        raw_activity_df.select(["major_id", "major_name"]).unique().sort("major_id")
    )
    major_df.write_csv(f"{year:.0f}-major-district.csv")
    return major_df


def write_parties(year: int, raw_votes_df: pl.DataFrame) -> pl.DataFrame:
    parties_df = raw_votes_df.select(["org_id", "org_name"]).unique().sort("org_id")
    parties_df.write_csv(f"{year:.0f}-parties.csv")
    return parties_df


def write_votes(
    year: int, raw_activity_df: pl.DataFrame, raw_votes_df: pl.DataFrame
) -> pl.DataFrame:
    votes_df = (
        raw_votes_df.join(
            raw_activity_df.select(["minor_gid", "major_id", "minor_id", "minor_name"]),
            on=["major_id", "minor_id", "minor_name"],
        )
        .select(["minor_gid", "org_id", "votes"])
        .group_by(["minor_gid", "org_id"])
        .agg(pl.col("votes").sum())
        .sort(["minor_gid", "org_id"])
    )
    votes_df.write_csv(f"{year:.0f}-votes.csv")
    return votes_df


def write_minor(
    year: int, raw_activity_df: pl.DataFrame, clean_votes_df: pl.DataFrame
) -> pl.DataFrame:
    minor_df = (
        raw_activity_df.select(
            [
                "minor_gid",
                "major_id",
                "minor_id",
                "minor_name",
                "registered_voters",
            ]
        )
        .join(
            clean_votes_df.group_by("minor_gid").agg(pl.col("votes").sum()),
            on="minor_gid",
        )
        .sort("minor_gid")
    )
    minor_df.write_csv(f"{year:.0f}-minor.csv")
    return minor_df


def main(year: int, activity_fn: str, votes_fn: str) -> None:
    activity_df = read_activity_file(activity_fn)
    votes_df = read_votes_data_file(votes_fn)

    _ = write_major(year, activity_df)
    _ = write_parties(year, votes_df)
    clean_votes_df = write_votes(year, activity_df, votes_df)
    _ = write_minor(year, activity_df, clean_votes_df)


if __name__ == "__main__":
    cli_run(main)
