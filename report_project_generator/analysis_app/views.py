import datetime
import pandas as pd
import numpy as np
from jinja2 import Environment, FileSystemLoader
from django.templatetags.static import static

import os
from report_project_generator.settings import STATIC_ROOT, BASE_DIR

from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpResponse
from .models import client_equipment, User, devices, analysis_results, ProbeDetailsInfo, OilTestTypesInfo, OilBrandInfo
from .models import ChargTransformersLimitValues_35_500, EquipmentVoltageClasses, RpnTypeInfo, TransformerDefTypes
from .models import EquipmentAndTestingPart, OilNormativeDocs, OilProbesIssues, CompanyDetails
from .models import oil_PC, PC_LimitValues
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.apps import apps
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.utils.timezone import now
from django.apps import apps
import json

from weasyprint import HTML
from django.template.loader import render_to_string
import tempfile
import pdb

import base64


@login_required(login_url='/authentication/login')
def index(request, *args, **kwargs):
    # Get all created analysis records
    analysis_infos = analysis_results.objects.all()

    # Create pagination
    paginator = Paginator(analysis_infos, 3)  # ограничиваем пагинацию до 3 элементов на странице
    page_number = request.GET.get('page')
    page_object = Paginator.get_page(paginator, page_number)

    context = {
        'analysis_infos': analysis_infos,
        'page_object': page_object,
    }

    return render(request, 'analysis_app/index.html', context)


@login_required(login_url='/authentication/login')
def index_engineer(request, *args, **kwargs):
    # Get all created analysis records
    task_info = ProbeDetailsInfo.objects.all()

    # Create pagination
    paginator = Paginator(task_info, 3)  # ограничиваем пагинацию до 3 элементов на странице
    page_number = request.GET.get('page')
    page_object = Paginator.get_page(paginator, page_number)

    context = {
        'task_info': task_info,
        'page_object': page_object,
        'values': request.POST
    }

    return render(request, 'analysis_app/index_engineer.html', context)


@login_required(login_url='/authentication/login')
def lab_task_list(request, *args, **kwargs):
    # Get all created analysis records
    task_info = analysis_results.objects.all()  # !TODO добавить ссылку на модель, создаваемую инженером

    # Create pagination
    paginator = Paginator(task_info, 3)  # ограничиваем пагинацию до 3 элементов на странице
    page_number = request.GET.get('page')
    page_object = Paginator.get_page(paginator, page_number)

    context = {
        'task_info': task_info,
        'page_object': page_object,
    }

    return render(request, 'analysis_app/index.html', context)  # !TODO Исправить ссылку


@login_required(login_url='/authentication/login')
def add_oil_extraction(request, *args, **kwargs):
    employees = User.objects.all()
    clients = client_equipment.objects.all()
    oil_brand_info = OilBrandInfo.objects.all()
    testing_parts = EquipmentAndTestingPart.objects.all().values('testing_part').distinct()
    probe_issues = OilProbesIssues.objects.all()

    context = {
        'employees': employees,
        'clients': clients,
        'values': request.POST,
        'oil_brand_info': oil_brand_info,
        'testing_parts': testing_parts,
        'probe_issues': probe_issues
    }

    if request.method == 'GET':
        return render(request, 'analysis_app/add_oil_extraction.html', context)

    if request.method == 'POST':
        # pdb.set_trace()
        tester_name = User.objects.get(username=request.POST['employee'])
        client_name = request.POST.get('client', False)
        equipment_serial_number = request.POST.get('equipment_serial_number', False)
        probe_date = request.POST['probe_date']
        test_type = request.POST.get('test_type', False)
        normative_doc = request.POST.get('normative_doc', False)
        chosen_container_type = request.POST.get('container_type', False)
        atm_temperature = request.POST['atm_temperature']
        oil_temperature = request.POST['oil_temperature']
        oil_brand_name = request.POST.get('oil_brand', False)
        load_value = request.POST['load_value']
        testing_part = request.POST.get('testing_part', False)
        probe_issue_id = request.POST.get('probe_issue', False)

        if not tester_name:
            messages.error(request, "Выберите работника!")
            return render(request, 'analysis_app/add_oil_extraction.html', context)
        if not client_name:
            messages.error(request, "Выберите заказчика!")
            return render(request, 'analysis_app/add_oil_extraction.html', context)
        if not equipment_serial_number:
            messages.error(request, "Выберите заводской номер!")
            return render(request, 'analysis_app/add_oil_extraction.html', context)
        if not probe_date:
            messages.error(request, "Выберите дату!")
            return render(request, 'analysis_app/add_oil_extraction.html', context)
        if not test_type:
            messages.error(request, "Выберите вид испытания!")
            return render(request, 'analysis_app/add_oil_extraction.html', context)
        if not chosen_container_type:
            messages.error(request, "Выберите вид тары используемой в отборе!")
            return render(request, 'analysis_app/add_oil_extraction.html', context)
        if not atm_temperature:
            messages.error(request, "Введите значение температуры окружающей среды!")
            return render(request, 'analysis_app/add_oil_extraction.html', context)
        if not oil_temperature:
            messages.error(request, "Введите значение температуры масла!")
            return render(request, 'analysis_app/add_oil_extraction.html', context)
        if not oil_brand_name:
            messages.error(request, "Выберите марку масла!")
            return render(request, 'analysis_app/add_oil_extraction.html', context)
        if not load_value:
            messages.error(request, "Введите значение нагрузки!")
            return render(request, 'analysis_app/add_oil_extraction.html', context)
        if not testing_part:
            messages.error(request, "Введите место отбора!")
            return render(request, 'analysis_app/add_oil_extraction.html', context)
        if not probe_issue_id:
            messages.error(request, "Введите причину отбора!")
            return render(request, 'analysis_app/add_oil_extraction.html', context)

        if test_type == 'ХАРГ':
            syringe_num = request.POST['container_type']
            bottle_num = '-'
        else:
            bottle_num = request.POST['container_type']
            syringe_num = '-'

        tested_client = client_equipment.objects.get(client_name=client_name,
                                                     equipment_serial_number=equipment_serial_number)
        oil_normative_id = OilNormativeDocs.objects.get(normative_doc=normative_doc).id
        test_doc_type = OilTestTypesInfo.objects.get(test_type=test_type, normative_doc=oil_normative_id)
        oil_brand = OilBrandInfo.objects.get(oil_brand=oil_brand_name)
        probe_issue = OilProbesIssues.objects.get(pk=probe_issue_id)

        ProbeDetailsInfo.objects.create(
            tester_name=tester_name,
            tested_client=tested_client,
            probe_date=probe_date,
            bottle_num=bottle_num,
            syringe_num=syringe_num,
            test_doc_type=test_doc_type,
            atm_temperature=atm_temperature,
            oil_temperature=oil_temperature,
            oil_brand=oil_brand,
            load_value=load_value,
            testing_part=testing_part,
            probe_issue=probe_issue
        )

        messages.success(request, 'Информация об отборе успешно сохранена')

        return redirect('index_engineer')


