from django.contrib import admin
from .models import Person, Position, Product
from datetime import datetime
from django.urls import path
from django.http import HttpResponse


class PositionAdmin(admin.ModelAdmin):
    list_filter = ["name"]


class PersonAdmin(admin.ModelAdmin):
    list_filter = ["position", "date_added"]
    readonly_fields = ["date_added"]
    list_display = ["name", "surname", "sex", "position_id", "owner"]
    search_fields = ('name','surname')


class ProductAdmin(admin.ModelAdmin):
    search_fields = ["product_text"]
    list_filter = ["publication_date"]
    list_display = ["product_text", "publication_date", "price"]
    fields = ('product_text', 'publication_date', 'price', 'image')

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('initial/<str:letter>/', self.admin_site.admin_view(self.products_by_initial_view),
                 name='products_by_initial_admin'),
            path('after/<str:date_str>/', self.admin_site.admin_view(self.products_published_after_view),
                 name='products_by_after_admin'),
            path('search/<str:substring>/', self.admin_site.admin_view(self.products_search_view),
                 name='products_search_admin'),
        ]
        return custom_urls + urls

    def products_by_initial_view(self, request, letter):
        products = Product.objects.filter(product_text__istartswith=letter)
        content = self._render_product_list(f"Products Starting with '{letter}'", products)
        return HttpResponse(content)

    def products_published_after_view(self, request, date_str):
        try:
            date = datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            return HttpResponse("<h1>Invalid date format. Use YYYY-MM-DD.</h1>")

        products = Product.objects.filter(publication_date__gt=date)
        content = self._render_product_list(f"Products Published After {date_str}", products)
        return HttpResponse(content)

    def products_search_view(self, request, substring):
        products = Product.objects.filter(product_text__icontains=substring)
        content = self._render_product_list(f"Products Containing '{substring}'", products)
        return HttpResponse(content)

    def _render_product_list(self, title, products):
        html = f"<h1>{title}</h1><ul>"
        for p in products:
            html += f"<li>{p.product_text} - {p.price} - {p.publication_date}</li>"
        html += "</ul>"
        html += '<p><a href="../">Back to Products</a></p>'
        return html


admin.site.register(Product, ProductAdmin)
admin.site.register(Person, PersonAdmin)
admin.site.register(Position, PositionAdmin)
