import re
from collections import defaultdict, namedtuple
from functools import partial
from itertools import groupby
from operator import itemgetter
from typing import Dict, Callable, List, Tuple, Set

import networkx as nx
from cachetools import cached
from cachetools.keys import hashkey
from pulp import *
from pulp import LpProblem, LpMinimize, LpStatusOptimal, LpStatus

from mungo.common import vparse, NodeId
from mungo.repositorydata import get_repository_data, RepositoryData

Version = namedtuple("Version", "version build")

from networkx.algorithms.shortest_paths.generic import shortest_path_length


def equal_compare(y):
    p = re.compile(y.replace(".*", "*").replace("*", "(\D.*)??\Z"))
    return lambda x: bool(p.match(x.version))


# 3.*
# 3a
# 3*
# 3.0a

operator_function: Dict[str, Callable[[Version, Version], bool]] = {
    ">=": lambda x, y: vparse(x.version) >= vparse(y.version),
    ">": lambda x, y: vparse(x.version) > vparse(y.version),
    "<=": lambda x, y: vparse(x.version) <= vparse(y.version),
    "<": lambda x, y: vparse(x.version) < vparse(y.version),
    "!=": lambda x, y: ~(vparse(x.version) == vparse(y.version))
                       and (vparse(x.version) < vparse(y.version, ".99999999999999")),
    "==": lambda x, y: vparse(x.version) == vparse(y.version),
    #    "=": lambda x, y: (vparse(x.version) >= vparse(y.version))
    #                      and (vparse(x.version) < vparse(y.version, ".99999999999999")),
}


def build_comp(x: Version, constraint: Version) -> bool:
    xb, yb = x.build, constraint.build
    return xb == yb \
           or yb.endswith("*") and xb.startswith(yb.rstrip("*")) \
           or yb == "*"


# class Node:
#     def __init__(self, name: str, version, p):
#         self.name = name
#         self.version = version
#         self.distance_root = -1
#         self._in_nodes = []
#         self._out_nodes = defaultdict(list)
#         self._x = None
#         self.p = p
#         self._mass_low = None
#         self._mass_high = None
#         self.invalid = False
#
#     def add_in_node(self, n: 'Node'):
#         self._in_nodes.append(n)
#
#     def remove_in_node(self, n: 'Node'):
#         self._in_nodes.remove(n)
#
#     def add_out_node(self, n: 'Node'):
#         self._out_nodes[n.name].append(n)
#
#     def remove_out_node(self, n: 'Node'):
#         self._out_nodes[n.name].remove(n)
#
#     @property
#     def channel_name(self) -> str:
#         if self.p is None or "channel" not in self.p:
#             return ""
#         return self.p['channel'].split('/')[-2]
#
#     @property
#     def installed(self) -> bool:
#         if self.p is None:
#             return False
#         # print(self.name, self.version, "installed" in self.p)
#         return "installed" in self.p and self.p["installed"]
#
#     @property
#     def in_nodes(self) -> List['Node']:
#         return self._in_nodes
#
#     @property
#     def out_nodes(self) -> List['Node']:
#         for nodes in self._out_nodes.values():
#             for n in nodes:
#                 yield n
#
#     @property
#     def x(self) -> LpVariable:
#         # create LP variable, if not exist
#         if self._x is None:
#             self._x = LpVariable("{name}-{version}".format(name=self.name, version=self.version), 0, 1, LpInteger)
#         return self._x
#
#     def delete(self):
#         for n in self.in_nodes:
#             n.remove_out_node(self)
#         for n in self.out_nodes:
#             n.remove_in_node(self)
#
#
# NodeDict = DefaultDict[str, Dict[str, Node]]


@cached(cache={}, key=lambda ls, _: hashkey(ls))
def valid_packages(ls: tuple, repodata: List[Dict]):
    # print(ls)
    all_valids = []
    for s in ls:
        name, is_valid = _valid_packages_function(s)
        all_valids.append(is_valid)

    # all_valid = lambda x: reduce((lambda a, b: a(x) and b(x)), all_valids)
    all_valid = lambda x: any([f(x) for f in all_valids])  # TODO: any or all?

    ret = dict()
    for r in repodata:
        # if repodata doesnt hold "name"
        if name not in r.data:
            continue
        for x in r.data[name]:
            if x not in ret and all_valid(Version(*x)):
                ret[(name, *x)] = r.data[name][x]
    return ret


