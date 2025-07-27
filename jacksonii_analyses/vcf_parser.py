import allel
import pandas as pd
import numpy as np


IUPAC_CODES = {
    frozenset(["A", "G"]): "R",
    frozenset(["C", "T"]): "Y",
    frozenset(["G", "C"]): "S",
    frozenset(["A", "T"]): "W",
    frozenset(["G", "T"]): "K",
    frozenset(["A", "C"]): "M",
    frozenset(["A"]): "A",
    frozenset(["C"]): "C",
    frozenset(["G"]): "G",
    frozenset(["T"]): "T",
    frozenset(["."]): "N",
}


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


def vcf_to_chr_pos_df(vcf_path: str) -> pd.DataFrame:
    callset = allel.read_vcf(vcf_path)
    chroms = callset["variants/CHROM"]
    positions = callset["variants/POS"]

    loci = loci_from_callset(callset)

    df = pd.DataFrame(
        {
            "chrom": chroms,
            "pos": positions,
            "locus": loci,
        }
    )

    return df


def vcf_to_snp_fasta(vcf_path: str, output: str, drop_samples: list = None) -> None:
    callset = allel.read_vcf(vcf_path)

    ref = callset["variants/REF"]
    alt = callset["variants/ALT"]

    is_snp = np.array(
        [
            len(r) == 1 and len(a[0]) == 1 if len(a) > 0 else False
            for r, a in zip(ref, alt)
        ]
    )
    snp_indices = np.where(is_snp)[0]

    ref = ref[snp_indices]
    alt = alt[snp_indices]

    gt = allel.GenotypeArray(callset["calldata/GT"])
    gt_snp = gt[snp_indices, :, :]

    vcf_samples = list(callset.get("samples", []))
    if drop_samples is not None:
        sample_indices = [i for i, s in enumerate(vcf_samples) if s not in drop_samples]
    else:
        sample_indices = range(gt_snp.shape[1])
    gt_snp = gt_snp[:, sample_indices, :]

    samples = [vcf_samples[i] for i in sample_indices]

    filtered_indices = []
    for j in range(gt_snp.shape[0]):
        unambig_bases = set()
        for i in range(len(samples)):
            alleles = []
            for ploid in gt_snp[j, i]:
                if ploid == 0:
                    alleles.append(ref[j])
                elif ploid == 1:
                    alleles.append(alt[j][0])
                else:
                    alleles.append(".")
            # Only consider unambiguous bases for this sample
            sample_unambig = {a for a in alleles if a in "ACGT"}
            if sample_unambig:
                unambig_bases.update(sample_unambig)
        # Keep site if at least two different unambiguous bases are present
        if len(unambig_bases) >= 2:
            filtered_indices.append(j)

    # Now build sequences only for filtered sites
    seqs = []
    for i, sample in enumerate(samples):
        seq = []
        for j in filtered_indices:
            alleles = []
            for ploid in gt_snp[j, i]:
                if ploid == 0:
                    alleles.append(ref[j])
                elif ploid == 1:
                    alleles.append(alt[j][0])
                else:
                    alleles.append(".")
            unique_alleles = set(alleles)
            code = IUPAC_CODES.get(frozenset(unique_alleles), "N")
            seq.append(code)
        seqs.append((sample, "".join(seq)))

    with open(output, "w") as fasta:
        for sample, seq in seqs:
            fasta.write(f">{sample}\n{seq}\n")
