from django.db import models
from django.contrib.auth.models import User

class Wavelength(models.Model):
	wid = models.AutoField(primary_key=True)
	center = models.DecimalField(max_digits=7,decimal_places=2)
	name = models.CharField(max_length=45)
	window = models.DecimalField(max_digits=5,decimal_places=2, null=True)
	has_images = models.BooleanField()

class Observation(models.Model):
	oid = models.AutoField(primary_key=True)
	filename = models.CharField(max_length=255)
	obj_name = models.CharField(max_length=255)
	redshift = models.DecimalField(max_digits=8,decimal_places=6)
	obs_date = models.DateField()
	ra = models.CharField(max_length=20)
	dec = models.CharField(max_length=20)
	exptime =  models.DecimalField(max_digits=6,decimal_places=1)
	airmass =  models.DecimalField(max_digits=5,decimal_places=3)
	sky_info = models.CharField(max_length=255)
	distance = models.DecimalField(max_digits=8,decimal_places=3)
	dist_std = models.DecimalField(max_digits=7,decimal_places=3, null=True)
	wavelengths = models.ManyToManyField(Wavelength)
	owned_by = models.ForeignKey(User)

class EmLine(models.Model):
	eid = models.AutoField(primary_key=True)
	observation = models.ForeignKey(Observation)
	wavelength = models.ForeignKey(Wavelength)
	pos_x = models.PositiveIntegerField()
	pos_y = models.PositiveIntegerField()

class Measured(EmLine):
	flux = models.FloatField(null=True)
	eqw = models.FloatField(null=True)
	fwhm = models.FloatField(null=True)

class Confirmation(models.Model):
	measured = models.ForeignKey(Measured)
	user = models.ForeignKey(User)
	score = models.IntegerField()

