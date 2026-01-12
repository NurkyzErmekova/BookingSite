from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from django.http import HttpResponse

schema_view = get_schema_view(
    openapi.Info(title="Hotel API", default_version='v1'),
    public=True,
    permission_classes=(permissions.AllowAny,),
)
urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
    path('accounts/', include('allauth.urls')),
]

urlpatterns += i18n_patterns(
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('accounts/profile/', lambda request: HttpResponse(
        f"<h1>Успешный вход!</h1><p>Привет, {request.user.username}</p><a href='/ru/'>На главную</a>")),
    path('', include('booking_app.urls')),
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)