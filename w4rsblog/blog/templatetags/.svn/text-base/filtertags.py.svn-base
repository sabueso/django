from django.template import Library, Node, TemplateSyntaxError
from django.template import VariableNode, FILTER_SEPARATOR
from django.template.loader_tags import BlockNode

register = Library()

FINALIZED_FILTER_NAME = 'finalized'

class FinalFilterNode(Node):
    def __init__(self, nodelist, filters):
        self.nodelist = nodelist
        self.filters = filters
        self.parsed = False

    def render(self, context):
        self.parse_nodes()
        return self.nodelist.render(context)
    
    def parse_nodes(self):
        if self.parsed:
            # Don't ever parse twice.
            return
        nodelist = self.nodelist
        # Parse inner FinalFilterNodes first (they may contain a
        # finalize filter).
        for node in nodelist.get_nodes_by_type(FinalFilterNode):
            node.parse_nodes()
        # Parse child nodes.
        for node in nodelist.get_nodes_by_type(VariableNode):
            node_filters = node.filter_expression.filters
            filter_funcs = [filter[0] for filter in node_filters]
            if finalized not in filter_funcs:
                # Ignore the node if it has the finalized functions in
                # its filters.
                for filter in self.filters:
                    if filter[0] not in filter_funcs:
                        # Don't double-up on filters which have already
                        # been applied to this VariableNode.
                        node_filters.append(filter)
        self.parsed = True

class ListFilterNode(Node):
    def __init__(self, context_list, filter_expr):
        self.context_list = context_list
        self.filter_expr = filter_expr
        
    def render(self, context):
        if context.get(self.context_list):
            context[self.context_list] = self.recursive_filter(context[self.context_list])
        return ''
    
    def recursive_filter(self, item):
        if hasattr(item, '__iter__'):
            # If the item is iterable then recurse.
            return map(self.recursive_filter, item)
        return self.filter_expr.resolve({self.filter_expr.var: item}, ignore_failures=True)

def finalfilter(parser, token):
    """
    Add common filters to all variable nodes within this block tag.
    Use the `finalized` filter in a variable node to skip adding the filters
    to that node. If a common filter has already been explicitly added to a
    variable node, it will *not* be added again.

    Filters can also be piped through each other, and they can have
    arguments -- just like in variable syntax.

    Note: This tag adds the filter(s) at render time so this happens across
    all extended block tags.

    Example usage::

        {% finalfilter escape %}
            {{ html_menu|finalized }}
            <h2>{{ object.company }}</h2>
            <p>
                <a href="{{ object.url }}">
                    {{ object.first_name }} {{ object.last_name }}
                </a>
            </p>
        {% endfinalfilter %}

    This example would add the escape filter to the end of each variable node
    except for `html_menu`.
    """
    nodelist = parser.parse(('endfinalfilter',))
    parser.delete_first_token()
    
    try:
        _, rest = token.contents.split(None, 1)
    except ValueError:
        raise TemplateSyntaxError, "'finalfilter' requires at least one filter"
    
    # Build the final filters list.
    filter_expression = parser.compile_filter('var%s%s' % (FILTER_SEPARATOR, rest))
    filters = filter_expression.filters

    return FinalFilterNode(nodelist, filters)
finalfilter = register.tag(finalfilter)

def listfilter(parser, token):
    """
    Replace a list in the context with one where each item has been processed
    by the given filters. This also works with nested lists.

    Filters can also be piped through each other, and they can have
    arguments -- just like in variable syntax.
    
    Example usage::

        list_menu = ['People', [['Bob & Anne', []]]]

        {% listfilter list_menu escape %}
        <ul>{{ list_menu|unordered_list}}</ul>

    This example would output::

        <ul><li>People
        <ul>
            <li>Bob &amp; Anne</li>
        </ul>
        </li></ul>
    """
    try:
        context_list, rest = token.contents.split(None, 2)[1:]
    except TypeError:
        raise TemplateSyntaxError, "'listfilter' requires at least one argument"
    
    filter_expr = parser.compile_filter('var%s%s' % (FILTER_SEPARATOR, rest))

    return ListFilterNode(context_list, filter_expr)
listfilter = register.tag(listfilter)

def finalized(value):
    """
    Filter used to cancel the effect of {% finalfilter %}, has no other effect.
    """
    return value
register.filter(FINALIZED_FILTER_NAME, finalized)