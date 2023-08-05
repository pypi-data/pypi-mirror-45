import logging
from collections import Counter

import pandas as pd
from ete3 import Tree

LEVEL = 'level'

DEPTH = 'depth'

DATE = 'date'


def get_dist_to_root(tip):
    dist_to_root = 0
    n = tip
    while not n.is_root():
        dist_to_root += n.dist
        n = n.up
    return dist_to_root


def date2years(d):
    if pd.notnull(d):
        first_jan_this_year = pd.datetime(year=d.year, month=1, day=1)
        day_of_this_year = d - first_jan_this_year
        first_jan_next_year = pd.datetime(year=d.year + 1, month=1, day=1)
        days_in_this_year = first_jan_next_year - first_jan_this_year
        return d.year + day_of_this_year / days_in_this_year
    else:
        return None


def annotate_depth(tree, depth_feature=DEPTH, level_feature=LEVEL):
    for node in tree.traverse('preorder'):
        if node.is_root():
            node.add_feature(depth_feature, node.dist)
            node.add_feature(level_feature, 0)
        depth = getattr(node, depth_feature)
        level = getattr(node, level_feature)
        for child in node.children:
            child.add_feature(depth_feature, depth + child.dist)
            child.add_feature(level_feature, level + 1)


def name_tree(tree):
    """
    Names all the tree nodes that are not named or have non-unique names, with unique names.

    :param tree: tree to be named
    :type tree: ete3.Tree

    :return: void, modifies the original tree
    """
    existing_names = Counter((_.name for _ in tree.traverse() if _.name))
    if sum(1 for _ in tree.traverse()) == len(existing_names):
        return
    i = 0
    existing_names = Counter()
    for node in tree.traverse('preorder'):
        name = node.name if node.is_leaf() else ('root' if node.is_root() else None)
        while name is None or name in existing_names:
            name = '{}{}'.format('t' if node.is_leaf() else 'n', i)
            i += 1
        node.name = name
        existing_names[name] += 1


def collapse_zero_branches(tree, features_to_be_merged=None):
    num_collapsed = 0

    if features_to_be_merged is None:
        features_to_be_merged = []

    for n in list(tree.traverse('postorder')):
        zero_children = [child for child in n.children if not child.is_leaf() and child.dist <= 0]
        if not zero_children:
            continue
        for feature in features_to_be_merged:
            feature_intersection = set.intersection(*(getattr(child, feature, set()) for child in zero_children)) \
                                   & getattr(n, feature, set())
            if feature_intersection:
                value = feature_intersection
            else:
                value = set.union(*(getattr(child, feature, set()) for child in zero_children)) \
                        | getattr(n, feature, set())
            if value:
                n.add_feature(feature, value)
        for child in zero_children:
            n.remove_child(child)
            for grandchild in child.children:
                n.add_child(grandchild)
        num_collapsed += len(zero_children)
    if num_collapsed:
        logging.getLogger('pastml').debug('Collapsed {} internal zero branches.'.format(num_collapsed))


def remove_certain_leaves(tr, to_remove=lambda node: False):
    """
    Removes all the branches leading to leaves identified positively by to_remove function.
    :param tr: the tree of interest (ete3 Tree)
    :param to_remove: a method to check is a leaf should be removed.
    :return: void, modifies the initial tree.
    """

    tips = [tip for tip in tr if to_remove(tip)]
    for node in tips:
        if node.is_root():
            return None
        parent = node.up
        parent.remove_child(node)
        # If the parent node has only one child now, merge them.
        if len(parent.children) == 1:
            brother = parent.children[0]
            brother.dist += parent.dist
            if parent.is_root():
                brother.up = None
                tr = brother
            else:
                grandparent = parent.up
                grandparent.remove_child(parent)
                grandparent.add_child(brother)
    return tr


def read_tree(tree_path):
    for f in (3, 2, 5, 1, 0, 3, 4, 6, 7, 8, 9):
        try:
            return Tree(tree_path, format=f)
        except:
            continue
    raise ValueError('Could not read the tree {}. Is it a valid newick?'.format(tree_path))

