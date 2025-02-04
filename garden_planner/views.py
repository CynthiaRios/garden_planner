from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import *
from .forms import * 

import pandas as pd
from datetime import datetime

def index(request): 
    context = {}
    context["upload_form"] = UploadCropFileForm()

    if request.method == "POST" and request.FILES: 
        upload_form = UploadCropFileForm(request.POST, request.FILES)
        upload_file = request.FILES["crop_file"]
        
        df = pd.read_excel(upload_file)

        for index, row in df.iterrows():
            crop = Crop()
            if not pd.isna(row['name']):
                if len(row['name']) > 2: 
                    crop.name = row['name']
                else: 
                    break
            if not pd.isna(row['variety']):
                crop.variety = row['variety']
            if not pd.isna(row['source']):
                crop.source = row['source']
            if not pd.isna(row['season']):
                crop.season = row['season']
            if not pd.isna(row['target_seed_start']):
                date = row['target_seed_start']
                target_seed_start = datetime.strptime(str(date), '%Y-%m-%d %H:%M:%S')
                print(target_seed_start)
                crop.target_seed_start = target_seed_start 
            if not pd.isna(row['target_transport_start']):
                date = row['target_transport_start']
                target_transport_start = datetime.strptime(str(date), '%Y-%m-%d %H:%M:%S')
                print(target_transport_start)
                crop.target_transport_start = target_transport_start 
            if not pd.isna(row['target_seed_start_outdoors']):
                date = row['target_seed_start_outdoors']
                target_seed_start_outdoors = datetime.strptime(str(date), '%Y-%m-%d %H:%M:%S')
                print(target_seed_start_outdoors)
                crop.target_seed_start_outdoors = target_seed_start_outdoors 
            if not pd.isna(row['planting_op']):
                crop.planting_op = row['planting_op']
            if not pd.isna(row['sunlight']):
                crop.sunlight = row['sunlight']
            if not pd.isna(row['instructions']):
                crop.instructions = row['instructions']
            if not pd.isna(row['square_footage_needed']):
                crop.square_footage_needed = row['square_footage_needed']
            if not pd.isna(row['qty_per_square_foot']):
                crop.qty_per_square_foot = row['qty_per_square_foot']
            crop.save()
            #print("COULD NOT ADD ROW: ", row)
    elif request.method =='POST':
        add_crop_q = request.POST.get('add_crop')
        add_plant_q = request.POST.get('add_plant')
    
        if add_crop_q: 
            name = request.POST.get('crop-name')
            variety = request.POST.get('crop-variety')

            source = request.POST.get('crop-source')
            target_seed_start = request.POST.get('crop-target_seed_start')
            target_transport_start = request.POST.get('crop-target_transport_start')
            target_transport_start = request.POST.get('crop-target_seed_start_outdoors')
            instruction = request.POST.get('crop-instruction')
            season = request.POST.get('crop-season')

            sunlight = request.POST.get('crop-sunlight')
            planting_op = request.POST.get('crop-planting_op')
            square_footage_needed = request.POST.get('crop-square_footage_needed')
            qty_per_square_foot = request.POST.get('crop-qty_per_square_foot')
        
            add_crop(name, variety, source, target_seed_start, target_transport_start, target_seed_start_outdoors, instruction, season, sunlight, planting_op, square_footage_needed, qty_per_square_foot)
        elif add_plant_q: 
            crop_id = request.POST.get('crop-id')
            qty = request.POST.get('plant-qty')

            date_planted = request.POST.get('plant-date_planted')
            if len(date_planted) == 0: 
                date_planted=None
            date_to_transplant = request.POST.get('plant-date_to_transplant')
            if len(date_to_transplant) == 0: 
                date_to_transplant=None
            date_to_harvest = request.POST.get('plant-date_to_harvest')
            if len(date_to_harvest) == 0: 
                date_to_harvest=None


            source = request.POST.get('plant-source')
            location = request.POST.get('plant-location')
            planting_op = request.POST.get('plant-planting_op')

            add_plant(crop_id, qty, date_planted, date_to_transplant, date_to_harvest, source, location, planting_op)

    context["crops"] = Crop.objects.all().order_by("name")
    context["plants"] = Plant.objects.all().order_by("crop")

    return render(request, "garden_planner/index.html", context)

def add_crop(name, variety=None, source=None, target_seed_start=None, target_transport_start=None, target_seed_start_outdoors=None, instruction=None, season=None, sunlight=None, planting_op=None, square_footage_needed=None, qty_per_square_foot=None): 
    crop = Crop()
    crop.name = name 
    crop.variety = variety 
    crop.source = source 
    crop.target_seed_start = target_seed_start
    crop.target_transport_start = target_transport_start
    crop.target_seed_start_outdoors = target_seed_start_outdoors
    crop.instructions = instruction
    crop.season = season
    crop.sunlight = sunlight
    crop.planting_op = planting_op
    crop.square_footage_needed = square_footage_needed
    crop.qty_per_square_foot = qty_per_square_foot
    crop.save()
    return

