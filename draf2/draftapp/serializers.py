from rest_framework import serializers
from draftapp.models import Tfsxsnps, Snps
from .GWASQuery import *
from rest_framework_dataclasses.serializers import DataclassSerializer


class TfsxsnpsSerializer(serializers.ModelSerializer):
    #efoid = serializers.RelatedField(read_only=True)
    class Meta:
        model = Tfsxsnps
        fields = ["tfid", "rsid", "diffbindpvalue", "adjustedpvalue", "posinmotif", "strand", "chr", "start", "end", "allele1", "allele2", "maf", "isleadsnp"]

class SnpsSerializer(serializers.ModelSerializer):
    Tfsxsnps_rsId = TfsxsnpsSerializer(many = True, read_only = True)
    class Meta:
        model = Snps
        fields = ["rsid", "chr", "start", "end", "allele1", "allele2", "allele3", "allele4", "Tfsxsnps_rsId"]


"""class SnpLineSerializer(serializers.Serializer):
    snp_info = serializers.CharField()
    tfs = serializers.CharField()
    genenames = serializers.CharField()
    geneids = serializers.CharField()
    enhancers = serializers.CharField()

class SnpListSerializer(serializers.Serializer):
    #snp_info = SnpLineSerializer()
    rsid = serializers.ListField()

class SnpDictSerializer(serializers.Serializer):
    #snp_info = SnpListSerializer()
    rsid = serializers.DictField()

class GwasDictSerializer(serializers.Serializer):
    #snpDict = SnpDictSerializer()
    gwasInfo = serializers.DictField()"""

class SnpLineSerializer(DataclassSerializer):
    class Meta:
        dataclass = SnpLine

class SnpListSerializer(DataclassSerializer):
    class Meta:
        dataclass = SnpList

class SnpDictSerializer(DataclassSerializer):
    class Meta:
        dataclass = SnpDict

class GwasDictSerializer(DataclassSerializer):
    class Meta:
        dataclass = GwasDict