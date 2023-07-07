from django.shortcuts import render
from django.views import generic
from .models import Enhancers, Enhancersxsnps, Snps, Gwas, Gwasinfo, Tfs, Tfsxsnps, Geneannotation, Enhancerxgene, Gwasinfo
from django.http import Http404
from asgiref.sync import sync_to_async
import httpx
from django.db.models import Q, Prefetch

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
    genes = Geneannotation.objects.values('genesymbol')
    return render(request, 'draftapp/gene_search.html', {"genes": genes})
                
            
def gene_search_results_snps(request):
    #not so sure whether enhancerxgene is really the type of object to work with for this view...
    if request.method == 'GET':
        query = request.GET.getlist('genes[]')
        if query:
            genes = Geneannotation.objects.filter(genesymbol__in = query)
            gene_dict= {}
            for gene in genes:
               #exs = Enhancersxsnps.objects.filter(enhancerid__targetgene__genesymbol__icontains = gene.genesymbol)
                snps = Snps.objects.filter(enhancersxsnpsrsid__enhancerid__targetgene__genesymbol__icontains = gene.genesymbol)\
                .prefetch_related('Tfsxsnps_rsId').prefetch_related('enhancersxsnpsrsid')
               #snps = Snps.objects.filter(enhancersxsnpsrsid__enhancerid__targetgene__genesymbol__icontains = gene['genesymbol'])\
                #.prefetch_related('Tfsxsnps_rsId').prefetch_related('enhancersxsnpsrsid')
                if snps: 
                    gene_dict[gene] = snps
                    ## I dont know why this code takes so long, in theory it should be a query object
                    #filter does not invoke database access, only later
                    #maybe the dictionary I create makes this somehow...however snps should still only be a query object
                    #which only gets evaluated once I iterate over it
            return render(request, 'draftapp/gene_search_results_snps.html', {'gene_dict': gene_dict})
        else:
                raise Http404("The given gene cannot be found")
    else:
        raise Http404("No gene given")

def snp_search(request):
    snps = Snps.objects.all()
    return render(request, 'draftapp/snp_search.html', {"snps": snps})

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
        snp_dict[snp["rsid"]] = [snp["chr"]+":"+str(snp["start"])+"-"+str(snp["end"]),"", "", "", ""]
        for tf in tfs:
            if tf["rsid"] == snp["rsid"]:
                snp_dict[snp["rsid"]][1] += tf["tfid"]+", "
        #for gene in genes:
            #snp_dict[snp["rsid"]][2] += gene["genesymbol"]+", "
            #snp_dict[snp["rsid"]][3] += gene["geneid"]+", "
        for ex in exs:
            if ex["rsid"] == snp["rsid"]:
                snp_dict[snp["rsid"]][4] += ex["enhancerid"]+", "
    """for snp in snps_unique:
        if trans_fac:
            tfs = Tfsxsnps.objects.filter(Q(tfid__name__in = trans_fac)& Q(rsid__rsid__in = snp["rsid"])& Q(efoid__efoid__name__exact = gwas)).distinct().values("tfid")
        else:
            tfs = Tfsxsnps.objects.filter(Q(rsid__rsid__in = snp["rsid"])& Q(efoid__efoid__name__exact = gwas)).distinct().values("tfid")
    #genes = Geneannotation.objects.filter(Q(gene_enhancers__Enhancersxsnps_enhancerId__rsid__rsid__in = snps)).values("genesymbol", "geneid")
        exs = Enhancersxsnps.objects.filter(rsid__rsid__in = snp["rsid"]).values("enhancerid")
        snp_dict[snp["rsid"]] = [snp["chr"]+":"+str(snp["start"])+"-"+str(snp["end"]),"", "", "", ""]
        for tf in tfs:
            #if tf["rsid"] == snp["rsid"]:
            snp_dict[snp["rsid"]][1] += tf["tfid"]+", "
        #for gene in genes:
            #snp_dict[snp["rsid"]][2] += gene["genesymbol"]+", "
            #snp_dict[snp["rsid"]][3] += gene["geneid"]+", "
        for ex in exs:
            #if ex["rsid"] == snp["rsid"]:
            snp_dict[snp["rsid"]][4] += ex["enhancerid"]+", """
        
    for snp, info in snp_dict.items():
        if snp_dict[snp][1] != "":
            snp_dict[snp][1] = info[1][:-2]
        else:
            snp_dict[snp][1] = "Unknown"
        if snp_dict[snp][4] != "":
            snp_dict[snp][2] = info[2][:-2]
            snp_dict[snp][3] = info[3][:-2]
            snp_dict[snp][4] = info[4][:-2]
        else:
            snp_dict[snp][2] = "Unknown"
            snp_dict[snp][3] = "Unknown"
            snp_dict[snp][4] = "Unknown"
    return snp_dict

def gwas_search_results_dict_2(request):
     if request.method == 'GET':
        gwas = request.GET.get('gwas_trait')
        tf = []
        for transcription_factor in request.GET.getlist('tf[]'):
            tf.append(transcription_factor)
        chromosome = request.GET.getlist('chromosome[]')
        if gwas:
            gwas_info = Gwasinfo.objects.filter(name__exact = gwas)#this we could leave out, but then no test whether GWAS exists: 
            #also this step should not be critical for performance...
            if gwas_info:
                snp_dict = {}
                if tf and chromosome:#would this whole thing be quicker if I could filter  for snps directly?
                    snps_unique = Snps.objects.filter(Q(Tfsxsnps_rsId__efoid__efoid__name__exact = gwas) & \
                                                        Q(Tfsxsnps_rsId__tfid__name__in = tf) & Q(chr__in = chromosome)).distinct()\
                                                         .values()
                    snp_dict = make_snp_dict_helper_2(snps_unique, snp_dict, tf, gwas)    
                elif chromosome:
                    snps_unique = Snps.objects.filter(Q(Tfsxsnps_rsId__efoid__efoid__name__exact = gwas) & \
                                                        Q(chr__in = chromosome)).distinct()\
                                                         .only("rsid", "chr", "start", "end").values()
                    snp_dict = make_snp_dict_helper_2(snps_unique, snp_dict, tf, gwas)
                elif tf:
                    snps_unique = Snps.objects.filter(Q(Tfsxsnps_rsId__efoid__efoid__name__exact = gwas) & \
                                                        Q(Tfsxsnps_rsId__tfid__name__in = tf)).distinct()\
                                                         .only("rsid", "chr", "start", "end").values()
                    
                    snp_dict = make_snp_dict_helper_2(snps_unique, snp_dict, tf, gwas)
                else:
                    snps_unique = Snps.objects.filter(Q(Tfsxsnps_rsId__efoid__efoid__name__exact = gwas)) \
                                                      .distinct().only("rsid", "chr", "start", "end").values()
                    snp_dict = make_snp_dict_helper_2(snps_unique, snp_dict, tf, gwas)
                return render(request, 'draftapp/gwas_search_results_dict.html', {'snp_dict': snp_dict, 'gwas': gwas})
            else:
                raise Http404("The given GWAS trait cannot be found")
        else:
                raise Http404("No GWAS given")