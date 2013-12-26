import json
from itertools import repeat, izip, izip_longest


class Node(object):
    """
    An object to represent a single graph node.
    """
    def __init__(self, name=None, labels=None, props=None):
        self.name = name or ''
        self.labels = labels or []
        self.props = props or {}

    def __repr__(self):
        return '({})'.format(self.name)


def nodestr(node, unique_key=None, abbrev=False):
    """
    Create a Geoff node string representation for a node with the given name,
    labels and properties. Optionally, the node may be created using the unique
    syntax. This will cause the node to be updated if it already exists. If
    `abbrev` is `True` the short version of a node will be produced, which is
    basically just the name in parentheses.

    :param node: The node to represent
    :type node: A `Node` object
    :param unique_key: Property keys to match for update syntax
    :type unique_key: String
    :param abbrev: Whether the abbreviated syntax should be used
    :type abbrev: Boolean

    TODO: Allow string for labels if only one label

    >>> alice = Node('alice', ['Person'], {'name': 'Alice'})
    >>> bob = Node('bob')
    >>> nodestr(alice)
    '(alice:Person {"name": "Alice"})'
    >>> nodestr(bob)
    '(bob)'
    >>> nodestr(alice, unique_key='name')
    '(alice:Person!name {"name": "Alice"})'
    >>> nodestr(alice, abbrev=True)
    '(alice)'
    """
    name = node.name
    labels = node.labels
    props = node.props

    if abbrev:
        return '({})'.format(name)

    if unique_key and unique_key not in props:
        raise Exception('props must contain unique_key if set')

    if unique_key and not labels:
        raise Exception('At least one label is required if unique=True')

    ps = json.dumps(props)

    if unique_key:
        if len(labels) > 1:
            ls = '{}!{}:{}'.format(labels[0], unique_key, ':'.join(labels[1:]))
        else:
            ls = '{}!{}'.format(labels[0], unique_key)
    else:
        ls = ':'.join(labels)

    if labels and props:
        ns = '({}:{} {})'.format(name, ls, ps)
    elif props:
        ns = '({} {})'.format(name, ps)
    elif labels:
        ns = '({}:{})'.format(name, ls)
    else:
        ns = '({})'.format(name)

    return ns


def relstr(node1, node2, kind, props={}, bidir=False, unique_key=None, abbrev=True):
    """
    Creates a path of directed relationships.

    :param node1: First node in the two-node chain
    :type node1: `Node` object
    :param node2: First node in the two-node chain
    :type node2: `Node` object
    :param kind: Relationship type
    :type kind: String
    :param props: Properties to be assigned to edges
    :type props: Iterable or dict, length one less than `nodes` if iterable
    :param bidir: Create two relationships, one in each direction
    :type bidir: Boolean
    :prop unique_key: Property key to match on for uniqueness
    :type unique_key: String
    :param abbrev: Whether the abbreviated node format should be used
    :type abbrev: Boolean

    >>> alice = Node('alice', ['Person'])
    >>> bob = Node('bob')
    >>> relstr(alice, bob, 'KNOWS')
    '(alice)-[:KNOWS]->(bob)'
    >>> relstr(alice, bob, 'KNOWS', {'since': 1999})
    '(alice)-[:KNOWS {"since": 1999}]->(bob)'
    >>> relstr(alice, bob, 'KNOWS', {'since': 1999}, unique_key='since')
    '(alice)-[:KNOWS!since {"since": 1999}]->(bob)'
    >>> relstr(alice, bob, 'KNOWS', bidir=True)
    '(alice)<-[:KNOWS]->(bob)'
    >>> relstr(alice, bob, 'KNOWS', abbrev=False)
    '(alice:Person)-[:KNOWS]->(bob)'
    """
    ns1 = nodestr(node1, abbrev=abbrev)
    ns2 = nodestr(node2, abbrev=abbrev)

    if unique_key and unique_key not in props:
        raise Exception('props must contain unique_key if set')

    if unique_key:
        if props:
            rs = '{}!{} {}'.format(kind, unique_key, json.dumps(props))
        else:
            rs = '{}!{}'.format(kind, unique_key)
    else:
        if props:
            rs = '{} {}'.format(kind, json.dumps(props))
        else:
            rs = kind

    if bidir:
        return '{}<-[:{}]->{}'.format(ns1, rs, ns2)
    else:
        return '{}-[:{}]->{}'.format(ns1, rs, ns2)
