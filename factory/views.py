from django.shortcuts import render
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.shortcuts import render,redirect,get_object_or_404
from django.db.models.query import Q  
from .models import Factory,District
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
import folium
import folium.plugins

def index(request):
    factories = Factory.objects.all()[0:5]
    districts = District.objects.all()
    ongoing = Factory.objects.filter(condition='Green')
    completed = Factory.objects.filter(condition='Completed')
    failed = Factory.objects.filter(condition='Brown')
    total = len(ongoing)+len(completed)+len(failed)


    context = {
        'factories':factories,
        'districts':len(districts),
        'districts_left':len(ongoing),
        'brown':len(failed),
        'completed':len(completed),
    }
    return render(request,'factory/index.html',context)

def factories(request):
    factories = Factory.objects.all()
    paginator = Paginator(factories, 12)
    page_var = 'page'
    page = request.GET.get(page_var)
    
    try:
        paginated_queryset = paginator.page(page)
    except PageNotAnInteger:
        paginated_queryset = paginator.page(1)
    except EmptyPage:
        paginated_queryset = paginator.page(paginator.num_pages)

        print(factories)
    context = {
        'page_var':page_var,
        'factories':paginated_queryset,
        'count':len(factories),
        'count_of':len(paginated_queryset),
        
    }
    return render(request,'factory/listing.html',context)

def districts(request):
    districts_list = District.objects.all()
    paginator = Paginator(districts_list, 12)
    page_var = 'page'
    page = request.GET.get(page_var)
    
    try:
        paginated_queryset = paginator.page(page)
    except PageNotAnInteger:
        paginated_queryset = paginator.page(1)
    except EmptyPage:
        paginated_queryset = paginator.page(paginator.num_pages)

        print(factories)
    context = {
        'page_var':page_var,
        'districts':paginated_queryset,
        'count':len(districts_list),
        'count_of':len(paginated_queryset),
        
    }
    return render(request,'factory/districts.html',context)


def details(request, factory_id):
    factory = get_object_or_404(Factory, pk=factory_id)
    m = folium.Map(location=[factory.lat,factory.lon],tiles="Stamen Terrain",zoom_start=9)
    folium.plugins.Geocoder().add_to(m)
    cd = (factory.lat,factory.lon)
    folium.Marker(cd,icon=folium.Icon(color="green", icon="industry",prefix='fa')).add_to(m)

    context = {
        'factory':factory, 
        'map':m._repr_html_(),
        'domain':get_current_site(request),
    }
    return render(request,'factory/details.html',context)

def search(request):
    query = request.GET.get('q')
    queryset = ''
    if query:
        queryset = Factory.objects.filter(
        Q(name__icontains = query)|
        Q(product__icontains = query)|
        Q(raw_materials__icontains = query)|
        Q(category__icontains = query)|
        Q(about__icontains = query)).distinct()

    paginator = Paginator(queryset, 6)
    page_var = 'page'
    page = request.GET.get(page_var)

    try:
        paginated_queryset = paginator.page(page)
    except PageNotAnInteger:
        paginated_queryset = paginator.page(1)
    except EmptyPage:
        paginated_queryset = paginator.page(paginator.num_pages)

    context = {
        'page_var':page_var,
        'factories':paginated_queryset,
        'count':len(queryset),
        'count_of':len(paginated_queryset),
        'query':query,
    }
    return render(request,'factory/listing.html',context)

def filter(request, cat_filter):
    factories = Factory.objects.filter(
        Q(condition__icontains = cat_filter)|
        Q(category__icontains = cat_filter)).distinct()
    paginator = Paginator(factories, 12)
    page_var = 'page'
    page = request.GET.get(page_var)
    
    try:
        paginated_queryset = paginator.page(page)
    except PageNotAnInteger:
        paginated_queryset = paginator.page(1)
    except EmptyPage:
        paginated_queryset = paginator.page(paginator.num_pages)
    context = {
        'page_var':page_var,
        'factories':paginated_queryset,
        'count':len(factories),
        'count_of':len(paginated_queryset),
        'query':cat_filter,
    }
    return render(request,'factory/listing.html',context)
