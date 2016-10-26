from django import forms
from django.db.models.fields import BLANK_CHOICE_DASH
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from wagtail.wagtailcore.blocks import Block, ChoiceBlock as WagtailChoiceBlock


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

class ChoiceBlock(WagtailChoiceBlock):
    """
    TODO: This exists until https://github.com/torchbox/wagtail/pull/2903 is pulled
    """
    def __init__(self, choices=None, required=True, help_text=None, include_blank=True, **kwargs):
        if choices is None:
            # no choices specified, so pick up the choice list defined at the class level
            choices = list(self.choices)
        else:
            choices = list(choices)

        # keep a copy of all kwargs (including our normalised choices list) for deconstruct()
        self._constructor_kwargs = kwargs.copy()
        self._constructor_kwargs['choices'] = choices
        if required is not True:
            self._constructor_kwargs['required'] = required
        if help_text is not None:
            self._constructor_kwargs['help_text'] = help_text

        # If choices does not already contain a blank option, insert one
        # (to match Django's own behaviour for modelfields:
        # https://github.com/django/django/blob/1.7.5/django/db/models/fields/__init__.py#L732-744)
        if include_blank:
            has_blank_choice = False
            for v1, v2 in choices:
                if isinstance(v2, (list, tuple)):
                    # this is a named group, and v2 is the value list
                    has_blank_choice = any([value in ('', None) for value, label in v2])
                    if has_blank_choice:
                        break
                else:
                    # this is an individual choice; v1 is the value
                    if v1 in ('', None):
                        has_blank_choice = True
                        break

            if not has_blank_choice:
                choices = BLANK_CHOICE_DASH + choices

        self.field = forms.ChoiceField(choices=choices, required=required, help_text=help_text)
        super(WagtailChoiceBlock, self).__init__(**kwargs)
