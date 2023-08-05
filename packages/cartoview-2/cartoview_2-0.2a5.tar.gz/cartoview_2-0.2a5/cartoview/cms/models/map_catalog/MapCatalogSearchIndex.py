from django import forms
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db import models
from wagtail.admin.edit_handlers import FieldPanel, TabbedInterface, ObjectList
from wagtail.core.models import Page
from django.db.models import Q
from cartoview.maps.models import Map


class MapCatalogSearchIndex(Page):
    parent_page_types = ['MapCatalogPage']
    selected_template = models.CharField(max_length=255, choices=(
        ('cms/map_catalog/map_catalog_search_index_default.html', 'Default Template'),
    ), default='cms/map_catalog/map_catalog_search_index_default.html')

    @property
    def template(self):
        return self.selected_template

    def get_context(self, request):
        q = request.GET.get('q', None)
        if q:
            maps = Map.objects.filter(Q(title__icontains=q) | Q(description__icontains=q) | Q(abstract__icontains=q))
        else:
            maps = []

        # Update template context
        context = super().get_context(request)
        paginator = Paginator(maps, 6)  # Show 6 resources per page
        page = request.GET.get('page')
        try:
            maps = paginator.page(page)
        except PageNotAnInteger:
            maps = paginator.page(1)  # If page is not an integer, deliver first page.
        except EmptyPage:
            maps = paginator.page(
                paginator.num_pages)  # If page is out of range (e.g. 9999), deliver last page of results.
        context['maps'] = maps
        return context

    content_panels = [
        FieldPanel('title', classname="full title"),
    ]

    theme_panels = [
        FieldPanel('selected_template', widget=forms.Select),
    ]

    edit_handler = TabbedInterface([
        ObjectList(content_panels, heading='Content'),
        ObjectList(theme_panels, heading='Theme'),
        ObjectList(Page.promote_panels, heading='Promote'),
        ObjectList(Page.settings_panels, heading='Settings', classname="settings"),
    ])

    class Meta:
        verbose_name = "Map Search"

    @classmethod
    def can_create_at(cls, parent):
        # You can only create one of these!
        return super(MapCatalogSearchIndex, cls).can_create_at(parent) \
               and parent.get_children().type(MapCatalogSearchIndex).count() == 0