def get_json_client_data(request):
    qs_val = list(client_equipment.objects.values())
    return JsonResponse({'data': qs_val})


def get_json_test_oil_types(request):
    qs_val = list(OilTestTypesInfo.objects.all().values())
    normative_docs = list(OilNormativeDocs.objects.all().values())
    return JsonResponse({'data': qs_val, 'normative_docs': normative_docs})


def get_json_equipment_serial_number(request, *args, **kwargs):
    selected_client = kwargs.get('client')
    # print(kwargs)
    obj_serial_num = list(client_equipment.objects.filter(client_name=selected_client).values())
    return JsonResponse({'data': obj_serial_num})


def get_json_equipment_name(request, *args, **kwargs, ):
    client_info_dict = json.loads(request.POST.get('data'))[0]

    client_details = client_equipment.objects.filter(
        client_name=client_info_dict['client'],
        equipment_serial_number=client_info_dict['serial_num']
    ).values()

    obj_info = list(client_details)
    obj_test_parts = list(EquipmentAndTestingPart.objects.filter(
        equipment_type_full=client_details[0]["equipment_type_full"]
    ).values_list('testing_part', flat=True))

    return JsonResponse({'data': obj_info, 'parts_data': obj_test_parts})


def get_json_probes_data(request):
    probes_data = list(ProbeDetailsInfo.objects.values())
    print(probes_data)
    clients_data = list(client_equipment.objects.values())
    voltage_classes = list(EquipmentVoltageClasses.objects.values())
    oil_brands = list(OilBrandInfo.objects.values())
    def_types = list(TransformerDefTypes.objects.values())
    probe_issues = list(OilProbesIssues.objects.values())
    return JsonResponse({'probes_data': probes_data,
                         'clients_data': clients_data,
                         'voltage_classes': voltage_classes,
                         'oil_brands': oil_brands,
                         'def_types': def_types,
                         'probe_issues': probe_issues,
                         })


