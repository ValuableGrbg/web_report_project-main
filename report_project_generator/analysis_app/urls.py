from django.urls import path, include
from . import views
from django.views.decorators.csrf import csrf_exempt


urlpatterns = [
    # path('', views.probe_page, name='probe_page'),
    path('', views.index, name='analysis_app'),
    path('add_analysis', views.add_analysis, name='add_analysis'),
    path('add_analysis/<int:id>', views.add_analysis, name='add_analysis'),
    path('analysis_edit/<int:id>', views.analysis_edit, name='analysis_edit'),
    path('analysis_delete/<int:id>', views.analysis_delete, name='analysis_delete'),
    path('export_pdf/<int:id>', views.export_pdf, name='export_pdf'),
    path('index_engineer', views.index_engineer, name='index_engineer'),
    path('add_oil_extraction', views.add_oil_extraction, name='add_oil_extraction'),
    path('clients-json/', views.get_json_client_data, name='clients-json'),
    path('probe_details-json/', views.get_json_test_oil_types, name='probe_details-json'),
    path('serial-number-json/<str:client>/', views.get_json_equipment_serial_number, name='serial-number-json'),
    path('equipment-info-json/', csrf_exempt(views.get_json_equipment_name), name='equipment-info-json'),
    path('index_clients', views.index_clients, name='index_clients'),
    path('add_client_info', views.add_client_info, name='add_client_info'),
    path('probes-json/', views.get_json_probes_data, name='probes-json'),

    path('add_analysis_PH', views.add_analysis_PH, name='add_analysis_PH'),
    path('index_PH', views.index_PH, name='index_PH'),
    path('analysis_edit_PH/<int:id>', views.analysis_edit_PH, name='analysis_edit_PH'),
    path('analysis_delete_PH/<int:id>', views.analysis_delete_PH, name='analysis_delete_PH'),
    path('export_pdf_ph/<int:id>', views.export_pdf_ph, name='export_pdf_ph'),
]