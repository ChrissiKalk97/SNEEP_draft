from django.shortcuts import render
from django.views import generic
from .models import Enhancers, Enhancersxsnps, Snps, Gwas, Gwasinfo, Tfs, Tfsxsnps, Geneannotation, Enhancerxgene
from django.db.models import Q 
from django.http import Http404
from itertools import chain



def gene_search_results(request):
    #not so sure whether enhancerxgene is really the type of object to work with for this view...
    if request.method == 'GET':
        query = request.GET.get('gene')
        if query:
            genes = Geneannotation.objects.filter(genesymbol__icontains = query)
            gene_dict= {}
            for gene in genes:
                exs = Enhancersxsnps.objects.select_related("rsid").select_related("efoid__efoid").\
            select_related("enhancerid").filter(enhancerid__targetgene__genesymbol__icontains = gene.genesymbol)
                #this needs to be exploited more, can lead to speeding up
                if exs: 
                    gene_dict[gene] = exs

            return render(request, 'draftapp/gene_search_results.html',{'gene_dict': gene_dict})
        else:
                raise Http404("The given gene cannot be found")
    else:
        raise Http404("No gene given")
                
            
