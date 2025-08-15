import re


def fasta_reader(fasta_file: str):
    result = {}
    with open(fasta_file) as f:
        lines = f.readlines()
    for header in filter(lambda x: x.startswith(">"), lines):
        seqidx = lines.index(header) + 1
        result[re.findall(r"^>?(.*)$", header)[0]] = lines[seqidx]
    return result


def to_bpp_phylip(seqs: dict):
    n_terminals = len(seqs)
    alignment_length = max([len(seqs[i].rstrip()) for i in seqs])
    max_header_string_length = max([len(i) for i in seqs])

    phylip = f"{n_terminals} {alignment_length}\n\n"

    for header in seqs:
        padding = max_header_string_length - len(header) + 2
        phylip += f"^{header}" + " " * padding + seqs[header]

    return phylip + "\n"


def get_ctl(
    seqfile_path,
    imapfile_path,
    initial_species,
    individuals_in_species,
    guide_tree,
    phase_data,
    number_of_loci,
):
    A10_CONTROL_FILE = f"""
    seed =  -1
    seqfile = {seqfile_path}
    Imapfile = {imapfile_path}
    jobname = A10_output

    speciesdelimitation = 1 1 2 1   * species delimitation rjMCMC algorithm finetune (a m)
    speciestree = 0                 * species tree NNI/SPR

    speciesmodelprior = 1           * 0: uniform LH; 1:uniform rooted trees; 2: uniformSLH; 3: uniformSRooted

    species&tree = {initial_species}
                   {individuals_in_species}
                   {guide_tree}
    phase =   {phase_data}

    usedata = 1                     * 0: no data (prior); 1:seq like
    nloci = {number_of_loci}                   * number of data sets in seqfile

    model = HKY

    cleandata = 0                   * remove sites with ambiguity data (1:yes, 0:no)?

    thetaprior = gamma 2 2000       * gamma(a, b) for theta (estimate theta)
    tauprior = gamma 2 1000         * gamma(a, b) for root tau & Dirichlet(a) for other tau's

    finetune = 1 Gage:5 Gspr:0.001 mix:0.3  

    print = 1 0 0 0                 * MCMC samples, locusrate, heredityscalars, Genetrees
    burnin = 8000
    sampfreq = 2
    nsample = 100000

    threads = 4 4 1
"""
    print(A10_CONTROL_FILE)
    return A10_CONTROL_FILE
