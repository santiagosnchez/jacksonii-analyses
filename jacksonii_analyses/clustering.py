import re
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans


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
