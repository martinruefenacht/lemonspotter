"""
"""

import sys
from pathlib import Path
from random import choice, random
from itertools import chain


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

    net = Network(height='100%', width='100%', directed=True, layout=True)
    # net.barnes_hut(overlap=1, central_gravity=2)

    nodes = Database().get_functions()

    # # filter down to non-independent
    # # TODO ignore for now, include after, they can be used always
    # nodes = [node for node in nodes if (node.needs_all or node.needs_any or
    #                                     node.leads_any or node.leads_all)]

    print(nodes)

    # starting points
    no_need_nodes = [node for node in nodes if (not node.needs_any and not node.needs_all and
                                                (node.leads_any or node.leads_all))]
    print(no_need_nodes)

    # end points
    no_lead_nodes = [node for node in nodes if (not node.leads_any and not node.leads_all and
                                                (node.needs_any or node.needs_all))]
    print(no_lead_nodes)

    internal_nodes = [node for node in nodes if ((node.leads_all or node.leads_any) and
                                                 (node.needs_all or node.needs_any))]
    print(internal_nodes)

    independent_nodes = [node for node in nodes if (not node.leads_all and not node.leads_any and
                                                    not node.needs_all and not node.needs_any)]
    print(independent_nodes)

    paths = []

    def generate_path():
        path = []

        # start
        path.append(no_need_nodes[0])

        while random() > 0.01:
            node = choice(list(chain(independent_nodes, internal_nodes)))

            if node in path:
                continue

            path.append(node)

        # end
        path.append(no_lead_nodes[0])

        return path

    for idx in range(1000):
        path = generate_path()

        if path not in paths:
            paths.append(path)

    for idx, path in enumerate(paths):
        # nodes
        for node in path:
            if node in no_lead_nodes:
                # end
                net.add_node(node.name+'_'+str(idx), label=node.name, color='#E76F51')

            elif node in no_need_nodes:
                # start
                net.add_node(node.name+'_'+str(idx), label=node.name, color='#F4A261')

            elif node in independent_nodes:
                net.add_node(node.name+'_'+str(idx), label=node.name, color='#E9C46A')

            else:
                net.add_node(node.name+'_'+str(idx), label=node.name, color='#2A9D8F')

        # edges
        for n0, n1 in zip(path, path[1:]):
            net.add_edge(n0.name+'_'+str(idx), n1.name+'_'+str(idx), color='#264653')

    net.show('plot.html')


if __name__ == '__main__':
    main()
