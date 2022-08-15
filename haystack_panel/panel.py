from django.conf import settings
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _
from debug_toolbar.panels import Panel
from haystack import connections


class HaystackDebugPanel(Panel):
    """
    Panel that displays queries made by Haystack backends.
    """
    name = 'Haystack'
    template = 'haystack_panel/haystack_panel.html'
    has_content = True

    def _get_query_count(self):
        return sum(map(lambda conn: len(conn.queries), connections.all()))

    def nav_title(self):
        return _('Haystack Queries')

    def nav_subtitle(self):
        return f"{self._get_query_count()} queries"

    def url(self):
        return ''

    def title(self):
        return self.nav_title()

    def generate_stats(self, request, response):
        query_list = [q for conn in connections.all() for q in conn.queries]
        if query_list:
            query_list.sort(key=lambda q: q['start'])
        self.record_stats(
            {
                'queries': query_list,
                'debug': getattr(settings, 'DEBUG', False),
            }
        )
