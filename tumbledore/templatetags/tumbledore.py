from django import template
from django.utils.safestring import mark_safe

register = template.Library()


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
