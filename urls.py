from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from RyansWebsite import settings
from . import views

urlpatterns = [
    path("admin/", admin.site.urls),
	path("/", views.index, name="index",),
	path("", views.index, name="index",),
	path("home/", views.index, name="index",),
	path("contact/", views.contact, name="contact",),
	path("about/", views.about, name="about",),
	path("products/", views.products_page, name="products_page",),
	path("products/collections/<str:collection_name>", views.collections, name="collections",),
	path("products/<str:product_name>/", views.individual_product_page, name="individual_product_page",),
	path("search=<str:product_query>/", views.product_search, name="product_search",),
	path("product_search/", views.product_search, name="product_search",),
]
urlpatterns += static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)