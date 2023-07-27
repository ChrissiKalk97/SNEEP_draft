from django.shortcuts import render
from django.views import generic
from .models import Enhancers, Enhancersxsnps, Snps, Gwas, Gwasinfo, Tfs, Tfsxsnps, Geneannotation, Enhancerxgene, Gwasinfo
from django.http import Http404
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from draftapp.serializers import TfsxsnpsSerializer, SnpsSerializer

# Create your views here.
def IndexView(request):
    return render(request, 'draftapp/index.html')
    



def gwas_search_extended(request):
    gwases = Gwasinfo.objects.all()
    chrs = ["chr1", "chr2", "chr3", "chr4", "chr5", "chr6","chr7", "chr8", "chr9","chr10", "chr11", "chr12",\
            "chr13", "chr14", "chr15","chr16", "chr17", "chr18","chr19", "chr20", "chr21","chrX", "chrY"]
    tfs = Tfs.objects.all()
    return render(request, 'draftapp/gwas_search_extended.html', {"gwases": gwases, "chrs": chrs, "tfs": tfs})

        


def gene_search(request):
    genes = Geneannotation.objects.all().values('genesymbol')
    return render(request, 'draftapp/gene_search.html', {"genes": genes})
                
            
def gene_search_results_snps(request):
    if request.method == 'GET':
        query = request.GET.get('genes')
        query = query.split(",")
        if query:
            no_hits = []#genes for which no coresponding snps etc are found
            hits = []#successfull genes
            genes = Geneannotation.objects.filter(genesymbol__in = query)
            gene_dict= {}
            for gene in genes:
                snps = Snps.objects.filter(enhancersxsnpsrsid__enhancerid__targetgene__genesymbol__exact = gene.genesymbol).distinct().values("rsid", "chr", "start", "end")
                if snps: 
                    hits.append(gene.genesymbol)
                    snps_rsid = [rsnp["rsid"] for rsnp in snps]
                    tfs = Tfsxsnps.objects.filter(Q(rsid__in = snps_rsid)).distinct().values("tfid", "rsid", "efoid")
                    exs = Enhancersxsnps.objects.filter(Q(rsid__in = snps_rsid)).distinct().values("enhancerid", "rsid")
                    list_per_gene =  []
                    for  snp in snps:
                        tf_list = [tf["tfid"] for tf in tfs if tf["rsid"] == snp["rsid"]]
                        tf_string = ", ".join(tf_list)
                        gwas_list = [tf["efoid"] for tf in tfs if tf["rsid"] == snp["rsid"]]
                        gwases = Gwasinfo.objects.filter(Q(efoid__in = gwas_list)).distinct().values("name", "efoid")
                        gwas_name_list = [gwas["name"] for gwas in gwases]
                        efoid_list = [gwas["efoid"] for gwas in gwases]#I think this might be necessary to keep the order
                        gwas_string = ", ".join(gwas_name_list)
                        #efoid_string = ", ".join(efoid_list)
                        exs_list = [ex["enhancerid"] for ex in exs if ex["rsid"] == snp["rsid"]]
                        exs_string = ", ".join(exs_list)
                        list_per_gene.append([snp["rsid"], snp["chr"]+":"+str(snp["start"])+"-"+str(snp["end"]), tf_string, gwas_string,\
                                            exs_string, efoid_list])
                    gene_dict[gene] = list_per_gene
                else:
                    no_hits.append(gene.genesymbol)
            no_hits = ", ".join(no_hits)
            hits = ", ".join(hits)
            return render(request, 'draftapp/gene_search_results_snps.html', {'gene_dict': gene_dict, "no_hits": no_hits, "hits": hits})
        else:
                raise Http404("The given gene cannot be found")
    else:
        raise Http404("No gene given")

def snp_search(request):
    snps = Snps.objects.all()
    return render(request, 'draftapp/snp_search.html', {"snps": snps})

class SnpsDetailView(generic.DetailView):
    model = Snps
    template_name = 'draftapp/snps_detail.html' 

def snp_search_results(request):
    if request.method == 'GET':
        query = request.GET.get('rSNP')
        snp = Snps.objects.get(rsid__exact = query)
    return render(request, 'draftapp/snps_detail.html', {"object": snp})

 
 

 