def split_package_constraint(s: str) -> Tuple[str, List[List[List[str]]]]:
    or_split = s.split("|")
    ret = []
    name = None

    for o in or_split:
        term = []
        for x in o.split(","):
            res = re.split('(==|!=|>=|<=|=|<|>| )', x)
            res = [y for y in res if y != " " and len(y) > 0]
            if name is None:
                name = res.pop(0)
            term.append(res)
        ret.append(term)
    return name, ret  # foo, [[]]


# print(split_package_constain("pysocks 4 rc3"))
# print(split_package_constain("pysocks >=1.5.6,<2.0,!=1.5.7"))
# print(split_package_constain("pysocks>=   1.5.6,  <  2.0,!= 1.5.7"))
# print(split_package_constain("pysocks 1=4"))
# f()

def _valid_packages_function(s: str) -> Tuple[str, Callable[[Version], bool]]:
    name, or_constraints = split_package_constraint(s)

    and_valids = []

    for constraints in or_constraints:
        is_valids = []  # lambda x: True

        for c in constraints:
            len_c = len(c)
            if len_c == 0:
                # no version constraint
                pass
            elif len_c == 1:
                # version constraint without operator (equals ==)
                version = c[0]
                is_valids.append(equal_compare(y=version))
            elif len_c == 2:
                # version constraint
                operator, v = c
                version = Version(v, "*")
                if operator == "=":
                    is_valids.append(equal_compare(y=v))
                elif operator in [">=", ">", "<=", "<", "!=", "=="]:
                    is_valids.append(partial(operator_function[operator], y=version))
                else:
                    # version build constraint with no operator
                    version = Version(*c)
                    if version.version != "*":
                        is_valids.append(equal_compare(y=version.version))
                    is_valids.append(partial(build_comp, constraint=version))
            elif len_c == 3:
                # operator version build
                operator, v, b = c
                version = Version(v, b)
                if operator == "=":
                    is_valids.append(equal_compare(y=v))
                elif operator in [">=", ">", "<=", "<", "!=", "=="]:
                    is_valids.append(partial(operator_function[operator], y=version))
                is_valids.append(partial(build_comp, constraint=version))
            else:
                raise Exception("invalid version constraint", s)

        def all_valids(x, is_valids=is_valids):
            return all([f(x) for f in is_valids])

        and_valids.append(all_valids)
    or_valid = lambda x: any([f(x) for f in and_valids])
    return name, or_valid


def create_node(G: nx.Graph,
                node_id: NodeId,
                repodata: List[RepositoryData],
                sender: NodeId = None,
                override_dependencies: List[str] = None):
    if node_id in G.nodes():
        return

    name, version, build = node_id
    vb = (version, build)

    if node_id == ("root", "0", "0"):
        G.add_node(node_id, **{"installed": False, "channel_name": ""})
    else:
        for r in repodata:  # TODO: option ignore order of repodata
            if name in r.data and vb in r.data[name]:
                G.add_node(node_id, **r.data[name][vb])
                dependencies = r.data[name][vb]["depends"]
                break

    if sender is not None:
        G.add_edge(sender, node_id)

    # get package information from repodata
    if override_dependencies is not None:
        dependencies = override_dependencies

    # TODO groupby

    grouped_dependencies = defaultdict(list)
    for dependency in dependencies:
        name = split_package_constraint(dependency)[0]
        grouped_dependencies[name].append(dependency)
    # print("python >=3.7,<3.8.0a0", valid_packages(("python >=3.7,<3.8.0a0", ), repodata))
    # exit()

    # print("openssl 1.0.1", list(valid_packages(["openssl 1.0.1"], repodata)))
    # print("valid_packages", valid_packages(("jpeg 9b",), repodata))
    # exit()

    # print("valid_packages", valid_packages(("zlib 1.2.*",), repodata))
    # exit()

    # print("valid_packages", valid_packages(("blas 1.1 openblas",), repodata))
    # exit()

    # print("valid_packages", valid_packages(("openmpi",), repodata))
    # exit()

    # print(name, version, grouped_dependencies)

    for dependency in grouped_dependencies.values():
        # make sure s is list like if string
        if isinstance(dependency, str):
            dependency = (dependency,)

        d_node_id = None

        for d_node_id, d_data in valid_packages(tuple(dependency), repodata).items():
            create_node(G, d_node_id, repodata, node_id)
            G.add_edge(node_id, d_node_id)

        if d_node_id is None:  # no versions were found for a dependency
            print_missing_package(dependency)
            # G.nodes[d_node]["invalid"] = True  # FIXME d_node(_id) is None here
            # raise Exception("no packages found for", *dependency)


