from django.shortcuts import render_to_response
from backend.models import *
from django.db.models import Count
from random import randint
from string import zfill

def index(request):
	wid=1

	# If there is a score and an EID sent from post (i.e. the user voted
	# on something) we need to store this result before we give them another
	if 'pk' in request.POST and 'score' in request.POST:
		conf = Confirmation(measured_id=request.POST['pk'], user_id=1, score=request.POST['score'])
		conf.save()
	
	# Restrict the confirmations to 1 object at one wavelength for now
	meases = Measured.objects.filter(observation_id=10, wavelength_id=wid)

	# Find the subset of meas that have not been confirmed yet
	not_confd = meases.annotate(num_conf=Count('confirmation')).filter(num_conf=0)

	# Pick one of not_confd at random
	rmeas = not_confd[ randint(0, not_confd.count()-1) ]
	
	# This is an ugly cludge, x and y positions in the image filenames are zero 
	# padded numbers (eg. 003 instead of 3), since you can't pull the padding 
	# off in the template, pad the number here, and send it to the template
	xpad = zfill(str(rmeas.pos_x),2)
	ypad = zfill(str(rmeas.pos_y),2)

	# Another ugly cludge, it just so happens that the image file names have a "B" in them
	# if they are H-beta and a R in the if they are H-alpha (corresponding to the red and
	# blue parts of the spectra where they reside). H-alpha happens to correspond with
	# a wid=1 and H-beta -> wid=2.  So figure out which one we are on, and pass the letter.
	#
	# Sugested fix for all this uglyness: rename the images [oid]/[wid]/[x_pos]_[y_pos].jpg
	# Additionally, as a fallback in case the database indexes are messed up, a text index 
	# could be stored at the [oid] and [wid] level folders explicitly stating what the 
	# indexes refer to.  
	if wid==1:
		wLetter = 'R' 
	elif wid==2:
		wLetter = 'B'

	# Render the template, pass the context variables
	return render_to_response('classify/index.html', {'meas':rmeas, 'x':xpad, 'y':ypad, 'wL':wLetter})

