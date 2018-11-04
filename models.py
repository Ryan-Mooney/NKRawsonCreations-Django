from django.db import models
from datetime import datetime

class products(models.Model):
	name=models.CharField(max_length=500, unique=True)
	picture_url=models.URLField(max_length=500)
	price=models.FloatField(default=0.00)
	description=models.CharField(max_length=5000)
	category=models.CharField(max_length=1000)
	date_added=models.DateTimeField(default=datetime.now, blank=True)
	paypal_button=models.CharField(max_length=5000)

	def __str__(self):
		return self.name
	def __unicode__(self):
		return self.name
