# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models



class Abcenhancersource(models.Model):
    id = models.CharField(max_length=255)
    enhancerid = models.CharField(db_column='enhancerId', primary_key=True, max_length=255)  # Field name made lowercase.
    celltype = models.CharField(max_length=255)
    source = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'abcEnhancerSource'


class Childtraits(models.Model):
    id = models.CharField(primary_key=True, max_length=255)
    efoid = models.ForeignKey('Gwasinfo', models.DO_NOTHING, db_column='efoId', related_name = 'Childtraits_efoId')  # Field name made lowercase.
    childtrait = models.ForeignKey('Gwasinfo', models.DO_NOTHING, db_column='childTrait', related_name = 'Childtraits_childTrait')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'childTraits'


class Geneannotation(models.Model):
    chr = models.CharField(max_length=10)
    start = models.IntegerField()
    end = models.IntegerField()
    geneid = models.CharField(db_column='geneID', primary_key=True, max_length=255)  # Field name made lowercase.
    genesymbol = models.CharField(db_column='geneSymbol', max_length=255, blank=True, null=True)  # Field name made lowercase.
    alternativegeneid = models.CharField(db_column='alternativeGeneID', max_length=255, blank=True, null=True)  # Field name made lowercase.
    strand = models.CharField(max_length=1)
    annotationversion = models.ForeignKey('Genomeannotation', models.DO_NOTHING, db_column='annotationVersion')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'geneAnnotation'


class Genomeannotation(models.Model):
    genomeversion = models.CharField(db_column='genomeVersion', max_length=4)  # Field name made lowercase.
    annotationversion = models.CharField(db_column='annotationVersion', primary_key=True, max_length=3)  # Field name made lowercase.
    databasename = models.CharField(db_column='databaseName', max_length=255)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'genomeAnnotation'


class Gwas(models.Model):
    id = models.CharField(primary_key=True, max_length=255)
    efoid = models.OneToOneField('Gwasinfo', models.DO_NOTHING, related_name = 'Gwas_efoId', db_column='efoId', unique=True)  # Field name made lowercase.
    numberleadsnps = models.IntegerField(db_column='numberLeadSNPs', blank=True, null=True)  # Field name made lowercase.
    numberproxysnps = models.IntegerField(db_column='numberProxySNPs', blank=True, null=True)  # Field name made lowercase.
    childrens = models.IntegerField(blank=True, null=True)
    snipaannotation = models.ForeignKey('Snipaversion', models.DO_NOTHING, db_column='snipaAnnotation')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'gwas'


class Gwasinfo(models.Model):
    efoid = models.CharField(db_column='efoId', primary_key=True, max_length=255)  # Field name made lowercase.
    name = models.CharField(max_length=255, blank=True, null=True)
    gwascatalogversion = models.CharField(db_column='gwasCatalogVersion', max_length=255)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'gwasInfo'


class Interactions(models.Model):
    enhancerid = models.CharField(db_column='enhancerId', primary_key=True, max_length=255)  # Field name made lowercase.
    chr = models.CharField(max_length=10)
    start = models.IntegerField()
    end = models.IntegerField()
    source = models.CharField(max_length=21)
    targetgene = models.ForeignKey('Geneannotation', models.DO_NOTHING, db_column='targetGene', max_length=255) # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'interactions'


class Interactionsxgenexsnps(models.Model):
    id = models.CharField(primary_key=True, max_length=255)
    enhancerid = models.ForeignKey(Interactions, models.DO_NOTHING, db_column='enhancerId')  # Field name made lowercase.
    geneid = models.ForeignKey(Geneannotation, models.DO_NOTHING, db_column='geneId')  # Field name made lowercase.
    rsid = models.ForeignKey('Snps', models.DO_NOTHING, db_column='rsId')  # Field name made lowercase.
    efoid = models.ForeignKey(Gwas, models.DO_NOTHING, db_column='efoId', related_name = "Interactions_gene_snps_efoids",to_field='efoid')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'interactionsXgeneXsnps'


class Snipaversion(models.Model):
    annotationversion = models.CharField(db_column='annotationVersion', primary_key=True, max_length=255)  # Field name made lowercase.
    cohort = models.CharField(max_length=255, blank=True, null=True)
    ldthreshold = models.FloatField(db_column='LdThreshold', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'snipaVersion'


class Snps(models.Model):
    rsid = models.CharField(db_column='rsId', primary_key=True, max_length=255)  # Field name made lowercase.
    chr = models.CharField(max_length=10)
    start = models.IntegerField()
    end = models.IntegerField()
    allele1 = models.CharField(max_length=1)
    allele2 = models.CharField(max_length=1)
    allele3 = models.CharField(max_length=1, blank=True, null=True)
    allele4 = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'snps'


class Tfs(models.Model):
    name = models.CharField(primary_key=True, max_length=255)
    tfid = models.CharField(db_column='tfId', max_length=255)  # Field name made lowercase.
    tfexternaldatabase = models.CharField(db_column='tfExternalDatabase', max_length=52, blank=True, null=True)  # Field name made lowercase.
    species = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'tfs'


class Tfsxsnps(models.Model):
    id = models.CharField(primary_key=True, max_length=255)
    tfid = models.ForeignKey(Tfs, models.DO_NOTHING, db_column='tfId', related_name = 'Tfsxsnps_tfId')  # Field name made lowercase.
    rsid = models.ForeignKey(Snps, models.DO_NOTHING, db_column='rsId', related_name = 'Tfsxsnps_rsId')  # Field name made lowercase.
    efoid = models.ForeignKey(Gwas, models.DO_NOTHING, db_column='efoId', related_name = 'Tfsxsnps_efoId', to_field='efoid')  # Field name made lowercase.
    diffbindpvalue = models.FloatField(db_column='diffBindPvalue')  # Field name made lowercase.
    adjustedpvalue = models.FloatField(db_column='adjustedPvalue')  # Field name made lowercase.
    posinmotif = models.CharField(db_column='posInMotif', max_length=255)  # Field name made lowercase.
    strand = models.CharField(max_length=10)
    chr = models.CharField(max_length=10)
    start = models.IntegerField()
    end = models.IntegerField()
    allele1 = models.CharField(max_length=1)
    allele2 = models.CharField(max_length=1)
    maf = models.FloatField()
    isleadsnp = models.CharField(db_column='isLeadSNP', max_length=1)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tfsXsnps'

        