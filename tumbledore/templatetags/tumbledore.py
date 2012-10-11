from django import template
from django.utils.safestring import mark_safe
from django.template.base import FilterExpression
from django.template.defaulttags import ForNode

models = __import__('tumbledore', None, None, [], 2).models
register = template.Library()

DEFAULT_NUMBER_OF_POSTS = 5


@register.tag(name='tumblevar')
def do_captureas(parser, token):
    try:
        tag_name, args = token.contents.split(None, 1)
    except ValueError:
        raise template.TemplateSyntaxError("'tumblevar' node requires a variable name.")
    nodelist = parser.parse(('endtumblevar',))
    parser.delete_first_token()
    return CaptureasNode(nodelist, args)


class CaptureasNode(template.Node):
    def __init__(self, nodelist, varname):
        self.nodelist = nodelist
        self.varname = varname

    def render(self, context):
        output = mark_safe(self.nodelist.render(context))
        context[self.varname] = output
        return ''


@register.tag(name='tumbleposts')
def do_tumbleposts(parser, token):
    '''
    Iterates given block over tumblelog posts.
    {% tumbleposts as post tumblelog_id=1 **kwargs %}
    {{ post.title }}
    {% endtumbleposts %}
    '''
    bits = token.contents.split()
    bits.reverse()
    bits = [bit.strip(',') for bit in bits]
    tag_name = bits.pop()
    as_name = bits.pop()
    var_name = bits.pop()
    order_by = None
    kwargs_list = [bit for bit in bits if '=' in bit]
    kwargs = {}

    #coerce kwargs to expected types
    for kwarg in kwargs_list:
        key, val = kwarg.split('=')
        if val in ['True', 'False']:
            val = bool(val)
        try:
            val = int(val)
        except ValueError:
            pass
        kwargs[key] = val

    # preflight kwargs before running any queries
    if not var_name or '=' in var_name or not kwargs.get('tumblelog_id'):
        raise template.TemplateSyntaxError("'%s' tag requires at a minimum a post variable name and tumblelog_id." % tag_name)
    if 'order_by' in kwargs:
        order_by = kwargs['order_by']
        del kwargs['order_by']
    if 'limit' in kwargs:
        limit = int(kwargs['limit'])
        del kwargs['limit']
    object_list = models.TumblelogPost.objects.filter(**kwargs)
    if order_by:
        object_list = object_list.order_by(order_by)
    if limit:
        object_list = object_list[:limit]

    # set up FilterExpression from object_list
    sequence = FilterExpression('', parser)
    sequence.filters = []
    sequence.var = object_list

    # gather node lists out of the template parser
    nodelist_loop = parser.parse(('empty', 'endtumbleposts'))
    token = parser.next_token()
    if token.contents == 'empty':
        nodelist_empty = parser.parse(('endtumbleposts',))
        parser.delete_first_token()
    else:
        nodelist_empty = None

    return ForNode([var_name], sequence, False, nodelist_loop, nodelist_empty)
