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

# class Comment(models.Model):