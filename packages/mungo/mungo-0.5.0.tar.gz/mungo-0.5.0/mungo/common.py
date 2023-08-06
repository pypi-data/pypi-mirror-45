from typing import Tuple, Set, Dict

import networkx as nx
from conda.models.version import VersionOrder

mungoversion = "0.5.0"
NodeId = Tuple[str, str, str]


def vparse(x: str, add: str = "") -> VersionOrder:
    # TODO: remove strip?
    if x != "*":
        x = x.strip("*").strip(".")
    return VersionOrder(f"{x}{add}")


def print_dag(G: nx.Graph, packages: Set[str], to_install: Dict[NodeId, Dict], installed: dict = None):
    from graphviz import Digraph
    dot = Digraph()
    # dot.attr("graph", splines="false")

    # ugly, but sufficient for the time being
    installed_keys = installed.keys() if installed is not None else {}
    changed = installed_keys & to_install.keys()
    local_versions = {name: list(installed[name].values())[0] for name in changed}
    remote_versions = {name: data for name, data in to_install.items() if name in changed}
    version_changes = {package: (local_versions[package], remote_versions[package]) for package in changed}
    upgrades = {package: (p_from, p_to)
                for (package, (p_from, p_to)) in version_changes.items()
                if vparse(p_from['version']) < vparse(p_to['version'])
                }
    downgrades = {package: (p_from, p_to)
                  for (package, (p_from, p_to)) in version_changes.items()
                  if vparse(p_from['version']) > vparse(p_to['version'])
                  }
    # nodes
    out_nodes = set()
    for ((name, version, build), _) in to_install.items():
        # color = "white" if v.name not in changed else "red"
        requested = name in packages
        upgrade = name in upgrades
        downgrade = name in downgrades
        local = name in installed_keys
        kwargs = {
            # 'shape': "house" if upgrade else "invhouse" if downgrade else "folder" if local else "note",
            'shape': "folder" if local else "note",
            'fillcolor': "#C0E2E7" if requested else "#CFE7C0" if upgrade else "#E7C6C0" if downgrade else "white",
            'style': 'filled',
            'fontname': 'Fira Sans',
        }
        dot.node(f"{name}_{version}", f"{name}\n{version} {build}", **kwargs)
        out_nodes.add((name, version, build))

    # edges
    distances = nx.shortest_path_length(G, ("root", "0", "0"))
    for (nvb, data) in to_install.items():
        for (_, c) in G.edges(nvb):
            if c in out_nodes:
                c_name, c_version, c_build = c
                for d in data["depends"]:
                    if d.startswith(c_name):  # find dependency
                        kwargs = {
                            'fontname': 'Fira Sans',
                        }
                        dot.edge(f"{nvb[0]}_{nvb[1]}", f"{c_name}_{c_version}",
                                 label='\n'.join(d.split(' ')),
                                 weight=f"{distances[nvb]}",
                                 **kwargs)
    dot.render('graph.tmp', view=True)
    # print(dot.source)
