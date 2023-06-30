from django.shortcuts import render
from django.views import generic
from .models import Enhancers, Enhancersxsnps, Snps, Gwas, Gwasinfo, Tfs, Tfsxsnps, Geneannotation, Enhancerxgene, Gwasinfo
from django.http import Http404
from asgiref.sync import sync_to_async
import httpx
from django.db.models import Q, Prefetch

# Create your views here.
class IndexView(generic.ListView):
    template_name = 'draftapp/index.html'
    #context_object_name = 'sneep'
    
    def get_queryset(self):
        queryset = {'enhancers': Enhancers.objects.all()[:10],
                   'enhancersxsnps': Enhancersxsnps.objects.all()[:10]}
        return queryset


class SnpsDetailView(generic.DetailView):
    model = Snps
    template_name = 'draftapp/snps_detail.html' 



def gwas_search(request):
    if request.method == 'GET':
        query = request.GET.get('gwas_trait')
        if query:
            gwas_info = Gwasinfo.objects.filter(name__icontains = query)
            if gwas_info:
                tfsxsnps = Tfsxsnps.objects.filter(efoid__efoid__name__icontains = query)
                enhnacerxsnps = Enhancersxsnps.objects.filter(efoid__efoid__name__icontains = query)
                return render(request, 'draftapp/gwas_search_results.html', {'tfsxsnps': tfsxsnps, 'enhnacerxsnps': enhnacerxsnps})
            else:
                raise Http404("The given GWAS trait cannot be found")
        else:
                raise Http404("No GWAS given")

def gwas_search_extended(request):
    gwases = Gwasinfo.objects.all()
    chrs = ["chr1", "chr2", "chr3", "chr4", "chr5", "chr6","chr7", "chr8", "chr9","chr10", "chr11", "chr12",\
            "chr13", "chr14", "chr15","chr16", "chr17", "chr18","chr19", "chr20", "chr21","chrX", "chrY"]
    tfs = Tfs.objects.all()
    return render(request, 'draftapp/gwas_search_extended.html', {"gwases": gwases, "chrs": chrs, "tfs": tfs})

        

def gwas_search_tfsxsnps_results(request):
     if request.method == 'GET':
        gwas = request.GET.get('gwas_trait')
        tf = request.GET.get('transcription_factor')
        chromosome = request.GET.get('chromosome')
        if gwas:
            gwas_info = Gwasinfo.objects.filter(name__icontains = gwas)#this we could leave out, but then no test whether GWAS exists: 
            #also this step should not be critical for performance...
            if gwas_info:
                if tf and chromosome:#would this whole thing be quicker if I could filter  for snps directly?
                    #enhnacerxsnps = Enhancersxsnps.objects.filter(Q(efoid__efoid__name__icontains = gwas) & Q(rsid__Tfsxsnps_rsId__tfid__name__icontains = tf) & Q(rsid__chr__icontains = chromosome))
                    tfsxsnps = Tfsxsnps.objects.filter(Q(efoid__efoid__name__icontains = gwas) & Q(tfid__name__icontains = tf) & Q(rsid__chr__icontains = chromosome))
                    snps_unique = Snps.objects.filter(Q(Tfsxsnps_rsId__efoid__efoid__name__icontains = gwas) & \
                    Q(Tfsxsnps_rsId__tfid__name__icontains = tf) & Q(chr__icontains = chromosome)).distinct().prefetch_related('Tfsxsnps_rsId').prefetch_related('enhancersxsnpsrsid')
                elif chromosome:
                    #enhnacerxsnps = Enhancersxsnps.objects.filter(Q(efoid__efoid__name__icontains = gwas) & Q(rsid__chr__icontains = chromosome)).select_related("rsid")
                    tfsxsnps = Tfsxsnps.objects.filter(Q(efoid__efoid__name__icontains = gwas) & Q(rsid__chr__icontains = chromosome)).select_related("rsid")
                    snps_unique = Snps.objects.filter(Q(Tfsxsnps_rsId__efoid__efoid__name__icontains = gwas) & \
                    Q(chr__icontains = chromosome)).distinct().prefetch_related('Tfsxsnps_rsId').prefetch_related('enhancersxsnpsrsid')
                elif tf:
                    #enhnacerxsnps = Enhancersxsnps.objects.filter(Q(efoid__efoid__name__icontains = gwas) & Q(rsid__Tfsxsnps_rsId__tfid__name__icontains = tf)).select_related("rsid")
                    tfsxsnps = Tfsxsnps.objects.filter(Q(efoid__efoid__name__icontains = gwas) & Q(tfid__name__icontains = tf)).select_related("rsid")
                    snps_unique = Snps.objects.filter(Q(Tfsxsnps_rsId__efoid__efoid__name__icontains = gwas) & \
                    Q(Tfsxsnps_rsId__tfid__name__icontains = tf)).distinct().prefetch_related('Tfsxsnps_rsId').prefetch_related('enhancersxsnpsrsid')
                else:
                    tfsxsnps = Tfsxsnps.objects.filter(efoid__efoid__name__icontains = gwas)
                    #enhnacerxsnps = Enhancersxsnps.objects.filter(efoid__efoid__name__icontains = gwas)
                    snps_unique = Snps.objects.filter(Q(Tfsxsnps_rsId__efoid__efoid__name__icontains = gwas)).distinct()\
                    .prefetch_related('Tfsxsnps_rsId').prefetch_related('enhancersxsnpsrsid')
                return render(request, 'draftapp/gwas_search_results_tfsxsnps.html', {'tfsxsnps': tfsxsnps, 'snps_unique': snps_unique, "gwas": gwas})#, "enhnacerxsnps": enhnacerxsnps
            else:
                raise Http404("The given GWAS trait cannot be found")
        else:
                raise Http404("No GWAS given")
        
