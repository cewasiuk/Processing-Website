from django.contrib import admin
from .customers import Customer
from .employees import Employee, Sales, Engineer
from .inventory import (
    WaferMaterial, WaferShape, BondMaterial, Tape, 
    Wheel, GrindWheel, PolishWheel
)


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    fields = ('company', 'address')
    list_display = ('company', 'address')
    search_fields = ('company', 'address')

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    fields = ('first_name', 'last_name', 'employee_number', 'department')
    ordering = ('last_name',)
    list_display = ('first_name', 'last_name', 'employee_number', 'department')
    search_fields = ('first_name', 'last_name', 'employee_number', 'department')

@admin.register(Sales)
class SalesAdmin(admin.ModelAdmin):
    fields = ('first_name', 'last_name', 'employee_number', 'department')
    ordering = ('last_name',)
    list_display = ('first_name', 'last_name', 'employee_number', 'department')
    search_fields = ('first_name', 'last_name', 'employee_number', 'department')

@admin.register(Engineer)
class EngineerAdmin(admin.ModelAdmin):
    fields = ('first_name', 'last_name', 'employee_number', 'department')
    ordering = ('last_name',)
    list_display = ('first_name', 'last_name', 'employee_number', 'department')
    search_fields = ('first_name', 'last_name', 'employee_number', 'department')

@admin.register(WaferMaterial)
class WaferMaterialAdmin(admin.ModelAdmin):
    list_display = ('wafer_material',)
    search_fields = ('wafer_material',)

@admin.register(Tape)
class TapeAdmin(admin.ModelAdmin):
    list_display = ('tape_spec','tape_THK', 'adhesive_strength',)
    ordering = ('tape_spec',)
    search_fields = ('tape_spec', 'tape_THK', 'base_film', 'adhesive_film',)

@admin.register(Wheel)
class WheelAdmin(admin.ModelAdmin):
    list_display = ('wheel_spec', 'code', 'lot_number', 'size_spec',)
    ordering = ('wheel_spec',)
    search_fields = ('wheel_spec', 'code', 'lot_number', 'size_spec',)

@admin.register(GrindWheel)
class GrindWheelAdmin(admin.ModelAdmin):
    list_display = ('wheel_spec', 'code', 'lot_number', 'size_spec',)
    ordering = ('wheel_spec',)
    search_fields = ('wheel_spec', 'code', 'lot_number', 'size_spec',)

@admin.register(PolishWheel)
class PolishWheelAdmin(admin.ModelAdmin):
    list_display = ('wheel_spec', 'code', 'lot_number', 'size_spec',)
    ordering = ('wheel_spec',)
    search_fields = ('wheel_spec', 'code', 'lot_number', 'size_spec',)

# admin.site.register(Customer)
# admin.site.register(Employee)
# admin.site.register(Sales)
# admin.site.register(Engineer)
# admin.site.register(WaferMaterial)
admin.site.register(WaferShape)
admin.site.register(BondMaterial)
# admin.site.register(Tape)
# admin.site.register(Wheel)
# admin.site.register(GrindWheel)
# admin.site.register(PolishWheel)