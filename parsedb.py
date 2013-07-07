#!/usr/bin/python

from django.core.management import setup_environ
from spec_classify import settings
from decimal import Decimal
from datetime import date

setup_environ(settings)

from backend.models import *

# Instantiate Wavelengths
# TODO: talk to Dr. Takamiya and maybe use http://www.pa.uky.edu/~peter/atomic/ to isolate 
# to find emission line names and exact centers
#
# Doing this the ugly looking way to make sure nothing stays in memory
w = Wavelength(center=6563, name="H-alpha (no sky sub)", window=250, has_images=True )
w.save()
w = Wavelength(center=4861, name="H-beta (no sky sub)", window=250, has_images=True )
w.save()
w = Wavelength(center=6548, name="6548", window=None, has_images=False )
w.save()
w = Wavelength(center=6563, name="H-alpha", window=None, has_images=False )
w.save()
w = Wavelength(center=6583, name="6583", window=None, has_images=False )
w.save()
w = Wavelength(center=6716, name="6716", window=None, has_images=False )
w.save()
w = Wavelength(center=6731, name="6731", window=None, has_images=False )
w.save()
w = Wavelength(center=3728, name="3728", window=None, has_images=False )
w.save()
w = Wavelength(center=4363, name="4363", window=None, has_images=False )
w.save()
w = Wavelength(center=4861, name="H-beta", window=None, has_images=False )
w.save()
w = Wavelength(center=4959, name="4959", window=None, has_images=False )
w.save()
w = Wavelength(center=5007, name="5007", window=None, has_images=False )
w.save()
w=False

obs = {}
with open("database_v9.dat", "r") as f:
    for l in f:
		# Split the textfile line by spaces
		ar = l.split()

		# Store the filename 
		fn = ar[2]

		# Account for specific cubes with overlapping names
		if fn=="TC10_128_063":
			if ar[12] == "1.615":
				fn="TC10_128_063_003"
			elif ar[12] == "1.530":
				fn="TC10_128_063_006"
		elif fn=="TC10_128_069":
			if ar[12] == "1.411":
				fn="TC10_128_069_003"
			elif ar[12] == "1.370":
				fn="TC10_128_069_006"
		elif fn=="TC10_128_058": 
			if ar[12] == "1.747":
				fn="TC10_128_058_003"
			elif ar[12] == "2.048":
				fn="TC10_128_058_006"
		
		# Add Observation if it isn't in the the already
		if fn not in obs:
			# Catch N/A values
			if ar[-1] == "N/A":
				d_std=None
			else:
				d_std=Decimal(ar[-1])
			
			o = Observation(filename=fn, obj_name=ar[1], redshift=Decimal(ar[3]), obs_date=date(int(ar[4]), int(ar[6]),int(ar[5])), ra=ar[7], dec=ar[8], exptime=Decimal(ar[11]), airmass=Decimal(ar[12]), sky_info=" ".join([ar[-6], ar[-5], ar[-4], ar[-3]]), distance=Decimal(ar[-2]), dist_std=d_std, owned_by_id=1 )
			
			# Commit the object to the db
			o.save()

			# Add all the wavelengths to this Observation
			for i in range(1,13):
				o.wavelengths.add( Wavelength.objects.get(pk=i) )
			
			# Keep track of observations without storing all the extra stuff
			obs[fn] = True

		#Convert all flux, eqw, and fwhm measurements from strings into floats or None
		for i in range(13, 47):
			if ar[i]=="INDEF":
				ar[i]=None
			else:
				ar[i]=float(ar[i])

		#Save all the emission line measurements
		# Do the two (non-sky-subtracted) H-alpha/ H-beta first
		m = Measured(observation=o, wavelength_id=1, pos_x=int(ar[9]), pos_y=int(ar[10]), flux=ar[13], eqw=None, fwhm=ar[14])
		m.save()
		m = Measured(observation=o, wavelength_id=2, pos_x=int(ar[9]), pos_y=int(ar[10]), flux=ar[15], eqw=None, fwhm=ar[16])
		m.save()

		# Then proceed through all the sky subtracted em line measurements
		for i in range(2, 12):
			m = Measured(observation=o, wavelength_id=i+1, pos_x=int(ar[9]), pos_y=int(ar[10]), flux=ar[i*3+11], eqw=ar[i*3+12], fwhm=ar[i*3+13])
			m.save()

