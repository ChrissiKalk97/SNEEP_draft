"""draf2 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path, re_path
from . import views


app_name = "draftapp"
urlpatterns = [
    #/draftapp/
    path('', views.IndexView, name = 'index'),  #app homepage
    path('Gwas_search_extended/', views.gwas_search_extended, name = 'gwas_search_extended'),
    path('Gwas_search_extended/Gwas_result/', views.gwas_search_results_dict_2, name = 'Gwas_search_results_dict'),
    path('Snp_search/', views.snp_search, name = 'snp_search'),
    path('Snp_search/<pk>/', views.SnpsDetailView.as_view(), name = 'snp_detail'),
    path('Snp_search_results/', views.snp_search_results, name = 'snp_search_results'),
    path('Gene_search/', views.gene_search, name = 'gene_search'),
    path('Gene_search/Gene_result/', views.gene_search_results_snps, name = 'gene_search_results'),
    path('REST_API/', views.REST_API_view),
    path('REST_API/snps/<pk>/', views.snps_detail),
 ]

