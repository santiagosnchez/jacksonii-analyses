import re
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from scipy.cluster.hierarchy import fclusterdata


def read_populations(pop_file: str) -> pd.DataFrame:
    pops = pd.read_csv(pop_file, sep="\t", header=None, names=["sample", "populations"])
    pops["populations_clean"] = pops["populations"].apply(
        lambda x: re.sub(" sp", " sp ", re.sub("Amanita", "A. ", x))
    )
    pops = pops.set_index("sample")
    return pops


def calculate_pca(
    geno_df: pd.DataFrame, n_components: int = 2, pops: pd.DataFrame = None
) -> pd.DataFrame:
    pca = PCA(n_components=n_components)
    pcs = pca.fit_transform(geno_df.values)

    pcs_df = pd.DataFrame(
        pcs, index=geno_df.index, columns=[f"PC{i+1}" for i in range(n_components)]
    )
    if pops is not None:
        pcs_df["populations"] = pops.loc[pcs_df.index, "populations_clean"].values

    return pcs_df


def cluster_variants_by_distance(
    pos_df: pd.DataFrame, distance_threshold: float = 10000
) -> pd.DataFrame:
    clusters = []

    for chrom, group in pos_df.groupby("chrom"):
        if len(group) > 2:
            positions = group["pos"].values.reshape(-1, 1)
            # Assign cluster labels based on distance threshold
            labels = fclusterdata(
                positions, t=distance_threshold, criterion="distance", method="single"
            )
            group = group.copy()
            group["cluster"] = labels
            group["cluster_id"] = (
                group["chrom"].astype(str) + "_" + group["cluster"].astype(str)
            )
            clusters.append(group)

    clusters_df = pd.concat(clusters).reset_index(drop=True)

    return clusters_df


def cluster_data_to_intervals(clust_df: pd.DataFrame) -> pd.DataFrame:
    intervals = []

    for _, group in clust_df.groupby("cluster_id"):
        start = group["pos"].min()
        end = group["pos"].max()

        intervals.append(
            {
                "chrom": group["chrom"].iloc[0],
                "start": start,
                "end": end,
                "cluster_id": group["cluster_id"].iloc[0],
                "size": end - start + 1,
                "n_variants": len(group),
            }
        )

    intervals_df = pd.DataFrame(intervals)
    intervals_df = intervals_df.sort_values(
        by=["chrom", "start", "end"], ascending=[True, True, True]
    ).reset_index(drop=True)

    return intervals_df


def distance_for_group(df: pd.DataFrame) -> pd.Series:
    if len(df) < 2:
        df["distance"] = 0
        return df

    shifted_start = df["start"].copy()
    shifted_start.iloc[0] = df["end"].iloc[0]
    df["distance"] = df["end"] - shifted_start

    return df