@login_required(login_url='/authentication/login')
def add_analysis(request, *args, **kwargs):
    try:
        probe_transfered_id = kwargs['id']
    except KeyError:
        probe_transfered_id = None

    employees = User.objects.all()
    chromotographs = devices.objects.all()

    if probe_transfered_id:
        probe_details = ProbeDetailsInfo.objects.get(pk=probe_transfered_id)
    else:
        probe_details = ProbeDetailsInfo.objects.all()

    context = {
        'employees': employees,
        'probe_id': probe_transfered_id,
        'probe_details': probe_details,
        'chromotographs': chromotographs,
        'values': request.POST
    }

    if request.method == 'GET':
        return render(request, 'analysis_app/add_analysis.html', context)

    if request.method == 'POST':
        probe_id = request.POST.get('probe_id', False)
        employee = User.objects.get(username=request.POST['employee'])
        # chromotograph = devices.objects.get(device_serial_number=request.POST['chromotograph'].rsplit(" ")[-1])
        chromotograph = devices.objects.get(id=request.POST.get('chromotograph', False))
        analysis_date = request.POST['analysis_date']
        delivery_date = request.POST['delivery_date']
        probe_code = request.POST.get('probe_code', False)
        description = request.POST['description']
        H2_value = request.POST['H2']
        CH4_value = request.POST['CH4']
        C2H4_value = request.POST['C2H4']
        C2H6_value = request.POST['C2H6']
        C2H2_value = request.POST['C2H2']
        CO2_value = request.POST['CO2']
        CO_value = request.POST['CO']
        N2_O2_value = request.POST['N2_O2']
        SRG_value = request.POST['SRG']
        test_condition_temp = request.POST.get('test_condition_temp', False)
        test_condition_humidity = request.POST.get('test_condition_humidity', False)
        test_condition_pressure = request.POST.get('test_condition_pressure', False)

        if not probe_id:
            messages.error(request, "Выберите пробу, по которой проводите анализ!")
            return render(request, 'analysis_app/add_analysis.html', context)
        if not analysis_date:
            messages.error(request, "Выберите дату!")
            return render(request, 'analysis_app/add_analysis.html', context)
        if not delivery_date:
            messages.error(request, "Выберите дату доставки пробы в лабораторию!")
            return render(request, 'analysis_app/analysis_edit.html', context)
        if not probe_code:
            messages.error(request, "Введите шифр пробы!")
            return render(request, 'analysis_app/add_analysis.html', context)
        if not H2_value:
            messages.error(request, "Введите значение водорода!")
            return render(request, 'analysis_app/add_analysis.html', context)
        if not CH4_value:
            messages.error(request, "Введите значение метана!")
            return render(request, 'analysis_app/add_analysis.html', context)
        if not C2H4_value:
            messages.error(request, "Введите значение этилена!")
            return render(request, 'analysis_app/add_analysis.html', context)
        if not C2H6_value:
            messages.error(request, "Введите значение этана!")
            return render(request, 'analysis_app/add_analysis.html', context)
        if not C2H2_value:
            messages.error(request, "Введите значение ацетилена!")
            return render(request, 'analysis_app/add_analysis.html', context)
        if not CO2_value:
            messages.error(request, "Введите значение диоксида углерода!")
            return render(request, 'analysis_app/add_analysis.html', context)
        if not CO_value:
            messages.error(request, "Введите значение оксида углерода!")
            return render(request, 'analysis_app/add_analysis.html', context)

        probe = ProbeDetailsInfo.objects.get(id=probe_id)
        client = ProbeDetailsInfo.objects.get(id=probe_id).tested_client

        # Генерация номера протокола
        analysis_instance = list(analysis_results.objects.filter(analysis_date=analysis_date).values('analysis_date'))
        # print(analysis_instance, f'\n length {len(analysis_instance)}')
        protocol_code = f'ХА-{len(analysis_instance) + 1}-{pd.to_datetime(analysis_date).strftime("%d-%m-%Y")}'

        # Checking for empty cells in form
        if N2_O2_value == '':
            N2_O2_value = None
        if SRG_value == '':
            SRG_value = None

        analysis_results.objects.create(
            analysis_date=analysis_date,
            delivery_date=delivery_date,
            probe_id=probe,
            employee=employee,
            client=client,
            chromotograph=chromotograph,
            probe_code=probe_code,
            description=description,
            H2_value=H2_value,
            CH4_value=CH4_value,
            C2H4_value=C2H4_value,
            C2H6_value=C2H6_value,
            C2H2_value=C2H2_value,
            CO2_value=CO2_value,
            CO_value=CO_value,
            N2_O2_value=N2_O2_value,
            SRG_value=SRG_value,
            protocol_code=protocol_code,
            test_condition_temp=test_condition_temp,
            test_condition_humidity=test_condition_humidity,
            test_condition_pressure=test_condition_pressure
        )

        messages.success(request, 'Анализ успешно сохранен')

        return redirect('analysis_app')


def analysis_edit(request, id):
    analysis = analysis_results.objects.get(pk=id)
    employees = User.objects.all()
    clients = client_equipment.objects.all()
    chromotographs = devices.objects.all()

    context = {
        'analysis': analysis,
        'values': analysis,
        'employees': employees,
        'clients': clients,
        'chromotographs': chromotographs,
    }
    if request.method == 'GET':
        return render(request, 'analysis_app/analysis_edit.html', context)

    if request.method == 'POST':
        employee = User.objects.get(username=request.POST['employee'])
        client = client_equipment.objects.get(id=request.POST['client'].split('.')[0])
        chromotograph = devices.objects.get(device_serial_number=request.POST['chromotograph'].rsplit(" ")[-1])
        analysis_date = request.POST['analysis_date']
        delivery_date = request.POST['delivery_date']
        description = request.POST['description']
        H2_value = request.POST['H2']
        CH4_value = request.POST['CH4']
        C2H4_value = request.POST['C2H4']
        C2H6_value = request.POST['C2H6']
        C2H2_value = request.POST['C2H2']
        CO2_value = request.POST['CO2']
        CO_value = request.POST['CO']
        N2_O2_value = request.POST['N2_O2']
        SRG_value = request.POST['SRG']

        if not analysis_date:
            messages.error(request, "Выберите дату проведения анализа!")
            return render(request, 'analysis_app/analysis_edit.html', context)
        if not delivery_date:
            messages.error(request, "Выберите дату доставки пробы в лабораторию!")
            return render(request, 'analysis_app/analysis_edit.html', context)
        if not H2_value:
            messages.error(request, "Введите значение водорода!")
            return render(request, 'analysis_app/analysis_edit.html', context)
        if not CH4_value:
            messages.error(request, "Введите значение метана!")
            return render(request, 'analysis_app/analysis_edit.html', context)
        if not C2H4_value:
            messages.error(request, "Введите значение этилена!")
            return render(request, 'analysis_app/analysis_edit.html', context)
        if not C2H6_value:
            messages.error(request, "Введите значение этана!")
            return render(request, 'analysis_app/analysis_edit.html', context)
        if not C2H2_value:
            messages.error(request, "Введите значение ацетилена!")
            return render(request, 'analysis_app/analysis_edit.html', context)
        if not CO2_value:
            messages.error(request, "Введите значение диоксида углерода!")
            return render(request, 'analysis_app/analysis_edit.html', context)
        if not CO_value:
            messages.error(request, "Введите значение оксида углерода!")
            return render(request, 'analysis_app/analysis_edit.html', context)

        # Checking for empty cells in form
        if N2_O2_value == '':
            N2_O2_value = None
        if SRG_value == '':
            SRG_value = None

        analysis.employee = employee
        analysis.client = client
        analysis.chromotograph = chromotograph
        analysis.analysis_date = analysis_date
        analysis.delivery_date = delivery_date
        analysis.description = description
        analysis.H2_value = H2_value
        analysis.CH4_value = CH4_value
        analysis.C2H4_value = C2H4_value
        analysis.C2H6_value = C2H6_value
        analysis.C2H2_value = C2H2_value
        analysis.CO2_value = CO2_value
        analysis.CO_value = CO_value
        analysis.N2_O2_value = N2_O2_value
        analysis.SRG_value = SRG_value

        analysis.save()
        messages.success(request, 'Анализ успешно обновлен')

        return redirect('analysis_app')

        messages.info(request, 'Обработка')


