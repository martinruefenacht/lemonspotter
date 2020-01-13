"""
"""

import sys
from pathlib import Path


from pyvis.network import Network


from lemonspotter.parsers.mpiparser import MPIParser
from lemonspotter.parsers.standardparser import StandardParser
from lemonspotter.core.database import Database
from lemonspotter.core.parameter import Direction


def main() -> None:
    """
    """

    # parser = MPIParser()
    # parser.parse(Path(sys.argv[1]))

    parser = StandardParser()
    parser(Path(sys.argv[1]))

    net = Network(height='100%', width='100%', directed=True)
    net.barnes_hut(overlap=1, central_gravity=2)

    # add all constants
    # net.add_node('MPI_COMM_WORLD', color='#F4A261')
    # net.add_node('MPI_COMM_SELF', color='#F4A261')
    # net.add_node('MPI_COMM_NULL', color='#F4A261')

    # add all nodes
    for id, function in enumerate(Database().get_functions()):
        net.add_node(function.name)

    # draw edges between constructors to consumers

    for producer in Database().get_functions():
        outs = []
        outs.append(producer.return_abstract_type)
        outs.extend([param.abstract_type for param in producer.parameters if param.direction == Direction('out')])

        for out_type in outs:
            found = False

            for consumer in Database().get_functions():
                # TODO self loop allowed?

                for param in consumer.parameters:
                    if param.direction == Direction('in') and param.abstract_type == out_type:
                        # draw edge
                        net.add_edge(producer.name, consumer.name, title=out_type)
                        found = True

            if not found:
                if not ('TYPE_' + out_type) in net.get_nodes():
                    net.add_node('TYPE_' + out_type, color='#E76F51')

                net.add_edge(producer.name, 'TYPE_' + out_type, color='#E76F51')

        for in_type in [param.abstract_type for param in producer.parameters if param.direction == Direction('in')]:
            if in_type not in outs:
                net.add_node('TYPE_' + in_type, color='#2A9D8F')
                net.add_edge('TYPE_' + in_type, producer.name, color='#2A9D8F')

    # constants exist, how do we represent it? a node per constant or a single constant node?

    net.show('plot.html')


if __name__ == '__main__':
    main()