def update_crop(request, id): 
    context = {}
    crop = Crop.objects.get(id=id)
    context["crop"] = crop

    try: 
        context["target_seed_start"] = crop.target_seed_start.strftime("%Y-%m-%d")
    except: 
        context["target_seed_start"] = None
    try: 
        context["target_transport_start"] = crop.target_transport_start.strftime("%Y-%m-%d")
    except: 
        context["target_transport_start"] = None
    try: 
        context["target_seed_start_outdoors"] = crop.target_seed_start_outdoors.strftime("%Y-%m-%d")
    except: 
        context["target_seed_start_outdoors"] = None

    if request.method =='POST':
        name = request.POST.get('crop-name')
        variety = request.POST.get('crop-variety')

        source = request.POST.get('crop-source')
        target_seed_start = request.POST.get('crop-target_seed_start')
        target_transport_start = request.POST.get('crop-target_transport_start')
        target_seed_start_outdoors = request.POST.get('crop-target_seed_start_outdoors')
        
        instruction = request.POST.get('crop-instruction')
        season = request.POST.get('crop-season')

        sunlight = request.POST.get('crop-sunlight')
        planting_op = request.POST.get('crop-planting_op')
        square_footage_needed = request.POST.get('crop-square_footage_needed')
        qty_per_square_foot = request.POST.get('crop-qty_per_square_foot')

        crop.name = name 
        crop.variety = variety 
        crop.source = source 

        if not target_seed_start or len(target_seed_start) < 2: 
            target_seed_start = None
        if not target_transport_start or len(target_transport_start) < 2: 
            target_transport_start = None
        if not target_seed_start_outdoors or len(target_seed_start_outdoors) < 2: 
            target_seed_start_outdoors = None


        crop.target_seed_start = target_seed_start
        crop.target_transport_start = target_transport_start
        crop.target_seed_start_outdoors = target_seed_start_outdoors
        
        crop.instructions = instruction
        crop.season = season
        crop.sunlight = sunlight
        crop.planting_op = planting_op
        crop.square_footage_needed = square_footage_needed
        crop.qty_per_square_foot = qty_per_square_foot
        crop.save()
        return HttpResponseRedirect("/")
    return render(request, "garden_planner/update_crop.html", context)

def delete_crop(request, id): 
    crop = Crop.objects.filter(id=id)
    crop.delete()
    return HttpResponseRedirect("/")

def add_plant(crop_id, qty=None, date_planted=None, date_to_transplant=None, date_to_harvest=None, source=None, location=None, planting_op=None):
    crop = Crop.objects.get(id=crop_id)

    plant = Plant()
    plant.crop = crop 
    plant.qty = qty 
    plant.date_planted = date_planted 
    plant.date_to_transplant = date_to_transplant
    plant.date_to_harvest = date_to_harvest
    plant.source = source
    plant.location = location
    plant.planting_op = planting_op
    plant.save()

    return

def update_plant(request, id): 
    context = {}
    plant = Plant.objects.get(id=id)
    context["plant"] = plant
    context["crops"] = Crop.objects.all().order_by("name")

    try: 
        context["date_planted"] = plant.date_planted.strftime("%Y-%m-%d")
    except: 
        context["date_planted"] = None
    try: 
        context["date_to_transplant"] = plant.date_to_transplant.strftime("%Y-%m-%d")
    except: 
        context["date_to_transplant"] = None
    try: 
        context["date_to_harvest"] = plant.date_to_harvest.strftime("%Y-%m-%d")
    except: 
        context["date_to_harvest"] = None

    if request.method =='POST':
        crop_id = request.POST.get('crop-id')
        qty = request.POST.get('plant-qty')
        date_planted = request.POST.get('plant-date_planted')
        date_to_transplant = request.POST.get('plant-date_to_transplant')
        date_to_harvest = request.POST.get('plant-date_to_harvest')
        source = request.POST.get('plant-source')
        location = request.POST.get('plant-location')
        planting_op = request.POST.get('plant-planting_op')

        crop = Crop.objects.get(id=crop_id)
        plant.crop = crop 
        plant.qty = qty 
        plant.date_planted = date_planted 
        plant.date_to_transplant = date_to_transplant
        plant.date_to_harvest = date_to_harvest
        plant.source = source
        plant.location = location
        plant.planting_op = planting_op
        plant.save()
        return HttpResponseRedirect("/")
    return render(request, "garden_planner/update_plant.html", context)

def delete_plant(request, id): 
    plant = Plant.objects.filter(id=id)
    plant.delete()
    return HttpResponseRedirect("/")


# AJAX Function for json parsing
def get_crop(request):
    if request.method == 'GET':
        crop = str(request.GET['crop'])
        crop = Crop.objects.get(id=crop)

        print(crop)
        print(crop.id)
        try: 
            perf_js_data = request.session['perf_js_data'] 
            opPropPool = perf_js_data["opPropPool"]
            message = opPropPool[opid]
            ###print(message)
            ###print("===============================")
            locs = json.dumps(message)
            ###print(locs)
            return HttpResponse(locs)
        except: 
            return HttpResponse("Could not index for op") # Sending an success response
    else:
        return HttpResponse("Request method is not a GET")