def make_snp_dict_helper_2(snps_unique, snp_dict, trans_fac, gwas):
    snps = [rsnp["rsid"] for rsnp in snps_unique]
    if trans_fac:
        tfs = Tfsxsnps.objects.filter(Q(tfid__name__in = trans_fac)& Q(rsid__rsid__in = snps)& Q(efoid__efoid__name__exact = gwas)).distinct().values("tfid", "rsid")
    else:
        tfs = Tfsxsnps.objects.filter(Q(rsid__rsid__in = snps)& Q(efoid__efoid__name__exact = gwas)).distinct().values("tfid", "rsid")
    #genes = Geneannotation.objects.filter(Q(gene_enhancers__Enhancersxsnps_enhancerId__rsid__rsid__in = snps)).values("genesymbol", "geneid")
    exs = Enhancersxsnps.objects.filter(rsid__rsid__in = snps).values("enhancerid", "rsid")
    for snp in snps_unique:
        snp_dict[snp["rsid"]] = [snp["chr"]+":"+str(snp["start"])+"-"+str(snp["end"]),"", "", "", "", gwas]
        snp_dict[snp["rsid"]][1] = ", ".join([tf["tfid"] for tf in tfs if tf["rsid"] == snp["rsid"]])
        snp_dict[snp["rsid"]][4] = ", ".join([ex["enhancerid"] for ex in exs if ex["rsid"] == snp["rsid"]])
        #snp_dict[snp["rsid"]][2] = ", ".join([gene["genesymbol"] for gene in genes if gene["rsid"] == snp["rsid"]])
        #snp_dict[snp["rsid"]][3] = ", ".join([gene["geneid"] for gene in genes if gene["rsid"] == snp["rsid"]])
            
        
    for snp, info in snp_dict.items():
        if info[1] == "":
            snp_dict[snp][1] = "Unknown"
        if info[4] == "":
            snp_dict[snp][2] = "Unknown"
            snp_dict[snp][3] = "Unknown"
            snp_dict[snp][4] = "Unknown"
    return snp_dict

def gwas_search_results_dict_2(request):
     if request.method == 'GET':
        gwas = request.GET.getlist('gwas[]')
        tf =  request.GET.getlist('tf[]')
        chromosome = request.GET.getlist('chromosome[]')
        if gwas:
            gwas_info = Gwasinfo.objects.filter(Q(name__in = gwas) | Q(efoid__in = gwas)).distinct().values("name", "efoid")
            snp_dict_complete = {}
            for gwas_trait in gwas_info:
                snp_dict = {}
                if tf and chromosome:
                    snps_unique = Snps.objects.filter(Q(Tfsxsnps_rsId__efoid__efoid__name__exact = gwas_trait["name"]) & \
                                                        Q(Tfsxsnps_rsId__tfid__name__in = tf) & Q(chr__in = chromosome)).distinct()\
                                                         .values("rsid", "chr", "start", "end")
                    snp_dict = make_snp_dict_helper_2(snps_unique, snp_dict, tf, gwas_trait["name"])    
                elif chromosome:
                    snps_unique = Snps.objects.filter(Q(Tfsxsnps_rsId__efoid__efoid__name__exact = gwas_trait["name"]) & \
                                                        Q(chr__in = chromosome)).distinct()\
                                                         .values("rsid", "chr", "start", "end")
                    snp_dict = make_snp_dict_helper_2(snps_unique, snp_dict, tf, gwas_trait["name"])
                elif tf:
                    snps_unique = Snps.objects.filter(Q(Tfsxsnps_rsId__efoid__efoid__name__exact = gwas_trait["name"]) & \
                                                        Q(Tfsxsnps_rsId__tfid__name__in = tf)).distinct()\
                                                         .values("rsid", "chr", "start", "end")
                    
                    snp_dict = make_snp_dict_helper_2(snps_unique, snp_dict, tf, gwas_trait["name"])
                else:
                    snps_unique = Snps.objects.filter(Q(Tfsxsnps_rsId__efoid__efoid__name__exact = gwas_trait["name"])) \
                                                      .distinct().values("rsid", "chr", "start", "end")
                    snp_dict = make_snp_dict_helper_2(snps_unique, snp_dict, tf, gwas_trait["name"])
                gwas_key = gwas_trait["name"]+", "+gwas_trait["efoid"]
                snp_dict_complete[gwas_key] = snp_dict
            return render(request, 'draftapp/gwas_search_results_dict.html', {'snp_dict': snp_dict_complete})
        else:
                raise Http404("No GWAS given")
        
    
@csrf_exempt
def snps_detail(request, pk):
    """
    Retrieve tfsxsnps data in json format
    """
    try:
        snp = Snps.objects.get(pk=pk)
    except Snps.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = SnpsSerializer(snp)
        return JsonResponse(serializer.data)