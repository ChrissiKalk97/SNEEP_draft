from django.shortcuts import render
from django.views import generic
from .models import Interactionsxgenexsnps, Snps, Gwasinfo, Tfs, Tfsxsnps, Geneannotation, Gwasinfo
from django.http import Http404
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from draftapp.serializers import SnpsSerializer, GwasDictSerializer, GeneDictSerializer
import json
from .GWASQuery import *


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
    genes = Geneannotation.objects.all().values('genesymbol', 'geneid')
    return render(request, 'draftapp/gene_search.html', {"genes": genes})


def gene_query(query):
    no_hits = []#genes for which no coresponding snps etc are found
    hits = []#successfull genes
    genes = Geneannotation.objects.filter(Q(genesymbol__in = query) | Q(geneid__in = query)).values("genesymbol", "geneid")
    gene_dict= {}
    for gene in genes:
        snps = Snps.objects.filter(Interactions_gene_snps_rsid__geneid__genesymbol__exact = gene["genesymbol"]).distinct().values("rsid", "chr", "start", "end")
        if snps: 
            hits.append(gene["genesymbol"])
            snps_rsid = [rsnp["rsid"] for rsnp in snps]
            tfs = Tfsxsnps.objects.filter(Q(rsid__in = snps_rsid)).distinct().values("tfid", "rsid", "efoid")
            exs = Interactionsxgenexsnps.objects.filter(Q(rsid__in = snps_rsid)).distinct().values("enhancerid", "rsid")
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
            gene_info = gene["genesymbol"]+", "+gene["geneid"]
            gene_dict[gene_info] = list_per_gene
        else:
            no_hits.append(gene["genesymbol"]+" (" + gene["geneid"] + ")")  
    return gene_dict, hits, no_hits   
            
def gene_search_results_snps(request):
    if request.method == 'GET':
        query = request.GET.getlist('genes[]')
        if query:
            gene_dict, hits, no_hits = gene_query(query)
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
        snps = request.GET.getlist('snps[]')
        snps_objects = Snps.objects.filter(rsid__in = snps).distinct().values("rsid", "start", "chr", "end")
        snps_rsid = [rsnp["rsid"] for rsnp in snps_objects]
        tfsxsnps = Tfsxsnps.objects.filter(Q(rsid__in = snps_rsid)).distinct().values("id", "rsid", "tfid", "allele1", "allele2",\
                                                                                      "strand", "posinmotif", "diffbindpvalue", "adjustedpvalue")
        tfsxsnps_rsid = list(set([tfsxsnp["rsid"] for tfsxsnp in tfsxsnps]))
        no_hits = list(set([snp for snp in snps if snp not in tfsxsnps_rsid]))
        no_hits = ", ".join(no_hits)
        exs = Interactionsxgenexsnps.objects.filter(Q(rsid__in = snps_rsid)).distinct().values("enhancerid", "rsid", "geneid")
        geneids = list(set([ex["geneid"]for ex in exs]))
        genes = Geneannotation.objects.filter(geneid__in = geneids).values("geneid", "genesymbol")
        snp_query = {}
        for tfsxsnp in tfsxsnps:
            snp_position = [snp["chr"]+":"+str(snp["start"])+"-"+str(snp["end"]) for snp in snps_objects if snp["rsid"] == tfsxsnp["rsid"]]
            snp_position = snp_position[0]
            interactions = ", ".join([ex["enhancerid"]for ex in exs if ex["rsid"] == tfsxsnp["rsid"]])
            if not interactions:
                interactions = "Unknown"
            linked_genes = [ex["geneid"]for ex in exs if ex["rsid"] == tfsxsnp["rsid"]]
            if not linked_genes:
                linked_geneids = "Unknown"
                linked_genenames = "Unknown"
            else:
                linked_genenames = [gene["genesymbol"] for gene in genes if gene["geneid"] in linked_genes]
                linked_genenames = ", ".join(linked_genenames)
                linked_geneids = ", ".join(linked_genes)

            snp_query[tfsxsnp["id"]] = [tfsxsnp["rsid"], snp_position, tfsxsnp["tfid"], tfsxsnp["allele1"], tfsxsnp["allele2"],\
                                        tfsxsnp["strand"], tfsxsnp["posinmotif"], tfsxsnp["diffbindpvalue"], tfsxsnp["adjustedpvalue"],\
                                              interactions, linked_geneids, linked_genenames]
    return render(request, 'draftapp/snps_query_results.html', {"tfxsnps": snp_query, "no_hits":no_hits})

 
 

 


