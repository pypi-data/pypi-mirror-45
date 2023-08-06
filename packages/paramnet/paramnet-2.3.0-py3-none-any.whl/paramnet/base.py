import networkx as nx

from paramnet.meta import ParametrizedMeta
from paramnet.view import ParamView

__all__ = []
__all__.extend([
    'Parametrized'
])


class Parametrized(object, metaclass=ParametrizedMeta):

    def __getattr__(self, attr_name):
        if attr_name in self._graph_params:
            return self.graph[attr_name]
        else:
            raise AttributeError(attr_name)

    def __setattr__(self, attr_name, value):
        if attr_name in self._graph_params:
            self.graph[attr_name] = value
        else:
            try:
                attr = super().__getattribute__(attr_name)
            except (AttributeError, KeyError):
                attr = None

            if isinstance(attr, ParamView):
                attr.set(value)
            else:
                super().__setattr__(attr_name, value)

    def __delattr__(self, attr_name):
        attr = super().__getattribute__(attr_name)
        if isinstance(attr, ParamView):
            raise AttributeError(
                f"Can't delete param attribute '{attr_name}'.")
        else:
            super().__delattr__(attr_name)

    def index(self, node):
        try:
            return list(self._node.keys()).index(node)
        except ValueError:
            raise nx.NetworkXError(f"The node {node} is not in the graph.")

    @property
    def node_params(self):
        return self._node_params

    @property
    def edge_params(self):
        return self._edge_params