def analysis_delete(request, id):
    analysis = analysis_results.objects.get(pk=id)
    analysis.delete()
    messages.success(request, 'Анализ удален!')
    return redirect('analysis_app')


@login_required(login_url='/authentication/login')
def add_client_info(request, *args, **kwargs):
    voltage_classes = EquipmentVoltageClasses.objects.all()
    rpn_types = RpnTypeInfo.objects.all()
    def_types = TransformerDefTypes.objects.all()
    equipments_parts = EquipmentAndTestingPart.objects.all().values('equipment_type_full').distinct()

    years = range(1900, datetime.datetime.now().year + 1, 1)

    context = {
        'voltage_classes': voltage_classes,
        'rpn_types': rpn_types,
        'def_types': def_types,
        'equipments_parts': equipments_parts,
        'values': request.POST,
        'years': years
    }

    if request.method == 'GET':
        return render(request, 'analysis_app/add_client_info.html', context)

    if request.method == 'POST':
        client_name = request.POST.get('client_name', False)
        substation_name = request.POST.get('substation_name', False)
        equipment_name = request.POST.get('equipment_name', False)
        equipment_type_full = request.POST.get('equipment_type_full', False)
        equipment_type = request.POST.get('equipment_type', False)
        equipment_serial_number = request.POST.get('equipment_serial_number', False)
        voltage_class_chosen = request.POST.get('voltage_class', False)
        equipment_power = request.POST.get('equipment_power', False)
        production_year = request.POST.get('production_year', False)
        setting_year = request.POST.get('setting_year', False)
        def_type_chosen = request.POST.get('def_type', False)
        rpn_type_chosen = request.POST.get('rpn_type', False)

        if not client_name:
            messages.error(request, "Внесите заказчика!")
            return render(request, 'analysis_app/add_client_info.html', context)
        if not substation_name:
            messages.error(request, "Внесите подстанцию!")
            return render(request, 'analysis_app/add_client_info.html', context)
        if not equipment_type_full:
            messages.error(request, "Внесите объект отбора!")
            return render(request, 'analysis_app/add_client_info.html', context)
        if not voltage_class_chosen:
            messages.error(request, "Введите класс напряжения!")
            return render(request, 'analysis_app/add_client_info.html', context)
        else:
            voltage_class = voltage_classes.get(voltage_class=voltage_class_chosen)
        if not equipment_power:
            messages.error(request, "Введите мощность оборудования!")
            return render(request, 'analysis_app/add_client_info.html', context)
        if not equipment_name:
            messages.error(request, "Внесите диспетчерское наименование!")
            return render(request, 'analysis_app/add_client_info.html', context)
        if not equipment_serial_number:
            messages.error(request, "Введите заводской номер оборудования!")
            return render(request, 'analysis_app/add_client_info.html', context)
        if not equipment_type:
            messages.error(request, "Введите тип оборудования!")
            return render(request, 'analysis_app/add_client_info.html', context)
        if not def_type_chosen and equipment_type_full == 'Трансформатор':
            messages.error(request, "Введите тип защиты трансформатора!")
            return render(request, 'analysis_app/add_client_info.html', context)
        elif equipment_type_full != 'Трансформатор' and not def_type_chosen:
            def_type = def_types.get(def_type="н/д")
            # def_type = "н/д"
        else:
            def_type = def_types.get(def_type=def_type_chosen)
        if not rpn_type_chosen and equipment_type_full == 'Трансформатор':
            messages.error(request, "Введите тип РПН!")
            return render(request, 'analysis_app/add_client_info.html', context)
        elif equipment_type_full != 'Трансформатор' and not rpn_type_chosen:
            rpn_type = rpn_types.get(rpn_type="н/д")
        else:
            rpn_type = rpn_types.get(rpn_type=rpn_type_chosen)
        if not production_year or not setting_year and setting_year:
            messages.error(request, "Выберите год производства или установки оборудования!")
            return render(request, 'analysis_app/add_client_info.html', context)

        # Проверка на наличие года выпуска/ установки и расчет числа лет эксплуатации на основе полученной проверки
        if production_year and not setting_year:
            usage_years = datetime.datetime.now().year - int(production_year)
            setting_year = None
        elif setting_year and not production_year:
            usage_years = datetime.datetime.now().year - int(setting_year)
            production_year = None
        else:
            usage_years = datetime.datetime.now().year - int(setting_year)

        client_equipment.objects.create(
            client_name=client_name,
            substation_name=substation_name,
            equipment_name=equipment_name,
            equipment_type_full=equipment_type_full,
            equipment_type=equipment_type,
            equipment_serial_number=equipment_serial_number,
            voltage_class=voltage_class,
            equipment_power=equipment_power,
            def_type=def_type,
            rpn_type=rpn_type,
            production_year=production_year,
            setting_year=setting_year,
            usage_years=usage_years,
        )

        messages.success(request, 'Информация об отборе успешно сохранена')

        return redirect('index_clients')


