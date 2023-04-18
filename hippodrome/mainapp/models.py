from django.db import models

# Create your models here.
class User(models.Model):

    class Meta:
        db_table = 'User'


class Rider(models.Model):
    class Meta:
        db_table = 'Rider'


class Owner(models.Model):
    class Meta:
        db_table = 'Owner'


class City(models.Model):
    class Meta:
        db_table = 'City'


class Role(models.Model):
    class Meta:
        db_table = 'Role'


class Position(models.Model):
    class Meta:
        db_table = 'Position'


class Horse(models.Model):
    class Meta:
        db_table = 'Horse'


class Participant(models.Model):
    class Meta:
        db_table = 'Participant'


class Ippodrom(models.Model):
    class Meta:
        db_table = 'Ippodrom'


class Race(models.Model):
    class Meta:
        db_table = 'Race'

