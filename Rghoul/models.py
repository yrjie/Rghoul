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
    pid = models.IntegerField()
    name = models.CharField(max_length=255)
    booth = models.CharField(max_length=20)
    ingredient = models.IntegerField()
    energy = models.IntegerField()
    price = models.IntegerField()
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
	date = models.DateTimeField(auto_now_add=True)

	def __unicode__(self):
		return self.context

class Poll(models.Model):
    id = models.AutoField(primary_key=True)
    owner = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    open = models.BooleanField(default=False)
    parent = models.CharField(max_length=10) # parent page: the date
    code = models.CharField(max_length=10)
    result = models.CharField(max_length=4096)
    count = models.IntegerField()

    def __unicode__(self):
        return self.code
