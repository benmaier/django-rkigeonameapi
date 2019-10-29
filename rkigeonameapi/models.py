# -*- coding: utf-8 -*-

from django.db import models
from humanfriendly import format_size

def _size(val):
    s = format_size(val)
    s = s.rstrip("bytes")
    s = s.rstrip("B")
    s = s.replace(" ","")
    return s

class Featurecode(models.Model):
    code = models.CharField(max_length=7,primary_key=True)
    name = models.CharField(max_length=191, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    searchorder_detail = models.FloatField(blank=True, null=True)

    class Meta:
        db_table = 'featureCodes'
        verbose_name = 'Featurecode'
        verbose_name_plural = 'Featurecodes'

    def __str__(self):
        return "{}: {}".format(self.code, self.name)

class Continent(models.Model):

    code = models.CharField(max_length=2,primary_key=True)
    name = models.CharField(max_length=20,blank=True,null=True)
    englishname = models.CharField(max_length=20,blank=True,null=True)
    geoname = models.IntegerField(db_column='geonameid',blank=True,null=True)

    class Meta:
        db_table = 'continentCodes'
        verbose_name = 'Kontinent'
        verbose_name_plural = 'Kontinente'

    def __str__(self):
        return "{} ({})".format(self.name, self.code)

class Countryinfo(models.Model):
    iso_alpha2 = models.CharField(max_length=2, primary_key=True)
    iso_alpha3 = models.CharField(max_length=3, blank=True, null=True)
    iso_numeric = models.IntegerField(blank=True, null=True)
    fips_code = models.CharField(max_length=3, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    englishname = models.CharField(max_length=255, blank=True, null=True)
    capital = models.CharField(max_length=200, blank=True, null=True)
    areainsqkm = models.FloatField(blank=True, null=True)
    population = models.IntegerField(blank=True, null=True)
    continent = models.ForeignKey(Continent,models.DO_NOTHING,blank=True,null=True,db_column='continent')
    tld = models.CharField(max_length=3, blank=True, null=True)
    currency = models.CharField(max_length=3, blank=True, null=True)
    currencyname = models.CharField(db_column='currencyName', max_length=20, blank=True, null=True)  # Field name made lowercase.
    phone = models.CharField(db_column='Phone', max_length=10, blank=True, null=True)  # Field name made lowercase.
    postalcodeformat = models.CharField(db_column='postalCodeFormat', max_length=100, blank=True, null=True)  # Field name made lowercase.
    postalcoderegex = models.CharField(db_column='postalCodeRegex', max_length=255, blank=True, null=True)  # Field name made lowercase.
    geonameid = models.IntegerField(db_column='geonameId', blank=True, null=True)  # Field name made lowercase.
    languages = models.CharField(max_length=200, blank=True, null=True)
    neighbours = models.CharField(max_length=100, blank=True, null=True)
    equivalentfipscode = models.CharField(db_column='equivalentFipsCode', max_length=10, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        db_table = 'countryinfo'
        verbose_name = 'Land'
        verbose_name_plural = 'Länder'

    def __str__(self):
        return "{} ({})".format(self.name, self.iso_alpha2)


class Geoname(models.Model):
    geonameid = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    englishname = models.CharField(max_length=255, blank=True, null=True)
    asciiname = models.CharField(max_length=101, blank=True, null=True)
    latitude = models.DecimalField(max_digits=10, decimal_places=7, blank=True, null=True)
    longitude = models.DecimalField(max_digits=10, decimal_places=7, blank=True, null=True)
    fclass = models.CharField(max_length=1, blank=True, null=True)
    fcode = models.ForeignKey(Featurecode, models.DO_NOTHING, blank=True, null=True,db_column='fcode')
    country = models.ForeignKey(Countryinfo,models.DO_NOTHING, blank=True, null=True,db_column='country')
    cc2 = models.CharField(max_length=191, blank=True, null=True)
    admin1 = models.CharField(max_length=20, blank=True, null=True)
    admin2 = models.CharField(max_length=80, blank=True, null=True)
    admin3 = models.CharField(max_length=20, blank=True, null=True)
    admin4 = models.CharField(max_length=20, blank=True, null=True)
    population = models.IntegerField(blank=True, null=True)
    elevation = models.IntegerField(blank=True, null=True)
    gtopo30 = models.IntegerField(blank=True, null=True)
    timezone = models.CharField(max_length=40, blank=True, null=True)
    moddate = models.DateField(blank=True, null=True)

    children = models.ManyToManyField('Geoname',through='Hierarchy',blank=True)

    class Meta:
        db_table = 'geoname'
        verbose_name = 'Geoname'
        verbose_name_plural = 'Geonames'

    def __str__(self):
        if self.country is not None and not self.fcode.code.startswith('PCLI'):
            country = " in {} ({})".format(self.country.name, self.country.iso_alpha2)
        else:
            country = ""

        return '{}{}; {}: {}; Population: {}'.format(self.name, country, self.fcode.code, self.fcode.name, _size(self.population) )



class Hierarchy(models.Model):
    hierarchy_id = models.AutoField(primary_key=True)
    parent = models.ForeignKey(Geoname,models.CASCADE,related_name='parent_to',db_column='parentId')
    child = models.ForeignKey(Geoname,models.CASCADE,related_name='child_to',db_column='childId')
    is_custom_entry = models.BooleanField(blank=True,null=True,default=True,editable=False)

    class Meta:
        db_table = 'hierarchy'
        verbose_name = 'Hierarchie'
        verbose_name_plural = 'Hierarchien'
        unique_together = [ 'parent', 'child' ]

    def __str__(self):
        return "{} -> {}".format(self.parent.name, self.child.name)
        

class Alternatename(models.Model):
    alternatenameid = models.IntegerField(db_column='alternatenameId', primary_key=True)  # Field name made lowercase.
    geonameid = models.ForeignKey(Geoname,models.DO_NOTHING, blank=True, null=True,db_column='geonameid',related_name='alternatenames')
    isolanguage = models.CharField(db_column='isoLanguage', max_length=7, blank=True, null=True)  # Field name made lowercase.
    alternatename = models.CharField(db_column='alternateName', max_length=191, blank=True, null=True)  # Field name made lowercase.
    ispreferredname = models.IntegerField(db_column='isPreferredName', blank=True, null=True)  # Field name made lowercase.
    isshortname = models.IntegerField(db_column='isShortName', blank=True, null=True)  # Field name made lowercase.
    iscolloquial = models.IntegerField(db_column='isColloquial', blank=True, null=True)  # Field name made lowercase.
    ishistoric = models.IntegerField(db_column='isHistoric', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        db_table = 'alternatename'
        verbose_name = 'Alternativname'
        verbose_name_plural = 'Alternativnamen'

    def __str__(self):
        return self.alternatename + " (" + self.geonameid.name + ")"

class Region(models.Model):
    region_id = models.CharField(primary_key=True, max_length=255)
    name = models.CharField(max_length=200)
    englishname = models.CharField(max_length=200,blank=True,null=True)
    geonameid = models.ForeignKey(Geoname,models.CASCADE,blank=True,null=True,db_column='geonameid')
    fcode = models.ForeignKey(Featurecode,models.CASCADE,blank=True,null=True,db_column='fcode')

    laender = models.ManyToManyField(Countryinfo)

    class Meta:
        db_table = 'region'
        verbose_name = "Region"
        verbose_name_plural = "Regionen"

    def __str__(self):
        if self.fcode is not None:
            fcode = " ({})".format(self.fcode.code)
        else:
            fcode = ""
        return "{}{}".format(self.name, fcode)
