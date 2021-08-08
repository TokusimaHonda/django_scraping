from django.contrib import admin
from django.urls import path, include

from rakuten.views import top

urlpatterns = [
    path('', top, name='top'),
    path('rakuten/', include('rakuten.urls')),
    path('admin/', admin.site.urls),
]
