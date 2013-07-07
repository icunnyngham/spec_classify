from django.shortcuts import render_to_response
from backend.models import *
from django.db.models import Max, Min
from browse.util import *

def index(request):
	obj_list = Observation.objects.all().values_list('obj_name', flat=True).distinct()
	return render_to_response('browse/index.html', {'object_list':obj_list})

def fmenu(request):
	file_list = Observation.objects.filter(obj_name= request.POST['obj'] ).values_list('filename', flat=True)
	return render_to_response('browse/fmenu.partial', {'file_list':file_list}) 

def obs_detail(request):
	obs = Observation.objects.get(filename= request.POST['file'] )
	w_list = obs.wavelengths.all().values("wid", "name")
	return render_to_response('browse/obs_detail.partial', {'obs':obs, 'w_list':w_list})

def wave_plot(request):
	oid = request.POST['obj_id']
	wid = request.POST['wave_id']
	m_type = request.POST['m_type']

	meas = Measured.objects.filter(observation_id=oid, wavelength_id=wid)
	extrema = meas.aggregate(Max('pos_x'), Max('pos_y'), val_max=Max(m_type), val_min=Min(m_type))
	vMin = extrema['val_min']
	vMax = extrema['val_max']
	
	grid = []
	for y in range(1, extrema['pos_y__max']+1):
		row = meas.filter(pos_y=y).order_by('pos_x').values('pos_x', 'pos_y', m_type) 
		for i in range(len(row)):
			row[i]['val'] = row[i][m_type]
			if row[i]['val'] is None or vMax is None or vMin is None:
				norm=0
			elif (vMax-vMin)==0:
				norm=0
			else:
				norm = ( (row[i]['val']-vMin)/(vMax-vMin)) 
			row[i]['val_color'] = colormap( norm )
		grid.append( row )
	
	if vMax is None or vMin is None or (vMax-vMin)==0:
		legend =[{'val': "NULL", 'color':"#000000"}]
	else:
		legend = [{'val': (vMax-vMin)*(x/10.0)+vMin, 'color':colormap(x/10.0)} for x in range(0, 11, 2)] 
	
	return render_to_response('browse/wave_plot.partial', {'grid':grid, 'extr': extrema, 'leg':legend})