def make_snp_dict_helper(tfsxsnps, snp_dict):
    for tfsxsnp in tfsxsnps:
        rsnp = tfsxsnp.rsid.rsid
        if rsnp in snp_dict.keys():
            snp_dict[rsnp][1] += tfsxsnp.tfid.name+", "
        else:
            snp_dict[rsnp] = [tfsxsnp.rsid.chr+":"+str(tfsxsnp.rsid.start)+"-"+str(tfsxsnp.rsid.end),\
                                      tfsxsnp.tfid.name+", ", "", "", ""]
            for exs in tfsxsnp.rsid.enhancersxsnpsrsid.all():
                if exs == tfsxsnp.rsid.enhancersxsnpsrsid.last():
                    snp_dict[rsnp][2] += exs.enhancerid.targetgene.geneid
                    snp_dict[rsnp][3] += exs.enhancerid.targetgene.genesymbol
                    snp_dict[rsnp][4] += exs.enhancerid.enhancerid
                else: 
                    snp_dict[rsnp][2] += exs.enhancerid.targetgene.geneid+", "
                    snp_dict[rsnp][3] += exs.enhancerid.targetgene.genesymbol+", "
                    snp_dict[rsnp][4] += exs.enhancerid.enhancerid+", "
    for snp, info in snp_dict.items():
        if snp_dict[snp][1] != "":
            snp_dict[snp][1] = info[0][:-2]
        else: 
            snp_dict[snp][1] = "Unknown"
        if snp_dict[snp][4] == "":
            snp_dict[snp][2] = "Unknown"
            snp_dict[snp][3] = "Unknown"
            snp_dict[snp][4] = "Unknown"
    return snp_dict

def gwas_search_results_dict(request):
     if request.method == 'GET':
        gwas = request.GET.get('gwas_trait')
        tf = request.GET.get('transcription_factor')
        chromosome = request.GET.get('chromosome')
        if gwas:
            gwas_info = Gwasinfo.objects.filter(name__icontains = gwas)#this we could leave out, but then no test whether GWAS exists: 
            #also this step should not be critical for performance...
            if gwas_info:
                snp_dict = {}
                if tf and chromosome:#would this whole thing be quicker if I could filter  for snps directly?
                    tfsxsnps = Tfsxsnps.objects.filter(Q(efoid__efoid__name__icontains = gwas) & Q(tfid__name__icontains = tf) \
                                                       & Q(rsid__chr__icontains = chromosome)).select_related("tfid")
                    snp_dict = make_snp_dict_helper(tfsxsnps, snp_dict)
                elif chromosome:
                    tfsxsnps = Tfsxsnps.objects.filter(Q(efoid__efoid__name__icontains = gwas)\
                                                        & Q(rsid__chr__icontains = chromosome)).select_related("tfid")
                    snp_dict = make_snp_dict_helper(tfsxsnps, snp_dict)
                elif tf:
                    tfsxsnps = Tfsxsnps.objects.filter(Q(efoid__efoid__name__icontains = gwas) &\
                                                        Q(tfid__name__icontains = tf)).select_related("tfid")
                    snp_dict = make_snp_dict_helper(tfsxsnps, snp_dict)
                else:
                    tfsxsnps = Tfsxsnps.objects.filter(efoid__efoid__name__icontains = gwas)
                    snp_dict = make_snp_dict_helper(tfsxsnps, snp_dict)
                return render(request, 'draftapp/gwas_search_results_dict.html', {'snp_dict': snp_dict, 'gwas': gwas})
            else:
                raise Http404("The given GWAS trait cannot be found")
        else:
                raise Http404("No GWAS given")