@login_required(login_url='/authentication/login')
def index_clients(request, *args, **kwargs):
    # Get all created analysis records
    clients_info = client_equipment.objects.all()

    # Create pagination
    paginator = Paginator(clients_info, 3)  # ограничиваем пагинацию до 3 элементов на странице
    page_number = request.GET.get('page')
    page_object = Paginator.get_page(paginator, page_number)

    context = {
        'clients_info': clients_info,
        'page_object': page_object,
        'values': request.POST
    }

    return render(request, 'analysis_app/index_clients.html', context)


def environment(**options):
    env = Environment(**options)
    env.globals.update({
        'static': static,
        'url': reverse,
    })
    return env


def get_mismatches(values, normatives):
    """
    Функция сравнения нормативных значений с полученными в результате испытаний.
    В результате возвращает список названий газов с превышением нормативных значений.
    """

    mismatches_dict = {}
    limit_pattern = 'pdz'

    mismatch_search_dict = {
        'H2': 'водорода',
        'CH4': 'метана',
        'C2H4': 'этилена',
        'C2H6': 'этана',
        'C2H2': 'ацетилена',
        'CO2': 'диоксида углерода',
        'CO': 'оксида углерода',
        'N2_O2': 'ОГС',
        'SRG': 'СРГ'
    }

    values_df = pd.DataFrame(values).filter(like='value').dropna(axis=1)
    print(values_df)
    normatives_df = pd.DataFrame(normatives).filter(like=f'value_{limit_pattern}')
    print(normatives_df)

    for i in values_df.columns.unique():
        i = i.rsplit('_', maxsplit=1)[-2]
        current_value = values_df.filter(items=[f'{i}_value'])[f'{i}_value'].max()
        current_normative = normatives_df.filter(items=[f'{i}_limit_value_{limit_pattern}'])[
            f'{i}_limit_value_{limit_pattern}'].max()
        print(f'{current_value} - {current_normative}')

        if current_normative < current_value:
            mismatches_dict[i] = mismatch_search_dict[i]

    return mismatches_dict


