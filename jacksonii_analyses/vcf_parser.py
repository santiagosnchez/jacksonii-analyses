import allel
import pandas as pd
import numpy as np


def loci_from_callset(callset: dict) -> np.ndarray:
    chroms = callset["variants/CHROM"]
    positions = callset["variants/POS"]

    variant_ids = np.char.add(chroms.astype(str), "_")
    variant_ids = np.char.add(variant_ids, positions.astype(str))

    return variant_ids


def samples_from_callset(callset: dict) -> list:
    # Get sample names if present, otherwise use default names
    return callset.get(
        "samples", [f"sample{i+1}" for i in range(callset["calldata/GT"].shape[0])]
    )


def vcf_to_geno_df(vcf_path) -> pd.DataFrame:
    callset = allel.read_vcf(vcf_path)
    loci = loci_from_callset(callset)
    samples = samples_from_callset(callset)

    gt = allel.GenotypeArray(callset["calldata/GT"])
    geno = gt.to_n_alt().T

    return pd.DataFrame(geno, index=samples, columns=loci)
