from django.contrib import admin
from .models import Product
import csv
from django.http import HttpResponse
from admin_numeric_filter.admin import NumericFilterModelAdmin, SliderNumericFilter
from django.utils.safestring import mark_safe


class CustomSliderNumericFilter(SliderNumericFilter):
    MAX_DECIMALS = 2
    STEP = 1

class ExportCsvMixin:
    def export_as_csv(self, request, queryset):

        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        writer = csv.writer(response, dialect='excel')

        writer.writerow(field_names)
        for obj in queryset:
            row = writer.writerow([getattr(obj, field) for field in field_names])

        return response

    export_as_csv.short_description = "Export Selected"


class ProductAdmin(NumericFilterModelAdmin, ExportCsvMixin):
    @mark_safe
    def product_image(self, obj,):
        return '<img src="%s" height="25"/>' % obj.image

    readonly_fields = ('product_image',)
    product_image.allow_tags = True
    search_fields = ('name', 'gtin12', 'brand', 'description', 'mpn')
    list_filter = (('price', CustomSliderNumericFilter), 'brand', 'color', 'manufacturer')
    list_display = ('name', 'brand', 'color', 'price', 'manufacturer', 'availability', 'product_image')
    actions = ["export_as_csv"]


admin.site.site_header = 'FeedThruster'
admin.site.register(Product, ProductAdmin)