def export_pdf(request, id):
    """ Генерация pdf страницы-отчета"""

    partials_dict = {
        'ХАРГ': 'Charg',
        'Физ.Хим': 'PH',
        'Трансформатор': 'Transformer',
        'Выключатель': 'Breaker',
        'Реактор': 'Reactor'
    }

    analysis = analysis_results.objects.get(pk=id)
    probe_details_info = ProbeDetailsInfo.objects.get(id=analysis.probe_id.id)
    company_info = CompanyDetails.objects.get(company_name='ООО "Сибэнергодиагностика"')

    # сбор необходимых данных из анализа для получения предельных значений газов
    current_equipment_type = analysis.client.equipment_type_full
    current_voltage_class = analysis.client.voltage_class.voltage_class
    current_def_type = analysis.client.def_type.def_type
    current_usage_years = analysis.client.usage_years
    current_oil_brand = probe_details_info.oil_brand.oil_brand
    current_rpn_type = analysis.client.rpn_type.rpn_type
    current_equipment_power = analysis.client.equipment_power
    current_test_type = probe_details_info.test_doc_type.test_type
    current_normative_document = probe_details_info.test_doc_type.normative_doc.normative_doc

    # получение поискового шаблона для модели предельных значений
    gain_partials = [
        partials_dict[i] for i in partials_dict.keys() if i in [current_equipment_type, current_test_type]
    ]

    if len(gain_partials) == 0:
        messages.error(request, f"Не удается получить поисковый шаблон")
        return redirect('analysis_app')

    joined_partial = ''.join(gain_partials)

    app_models = [
        model for model in apps.get_models() if joined_partial in model.__name__
    ]

    # получение предельных значений
    try:
        limit_values = app_models[0].objects.get(
            normative_doc=current_normative_document,
            voltage_class=current_voltage_class,
            def_type=current_def_type,
            years_periods_include__contains=current_usage_years,
            oil_brand__contains=[current_oil_brand],
            rpn_type__contains=[current_rpn_type],
            equipment_power__contains=current_equipment_power
        )
    except app_models[0].DoesNotExist:
        messages.error(request,
                       f"По данной конфигурации запроса нет подходящих предельных значений. Может быть некорректный {current_normative_document}")
        return redirect('analysis_app')

    # python manage.py loaddata analysis_app/fixtures/ChargTransformersLimitValues35_500.json --app analysis_app.ChargTransformersLimitValues35_500
    # TODO! вставить модель для получения ПД ОГС
    mismatches = get_mismatches(values=analysis_results.objects.filter(pk=id).values(),
                                normatives=app_models[0].objects.filter(
                                    normative_doc=current_normative_document,
                                    voltage_class=current_voltage_class,
                                    def_type=current_def_type,
                                    years_periods_include__contains=current_usage_years,
                                    oil_brand__contains=[current_oil_brand],
                                    rpn_type__contains=[current_rpn_type],
                                    equipment_power__contains=current_equipment_power
                                ).values()
                                )

    css = r'report_project_generator/static/css/pdf_style.css'
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename=Analysis {str(datetime.datetime.now())}.pdf'
    response['Content_Transfer-Encoding'] = 'binary'

    env = Environment(loader=FileSystemLoader(r'templates/analysis_app'))
    # env = environment(loader=FileSystemLoader(r'templates/analysis_app'))

    template = env.get_template('export_pdf.html')

    logo = os.path.normpath(os.path.join(STATIC_ROOT, r'img/logo.jpg'))
    # logo = r'file:///Users\\Dmitriy\\PycharmProjects\\web_report_project\report_project_generator\staticfiles\img\logo.jpg'
    rendered_string = template.render(
        analysis=analysis,
        logo=logo,
        limit_values=limit_values,
        probe_details_info=probe_details_info,
        mismatches=mismatches,
        company_info=company_info
    )
    html = HTML(string=rendered_string)

    result = html.write_pdf(stylesheets=[css])
    response.write(result)

    return response


@login_required(login_url='/authentication/login')
def add_analysis_PH(request, *args, **kwargs):
    try:
        probe_transfered_id = kwargs['id']
    except KeyError:
        probe_transfered_id = None

    employees = User.objects.all()

    if probe_transfered_id:
        probe_details = ProbeDetailsInfo.objects.get(pk=probe_transfered_id)
    else:
        probe_details = ProbeDetailsInfo.objects.all()

    context = {
        'employees': employees,
        'probe_id': probe_transfered_id,
        'probe_details': probe_details,
        'values': request.POST
    }

    if request.method == 'GET':
        return render(request, 'analysis_app/add_analysis_PH.html', context)

    if request.method == 'POST':
        probe_id = request.POST.get('probe_id', False)
        employee = User.objects.get(username=request.POST['employee'])
        analysis_date = request.POST['analysis_date']
        delivery_date = request.POST['delivery_date']
        probe_code = request.POST.get('probe_code', False)
        description = request.POST['description']
        color_value = request.POST['color']
        transparency_value = request.POST['transparency']

        BV_CV_value = request.POST['BV_CV']
        acid_number_value = request.POST['acid_number']
        flash_rate_value = request.POST['flash_rate']
        moisture_value = request.POST['moisture']
        KPC_value = request.POST['KPC']
        tan_d_value = request.POST['tan_d']
        ph_value = request.POST['ph']
        ionol_value = request.POST['ionol']
        gas_value = request.POST['gas']
        furan_value = request.POST['furan']

        sludge_value = request.POST.get('sludge', None)
        solidification_value = request.POST.get('solid', None)
        oxidation_stability_value = request.POST.get('oxid', None)
        sulfur_value = request.POST.get('sulfur', None)
        corrosive_sulfur_value = request.POST.get('corrosion', None)

        test_condition_temp = request.POST.get('test_condition_temp', False)
        test_condition_humidity = request.POST.get('test_condition_humidity', False)
        test_condition_pressure = request.POST.get('test_condition_pressure', False)

        if not probe_id:
            messages.error(request, "Выберите пробу, по которой проводите анализ!")
            return render(request, 'analysis_app/add_analysis_PH.html', context)
        if not analysis_date:
            messages.error(request, "Выберите дату!")
            return render(request, 'analysis_app/add_analysis_PH.html', context)
        if not delivery_date:
            messages.error(request, "Выберите дату доставки пробы в лабораторию!")
            return render(request, 'analysis_app/analysis_edit.html', context)
        if not probe_code:
            messages.error(request, "Введите шифр пробы!")
            return render(request, 'analysis_app/add_analysis_PH.html', context)
        if not color_value:
            messages.error(request, "Введите цвет!")
            return render(request, 'analysis_app/add_analysis_PH_PH.html', context)
        if not transparency_value:
            messages.error(request, "Введите прозрачность!")
            return render(request, 'analysis_app/add_analysis_PH.html', context)

        probe = ProbeDetailsInfo.objects.get(id=probe_id)
        client = ProbeDetailsInfo.objects.get(id=probe_id).tested_client

        # Генерация номера протокола
        analysis_instance = list(analysis_results.objects.filter(analysis_date=analysis_date).values('analysis_date'))
        protocol_code = f'ФХ-{len(analysis_instance) + 1}-{pd.to_datetime(analysis_date).strftime("%d-%m-%Y")}'

        # Checking for empty cells in form
        if BV_CV_value == '':
            BV_CV_value = None
        if acid_number_value == '':
            acid_number_value = None
        if flash_rate_value == '':
            flash_rate_value = None
        if moisture_value == '':
            moisture_value = None
        if KPC_value == '':
            KPC_value = None
        if tan_d_value == '':
            tan_d_value = None
        if ph_value == '':
            ph_value = None
        if ionol_value == '':
            ionol_value = None
        if sludge_value == '':
            sludge_value = None
        if gas_value == '':
            gas_value = None
        if furan_value == '':
            furan_value = None

        if solidification_value == '':
            solidification_value = None
        if oxidation_stability_value == '':
            oxidation_stability_value = None
        if sulfur_value == '':
            sulfur_value = None
        if corrosive_sulfur_value == '':
            corrosive_sulfur_value = None

        oil_PC.objects.create(
            analysis_date=analysis_date,
            delivery_date=delivery_date,
            probe_id=probe,
            employee=employee,
            client=client,
            probe_code=probe_code,
            description=description,
            color_value=color_value,
            transparency_value=transparency_value,
            BV_CV_value=BV_CV_value,
            acid_number_value=acid_number_value,
            flash_rate_value=flash_rate_value,
            moisture_value=moisture_value,
            KPC_value=KPC_value,
            tan_d_value=tan_d_value,
            ph_value=ph_value,
            ionol_value=ionol_value,
            gas_value=gas_value,
            furan_value=furan_value,
            sludge_value=sludge_value,
            solidification_value=solidification_value,
            oxidation_stability_value=oxidation_stability_value,
            sulfur_value=sulfur_value,
            corrosive_sulfur_value=corrosive_sulfur_value,
            protocol_code=protocol_code,
            test_condition_temp=test_condition_temp,
            test_condition_humidity=test_condition_humidity,
            test_condition_pressure=test_condition_pressure
        )

        messages.success(request, 'Анализ успешно сохранен')

        return redirect('index_PH')


