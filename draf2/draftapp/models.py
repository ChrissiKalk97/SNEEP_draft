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

"""
class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING, related_name = 'user')
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING, related_name = 'group')

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING, related_name = 'user')
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING, related_name = 'permission')

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)
"""

class Childtraits(models.Model):
    id = models.CharField(primary_key=True, max_length=255)
    efoid = models.ForeignKey('Gwasinfo', models.DO_NOTHING, db_column='efoId', related_name = 'Childtraits_efoId')  # Field name made lowercase.
    childtrait = models.ForeignKey('Gwasinfo', models.DO_NOTHING, db_column='childTrait', related_name = 'Childtraits_childTrait')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'childTraits'

"""
class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True, related_name = 'content_type')
    user = models.ForeignKey(AuthUser, models.DO_NOTHING, related_name = 'user')

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'
"""

class Enhancerxgene(models.Model):
    id = models.CharField(primary_key=True, max_length=255)
    enhancerid = models.ForeignKey('Enhancers', models.DO_NOTHING, db_column='enhancerId', related_name = 'Enhancerxgene_enhancerId')  # Field name made lowercase.
    geneid = models.ForeignKey('Geneannotation', models.DO_NOTHING, db_column='geneId', related_name = 'Enhancerxgene_geneId')  # Field name made lowercase.
    efoid = models.ForeignKey('Gwas', models.DO_NOTHING, db_column='efoId', to_field='efoid', related_name = 'Enhancerxgene_efoId')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'enhancerXgene'


class Enhancers(models.Model):
    enhancerid = models.CharField(db_column='enhancerId', primary_key=True, max_length=255)  # Field name made lowercase.
    chr = models.CharField(max_length=10)
    start = models.IntegerField()
    end = models.IntegerField()
    source = models.CharField(max_length=21)
    targetgene = models.ForeignKey('Geneannotation', models.DO_NOTHING, db_column='targetGene', max_length=255, related_name = 'gene_enhancers')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'enhancers'


class Enhancersxsnps(models.Model):
    id = models.CharField(primary_key=True, max_length=255)
    enhancerid = models.ForeignKey(Enhancers, models.DO_NOTHING, db_column='enhancerId', related_name = 'Enhancersxsnps_enhancerId')  # Field name made lowercase.
    rsid = models.ForeignKey('Snps', models.DO_NOTHING, db_column='rsId', related_name = 'enhancersxsnpsrsid')  # Field name made lowercase.
    efoid = models.ForeignKey('Gwas', models.DO_NOTHING, db_column='efoId', to_field='efoid', related_name = 'Enhancersxsnps_efoId')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'enhancersXsnps'


class Geneannotation(models.Model):
    chr = models.CharField(max_length=10)
    start = models.IntegerField()
    end = models.IntegerField()
    geneid = models.CharField(db_column='geneID', primary_key=True, max_length=255)  # Field name made lowercase.
    genesymbol = models.CharField(db_column='geneSymbol', max_length=255, blank=True, null=True)  # Field name made lowercase.
    alternativegeneid = models.CharField(db_column='alternativeGeneID', max_length=255, blank=True, null=True)  # Field name made lowercase.
    strand = models.CharField(max_length=1)
    annotationversion = models.ForeignKey('Genomeannotation',  models.DO_NOTHING, db_column='annotationVersion', related_name = 'Geneannotation_annotationVersion')  # Field name made lowercase.

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
    snipaannotation = models.ForeignKey('Snipaversion', models.DO_NOTHING, related_name = 'Gwas_snipaAnnotation', db_column='snipaAnnotation')  # Field name made lowercase.

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
    
    def __repr__(self):
        return '%d: %s' % (self.efoid, self.name)


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
    name = models.CharField(max_length=255, primary_key=True)
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
    efoid = models.ForeignKey(Gwas, models.DO_NOTHING, db_column='efoId', related_name = 'Tfsxsnps_efoId',to_field='efoid')  # Field name made lowercase.
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
        