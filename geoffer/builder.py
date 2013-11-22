import json
from collections import namedtuple


class Node(object):
    def __init__(self, name, labels=None, props=None):
        self.name = name
        self.labels = labels or []
        self.props = props or {}


class Rel(object):
    def __init__(self, kind, nodes, props=None):
        self.kind = kind
        self.nodes = nodes
        self.props = props or {}


def node_string(node, hook=False, hook_keys=()):
    """
    Create a Geoff node string representation for a node with the given name,
    labels and properties. Optionally, the node may be represented as a hook
    (in which case at least one label is required) and optional keys may be
    provided that will be matched to node properties along with the hook.

    TODO: Check that hook keys are in properties dictionary
    TODO: Allow string for labels if only one label

    >>> node_string(Node('alice'))
    '(alice)'
    >>> node_string(Node('alice', ['Person']))
    '(alice:Person)'
    >>> node_string(Node('alice', ['Person'], {'name': 'Alice'}))
    '(alice:Person {"name": "Alice"})'
    >>> node_string(Node('alice', ['Person']), hook=True)
    ':Person:=>(alice:Person)'
    >>> node_string(Node('alice', ['Person'], {'name': 'Alice'}), hook=True, hook_keys=('name',))
    ':Person:name:=>(alice:Person {"name": "Alice"})'
    """
    name = node.name
    labels = node.labels
    props = node.props

    ps = json.dumps(props)
    ls = ':'.join(labels)

    if labels and props:
        ns = '({}:{} {})'.format(name, ls, ps)
    elif props:
        ns = '({} {})'.format(name, ps)
    elif labels:
        ns = '({}:{})'.format(name, ls)
    else:
        ns = '({})'.format(name)

    hks = ':'.join(hook_keys)

    if hook and not labels:
        raise Exception('At least one label is required if hook=True')

    if hook and hook_keys:
        hs = ':{}:{}:=>'.format(ls, hks)
    elif hook:
        hs = ':{}:=>'.format(ls)
    else:
        hs = ''

    return hs + ns


def rel_string(rel):
    """
    Create a Geoff relationship string representation for a chain of nodes. The
    relationship direction will be left-to-right (first-to-last) so, for
    example, if two nodes are given, the output will be a directed relationship
    from the first (element zero) to the second (element one). At least two
    nodes much be given.
    """
    pass