@login_required(login_url='/authentication/login')
def index_PH(request, *args, **kwargs):
    # Get all created analysis records
    analysis_infos = oil_PC.objects.all()

    # Create pagination
    paginator = Paginator(analysis_infos, 3)  # ограничиваем пагинацию до 3 элементов на странице
    page_number = request.GET.get('page')
    page_object = Paginator.get_page(paginator, page_number)

    context = {
        'analysis_infos': analysis_infos,
        'page_object': page_object,
    }

    return render(request, 'analysis_app/index_PH.html', context)


def analysis_edit_PH(request, id):
    analysis = oil_PC.objects.get(pk=id)
    employees = User.objects.all()

    context = {
        'analysis': analysis,
        'employees': employees,
        'values': analysis
    }

    if request.method == 'GET':
        return render(request, 'analysis_app/analysis_edit_PH.html', context)

    if request.method == 'POST':
        description = request.POST['description']
        color_value = request.POST['color']
        transparency_value = request.POST['transparency']
        BV_CV_value = request.POST['BV_CV']
        acid_number_value = request.POST['acid_number']
        flash_rate_value = request.POST['flash_rate']
        moisture_value = request.POST['moisture']
        KPC_value = request.POST['KPC']
        tan_d_value = request.POST['tan_d']
        ph_value = request.POST['ph']
        ionol_value = request.POST['ionol']
        sludge_value = request.POST['sludge']
        gas_value = request.POST['gas']
        furan_value = request.POST['furan']

        if not color_value:
            messages.error(request, "Введите цвет!")
            return render(request, 'analysis_app/analysis_edit_PH.html', context)
        if not transparency_value:
            messages.error(request, "Введите прозрачность!")
            return render(request, 'analysis_app/analysis_edit_PH.html', context)

        # Checking for empty cells in form
        if acid_number_value == '':
            acid_number_value = None

        analysis.description = description,
        analysis.color_value = color_value,
        analysis.transparency_value = transparency_value,
        analysis.BV_CV_value = BV_CV_value,
        analysis.acid_number_value = acid_number_value,
        analysis.flash_rate_value = flash_rate_value,
        analysis.moisture_value = moisture_value,
        analysis.KPC_value = KPC_value,
        analysis.tan_d_value = tan_d_value,
        analysis.ph_value = ph_value,
        analysis.ionol_value = ionol_value,
        analysis.sludge_value = sludge_value,
        analysis.gas_value = gas_value
        analysis.furan_value = furan_value,
        analysis.tan_d_value = tan_d_value,

        analysis.save()
        messages.success(request, 'Анализ успешно обновлен')

        return redirect('index_PH')


def analysis_delete_PH(request, id):
    analysis = oil_PC.objects.get(pk=id)
    analysis.delete()
    messages.success(request, 'Анализ удален!')
    return redirect('index_PH')


