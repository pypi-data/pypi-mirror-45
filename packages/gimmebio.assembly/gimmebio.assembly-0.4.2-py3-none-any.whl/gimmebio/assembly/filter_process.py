
import networkx as nx
from Bio import SeqIO


def filter_homologous(m8file, fasta, min_perc_id=0.95, min_len_frac=0.8):
    """Return a generator of contigs.

    Filter contigs that are homologous to one another keeping the largest.

    Find connected components in the m8 file (presumed to be an
    autologous alignment). Edges exist between contigs where
    an alignment is:
    1) Greater than <min_perc_id> similar
    2) Longer than <min_len_frac> * min(len(c1), len(c2))
    For each component take the longest contig and write it to a fasta.
    """
    length_map = {rec.id: len(rec.seq) for rec in SeqIO.parse(fasta, 'fasta')}
    fasta.seek(0)
    components = find_m8_components(
        m8file, length_map, min_perc_id=min_perc_id, min_len_frac=min_len_frac
    )
    my_maxes = set()
    for component in components:
        max_contig = None
        for contig in component:
            if max_contig is None or length_map[contig] > length_map[max_contig]:
                max_contig = contig
        my_maxes.add(max_contig)

    for rec in SeqIO.parse(fasta, 'fasta'):
        if rec.id in my_maxes:
            yield rec


def find_m8_components(m8file, length_map, min_perc_id=0.95, min_len_frac=0.8):
    """Return an iterator of sets where each set lists contigs in a component."""
    G = nx.Graph()
    for tkns in (line.strip().split('\t') for line in m8file):
        c1, c2, perc_id, length = tkns[:4]
        length, perc_id = int(length), float(perc_id)
        if perc_id < min_perc_id:
            continue
        if length < (min_len_frac * min(length_map[c1], length_map[c2])):
            continue
        G.add_edge(c1, c2)
    return nx.algorithms.components.connected_components(G)
