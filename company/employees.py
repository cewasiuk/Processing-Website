from django.db import models
from django.db.models.fields import TextField


class Employee(models.Model):
    first_name = models.CharField('First Name', max_length=100)
    last_name = models.CharField('Last Name', max_length=100)
    employee_number = models.CharField('Employee Number', max_length=6)
    department = models.CharField('Department', max_length=100)

    def __str__(self):
        return self.first_name + ' ' + self.last_name


class Sales(Employee):
    pass


class Engineer(Employee):
    speciality = models.TextField('Engineering Speciality', max_length=100, blank=True)

    # TODO: Add an 'ability' (or something similar) section to denote what kind of work the engineer can do (eg. grinding, dicing, laser etc.)

    