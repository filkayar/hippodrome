from django.db import models

# Create your models here.
class User(models.Model):
    pk = models.IntegerField(verbose_name='ID',primary_key=True)
    city = models.ForeignKey('City', on_delete=models.SET_NULL, verbose_name='Город', blank=True)
    f = models.CharField(max_length=255, verbose_name='Фамилия', blank=False)
    i = models.CharField(max_length=255, verbose_name='Имя', blank=False)
    o = models.CharField(max_length=255, verbose_name='Отчество', blank=True)
    phone = models.CharField(max_length=20, verbose_name='Телефон', blank=True)
    birth = models.DateField(verbose_name='Дата рождения', blank=False)
    s_passport = models.IntegerField(blank=False, verbose_name='Серия паспорта')
    n_passport = models.IntegerField(blank=False, verbose_name='Номер паспорта')
    d_passport = models.DateField(blank=False, verbose_name='Дата выдачи паспорта')
    w_passport = models.CharField(blank=False, verbose_name='Кем выдан паспорт')
    role = models.ForeignKey('Role',on_delete=models.SET_NULL)
    login = models.CharField(blank=False, verbose_name='Логин', max_length=30)
    password = models.CharField(blank=False, max_length=255, verbose_name='Пароль')
    photo = models.ImageField(verbose_name='Фото',upload_to='photos/user/%Y/%m/%d/')

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['f', 'i', 'o']
        db_table = 'User'


class Jockey(models.Model):
    pk = models.IntegerField(verbose_name='ID', primary_key=True)
    user = models.ForeignKey('User', on_delete=models.CASCADE, verbose_name='Пользователь')
    category = models.CharField(verbose_name='Категория', max_length=255, blank=False)
    class Meta:
        verbose_name = 'Наездник'
        verbose_name_plural = 'Наездники'
        ordering = ['pk']
        db_table = 'Jockey'


class Owner(models.Model):
    pk = models.IntegerField(verbose_name='ID', primary_key=True)
    user = models.ForeignKey('User', on_delete=models.CASCADE, verbose_name='Пользователь')
    class Meta:
        verbose_name = 'Собственник'
        verbose_name_plural = 'Собственники'
        ordering = ['pk']
        db_table = 'Owner'


class City(models.Model):
    pk = models.IntegerField(verbose_name='ID', primary_key=True)
    name = models.CharField(blank=False, max_length=50, verbose_name='Название')
    photo = models.ImageField(verbose_name='Фото', upload_to='photos/city/%Y/%m/%d/')
    class Meta:
        verbose_name = 'Город'
        verbose_name_plural = 'Города'
        ordering = ['name']
        db_table = 'City'


class Role(models.Model):
    pk = models.IntegerField(verbose_name='ID', primary_key=True)
    name = models.CharField(blank=False, max_length=50, verbose_name='Название')
    class Meta:
        verbose_name = 'Роль'
        verbose_name_plural = 'Роли'
        ordering = ['name']
        db_table = 'Role'


class Horse(models.Model):
    pk = models.IntegerField(verbose_name='ID', primary_key=True)
    name = models.CharField(verbose_name='Кличка', max_length=50, blank=False)
    mast = models.CharField(verbose_name='Масть', max_length=50, blank=False)
    age = models.IntegerField(verbose_name='Возраст', blank=False)
    owner = models.ForeignKey('Owner', on_delete=models.SET_NULL)
    class Meta:
        verbose_name = 'Лошадь'
        verbose_name_plural = 'Лошади'
        ordering = ['name']
        db_table = 'Horse'


class Couple(models.Model):
    pk = models.IntegerField(verbose_name='ID', primary_key=True)
    horse = models.ForeignKey('Horse', on_delete=models.CASCADE, verbose_name='Лошадь')
    jockey = models.ForeignKey('Jockey', on_delete=models.CASCADE, verbose_name='Жокей')
    race = models.ForeignKey('Race', on_delete=models.CASCADE, verbose_name='Заезд')
    result = models.IntegerField(blank=True, verbose_name='Результат')
    time = models.TimeField(null=True, verbose_name='Итоговое время')
    class Meta:
        verbose_name = 'Участник'
        verbose_name_plural = 'Участники'
        ordering = ['pk']
        db_table = 'Couple'


class Hippodrome(models.Model):
    pk = models.IntegerField(verbose_name='ID', primary_key=True)
    name = models.CharField(verbose_name='Название', blank=False, max_length=100)
    city = models.ForeignKey('City', on_delete=models.SET_NULL, verbose_name='Город', blank=True)
    address = models.CharField(blank=False, verbose_name='Адрес', max_length=500)
    class Meta:
        verbose_name = 'Ипподром'
        verbose_name_plural = 'Ипподромы'
        ordering = ['name', 'city']
        db_table = 'Hippodrome'


class Race(models.Model):
    pk = models.IntegerField(verbose_name='ID', primary_key=True)
    date = models.DateField(verbose_name='Дата', blank=False)
    time_begin = models.TimeField(verbose_name='Время начала', blank=False)
    time_end = models.TimeField(verbose_name='Время завершения', blank=False)
    hippodrome = models.ForeignKey('Hippodrome', on_delete=models.CASCADE, blank=False, verbose_name='Ипподром')
    title = models.CharField(blank=False, max_length=255, verbose_name='Заголовок')
    summa = models.IntegerField(verbose_name='Призовой фонд', blank=False)
    org = models.CharField(verbose_name='Организатор', max_length=255, blank=False)
    distance = models.IntegerField(verbose_name='Дистанция', blank=False)
    class Meta:
        verbose_name = 'Заезд'
        verbose_name_plural = 'Заезды'
        ordering = ['date', 'time_begin', 'time_end']
        db_table = 'Race'