def reduce_dag(G: nx.Graph, channels: List[str]):
    # reduce DAG

    # for name, versions in all_nodes.items():
    #    for current_node in versions.values():
    #        print(current_node.name, current_node.version)

    channel_order = dict()
    for priority, channel in enumerate(reversed(channels)):
        if channel == "defaults":
            channel_order['main'] = priority
            channel_order['free'] = priority
            channel_order['pro'] = priority
            channel_order['r'] = priority
        else:
            channel_order[channel] = priority
        channel_order[""] = priority + 1  # highest priority for local installed packages

    nodes_to_keep = set()

    grouped_nodes = [list(node_ids) for _, node_ids in groupby(sorted(G.nodes()), key=lambda x: x[0])]

    H = G.reverse()

    for group in grouped_nodes:
        seen = defaultdict(list)
        for node_id in group:
            children = tuple(sorted(G.edges(node_id)))
            parents = tuple(sorted(H.edges(node_id)))
            seen[(children, parents)].append(node_id)

        for key, node_ids in seen.items():
            nodes_to_keep.add(max(node_ids, key=partial(package_order, G=G, installed_priority=priority + 1, channel_order=channel_order)))

    return G.subgraph(nodes_to_keep)


def distances_dag(G: nx.Graph):
    return shortest_path_length(G, ("root", "0", "0"))
    # q = [root]
    # root.distance_root = 0
    #
    # while len(q) > 0:
    #     current_node = q.pop(0)
    #     for child in current_node.out_nodes:
    #         if child.distance_root == -1:
    #             child.distance_root = current_node.distance_root + 1
    #             q.append(child)


def create_dag(channels: List[str],
               packages: Set[str],
               local_repodata: List[RepositoryData],
               njobs: int = 8,
               offline: bool = False,
               force_download: bool = False) -> nx.Graph:
    print("download repodata")
    repodata = get_repository_data(channels, njobs, offline, force_download)

    print("build dag")

    # default_packages = {"sqlite", "wheel", "pip"}
    default_packages = set()

    G = nx.DiGraph()
    # G.add_node(("root", "0", "0"), attr_dict={"depends": list(packages | default_packages)})

    create_node(G, ("root", "0", "0"), repodata,
                override_dependencies=list(packages | default_packages))

    # reduce DAG
    reduce_dag(G, channels)
    # reduce_dag(all_nodes, channels)
    return G


def package_order(node_id, G, installed_priority, channel_order):
    attributes = G.nodes[node_id]
    return channel_order[attributes.get("channel_name", "")] \
           + attributes.get("installed", False) * installed_priority, vparse(node_id[1])


