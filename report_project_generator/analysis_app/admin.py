from django.contrib import admin
from .models import client_equipment, devices, analysis_info, analysis_results, OilBrandInfo, OilTestTypesInfo
from .models import ProbeDetailsInfo, OilNormativeDocs, TransformerDefTypes, RpnTypeInfo, EquipmentVoltageClasses
from .models import EquipmentAndTestingPart, OilProbesIssues
from .models import oil_PC, PC_LimitValues

from .models import CompanyDetails
# Register your models here.

admin.site.register(analysis_results)
admin.site.register(client_equipment)
admin.site.register(devices)
admin.site.register(OilBrandInfo)
admin.site.register(OilTestTypesInfo)
admin.site.register(ProbeDetailsInfo)
admin.site.register(OilNormativeDocs)
admin.site.register(TransformerDefTypes)
admin.site.register(RpnTypeInfo)
admin.site.register(EquipmentVoltageClasses)
admin.site.register(EquipmentAndTestingPart)
admin.site.register(OilProbesIssues)

admin.site.register(CompanyDetails)
admin.site.register(oil_PC)
admin.site.register(PC_LimitValues)


# class ClientEquipmentAdmin(admin.ModelAdmin):
#     list_display = (
#         'id',
#         'client_name',
#         'substation_name',
#         'equipment_name',
#         'equipment_type_full',
#         'equipment_type',
#         'testing_part',
#         'equipment_serial_number'
#     )
#
#
# class DevicesAdmin(admin.ModelAdmin):
#     list_display = (
#         'id',
#         'device_name',
#         'device_type',
#         'device_serial_number',
#         'device_certification_number',
#         'next_device_certification_date'
#     )
#
#
# class AnalysisInfoAdmin(admin.ModelAdmin):
#     list_display = (
#         'id',
#         'protocol_name',
#         'created_date',
#         'updated_date',
#         'protocol_status',
#         'fk_client_equipment_id',
#         'fk_devices_id'
#     )
#
#
# admin.site.register(client_equipment, ClientEquipmentAdmin)
# admin.site.register(devices, DevicesAdmin)
# admin.site.register(analysis_info, AnalysisInfoAdmin)
