from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from debug_toolbar.toolbar import debug_toolbar_urls
from django.views.decorators.csrf import csrf_exempt
from graphene_django.views import GraphQLView

urlpatterns = [
    path("polls/", include("polls.urls")),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path("graphql", csrf_exempt(GraphQLView.as_view(graphiql=True)))

]

urlpatterns += [
    path('api-auth/', include('rest_framework.urls')),
]

if not settings.TESTING:
    urlpatterns = [
        *urlpatterns,
    ] + debug_toolbar_urls()