def nodes_to_install(G: nx.Graph, channels: List[str]) -> Dict[NodeId, Dict]:
    channel_order = dict()
    for priority, channel in enumerate(reversed(channels)):
        if channel == "defaults":
            channel_order['main'] = priority
            channel_order['free'] = priority
            channel_order['pro'] = priority
            channel_order['r'] = priority
        else:
            channel_order[channel] = priority
        channel_order[""] = priority + 1  # highest priority for local installed packages

    # create ILP problem
    prob = LpProblem("DependencySolve", LpMinimize)

    # build LP on the reduced DAG
    objective = []

    # n.p['channel'].split('/')[-2]

    # create LP variables
    for node_id in G.nodes():
        G.nodes[node_id]["x"] = LpVariable(node_id, 0, 1, LpInteger)

    grouped_nodes = [list(node_ids) for _, node_ids in groupby(sorted(G.nodes()), key=lambda x: x[0])]

    constraints = []
    for node_ids in grouped_nodes:
        constraints.append(pulp.lpSum([G.nodes[node_id]["x"] for node_id in node_ids]) <= 1)

    # create brother information
    for node_ids in grouped_nodes:
        big_brother = None
        # small hack to make local always be the highest
        for node_id in sorted(node_ids, key=partial(package_order, G=G, installed_priority=priority + 1,
                                                channel_order=channel_order), reverse=True):
            node = G.nodes[node_id]
            node["big_brother"] = big_brother
            big_brother = node_id

    prob += G.nodes[("root", "0", "0")]["x"] == 1

    distances = distances_dag(G)

    def mass(node_id: NodeId):
        if node_id is None:
            return 0, 0

        node = G.nodes[node_id]

        if node.get("_mass_low") is None:
            # n._mass_low = 0  # temporarily set mass to 0 for loops in "DAG"
            # n._mass_high = 0  # temporarily set mass to 0 for loops in "DAG"
            m_low = 0
            m_high = 0
            # print(n.name, n.distance_root)

            grouped_children = [list(g) for _, g in
                                groupby(sorted(map(itemgetter(1), G.edges(node_id))), key=itemgetter(0))]
            for children in grouped_children:
                children_masses = [mass(c) for c in children if distances[c] > distances[node_id]]
                if len(children_masses) > 0:
                    m_low += min([c for c, _ in children_masses])
                    m_high += max([c for _, c in children_masses])
                else:
                    m_low = 0
                    m_high = 1
            # n._mass_low = m_low + 1 + mass(n.big_brother)[1]
            # n._mass_high = m_high + 1 + mass(n.big_brother)[1]
            node["_mass_high"] = m_high - m_low + 1 + mass(node["big_brother"])[1]
            node["_mass_low"] = 1 + mass(node["big_brother"])[1]
        return node["_mass_low"], node["_mass_high"]

    # for name, versions in all_nodes.items():
    #     for version, n in versions.items():
    #         print(name, version, mass(n))

    # create ILP
    for node_id in G.nodes():
        # exclude invalid node
        node = G.nodes[node_id]

        if node.get("invalid", False):  # exlude invalid nodes
            constraints.append(node["x"] == 0)
            continue

        grouped_children = [list(g) for _, g in
                            groupby(sorted(map(itemgetter(1), G.edges(node_id))), key=itemgetter(0))]

        # constraint: if a parent is installed, one version of each dependency must be installed too
        for children_group in grouped_children:
            constraints.append(pulp.lpSum(G.nodes[c]["x"] for c in children_group) >= node["x"])

        # storing the objectives
        objective.append(mass(node_id)[0] * node["x"])
        # print([(n.name, n.normalized_version, n.factor) for n in versions.values()])

    prob.extend(constraints)
    prob.setObjective(pulp.lpSum(objective))
    prob.writeLP("WhiskasModel.lp")
    prob.solve()

    if prob.status != LpStatusOptimal:
        print(f"ERROR: Solution is not optimal (status: {LpStatus[prob.status]}).\nAborting.", file=sys.stderr)
        exit(1)

    # for v in prob.variables():
    #     print(v.name, v.varValue)

    # collect all install nodes
    install_nodes = dict()
    for node_id in sorted(G.nodes()):
        # print(n.name, n.version, n.x.varValue, "installed" in n.p)
        if node_id == ("root", "0", "0"):  # skip root
            continue

        if G.nodes[node_id]["x"].varValue == 1.0:
            install_nodes[node_id] = G.nodes[node_id]
            # install_nodes.append(node_id)

    return install_nodes


missing_dependencies = set()


def print_missing_package(dependency: list):
    # print missing package information for a dependency constraint
    # only print once by remembering
    dependency = tuple(dependency)
    if dependency not in missing_dependencies:
        print("WARNING:", "no packages found for", *dependency, file=sys.stderr)
        missing_dependencies.add(dependency)
