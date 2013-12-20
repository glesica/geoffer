import json
from itertools import repeat, izip, izip_longest


class Node(object):
    """
    An object to represent a single graph node.
    """
    def __init__(self, name, labels=None, props=None):
        self.name = name
        self.labels = labels or []
        self.props = props or {}


def nodestr(node, hook=False, hook_keys=(), abbrev=False):
    """
    Create a Geoff node string representation for a node with the given name,
    labels and properties. Optionally, the node may be represented as a hook
    (in which case at least one label is required) and optional keys may be
    provided that will be matched to node properties along with the hook. If
    `abbrev` is `True` the short version of a node will be produced, which is
    basically just the name in parentheses.

    :param node: The node to represent
    :type node: A `Node` object
    :param hook: Whether the update (hook) syntax should be used
    :type hook: Boolean
    :param hook_keys: Property keys to match for hook syntax
    :type hook_keys: Iterable
    :param abbrev: Whether the abbreviated syntax should be used
    :type abbrev: Boolean

    TODO: Check that hook keys are in properties dictionary
    TODO: Allow string for labels if only one label

    >>> nodestr(Node('alice'))
    '(alice)'
    >>> nodestr(Node('alice', ['Person']))
    '(alice:Person)'
    >>> nodestr(Node('alice', ['Person'], {'name': 'Alice'}))
    '(alice:Person {"name": "Alice"})'
    >>> nodestr(Node('alice', ['Person']), hook=True)
    ':Person:=>(alice:Person)'
    >>> nodestr(Node('alice', ['Person'], {'name': 'Alice'}), hook=True, hook_keys=('name',))
    ':Person:name:=>(alice:Person {"name": "Alice"})'
    >>> nodestr(Node('alice', ['Person'], {'name': 'Alice'}), abbrev=True)
    '(alice)'
    """
    name = node.name
    labels = node.labels
    props = node.props

    if abbrev:
        return '({})'.format(name)

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


def relstr(nodes, kinds, props={}, abbrevs=False):
    """
    Creates a path of directed relationships.

    :param nodes: Nodes to be linked in a chain
    :type nodes: Iterable of `Node` objects
    :param kinds: Strings describing relationship types
    :type kinds: Iterable or string, length one less than `nodes` if iterable
    :param props: Properties to be assigned to edges
    :type props: Iterable or dict, length one less than `nodes` if iterable
    :param abbrevs: Whether the abbreviated node format should be used
    :type abbrevs: Iterable or boolean, same length as `nodes` if iterable

    >>> n1 = Node('alice', ['Person'], {'name': 'Alice'})
    >>> n2 = Node('bob', ['Person'], {'name': 'Bob'})
    >>> n3 = Node('carol', ['Person'], {'name': 'Carol'})
    >>> relstr([n1, n2, n3], ['KNOWS', 'LIKES'], abbrevs=True)
    '(alice)-[:KNOWS]->(bob)-[:LIKES]->(carol)'
    >>> relstr([n1, n2, n3], ['KNOWS', 'LIKES'], [{'since': 'yesterday'}, {'since': 'today'}], abbrevs=True)
    '(alice)-[:KNOWS {"since": "yesterday"}]->(bob)-[:LIKES {"since": "today"}]->(carol)'
    """
    numrels = len(nodes) - 1
    if type(kinds) not in (list, tuple):
        kinds = repeat(kinds, numrels)

    if type(props) not in (list, tuple):
        props = repeat(props, numrels)

    if type(abbrevs) not in (list, tuple):
        abbrevs = repeat(abbrevs, len(nodes))

    ks = ['-[:{}'.format(k) for k in kinds]
    ps = [' {}]->'.format(json.dumps(p)) if p else ']->' for p in props]
    rs = [k + p for k, p in izip(ks, ps)]
    ns = [nodestr(n, abbrev=a) for n, a in izip(nodes, abbrevs)]

    return ''.join([n + r for n, r in izip_longest(ns, rs, fillvalue='')])