def gene_search(request):
    genes = Geneannotation.objects.all()
    return render(request, 'draftapp/gene_search.html', {"genes": genes})
                
            
def gene_search_results_snps(request):
    #not so sure whether enhancerxgene is really the type of object to work with for this view...
    if request.method == 'GET':
        #async with httpx.AsyncClient() as client:
            #query = await client.get('gene')

        query = request.GET.get('gene')
        if query:
            genes = Geneannotation.objects.filter(genesymbol__icontains = query)
            gene_dict= {}
            for gene in genes:
               #exs = Enhancersxsnps.objects.filter(enhancerid__targetgene__genesymbol__icontains = gene.genesymbol)
               snps = Snps.objects.filter(enhancersxsnpsrsid__enhancerid__targetgene__genesymbol__icontains = gene.genesymbol)#\
                #.prefetch_related('Tfsxsnps_rsId').prefetch_related('enhancersxsnpsrsid')
               #snps = Snps.objects.filter(enhancersxsnpsrsid__enhancerid__targetgene__genesymbol__icontains = gene['genesymbol'])\
                #.prefetch_related('Tfsxsnps_rsId').prefetch_related('enhancersxsnpsrsid')
               if snps: 
                    gene_dict[gene] = snps
                    # I dont know why this code takes so long, in theory it should be a query object
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
        snp = Snps.objects.get(rsid = query)
    return render(request, 'draftapp/snps_detail.html', {"object": snp})

 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 #.prefetch_related('Tfsxsnps_rsId').prefetch_related('enhancersxsnpsrsid')\
def gwas_search_test(request):
        if request.method == 'GET':
            gwas = request.GET.get('gwas_trait')
            tf = request.GET.get('transcription_factor')
            chromosome = request.GET.get('chromosome')
        if gwas:
            gwas_info = Gwasinfo.objects.filter(name__icontains = gwas)
            if gwas_info:
                if tf and chromosome:
                    #tfsxsnps = Tfsxsnps.objects.filter(Q(efoid__efoid__name__icontains = gwas) & Q(tfid__name__icontains = tf) & Q(rsid__chr__icontains = chromosome)).select_related("rsid").select_related("tfid")
                    snps_unique = Snps.objects.filter(Q(Tfsxsnps_rsId__efoid__efoid__name__icontains = gwas) & \
                                Q(Tfsxsnps_rsId__tfid__name__icontains = tf) & Q(chr__icontains = chromosome)).distinct()\
                                .only("rsid", "chr", "start", "end")\
                                .prefetch_related(Prefetch('Tfsxsnps_rsId', queryset = Tfsxsnps.objects.only("tfid__name"), to_attr = "tf"))\
                                .prefetch_related(Prefetch('enhancersxsnpsrsid', queryset = Enhancersxsnps.objects.only("enhancerid__targetgene__genesymbol", "enhancerid__enhancerid"), to_attr = "exs"))

                                                        
                elif chromosome:
                    #tfsxsnps = Tfsxsnps.objects.filter(Q(efoid__efoid__name__icontains = gwas) & Q(rsid__chr__icontains = chromosome)).select_related("rsid").select_related("tfid")
                    snps_unique = Snps.objects.filter(Q(Tfsxsnps_rsId__efoid__efoid__name__icontains = gwas) & \
                                                        Q(chr__icontains = chromosome)).distinct().only("rsid", "chr", "start", "end")\
                                                        .prefetch_related(Prefetch('Tfsxsnps_rsId', queryset = Tfsxsnps.objects.only("tfid__name"), to_attr = "tf"))\
                                .prefetch_related(Prefetch('enhancersxsnpsrsid', queryset = Enhancersxsnps.objects.only("enhancerid__targetgene__genesymbol", "enhancerid__enhancerid"), to_attr = "exs"))
                elif tf:
                    #tfsxsnps = Tfsxsnps.objects.filter(Q(efoid__efoid__name__icontains = gwas) & Q(tfid__name__icontains = tf)).select_related("rsid").select_related("tfid")
                    snps_unique = Snps.objects.filter(Q(Tfsxsnps_rsId__efoid__efoid__name__icontains = gwas) & \
                                                        Q(Tfsxsnps_rsId__tfid__name__icontains = tf)).distinct()\
                                                         .only("rsid", "chr", "start", "end")\
                                .prefetch_related(Prefetch('Tfsxsnps_rsId', queryset = Tfsxsnps.objects.only("tfid__name"), to_attr = "tf"))\
                                .prefetch_related(Prefetch('enhancersxsnpsrsid', queryset = Enhancersxsnps.objects.only("enhancerid__targetgene__genesymbol", "enhancerid__enhancerid"), to_attr = "exs"))

                else:
                    #tfsxsnps = Tfsxsnps.objects.filter(efoid__efoid__name__icontains = gwas).select_related("rsid").select_related("tfid")
                    snps_unique = Snps.objects.filter(Q(Tfsxsnps_rsId__efoid__efoid__name__icontains = gwas)).distinct()\
                                                       .only("rsid", "chr", "start", "end")\
                                .prefetch_related(Prefetch('Tfsxsnps_rsId', queryset = Tfsxsnps.objects.only("tfid__name"), to_attr = "tf"))\
                                .prefetch_related(Prefetch('enhancersxsnpsrsid', queryset = Enhancersxsnps.objects.only("enhancerid__targetgene__genesymbol", "enhancerid__enhancerid"), to_attr = "exs"))
                    
                return render(request, 'draftapp/gwas_search_results_test.html', {"snps_unique": snps_unique,"gwas": gwas})
            else:
                raise Http404("The given GWAS trait cannot be found")
        else:
                raise Http404("No GWAS given")
        





