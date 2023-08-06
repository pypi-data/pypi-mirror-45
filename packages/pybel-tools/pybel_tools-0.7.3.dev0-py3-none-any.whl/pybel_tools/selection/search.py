# -*- coding: utf-8 -*-

from pybel.struct.filters import build_node_name_search, filter_nodes
from ..filters.node_filters import namespace_inclusion_builder

__all__ = [
    'search_node_names',
    'search_node_namespace_names',
    'search_node_hgnc_names',
]


def search_node_names(graph, query):
    """Search for nodes containing a given string(s).

    :param pybel.BELGraph graph: A BEL graph
    :param query: The search query
    :type query: str or iter[str]
    :return: An iterator over nodes whose names match the search query
    :rtype: iter

    Example:

    .. code-block:: python

        >>> from pybel.examples import sialic_acid_graph
        >>> from pybel_tools.selection import search_node_names
        >>> list(search_node_names(sialic_acid_graph, 'CD33'))
        [('Protein', 'HGNC', 'CD33'), ('Protein', 'HGNC', 'CD33', ('pmod', ('bel', 'Ph')))]
    """
    return filter_nodes(graph, build_node_name_search(query))


def search_node_namespace_names(graph, query, namespace):
    """Search for nodes with the given namespace(s) and whose names containing a given string(s).

    :param pybel.BELGraph graph: A BEL graph
    :param query: The search query
    :type query: str or iter[str]
    :param namespace: The namespace(s) to filter
    :type namespace: str or iter[str]
    :return: An iterator over nodes whose names match the search query
    :rtype: iter
    """
    node_predicates = [
        namespace_inclusion_builder(namespace),
        build_node_name_search(query)
    ]

    return filter_nodes(graph, node_predicates)


def search_node_hgnc_names(graph, query):
    """Search for nodes with the HGNC namespace and whose names containing a given string(s).

    :param pybel.BELGraph graph: A BEL graph
    :param query: The search query
    :type query: str or iter[str]
    :return: An iterator over nodes whose names match the search query
    :rtype: iter
    """
    return search_node_namespace_names(graph, query, namespace='HGNC')
