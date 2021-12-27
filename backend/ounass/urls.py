"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.urls import path, include, re_path
from django.views import static
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions, routers
from api.views import CampaignViewSet, AddsetViewSet, AdCreativeViewSet, CampaignView, AddsetView, AdPreviewView, \
    AdSetInsightAPi, CreativePreviewApi
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

schema_view = get_schema_view(
    openapi.Info(
        title="Ounass API",
        default_version='v1',
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,)
)

router = routers.DefaultRouter()
router.register('campaigns', CampaignViewSet, basename='campaigns')
router.register('addsets', AddsetViewSet, basename='addsets')
router.register('adcreative', AdCreativeViewSet, basename='ad_creative')

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api-auth/', include('rest_framework.urls')),

    # Must be last in list.
    # Additionally, must be catch-all for pushState to work.

    re_path(r'^static/(?P<path>.*)$', static.serve, {'document_root': settings.STATIC_ROOT,
                                                     'show_indexes': settings.DEBUG}),
    re_path(r'^media/(?P<path>.*)$', static.serve, {'document_root': settings.MEDIA_ROOT,
                                                    'show_indexes': settings.DEBUG}),

    re_path(r'^api/v1/frontend/campaigns/$', CampaignView.as_view(), name='campaign_view'),
    re_path(r'^api/v1/frontend/adsets/$', AddsetView.as_view(), name='adsets_view'),
    re_path(r'^api/v1/frontend/adpreviews/$', AdPreviewView.as_view(), name='adpreview'), #<AD_CREATIVE_ID>
    re_path(r'^api/v1/insight/(?P<ad_set_id>.*)', AdSetInsightAPi.as_view(), name='ad_set_insight'),
    re_path(r'^api/v1/previews/(?P<creative_id>.*)', CreativePreviewApi.as_view(), name='creative_previews'),
    path('api/v1/', include(router.urls)),

]
