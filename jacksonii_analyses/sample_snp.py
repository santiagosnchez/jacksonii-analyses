import pandas as pd
import secrets


def sample_snps_in_chrom_based_on_distance(df, chunk_size, distance):
    sample = []

    for i in range(0, len(df), chunk_size):
        chunk = df.iloc[i : i + chunk_size]
        rand_idx = secrets.choice(chunk.index)
        snp = chunk.loc[[rand_idx]]
        if len(sample) == 0:
            sample.append(snp)
        else:
            last_pos = sample[-1]["pos"].values[0]
            if (snp["pos"].values[0] - last_pos) >= distance:
                sample.append(snp)

    return pd.concat(sample).reset_index(drop=True)


def subsample_snps_with_distance(snps, window, distance):
    return (
        snps.groupby("chrom")
        .apply(
            lambda df: sample_snps_in_chrom_based_on_distance(df, window, distance),
            include_groups=False,
        )
        .reset_index()
        .drop(columns=["level_1"])
    )
