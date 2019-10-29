from django.shortcuts import render
from rest_framework import generics
from rest_framework.decorators import api_view
#from rest_framework.response import Response
from django.http import JsonResponse

from django.db.models import Q

from .models import (
            Featurecode,
            Continent,
            Countryinfo,
            Geoname,
            Hierarchy,
            Alternatename,
            Region,
        )

from .serializers import (
            FeaturecodeSerializer,
            CountryinfoSerializer,
            ContinentSerializer,
            GeonameSerializer,
            GeonameMinimalSerializer,
            GeonameSearchSerializer,
            GeonameChildrenUpdateSerializer,
            RegionSerializer,
            RegionCountriesUpdateSerializer,

        )

# Create your views here.

class FeaturecodeList(generics.ListCreateAPIView):
    queryset = Featurecode.objects.all()
    serializer_class = FeaturecodeSerializer

class FeaturecodeDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Featurecode.objects.all()
    serializer_class = FeaturecodeSerializer

class CountryinfoList(generics.ListCreateAPIView):
    queryset = Countryinfo.objects.all()
    serializer_class = CountryinfoSerializer

class CountryinfoDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Countryinfo.objects.all()
    serializer_class = CountryinfoSerializer

class ContinentList(generics.ListCreateAPIView):
    queryset = Continent.objects.all()
    serializer_class = ContinentSerializer

class ContinentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Continent.objects.all()
    serializer_class = ContinentSerializer

class GeonameList(generics.ListCreateAPIView):
    queryset = Geoname.objects.all()
    serializer_class = GeonameSerializer

class GeonameDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Geoname.objects.all()
    serializer_class = GeonameSerializer

class GeonameChildrenUpdateDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Geoname.objects.all()
    serializer_class = GeonameChildrenUpdateSerializer

class RegionList(generics.ListCreateAPIView):
    queryset = Region.objects.all()
    serializer_class = RegionSerializer

class RegionDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Region.objects.all()
    serializer_class = RegionSerializer

class RegionCountriesUpdateDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Region.objects.all()
    serializer_class = RegionCountriesUpdateSerializer

@api_view(['GET'])
def geoname_children_by_fcode(request, pk):
    """
    List all children of a geoname filtered by a list of featurecodes
    """
    if request.query_params.get('fcode'):
        fcodes = [ s.upper() for s in request.query_params.get('fcode').split(',')]
    else:
        fcodes = []

    if request.method == 'GET':
        geoname = Geoname.objects.get(geonameid=pk)
        if len(fcodes) > 0:
            geoname = geoname.children.filter(fcode__code__in=fcodes)
        serializer = GeonameMinimalSerializer(geoname)
        return JsonResponse(serializer.data, safe=False)

@api_view(['GET'])
def geoname_exhaustive_search(request, searchstring):
    """
    List all children of a geoname filtered by a list of featurecodes
    """

    if request.query_params.get('fcode'):
        fcodes = [ s.upper() for s in request.query_params.get('fcode').split(',')]
    else:
        fcodes = []

    limit = request.query_params.get('limit') or 50

    if request.method == 'GET':
        geonames = Geoname.objects \
                          .filter(
                                    Q(englishname__startswith=searchstring) | 
                                    Q(alternatenames__alternatename__startswith=searchstring,
                                      alternatenames__iscolloquial=0
                                     )
                                 ) \
                          .order_by('-population','-fcode__searchorder_detail').distinct()
        if len(fcodes) > 0:
            geonames = geonames.filter(fcode__code__in=fcodes)

        if limit:
            geonames = geonames[:limit]
        serializer = GeonameSearchSerializer(geonames,many=True)
        return JsonResponse(serializer.data, safe=False)

@api_view(['GET'])
def geoname_search(request, searchstring):
    """
    List all children of a geoname filtered by a list of featurecodes
    """

    if request.query_params.get('fcode'):
        fcodes = [ s.upper() for s in request.query_params.get('fcode').split(',')]
    else:
        fcodes = []

    limit = request.query_params.get('limit') or 50

    if request.method == 'GET':
        geonames = Geoname.objects \
                          .filter(
                                    Q(englishname__icontains=searchstring) | 
                                    Q(name__icontains=searchstring)
                                 ) \
                          .order_by('-population','-fcode__searchorder_detail').distinct()
        if len(fcodes) > 0:
            geonames = geonames.filter(fcode__code__in=fcodes)

        if limit:
            geonames = geonames[:limit]
        serializer = GeonameSearchSerializer(geonames,many=True)
        return JsonResponse(serializer.data, safe=False)

