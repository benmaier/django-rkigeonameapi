from rest_framework.renderers import BrowsableAPIRenderer

class BrowsableAPIRendererWithoutForms(BrowsableAPIRenderer):
    """Renders the browsable API, but excludes the forms."""
    def get_rendered_html_form(self, data, view, method, request):
        return None
