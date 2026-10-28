from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView


urlpatterns = [
    path("", TemplateView.as_view(template_name="index.html"), name="home"),
    path("admin/", admin.site.urls),
    path("api/auth/", include("apps.accounts.urls")),
    path("api/patients/", include("apps.patients.urls")),
    path("api/doctors/", include("apps.doctors.urls")),
    path("api/mappings/", include("apps.mappings.urls")),
]
