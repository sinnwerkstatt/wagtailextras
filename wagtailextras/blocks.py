from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from wagtail.wagtailcore.blocks import Block


class EmptyBlock(Block):
    """
    A block that does not take any input.
    Instead a placeholder can be rendered in the Wagtail admin interface.

    Simply define a Meta.placeholder-variable or override get_placeholder() for more complex logic.
    Beware: both will be marke_safe'd and therefore html will be escaped.
    """

    def render_form(self, value, prefix='', errors=None):
        return render_to_string('wagtailextras/empty_block.html', {
            'name': self.name,
            'classes': self.meta.classname,
            'placeholder': mark_safe(self.get_placeholder()),
        })

    def get_default(self):
        return ''

    def value_from_datadict(self, data, files, prefix):
        return ''

    def get_placeholder(self):
        if hasattr(self.meta, 'placeholder') and self.meta.placeholder:
            placeholder = self.meta.placeholder
        else:
            placeholder = self.name.title()
        return placeholder
