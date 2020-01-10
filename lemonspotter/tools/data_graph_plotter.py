"""
"""

import sys
from pathlib import Path


from pyvis.network import Network


from lemonspotter.parsers.mpiparser import MPIParser
from lemonspotter.parsers.standardparser import StandardParser
from lemonspotter.core.database import Database


def main() -> None:
    """
    """

    # parser = MPIParser()
    # parser.parse(Path(sys.argv[1]))

    parser = StandardParser()
    parser(Path(sys.argv[1]))

    net = Network(height='100%', width='100%', directed=True)
    net.barnes_hut(overlap=1, central_gravity=2)

    idmap = {}

    # add all nodes
    for id, function in enumerate(Database().get_functions()):
        idmap[function.name] = id

        net.add_node(id, function.name)

    # draw edges between constructors to consumers

    # constants exist, how do we represent it? a node per constant or a single constant node?

    net.show('plot.html')


if __name__ == '__main__':
    main()
