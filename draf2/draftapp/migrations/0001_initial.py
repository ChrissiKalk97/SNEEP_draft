# Generated by Django 4.1 on 2023-04-26 13:26

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Abcenhancersource',
            fields=[
                ('id', models.CharField(max_length=255)),
                ('enhancerid', models.CharField(db_column='enhancerId', max_length=255, primary_key=True, serialize=False)),
                ('celltype', models.CharField(max_length=255)),
                ('source', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'abcEnhancerSource',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Childtraits',
            fields=[
                ('id', models.CharField(max_length=255, primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'childTraits',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Enhancers',
            fields=[
                ('enhancerid', models.CharField(db_column='enhancerId', max_length=255, primary_key=True, serialize=False)),
                ('chr', models.CharField(max_length=10)),
                ('start', models.IntegerField()),
                ('end', models.IntegerField()),
                ('source', models.CharField(max_length=21)),
                ('targetgene', models.CharField(db_column='targetGene', max_length=255)),
            ],
            options={
                'db_table': 'enhancers',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Enhancersxsnps',
            fields=[
                ('id', models.CharField(max_length=255, primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'enhancersXsnps',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Enhancerxgene',
            fields=[
                ('id', models.CharField(max_length=255, primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'enhancerXgene',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Geneannotation',
            fields=[
                ('chr', models.CharField(max_length=10)),
                ('start', models.IntegerField()),
                ('end', models.IntegerField()),
                ('geneid', models.CharField(db_column='geneID', max_length=255, primary_key=True, serialize=False)),
                ('genesymbol', models.CharField(blank=True, db_column='geneSymbol', max_length=255, null=True)),
                ('alternativegeneid', models.CharField(blank=True, db_column='alternativeGeneID', max_length=255, null=True)),
                ('strand', models.CharField(max_length=1)),
            ],
            options={
                'db_table': 'geneAnnotation',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Genomeannotation',
            fields=[
                ('genomeversion', models.CharField(db_column='genomeVersion', max_length=4)),
                ('annotationversion', models.CharField(db_column='annotationVersion', max_length=3, primary_key=True, serialize=False)),
                ('databasename', models.CharField(db_column='databaseName', max_length=255)),
            ],
            options={
                'db_table': 'genomeAnnotation',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Gwas',
            fields=[
                ('id', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('numberleadsnps', models.IntegerField(blank=True, db_column='numberLeadSNPs', null=True)),
                ('numberproxysnps', models.IntegerField(blank=True, db_column='numberProxySNPs', null=True)),
                ('childrens', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'gwas',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Gwasinfo',
            fields=[
                ('efoid', models.CharField(db_column='efoId', max_length=255, primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('gwascatalogversion', models.CharField(db_column='gwasCatalogVersion', max_length=255)),
            ],
            options={
                'db_table': 'gwasInfo',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Snipaversion',
            fields=[
                ('annotationversion', models.CharField(db_column='annotationVersion', max_length=255, primary_key=True, serialize=False)),
                ('cohort', models.CharField(blank=True, max_length=255, null=True)),
                ('ldthreshold', models.FloatField(blank=True, db_column='LdThreshold', null=True)),
            ],
            options={
                'db_table': 'snipaVersion',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Snps',
            fields=[
                ('rsid', models.CharField(db_column='rsId', max_length=255, primary_key=True, serialize=False)),
                ('chr', models.CharField(max_length=10)),
                ('start', models.IntegerField()),
                ('end', models.IntegerField()),
                ('allele1', models.CharField(max_length=1)),
                ('allele2', models.CharField(max_length=1)),
                ('allele3', models.CharField(blank=True, max_length=1, null=True)),
                ('allele4', models.CharField(blank=True, max_length=1, null=True)),
            ],
            options={
                'db_table': 'snps',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Tfs',
            fields=[
                ('name', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('tfid', models.CharField(db_column='tfId', max_length=255)),
                ('tfexternaldatabase', models.CharField(blank=True, db_column='tfExternalDatabase', max_length=52, null=True)),
                ('species', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'tfs',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Tfsxsnps',
            fields=[
                ('id', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('diffbindpvalue', models.FloatField(db_column='diffBindPvalue')),
                ('adjustedpvalue', models.FloatField(db_column='adjustedPvalue')),
                ('posinmotif', models.CharField(db_column='posInMotif', max_length=255)),
                ('strand', models.CharField(max_length=10)),
                ('chr', models.CharField(max_length=10)),
                ('start', models.IntegerField()),
                ('end', models.IntegerField()),
                ('allele1', models.CharField(max_length=1)),
                ('allele2', models.CharField(max_length=1)),
                ('maf', models.FloatField()),
                ('isleadsnp', models.CharField(db_column='isLeadSNP', max_length=1)),
            ],
            options={
                'db_table': 'tfsXsnps',
                'managed': False,
            },
        ),
    ]
