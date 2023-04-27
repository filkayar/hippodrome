from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    city = models.ForeignKey('City', on_delete=models.RESTRICT, verbose_name='Город', blank=True)
    middle_name = models.CharField(max_length=255, verbose_name='Отчество', blank=True)
    phone = models.CharField(max_length=20, verbose_name='Телефон', blank=True)
    birth = models.DateField(verbose_name='Дата рождения', blank=False)
    s_passport = models.IntegerField(blank=False, verbose_name='Серия паспорта')
    n_passport = models.IntegerField(blank=False, verbose_name='Номер паспорта')
    d_passport = models.DateField(blank=False, verbose_name='Дата выдачи паспорта')
    w_passport = models.CharField(max_length=500, blank=False, verbose_name='Кем выдан паспорт')
    photo = models.ImageField(verbose_name='Фото',upload_to='photos/user/%Y/%m/%d/')
    def __str__(self):
        return self.user.last_name + ' ' + self.user.first_name + ' ' + self.middle_name
    class Meta:
        verbose_name = 'Профиль пользователя'
        verbose_name_plural = 'Профили пользователей'
        db_table = 'Profile'


class Jockey(models.Model):
    user = models.ForeignKey('Profile', on_delete=models.CASCADE, verbose_name='Пользователь')
    category = models.CharField(verbose_name='Категория', max_length=255, blank=False)
    def __str__(self):
        return self.user.__str__()
    def get_absolute_url(self):
        return reverse('jockey_id', args=[str(self.id)])
    class Meta:
        verbose_name = 'Наездник'
        verbose_name_plural = 'Наездники'
        ordering = ['id']
        db_table = 'Jockey'


class Owner(models.Model):
    user = models.ForeignKey('Profile', on_delete=models.CASCADE, verbose_name='Пользователь')
    def __str__(self):
        return self.user.__str__()
    def get_absolute_url(self):
        return reverse('owner_id', args=[str(self.id)])
    class Meta:
        verbose_name = 'Собственник'
        verbose_name_plural = 'Собственники'
        ordering = ['id']
        db_table = 'Owner'


class City(models.Model):
    name = models.CharField(blank=False, max_length=50, verbose_name='Название')
    photo = models.ImageField(verbose_name='Фото', upload_to='photos/city/%Y/%m/%d/')
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = 'Город'
        verbose_name_plural = 'Города'
        ordering = ['name']
        db_table = 'City'


class Horse(models.Model):
    name = models.CharField(verbose_name='Кличка', max_length=50, blank=False)
    mast = models.CharField(verbose_name='Масть', max_length=50, blank=False)
    age = models.IntegerField(verbose_name='Возраст', blank=False)
    owner = models.ForeignKey('Owner', on_delete=models.RESTRICT)
    photo = models.ImageField(verbose_name='Фото',upload_to='photos/horse/%Y/%m/%d/', default='')
    def __str__(self):
        return self.name
    def get_absolute_url(self):
        return reverse('horse_id', args=[str(self.id)])
    class Meta:
        verbose_name = 'Лошадь'
        verbose_name_plural = 'Лошади'
        ordering = ['name']
        db_table = 'Horse'


class Couple(models.Model):
    horse = models.ForeignKey('Horse', on_delete=models.CASCADE, verbose_name='Лошадь')
    jockey = models.ForeignKey('Jockey', on_delete=models.CASCADE, verbose_name='Жокей')
    race = models.ForeignKey('Race', on_delete=models.CASCADE, verbose_name='Заезд')
    result = models.IntegerField(blank=True, verbose_name='Результат')
    time = models.TimeField(blank=True, verbose_name='Итоговое время')
    def __str__(self):
        return self.horse.__str__() + ' - ' + self.jockey.__str__()
    class Meta:
        verbose_name = 'Участник'
        verbose_name_plural = 'Участники'
        ordering = ['id']
        db_table = 'Couple'


class Hippodrome(models.Model):
    name = models.CharField(verbose_name='Название', blank=False, max_length=100)
    city = models.ForeignKey('City', on_delete=models.RESTRICT, verbose_name='Город', blank=True)
    address = models.CharField(blank=False, verbose_name='Адрес', max_length=500)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = 'Ипподром'
        verbose_name_plural = 'Ипподромы'
        ordering = ['name', 'city']
        db_table = 'Hippodrome'


class Race(models.Model):
    date = models.DateField(verbose_name='Дата', blank=False)
    time_begin = models.TimeField(verbose_name='Время начала', blank=False)
    time_end = models.TimeField(verbose_name='Время завершения', blank=False)
    hippodrome = models.ForeignKey('Hippodrome', on_delete=models.CASCADE, blank=False, verbose_name='Ипподром')
    title = models.CharField(blank=False, max_length=255, verbose_name='Заголовок')
    summa = models.IntegerField(verbose_name='Призовой фонд', blank=False)
    org = models.CharField(verbose_name='Организатор', max_length=255, blank=False)
    distance = models.IntegerField(verbose_name='Дистанция', blank=False)

    def __str__(self):
        return self.title
    def get_absolute_url(self):
        return reverse('race_id', args=[str(self.id)])
    class Meta:
        verbose_name = 'Заезд'
        verbose_name_plural = 'Заезды'
        ordering = ['date', 'time_begin', 'time_end']
        db_table = 'Race'