def make_snp_dict_helper_2(snps_unique, snp_dict, trans_fac, gwas):
    snps = [rsnp["rsid"] for rsnp in snps_unique]
    if trans_fac:
        tfs = Tfsxsnps.objects.filter(Q(tfid__name__in = trans_fac)& Q(rsid__rsid__in = snps)& Q(efoid__efoid__name__exact = gwas)).distinct().values("tfid", "rsid")
    else:
        tfs = Tfsxsnps.objects.filter(Q(rsid__rsid__in = snps)& Q(efoid__efoid__name__exact = gwas)).distinct().values("tfid", "rsid")
    exs = Interactionsxgenexsnps.objects.filter(rsid__rsid__in = snps).values("enhancerid", "rsid", "geneid")
    gene_ids_for_filter = [ex["geneid"] for ex in exs]
    gene_annos = Geneannotation.objects.filter(Q(geneid__in = gene_ids_for_filter )).values("geneid", "genesymbol")
    for snp in snps_unique:
        snp_dict[snp["rsid"]] = [snp["chr"]+":"+str(snp["start"])+"-"+str(snp["end"]),"", "", "", ""]
        snp_dict[snp["rsid"]][1] = ", ".join([tf["tfid"] for tf in tfs if tf["rsid"] == snp["rsid"]])
        geneids = [ex["geneid"] for ex in exs if ex["rsid"] == snp["rsid"]]
        genes = [gene_anno["genesymbol"] for gene_anno in gene_annos if gene_anno["geneid"] in geneids]
        snp_dict[snp["rsid"]][2] = ", ".join([geneid for geneid in geneids])
        snp_dict[snp["rsid"]][3] = ", ".join([genename for genename in genes])
        snp_dict[snp["rsid"]][4] = ", ".join([ex["enhancerid"] for ex in exs if ex["rsid"] == snp["rsid"]])
        
            
        
    for snp, info in snp_dict.items():
        if info[1] == "":
            snp_dict[snp][1] = "Unknown"
        if info[4] == "":
            snp_dict[snp][2]  = "Unknown"
            snp_dict[snp][3]  = "Unknown"
            snp_dict[snp][4]  = "Unknown"
    return snp_dict

def get_snp_dict(gwas, tf, chromosome):
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
    return snp_dict_complete

def gwas_search_results_dict_2(request):
    if request.method == 'GET':
        gwas = request.GET.getlist('gwas[]')
        tf =  request.GET.getlist('tf[]')
        chromosome = request.GET.getlist('chromosome[]')
        if gwas:
            snp_dict_complete = get_snp_dict(gwas, tf, chromosome)
            return render(request, 'draftapp/gwas_search_results_dict.html', {'snp_dict': snp_dict_complete})
        else:
            raise Http404("No GWAS given")
    else:
        raise Http404("No GWAS given")


def REST_API_view(request):
    return render(request, 'draftapp/REST_API_home.html', {})       
    
@csrf_exempt
def snps_detail(request, pk):
    """
    Retrieve tfsxsnps data in json format
    With url: draftapp/REST_API/snps/rsid
    """
    if "&" in pk:
            snps = pk.split("&")
            snp_instances = Snps.objects.filter(Q(rsid__in = snps))
            if request.method == 'GET':
                snp_list = list(snp_instances)
                serializer = SnpsSerializer(snp_list, many=True)
                return JsonResponse(serializer.data, safe = False)
            
    else:
        try:
            snp = Snps.objects.get(pk=pk)
        except Snps.DoesNotExist:
            return HttpResponse(status=404)

        if request.method == 'GET':
            serializer = SnpsSerializer(snp)
            return JsonResponse(serializer.data)
    
def GWASQueryRESTAPIview(request, pk):
    """
    Retrieve GWAS query resutls
    With url: draftapp/REST_API/GWASQuery/trait&trait2...
    trait can be trait name (with spaces etc..) or Efoid
    """
    if request.method == 'GET':
        if "&" in pk:
            gwas_traits = pk.split("&")
        else:
            gwas_traits = [pk]
        snp_dict_complete = get_snp_dict(gwas_traits, [], [])
        for gwas, gwas_values in snp_dict_complete.items():
            for rsid, snp_list in gwas_values.items():
               line = SnpLine(snp_list[0], snp_list[1], snp_list[2], snp_list[3], snp_list[4])
               snp_dict_complete[gwas][rsid] = line
            snp_dict_complete[gwas] = SnpDict(snp_dict_complete[gwas])
        Gwas_dict = GwasDict(snp_dict_complete)
        serializer = GwasDictSerializer(Gwas_dict)
        return JsonResponse(serializer.data, safe = False)
    else:
        raise Http404("No GWAS given")
    
def GeneQueryRESTAPIview(request, genes):
    if request.method == 'GET':
        if "&" in genes:
            gene_list = genes.split("&")
        else:
            gene_list = [genes]
        gene_dict, _, _ = gene_query(gene_list)
        for geneinfo, gene_values in gene_dict.items():
            for idx, line in enumerate(gene_values):
                gene_values[idx][5] = " ,".join(line[5])
                gene_values[idx] = GeneLine(gene_values[idx][0], gene_values[idx][1], gene_values[idx][2], gene_values[idx][3], gene_values[idx][4], gene_values[idx][5])
            gene_dict[geneinfo] = gene_values
        gene_dict = GeneDict(gene_dict)
        serializer = GeneDictSerializer(gene_dict)
        #genes_json = json.dumps(gene_dict)
        return JsonResponse(serializer.data, safe = False)
    else:
        raise Http404("No genes given")

    