from django.shortcuts import render
from .forms import CsvModelForm
from .models import Csv, data_table
from numpy import interp
from colour import Color
from django.conf import settings
from django.templatetags.static import static

import csv
import branca.colormap as cm
import pandas as pd
import folium
import numpy as np
import pynmea2
import math

def home(request):
    return render(request,'plataforma/dashboard.html')

def cargar_csv(request):
    form = CsvModelForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        form = CsvModelForm()
        obj = Csv.objects.get(activated=False)
        with open(obj.file_name.path, 'r') as f:
            reader = csv.reader(f)

            for i, row in enumerate(reader):
                if i==0:
                    pass
                else:
                    
                    data_table.objects.create(
                        latitud = row[0],
                        longitud = row[1],
                        imsi = row[10],
                        date = row[4],
                        test_name = row[5],
                        pot_db = row[2],
                        operador = row[7],
                        user = row[3],
                        observacion = row[6],
                    )
                    #print(row)
                    #print(type(row))

    return render(request,'plataforma/subircsv.html', {'form':form})


def maps_app(request):

    data_display = data_table.objects.all().order_by('-id')
    rootcsv = "mapsV1.csv"
    rootcsv1 = "maps1V1.csv"
    rootxlxs = "mapsV1.xlsx"



    #mediFitro = tablaFilter(request.GET, queryset=data_display)
    datos = data_display
    

    with open(rootcsv, 'w') as crearcsv:
        writer = csv.writer(crearcsv)
        writer.writerow([
            'user',
            'latitud', 
            'longitud',
            'pot_db',
            'fecha',
            'imsi',
            'test_name',
     
            ])
        for dat in data_display.values_list(
            'user',
            'latitud',
            'longitud',
            'pot_db',
            'date',
            'imsi',
 

            
            ):

            writer.writerow(dat)

    
    newd_csv=pd.read_csv(rootcsv)
    newd_csv["pot_db"]=newd_csv['pot_db'].apply(lambda x: interp(x,[-120,-50],[0,29]))
    newd_csv.to_csv(rootcsv1, index=False)
    datos_csv=pd.read_csv(rootcsv1)
    datos_csv1=pd.read_csv(rootcsv)
    datos_csv1.to_excel(rootxlxs,index = None, header=True)
    if(datos_csv.empty):
        default_lat = -17.4140
        default_lon = -66.1653
    else:
        default_lat= datos_csv['latitud'].mean()
        default_lon= datos_csv['longitud'].mean()

    print(default_lat, default_lon)
  
    
    m = folium.Map(
            width='100%', 
            height='100%', 
            location=(default_lat, default_lon),
            tiles='OpenStreetMap',
            control_scale=True,
            min_zoom=10, 
            max_zoom=16,
            zoom_start=14,
            #scaleRadius= True,
            #scale_radius=True,
            
            
            )
    lat_lon=datos_csv[['latitud','longitud','pot_db']].values
    lat_lon1=datos_csv[['latitud','longitud','pot_db']].values
    
    
    colormap = cm.LinearColormap(colors=[ 'blue', 'cyan', 'yellow', 'orange', 'red'],
                             index=[-120, -110, -100, -95, -90], vmin=-120, vmax=-90,
                             caption='Gradiente de la señal en dBm 4G')

    m.add_child(colormap);  
    pp=0
    for i, r in datos_csv.iterrows():

        
        blue = Color("blue")
        colors = list(blue.range_to(Color("red"),30))
        cvalue = colors[round(float(r['pot_db']))]
        print(cvalue)
        
        pp += 1
        folium.Circle([r['latitud'],r['longitud']],
                        radius=100,
                        fill=True,
                        #color = 'grey',
                        fill_opacity = 0.2,
                        #fill_color = '#48c6dd',
                        fill_color = '%s' %cvalue,
                        stroke = False,
                        interactive = True,
                        bubblingMouseEvents = True,
                        tooltip = '%s' %pp,
                    ).add_to(m)                   

    m.save('map_V1.html')
    m = m._repr_html_()
    
    context = {
        #'filtro':mediFitro,
        'datos':datos,
        'map':m,
    }
    

    return render(request, 'plataforma/map_v1.html', context)