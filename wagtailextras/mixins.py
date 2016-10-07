from django.db import ProgrammingError


class UniquePageMixin(object):
    """
    Mixin for Wagtail pages to ensure that only one instance of this Page type exists.
    """

    @classmethod
    def clean_parent_page_models(cls):
        # Only allow a single instance.
        try:
            if cls.objects and cls.objects.exists():
                return []
        except ProgrammingError:  # not migrated yet.
            pass
        return super(UniquePageMixin, cls).clean_parent_page_models()
