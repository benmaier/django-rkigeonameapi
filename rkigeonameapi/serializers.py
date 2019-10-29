from rest_framework import serializers

from .models import (
            Featurecode,
            Continent,
            Countryinfo,
            Geoname,
            Hierarchy,
            Alternatename,
            Region,
        )

class FeaturecodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Featurecode
        fields = ['code', 'name', 'description', 'searchorder_detail']

class NestedFeaturecodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Featurecode
        fields = ['code', 'name']

class NestedFeaturecodeMinimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Featurecode
        fields = ['code']

class ContinentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Continent
        fields = ['code','name','englishname','geoname']

class NestedCountryinfoSerializer(serializers.ModelSerializer):
    continent = ContinentSerializer()
    class Meta:
        model = Countryinfo
        fields = ['iso_alpha2', 'name', 'continent','population']

class CountryinfoSerializer(serializers.ModelSerializer):
    continent = ContinentSerializer()
    class Meta:
        model = Countryinfo
        exclude = []

class NestedAlternatenameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alternatename
        fields = ['alternatename','isolanguage','ispreferredname','isshortname','iscolloquial','ishistoric']
            
class NestedGeonameSerializer(serializers.ModelSerializer):
    fcode = NestedFeaturecodeSerializer()
    class Meta:
        model = Geoname
        fields = ['geonameid', 'name','fcode']

class GeonameChildrenUpdateSerializer(serializers.ModelSerializer):
    children_ids = serializers.PrimaryKeyRelatedField(many=True,read_only=False,queryset=Geoname.objects.all(),source='children')
    class Meta:
        model = Geoname
        fields = ['geonameid','children_ids']

class GeonameSerializer(serializers.ModelSerializer):
    country = NestedCountryinfoSerializer()
    children = NestedGeonameSerializer(many=True)
    alternatenames = NestedAlternatenameSerializer(many=True)
    class Meta:
        model = Geoname
        exclude = []

class GeonameSearchSerializer(serializers.ModelSerializer):
    country = NestedCountryinfoSerializer()
    fcode = NestedFeaturecodeSerializer()
    class Meta:
        model = Geoname
        fields = ['geonameid', 'name', 'englishname', 'country', 'fcode', 'population' ] 

class NestedGeonameMinimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Geoname
        fields = ['geonameid', 'name']

class GeonameMinimalSerializer(serializers.ModelSerializer):
    children = NestedGeonameMinimalSerializer(many=True)
    class Meta:
        model = Geoname
        fields = ['geonameid','name','children']

class RegionSerializer(serializers.ModelSerializer):
    laender = NestedCountryinfoSerializer(many=True)
    class Meta:
        model = Region
        exclude = []

class RegionCountriesUpdateSerializer(serializers.ModelSerializer):
    laender_ids = serializers.PrimaryKeyRelatedField(many=True,read_only=False,queryset=Countryinfo.objects.all(),source='laender')
    class Meta:
        model = Region
        fields = ['region_id', 'laender_ids']

