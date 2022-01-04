from django.db import models


# Wheel Information:
class Wheel(models.Model):
    wheel_spec = models.CharField("Full Wheel Spec", max_length=30)
    code = models.CharField("Wheel Code", max_length=10, blank=True)
    size_spec = models.CharField("Full Size Spec", max_length=20, blank=True)
    lot_number = models.CharField("Lot Number", max_length=20)

    def __str__(self):
        return self.wheel_spec


class GrindWheel(Wheel):
    name = "Grinding Wheel"


class PolishWheel(Wheel):
    name = "Polishing Wheel"


# Wafer information: 
class WaferShape(models.Model):
    wafer_shape = models.CharField("Wafer Shape", max_length=150)

    # TODO: Calculating and inputting dimensions for the wafers

    def __str__(self):
        return self.wafer_shape


class WaferMaterial(models.Model):
    wafer_material = models.CharField("Wafer Material", max_length=150)

    # TODO: Add additional information about each material:
    # hardness, index of refraction, structure, etc.

    def __str__(self):
        return self.wafer_material

    
class BondMaterial(models.Model):
    bond_material = models.CharField("Bond Material", max_length=150)

    def __str__(self):
        return self.bond_material


# Tape information:
class Tape(models.Model):
    tape_spec = models.CharField("Full Tape Spec", max_length=50)
    tape_THK = models.IntegerField("Tape Thickness")
    base_film = models.CharField("Base Film", max_length=50, blank=True)
    base_THK = models.IntegerField("Base Film Thickness", blank=True, null=True, default=0)
    adhesive_film = models.CharField("Adhesive Film", max_length=50, blank=True)
    adhesive_THK = models.IntegerField("Adhesive Film Thickness", blank=True, null=True, default=0)
    adhesive_strength = models.IntegerField("Adhesive Film Strength", blank=True, null=True, default=0)
    

    def __str__(self):
        return self.tape_spec