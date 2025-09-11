import dendropy as dp


def read_tree(tree_file: str) -> dp.Tree:
    tree = dp.Tree.get_from_path(tree_file, schema="newick", preserve_underscores=True)
    return tree


def find_mrca(tree, tips):
    nodes = [tree.find_node_with_taxon_label(label) for label in tips]
    taxa = [node.taxon for node in nodes if node is not None]
    mrca = tree.mrca(taxa=taxa)
    return mrca


def get_tips_as_list(node):
    return [leaf.taxon.label for leaf in node.leaf_nodes()]


def check_if_clade_is_monophyletic(tree, tips):
    mrca = find_mrca(tree, tips)
    tips_in_mrca = [leaf.taxon.label for leaf in mrca.leaf_nodes()]
    tips_in_tree = [
        tip for tip in tips if tree.find_node_with_taxon_label(tip) is not None
    ]
    return set(tips_in_tree) == set(tips_in_mrca)


def get_node_annotation(tree, tips):
    mrca = find_mrca(tree, tips)
    return mrca.label


def reroot_tree(tree, outgroup=None):
    if outgroup:
        outgroup = [tree.find_node_with_taxon_label(label) for label in outgroup]
        node = tree.mrca(taxa=[node.taxon for node in outgroup if node is not None])
    else:
        node = tree.reroot_at_midpoint(update_bipartitions=False)
    return tree.reroot_at_node(node, update_bipartitions=False)
