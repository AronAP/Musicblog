from django.contrib import admin
from django.conf.urls import include
from django.views.generic import RedirectView
from django.conf.urls import url
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    path('blog/', include('blog.urls')),
    url(r'^$', RedirectView.as_view(url='/blog/', permanent=True)),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