def make_snp_dict_helper_2(snps_unique, snp_dict, trans_fac, gwas):
    #if trans_fac:
        #tf_query = Tfs.objects.filter(Q(Tfsxsnps_tfId__efoid__efoid__name__icontains = gwas) & Q(name__in = trans_fac))
    #else:
        #tf_query = Tfs.objects.filter(Q(Tfsxsnps_tfId__efoid__efoid__name__icontains = gwas))
    for snp in snps_unique:
        if trans_fac:
            tfs = Tfs.objects.filter(Q(name__in = trans_fac)& Q(Tfsxsnps_tfId__rsid__rsid__exact = snp["rsid"])& Q(Tfsxsnps_tfId__efoid__efoid__name__exact = gwas)).distinct().values("name")
        else:
            tfs = Tfs.objects.filter(Q(Tfsxsnps_tfId__rsid__rsid__exact = snp["rsid"])& Q(Tfsxsnps_tfId__efoid__efoid__name__exact = gwas)).distinct().values("name")
        
        #tfs =  tf_query.filter(Q(Tfsxsnps_tfId__rsid__rsid__icontains = snp["rsid"])).distinct().values("name")
        #enhancers = Enhancers.objects.filter(Q(Enhancersxsnps_enhancerId__rsid__rsid__icontains = snp["rsid"])).values("enhancerid")
        genes = Geneannotation.objects.filter(Q(gene_enhancers__Enhancersxsnps_enhancerId__rsid__rsid__exact = snp["rsid"])).values("genesymbol", "geneid")
        exs = Enhancersxsnps.objects.filter(rsid__rsid__exact = snp["rsid"]).values("enhancerid")
        snp_dict[snp["rsid"]] = [snp["chr"]+":"+str(snp["start"])+"-"+str(snp["end"]),"", "", "", ""]
        for tf in tfs:
            snp_dict[snp["rsid"]][1] += tf["name"]+", "
        for gene in genes:
            snp_dict[snp["rsid"]][2] += gene["genesymbol"]+", "
            snp_dict[snp["rsid"]][3] += gene["geneid"]+", "
        #for en in enhancers:
            #snp_dict[snp["rsid"]][4] += en["enhancerid"]+", "
        for ex in exs:
            snp_dict[snp["rsid"]][4] += ex["enhancerid"]+", "
       
    for snp, info in snp_dict.items():
        if snp_dict[snp][1] != "":
            snp_dict[snp][1] = info[1][:-2]
        else: 
            snp_dict[snp][1] = "Unknown"
        if snp_dict[snp][2] != "":
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