def get_mismatches_ph(values, normatives):
    mismatches = []
    limit_pattern = 'pd'
    limit_pattern_2 = "ons"

    values_df = pd.DataFrame(values).filter(like='value').dropna(axis=1)
    normatives_df = pd.DataFrame(normatives).filter(like=f'value_{limit_pattern}')
    normatives_df_ons = pd.DataFrame(normatives).filter(like=f'value_{limit_pattern_2}')

    for i in values_df.columns.unique():
        i = i.rsplit('_', maxsplit=1)[-2]
        current_value = values_df.filter(items=[f'{i}_value'])[f'{i}_value'].max()
        current_normative = normatives_df.filter(items=[f'{i}_limit_value_{limit_pattern}'])[
            f'{i}_limit_value_{limit_pattern}'].max()
        if pd.isna(current_normative):
            current_normative = normatives_df_ons.filter(items=[f'{i}_limit_value_{limit_pattern_2}'])[
                f'{i}_limit_value_{limit_pattern_2}'].max()
        print(f'{i}: {current_value} - {current_normative}')

        if i == 'BV_CV':
            current_value = current_value.replace(',', '.')
            BV, CV = map(float, current_value.split('/'))
            BV_norma, CV_norma = map(float, current_normative.split('/'))
            if BV<BV_norma:
                mismatches.append("BV")
            if CV > CV_norma:
                mismatches.append("CV")
        elif i in ["flash_rate", "ph","ionol"]:
            if current_normative > current_value:
                mismatches.append(i)
        elif i == "color" or i == "transparency":
            continue
        elif current_normative < current_value:
            mismatches.append(i)

    return mismatches

def get_image_file_as_base64_data(filename):
    # path = os.path.normpath(os.path.join(STATIC_ROOT, r'img/logo.png'))
    path = os.path.normpath(os.path.join(STATIC_ROOT, rf'img/{filename}'))
    with open(path, 'rb') as image_file:
        return base64.b64encode(image_file.read()).decode()


def export_pdf_ph(request, id, key):
    analysis = oil_PC.objects.get(pk=id)
    probe_details_info = ProbeDetailsInfo.objects.get(id=analysis.probe_id.id)
    company_info = CompanyDetails.objects.get(company_name='ООО "Сибэнергодиагностика"')

    current_voltage_class = analysis.client.voltage_class.voltage_class
    current_def_type = analysis.client.def_type.def_type
    current_oil_brand = probe_details_info.oil_brand.oil_brand
    current_probe_issue = probe_details_info.probe_issue
    current_normative_document = probe_details_info.test_doc_type.normative_doc.normative_doc

    limit_values = None
    try:
        limit_values = PC_LimitValues.objects.get(
            voltage_class=current_voltage_class,
            def_type=current_def_type,
            oil_brand__contains=[current_oil_brand],
            probe_issue=current_probe_issue,
            normative_doc=current_normative_document,
        )
        print(f'{limit_values.BV_CV_limit_value_ons}')
    except limit_values.ObjectDoesNotExist:
        messages.error(request,
                       f"По данной конфигурации запроса нет подходящих предельных значений. Может быть некорректный {current_normative_document}")
        return redirect('index_PH')

    mismatches = get_mismatches_ph(values=oil_PC.objects.filter(pk=id).values(),
                                   normatives=PC_LimitValues.objects.filter(
                                       voltage_class=current_voltage_class,
                                       def_type=current_def_type,
                                       oil_brand__contains=[current_oil_brand],
                                       probe_issue=current_probe_issue,
                                       normative_doc=current_normative_document
                                   ).values()
                                   )

    print(f'mismatches {mismatches}')

    css = r'report_project_generator/static/css/pdf_style.css'
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename=Analysis {str(datetime.datetime.now())}.pdf'
    response['Content_Transfer-Encoding'] = 'binary'

    env = Environment(loader=FileSystemLoader(r'templates/analysis_app'))

    template = env.get_template('export_pdf_ph.html')

    logo = get_image_file_as_base64_data("logo.png")
    signature = get_image_file_as_base64_data("sign.png")
    stamp = get_image_file_as_base64_data("stamp.png")

    rendered_string = template.render(
        analysis=analysis,
        logo=logo,
        signature=signature,
        stamp=stamp,
        limits=limit_values,
        probe_details_info=probe_details_info,
        mismatches=mismatches,
        company_info=company_info,
        key=key,
    )
    html = HTML(string=rendered_string)
    result = html.write_pdf(stylesheets=[css])
    response.write(result)

    cur_year = datetime.datetime.now().year
    client = str(analysis.client.client_name)
    client = client.replace(" ", "")
    client = client.replace('"', '_')

    pdfs_dir = os.path.join(BASE_DIR, 'pdfs')
    os.makedirs(pdfs_dir, exist_ok=True)
    year_dir = os.path.join(pdfs_dir, f'{cur_year}')
    os.makedirs(year_dir, exist_ok=True)
    client_dir = os.path.join(year_dir, f'{client}')
    os.makedirs(client_dir, exist_ok=True)

    date = str(datetime.datetime.now())
    date = date.replace(":","_")
    filename = os.path.join(client_dir, f'Analysis {date}.pdf')
    with open(filename, 'wb') as file:
        file.write(result)

    return response

    #return redirect('index_PH')
