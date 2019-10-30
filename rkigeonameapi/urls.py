from django.urls import path, include
from django.conf.urls import url
#from rest_framework.urlpatterns import format_suffix_patterns
from .views import (
            FeaturecodeList,
            FeaturecodeDetail,
            CountryinfoList,
            CountryinfoDetail,
            GeonameList,
            GeonameDetail,
            GeonameChildrenUpdateDetail,
            ContinentList,
            ContinentDetail,
            RegionList,
            RegionDetail,
            RegionCountriesUpdateDetail,
            geoname_children_by_fcode,
            geoname_search,
            geoname_exhaustive_search,
        )

urlpatterns = [
    path('api/featurecode/', FeaturecodeList.as_view()),
    path('api/featurecode/<str:pk>', FeaturecodeDetail.as_view()),
    path('api/country/', CountryinfoList.as_view()),
    path('api/country/<str:pk>', CountryinfoDetail.as_view()),
    path('api/continent/', ContinentList.as_view()),
    path('api/continent/<str:pk>', ContinentDetail.as_view()),
    path('api/geoname/', GeonameList.as_view()),
    path('api/geoname/<int:pk>', GeonameDetail.as_view()),
    path('api/geonamechildren/<int:pk>', GeonameChildrenUpdateDetail.as_view()),
    path('api/region/', RegionList.as_view()),
    path('api/region/<str:pk>', RegionDetail.as_view()),
    path('api/regioncountries/<str:pk>', RegionCountriesUpdateDetail.as_view()),
    path('api/geonamefcodechildren/<str:pk>', geoname_children_by_fcode),
    path('api/geonamesearch/<str:searchstring>', geoname_search),
    path('api/geonameexhaustivesearch/<str:searchstring>', geoname_exhaustive_search),
]

#urlpatterns = format_suffix_patterns(urlpatterns)
