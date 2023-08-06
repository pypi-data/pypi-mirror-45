from collections import OrderedDict

import networkx as nx

from paramnet.exceptions import FieldConflictError
from paramnet.view import NodeParamView, EdgeParamView

__all__ = []
__all__.extend([
    'ParametrizedMeta'
])


class ParametrizedMeta(type):

    def __new__(mcs, name, bases, attrs, node_params=None, edge_params=None,
                graph_params=None, *args, **kwargs):
        if node_params is None:
            node_params = set()
        if edge_params is None:
            edge_params = set()
        if graph_params is None:
            graph_params = set()

        def getattr_union(attr):
            return set.union(*[getattr(b, attr, set()) for b in bases])

        attrs['_node_params'] = getattr_union('_node_params')
        attrs['_edge_params'] = getattr_union('_edge_params')
        attrs['_graph_params'] = getattr_union('_graph_params')

        attrs['_node_params'].update(node_params)
        attrs['_edge_params'].update(edge_params)
        attrs['_graph_params'].update(graph_params)

        attrs['node_dict_factory'] = OrderedDict

        return super().__new__(mcs, name, bases, attrs, *args, **kwargs)

    def __call__(cls, *args, **kwargs):
        if not issubclass(cls, nx.Graph):
            raise TypeError("Can't parametrize a non-graph class.")

        obj = super().__call__(*args, **kwargs)

        # add descriptors for param access

        # adjacency matrix
        setattr(obj, "A", EdgeParamView("weight", obj, default=1.0))

        for field in obj._node_params:
            if hasattr(obj, field):
                raise FieldConflictError(
                    f"Trying to overwrite existing field {field} for class "
                    f"{cls.__name__}.")
            setattr(obj, field, NodeParamView(field, obj))

        for field in obj._edge_params:
            if field == 'weight':
                continue
            if hasattr(obj, field):
                raise FieldConflictError(
                    f"Trying to overwrite existing field {field} for class "
                    f"{cls.__name__}.")
            setattr(obj, field, EdgeParamView(field, obj))

        return obj
