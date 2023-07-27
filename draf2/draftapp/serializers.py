from rest_framework import serializers
from draftapp.models import Tfsxsnps, Snps

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