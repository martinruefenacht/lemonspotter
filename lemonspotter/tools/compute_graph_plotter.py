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

        if not function.leads_all and not function.leads_any and not function.needs_all and not function.needs_any:
            net.add_node(id, function.name, color='#F4F1BB')

        elif not function.needs_all and not function.needs_any:
            net.add_node(id, function.name, color='#ED6A5A')

        elif not function.leads_all and not function.leads_any:
            net.add_node(id, function.name, color='#E6EBE0')

        else:
            net.add_node(id, function.name)

    # add need edges
    for function in Database().get_functions():
        for need in function.needs_any:
            if function in need.leads_all or function in need.leads_any:
                continue

            net.add_edge(idmap[need.name], idmap[function.name], color='#95C623')

    # add lead edges
    for function in Database().get_functions():
        for lead in function.leads_any:
            if function in lead.needs_all or function in lead.needs_any:
                continue

            net.add_edge(idmap[function.name], idmap[lead.name], color='#0E4749')

    # add critical edges, start -> end
    for function in Database().get_functions():
        for lead in function.leads_any:
            if function in lead.needs_any:
                net.add_edge(idmap[function.name], idmap[lead.name], color='#E55812')

    net.show('plot.html')


if __name__ == '__main__':
    main()
