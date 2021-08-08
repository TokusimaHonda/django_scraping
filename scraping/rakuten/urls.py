from django.urls import path

from rakuten import views

urlpatterns = [
    path("new/", views.rakuten_new, name="rakuten_new"),
    path("<int:rakuten_id>/", views.rakuten_detail, name="rakuten_detail"),
    path("<int:rakuten_id>/edit/", views.rakuten_edit, name="rakuten_edit"),
]

