'''
Created on 2015-08-29

@author: ruijie.yang
'''
from django.db import models
from math import floor

class Picture(models.Model):
    id = models.AutoField(primary_key=True)
    picName = models.CharField(max_length=255)
    date = models.DateField(auto_now_add=True)
    mealTime = models.CharField(max_length=2) # L: Lunch, or D: Dinner
    floor = models.IntegerField()
    like = models.IntegerField()
    dislike = models.IntegerField()

    def __unicode__(self):
        return self.picName

class Dish(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    booth = models.CharField(max_length=20)
    ingredient = models.IntegerField()
    pirce = models.IntegerField()
    date = models.DateField(auto_now_add=True)
    mealTime = models.CharField(max_length=2) # L: Lunch, or D: Dinner
    floor = models.IntegerField()
    like = models.IntegerField()
    dislike = models.IntegerField()

    def __unicode__(self):
        return self.name

class Comment(models.Model):
	id = models.AutoField(primary_key=True)
	author = models.CharField(max_length=255)
	context = models.CharField(max_length=2047)
	parent = models.CharField(max_length=10) # parent page: the date
	date = models.DateField(auto_now_add=True)

	def __unicode__(self):
		return self.context
