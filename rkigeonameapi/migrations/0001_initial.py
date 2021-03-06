# Generated by Django 2.2.6 on 2019-11-11 12:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Continent',
            fields=[
                ('code', models.CharField(max_length=2, primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=20, null=True)),
                ('englishname', models.CharField(blank=True, max_length=20, null=True)),
                ('geoname', models.IntegerField(blank=True, db_column='geonameid', null=True)),
            ],
            options={
                'verbose_name': 'Kontinent',
                'verbose_name_plural': 'Kontinente',
                'db_table': 'continentCodes',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Countryinfo',
            fields=[
                ('iso_alpha2', models.CharField(max_length=2, primary_key=True, serialize=False)),
                ('iso_alpha3', models.CharField(blank=True, max_length=3, null=True)),
                ('iso_numeric', models.IntegerField(blank=True, null=True)),
                ('fips_code', models.CharField(blank=True, max_length=3, null=True)),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('englishname', models.CharField(blank=True, max_length=255, null=True)),
                ('capital', models.CharField(blank=True, max_length=200, null=True)),
                ('areainsqkm', models.FloatField(blank=True, null=True)),
                ('population', models.IntegerField(blank=True, null=True)),
                ('tld', models.CharField(blank=True, max_length=3, null=True)),
                ('currency', models.CharField(blank=True, max_length=3, null=True)),
                ('currencyname', models.CharField(blank=True, db_column='currencyName', max_length=20, null=True)),
                ('phone', models.CharField(blank=True, db_column='Phone', max_length=10, null=True)),
                ('postalcodeformat', models.CharField(blank=True, db_column='postalCodeFormat', max_length=100, null=True)),
                ('postalcoderegex', models.CharField(blank=True, db_column='postalCodeRegex', max_length=255, null=True)),
                ('geonameid', models.IntegerField(blank=True, db_column='geonameId', null=True)),
                ('languages', models.CharField(blank=True, max_length=200, null=True)),
                ('neighbours', models.CharField(blank=True, max_length=100, null=True)),
                ('equivalentfipscode', models.CharField(blank=True, db_column='equivalentFipsCode', max_length=10, null=True)),
                ('continent', models.ForeignKey(blank=True, db_column='continent', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='rkigeonameapi.Continent')),
            ],
            options={
                'verbose_name': 'Land',
                'verbose_name_plural': 'Länder',
                'db_table': 'countryinfo',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Featurecode',
            fields=[
                ('code', models.CharField(max_length=7, primary_key=True, serialize=False, verbose_name='Featurecode')),
                ('name', models.CharField(blank=True, max_length=191, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('searchorder_detail', models.FloatField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'Featurecode',
                'verbose_name_plural': 'Featurecodes',
                'db_table': 'featureCodes',
                'ordering': ['-searchorder_detail', 'code'],
            },
        ),
        migrations.CreateModel(
            name='Geoname',
            fields=[
                ('geonameid', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('englishname', models.CharField(blank=True, max_length=255, null=True)),
                ('asciiname', models.CharField(blank=True, max_length=101, null=True)),
                ('latitude', models.DecimalField(blank=True, decimal_places=7, max_digits=10, null=True)),
                ('longitude', models.DecimalField(blank=True, decimal_places=7, max_digits=10, null=True)),
                ('fclass', models.CharField(blank=True, max_length=1, null=True)),
                ('cc2', models.CharField(blank=True, max_length=191, null=True)),
                ('admin1', models.CharField(blank=True, max_length=20, null=True)),
                ('admin2', models.CharField(blank=True, max_length=80, null=True)),
                ('admin3', models.CharField(blank=True, max_length=20, null=True)),
                ('admin4', models.CharField(blank=True, max_length=20, null=True)),
                ('population', models.IntegerField(blank=True, null=True)),
                ('elevation', models.IntegerField(blank=True, null=True)),
                ('gtopo30', models.IntegerField(blank=True, null=True)),
                ('timezone', models.CharField(blank=True, max_length=40, null=True)),
                ('moddate', models.DateField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'Geoname',
                'verbose_name_plural': 'Geonames',
                'db_table': 'geoname',
                'ordering': ['-population', 'name'],
            },
        ),
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('region_id', models.CharField(max_length=255, unique=True, verbose_name='Region-ID')),
                ('name', models.CharField(max_length=200)),
                ('englishname', models.CharField(blank=True, max_length=200, null=True)),
                ('fcode', models.ForeignKey(blank=True, db_column='fcode', null=True, on_delete=django.db.models.deletion.CASCADE, to='rkigeonameapi.Featurecode', verbose_name='Featurecode')),
                ('geonameid', models.ForeignKey(blank=True, db_column='geonameid', null=True, on_delete=django.db.models.deletion.CASCADE, to='rkigeonameapi.Geoname', verbose_name='Geoname-Objekt')),
                ('laender', models.ManyToManyField(to='rkigeonameapi.Countryinfo', verbose_name='Beinhaltete Länder')),
            ],
            options={
                'verbose_name': 'Region',
                'verbose_name_plural': 'Regionen',
                'db_table': 'region',
                'ordering': ['-geonameid__population', 'name'],
            },
        ),
        migrations.CreateModel(
            name='Hierarchy',
            fields=[
                ('hierarchy_id', models.AutoField(primary_key=True, serialize=False)),
                ('is_custom_entry', models.BooleanField(blank=True, default=True, editable=False, null=True, verbose_name='Is custom entry?')),
                ('child', models.ForeignKey(db_column='childId', on_delete=django.db.models.deletion.CASCADE, related_name='child_to', to='rkigeonameapi.Geoname')),
                ('parent', models.ForeignKey(db_column='parentId', on_delete=django.db.models.deletion.CASCADE, related_name='parent_to', to='rkigeonameapi.Geoname')),
            ],
            options={
                'verbose_name': 'Hierarchie',
                'verbose_name_plural': 'Hierarchien',
                'db_table': 'hierarchy',
                'ordering': ['parent__geonameid'],
                'unique_together': {('parent', 'child')},
            },
        ),
        migrations.AddField(
            model_name='geoname',
            name='children',
            field=models.ManyToManyField(blank=True, through='rkigeonameapi.Hierarchy', to='rkigeonameapi.Geoname'),
        ),
        migrations.AddField(
            model_name='geoname',
            name='country',
            field=models.ForeignKey(blank=True, db_column='country', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='rkigeonameapi.Countryinfo'),
        ),
        migrations.AddField(
            model_name='geoname',
            name='fcode',
            field=models.ForeignKey(blank=True, db_column='fcode', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='rkigeonameapi.Featurecode'),
        ),
        migrations.CreateModel(
            name='Alternatename',
            fields=[
                ('alternatenameid', models.IntegerField(db_column='alternatenameId', primary_key=True, serialize=False)),
                ('isolanguage', models.CharField(blank=True, db_column='isoLanguage', max_length=7, null=True)),
                ('alternatename', models.CharField(blank=True, db_column='alternateName', max_length=191, null=True)),
                ('ispreferredname', models.IntegerField(blank=True, db_column='isPreferredName', null=True)),
                ('isshortname', models.IntegerField(blank=True, db_column='isShortName', null=True)),
                ('iscolloquial', models.IntegerField(blank=True, db_column='isColloquial', null=True)),
                ('ishistoric', models.IntegerField(blank=True, db_column='isHistoric', null=True)),
                ('geonameid', models.ForeignKey(blank=True, db_column='geonameid', null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='alternatenames', to='rkigeonameapi.Geoname')),
            ],
            options={
                'verbose_name': 'Alternativname',
                'verbose_name_plural': 'Alternativnamen',
                'db_table': 'alternatename',
                'ordering': ['alternatenameid'],
            },
        ),
    ]
