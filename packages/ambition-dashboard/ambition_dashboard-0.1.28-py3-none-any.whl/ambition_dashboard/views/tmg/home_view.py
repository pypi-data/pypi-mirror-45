from django.conf import settings
from django.views.generic import TemplateView
from edc_dashboard.view_mixins import EdcViewMixin
from edc_navbar import NavbarViewMixin


class HomeView(EdcViewMixin, NavbarViewMixin, TemplateView):

    template_name = (
        f"ambition_dashboard/bootstrap{settings.EDC_BOOTSTRAP}/tmg/home.html"
    )
    navbar_name = "ambition_dashboard"
    navbar_selected_item = "tmg_home"
