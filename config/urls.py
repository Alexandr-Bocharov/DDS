from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("cash_flow.urls", namespace="cashflow")),
    path("api/", include("cash_flow.api_urls", namespace="cashflow_api"))
]
