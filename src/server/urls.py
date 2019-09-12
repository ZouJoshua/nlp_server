"""web URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from django.conf.urls import include
import os



def get_server_path(server_name):
    if server_name == "news_parser":
        return path('nlp_parser/', include('{}.urls'.format(server_name), namespace=server_name))
    elif server_name == "news_regional":
        return path('nlp_regional/', include('{}.urls'.format(server_name), namespace=server_name))
    elif server_name == "news_category":
        return path('nlp_category/', include('{}.urls'.format(server_name), namespace=server_name))
    elif server_name == 'news_taste':
        return path('nlp_category/', include('{}.urls'.format(server_name), namespace=server_name))
    elif server_name == "video_category":
        return path('nlp_category/', include('{}.urls'.format(server_name), namespace=server_name))
    elif server_name == "video_browser_category":
        return path('nlp_category/', include('{}.urls'.format(server_name), namespace=server_name))
    elif server_name == "video_classification":
        return path('nlp_category/', include('{}.urls'.format(server_name), namespace=server_name))
    elif server_name == 'video_tags':
        return path('polls/', include('{}.urls'.format(server_name), namespace=server_name))
    else:
        raise Exception("服务不存在，请检查服务是否正确, 如正确，请添加服务路由")


SERVER_NAME = os.environ.get("NLP_SERVER_NAME")
server_url_path = get_server_path(SERVER_NAME)


urlpatterns = [
    path('admin/', admin.site.urls),
    server_url_path
]