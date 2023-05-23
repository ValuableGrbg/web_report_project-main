from django.db import models
# from django.core.exceptions import ValidationError
# from django.utils.translation import gettext_lazy
from datetime import datetime
from django.utils.timezone import now
from django.contrib.auth.models import User
from django.contrib.postgres.fields import IntegerRangeField, ArrayField
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


# Create your models here.
# def status_validator(protocol_status):
#     if protocol_status not in ['сгенерирован', 'не сгенерирован']:
#         raise ValidationError(
#             gettext_lazy('%(protocol_status)s - некорректный статус. Выберите из (сгенерирован, не сгенерирован)'),
#             params={'protocol_status': protocol_status},
#         )


class CompanyDetails(models.Model):
    """Информация об организации, которая проводит испытания"""

    class Meta:
        verbose_name = 'информацию о компании'
        verbose_name_plural = 'информация о компаниях, проводящих испытания'

    company_name = models.CharField(max_length=100, verbose_name='Название организации')
    address = models.CharField(max_length=100, verbose_name='Адрес организации')
    inn = models.CharField(max_length=100, verbose_name='ИНН организации')
    kpp = models.CharField(max_length=100, verbose_name='КПП организации')
    site_url = models.CharField(max_length=100, verbose_name='Ссылка на сайт')
    email = models.CharField(max_length=100, verbose_name='E-mail организации')
    telephone = models.CharField(max_length=100, verbose_name='Телефон организации')
    accreditation_certificate = models.CharField(max_length=150, default='-', verbose_name='Аттестат аккредитации')

    def __str__(self):
        return f'{self.company_name}'


class OilBrandInfo(models.Model):
    """Информация о марках масла"""

    class Meta:
        verbose_name = 'марку масла'
        verbose_name_plural = 'марки масел'

    oil_brand = models.CharField(max_length=100, verbose_name='Марка масла')

    def __str__(self):
        return f'{self.oil_brand}'


class EquipmentAndTestingPart(models.Model):
    """Виды оборудования и соответствующие места отбора масла"""

    class Meta:
        verbose_name = 'оборудование и место отбора'
        verbose_name_plural = 'оборудования и места отбора'

    equipment_type_full = models.CharField(max_length=100, verbose_name='Вид оборудования')
    testing_part = models.CharField(max_length=100, verbose_name='Место отбора')

    def __str__(self):
        return f'{self.equipment_type_full}, место отбора: {self.testing_part}'


class TransformerDefTypes(models.Model):
    """Типы защит трансформаторного масла от воздействий окружающей среды"""

    class Meta:
        verbose_name = 'тип защиты'
        verbose_name_plural = 'типы защиты'

    def_type = models.CharField(max_length=100, verbose_name='Тип защиты')

    def __str__(self):
        return f'{self.def_type}'


class RpnTypeInfo(models.Model):
    """Информация о типах РПН трансформатора"""

    class Meta:
        verbose_name = 'тип РПН'
        verbose_name_plural = 'типы РПН'

    rpn_type = models.CharField(max_length=100, verbose_name='Тип РПН')

    def __str__(self):
        return f'{self.rpn_type}'


class EquipmentVoltageClasses(models.Model):
    """Информация о классах напряжения оборудования"""

    class Meta:
        verbose_name = 'класс напряжения'
        verbose_name_plural = 'классы напряжения'

    voltage_class = models.IntegerField(verbose_name='Класс напряжения, кВ', default=0)

    def __str__(self):
        return f'{self.voltage_class}'


class client_equipment(models.Model):
    """Заказчик и его оборудование"""

    class Meta:
        verbose_name = 'заказчик и его оборудование'
        verbose_name_plural = 'заказчики и их оборудование'

    client_name = models.CharField(max_length=100, verbose_name='Наименование организации-заказчика')
    substation_name = models.CharField(max_length=100, verbose_name='Наименование подстанции')
    equipment_type_full = models.CharField(max_length=100, verbose_name='Вид оборудования')
    voltage_class = models.ForeignKey(
        to=EquipmentVoltageClasses,
        on_delete=models.RESTRICT,
        verbose_name='Класс напряжения',
        default=None
    )
    equipment_power = models.IntegerField(verbose_name='Мощность трансформатора, МВт', default=0)
    equipment_name = models.CharField(max_length=100, verbose_name='Диспетчерское наименование оборудования')
    equipment_serial_number = models.CharField(max_length=100, verbose_name='Заводской номер')
    equipment_type = models.CharField(max_length=100, verbose_name='Тип оборудования')
    def_type = models.ForeignKey(to=TransformerDefTypes, on_delete=models.RESTRICT, verbose_name='Тип защиты', default=None)
    rpn_type = models.ForeignKey(to=RpnTypeInfo, on_delete=models.RESTRICT, verbose_name='Тип РПН', default=None)
    production_year = models.PositiveIntegerField(
        validators=[
            MinValueValidator(1900),
            MaxValueValidator(datetime.now().year)],
        help_text="Год в формате: YYYY",
        verbose_name='Год изготовления',
        default=None,
        null=True
    )
    setting_year = models.PositiveIntegerField(
        validators=[
            MinValueValidator(1900),
            MaxValueValidator(datetime.now().year)],
        help_text="Год в формате: YYYY",
        verbose_name='Год установки',
        default=None,
        null=True
    )
    usage_years = models.IntegerField(verbose_name='Число лет использования', default=0)


    def __str__(self):
        return f'{self.id}. {self.client_name} - {self.equipment_name}'


class OilNormativeDocs(models.Model):
    """Нормативные документы"""

    class Meta:
        verbose_name = 'Нормативный документ'
        verbose_name_plural = 'Нормативные документы'

    normative_doc = models.CharField(max_length=100, verbose_name='Нормативный документ')


    def __str__(self):
        return f'{self.normative_doc}'


class OilTestTypesInfo(models.Model):
    """Информация о типах проводимых испытаний и соответствующих НТД"""

    class Meta:
        verbose_name = 'информацию о типах проводимых испытаний'
        verbose_name_plural = 'информация о типах проводимых испытаний'

    test_type = models.CharField(max_length=20, verbose_name='Название испытания')
    normative_doc = models.ForeignKey(to=OilNormativeDocs, on_delete=models.RESTRICT, verbose_name='Нормативный документ')
    # equipment_type
    # limit_values

    def __str__(self):
        return f'{self.test_type}, НД: {self.normative_doc}'


class OilProbesIssues(models.Model):
    """Причины проведения испытаний масла"""

    class Meta:
        verbose_name = 'причину проведения испытаний'
        verbose_name_plural = 'причины проведения испытаний'

    probe_issue_type = models.CharField(max_length=20, verbose_name='Название причины испытания масла')

    def __str__(self):
        return f'{self.probe_issue_type}'


class ProbeDetailsInfo(models.Model):
    """Информация об отборе"""

    class Meta:
        verbose_name = 'информацию об отборе'
        verbose_name_plural = 'Информация об отборе'

    tester_name = models.ForeignKey(to=User, on_delete=models.RESTRICT, verbose_name='Производивший отбор', default=None)
    tested_client = models.ForeignKey(to=client_equipment, on_delete=models.RESTRICT, verbose_name='Заказчик', default=None)
    probe_date = models.DateField(default=now, verbose_name='Дата отбора')
    bottle_num = models.CharField(max_length=20, verbose_name='Номер бутылки')
    syringe_num = models.CharField(max_length=20, verbose_name='Номер шприца', default=None)
    test_doc_type = models.ForeignKey(to=OilTestTypesInfo, on_delete=models.RESTRICT, verbose_name='Вид испытания', default=None)
    atm_temperature = models.CharField(max_length=20, verbose_name='Температура окружающей среды')
    oil_temperature = models.CharField(max_length=20, verbose_name='Температура масла')
    oil_brand = models.ForeignKey(to=OilBrandInfo, on_delete=models.RESTRICT, verbose_name='Марка масла')
    load_value = models.CharField(max_length=20, verbose_name='Нагрузка во время отбора')
    testing_part = models.CharField(max_length=100, verbose_name='Место отбора', default=None)
    probe_issue = models.ForeignKey(to=OilProbesIssues, on_delete=models.RESTRICT, verbose_name='Причина отбора', default=None)


    def __str__(self):
        return f'{self.probe_date.strftime("%d.%m.%Y")}| {self.tested_client.client_name}: {self.tested_client.substation_name}, {self.tested_client.equipment_name}'


class analysis_results(models.Model):
    """Результаты анализов"""

    class Meta:
        ordering: ['-date']
        verbose_name = 'Проведенные анализы'
        verbose_name_plural = 'Проведенные анализы'

    analysis_date = models.DateField(default=now, verbose_name='Дата проведения анализа')
    delivery_date = models.DateField(default=now, verbose_name='Дата доставки пробы в лабораторию')
    probe_id = models.ForeignKey(to=ProbeDetailsInfo, on_delete=models.RESTRICT, verbose_name='Проба из отбора', default=None)
    probe_code = models.CharField(max_length=30, verbose_name='Шифр пробы', default=None)
    description = models.TextField(null=True, blank=True, max_length=266, verbose_name='Заметки')
    employee = models.ForeignKey(to=User, on_delete=models.RESTRICT, verbose_name='Работник')
    client = models.ForeignKey('client_equipment', on_delete=models.RESTRICT, verbose_name='Заказчик - оборудование')
    chromotograph = models.ForeignKey('devices', on_delete=models.RESTRICT, verbose_name='Идентификатор диагностирующего хроматографа')
    H2_value = models.FloatField(max_length=12, verbose_name='Водород')
    CH4_value = models.FloatField(max_length=12, verbose_name='Метан')
    C2H4_value = models.FloatField(max_length=12, verbose_name='Этилен')
    C2H6_value = models.FloatField(max_length=12, verbose_name='Этан')
    C2H2_value = models.FloatField(max_length=12, verbose_name='Ацетилен')
    CO2_value = models.FloatField(max_length=12, verbose_name='Диоксид углерода')
    CO_value = models.FloatField(null=True, blank=True, max_length=12, verbose_name='Оксид углерода')
    N2_O2_value = models.FloatField(null=True, blank=True, max_length=12, verbose_name='ОГС')
    SRG_value = models.FloatField(null=True, blank=True, max_length=12, verbose_name='СРГ')
    protocol_code = models.CharField(max_length=50, verbose_name='Шифр протокола', default=0)
    test_condition_temp = models.FloatField(max_length=4, verbose_name='Температура помещения, °C', default=None)
    test_condition_humidity = models.FloatField(max_length=4, verbose_name='Влажность, %', default=None)
    test_condition_pressure = models.FloatField(max_length=4, verbose_name='Давление, мм.рт.ст.', default=None)

    def __str__(self):
        return f'{self.analysis_date}: {self.client}'


class devices(models.Model):
    """Диагностирующее оборудование"""

    class Meta:
        verbose_name = 'Диагностирующее оборудование'
        verbose_name_plural = 'Диагностирующее оборудование'

    device_name = models.TextField(max_length=100, verbose_name='Наименование оборудования')
    device_type = models.CharField(max_length=100, verbose_name='Тип оборудования')
    device_serial_number = models.IntegerField(verbose_name='Серийный номер хроматографа', default=None)
    device_certification_number = models.CharField(max_length=100, verbose_name='Свидетельство о поверке')
    device_precision = models.CharField(max_length=150, verbose_name='Погрешность измерений', default=None)
    next_device_certification_date = models.DateField(verbose_name='Дата следующей поверки', null=True)

    def __str__(self):
        return f'{self.device_name} - {self.device_serial_number}'


class analysis_info(models.Model):
    """Информация об анализах"""

    class Meta:
        verbose_name = 'Информация об анализах'
        verbose_name_plural = 'Информация об анализах'

    statuses = (('generated', 'сгенерирован'),
                ('not generated', 'не сгенерирован'))

    protocol_name = models.CharField(max_length=100, verbose_name='Наименование протокола')
    created_date = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True)
    updated_date = models.DateTimeField(verbose_name='Последнее изменение', auto_now=True)
    protocol_status = models.CharField(max_length=100, verbose_name='Статус данного протокола', choices=statuses)
    fk_client_equipment_id = models.ForeignKey(
        'client_equipment',
        default=None,
        on_delete=models.RESTRICT,
        verbose_name='Идентификатор диагностируемого оборудования'
    )

    fk_devices_id = models.ForeignKey(
        'devices',
        default=None,
        on_delete=models.RESTRICT,
        verbose_name='Идентификатор диагностирующего хроматографа'
    )

    def save(self, *args, **kwargs):
        self.updated_date = datetime.now()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.protocol_name


class ChargTransformersLimitValues_35_500(models.Model):
    """Предельные концентрации газов для трансформаторов класса напряжения 35-500 кВ"""

    class Meta:
        verbose_name = 'Предельные концентрации газов трансформаторов 35-500 кВ'
        verbose_name_plural = 'Предельная концентрация газов трансформаторов 35-500 кВ'

    normative_doc = models.CharField(max_length=100, verbose_name='Наименование НТД')
    voltage_class = models.IntegerField(verbose_name='Класс напряжения')
    def_type = models.CharField(max_length=100, verbose_name='Тип защиты')
    years_periods_include = IntegerRangeField()
    SRG_limit_value_pdz = models.FloatField(null=True, blank=True)
    H2_limit_value_pdz = models.FloatField(null=True, blank=True)
    CH4_limit_value_pdz = models.FloatField(null=True, blank=True)
    C2H6_limit_value_pdz = models.FloatField(null=True, blank=True)
    C2H4_limit_value_pdz = models.FloatField(null=True, blank=True)
    C2H2_limit_value_pdz = models.FloatField(null=True, blank=True)
    CO_limit_value_pdz = models.FloatField(null=True, blank=True)
    CO2_limit_value_pdz = models.FloatField(null=True, blank=True)
    SRG_limit_value_dz = models.FloatField(null=True, blank=True)
    H2_limit_value_dz = models.FloatField(null=True, blank=True)
    CH4_limit_value_dz = models.FloatField(null=True, blank=True)
    C2H6_limit_value_dz = models.FloatField(null=True, blank=True)
    C2H4_limit_value_dz = models.FloatField(null=True, blank=True)
    C2H2_limit_value_dz = models.FloatField(null=True, blank=True)
    CO_limit_value_dz = models.FloatField(null=True, blank=True)
    CO2_limit_value_dz = models.FloatField(null=True, blank=True)
    oil_brand = ArrayField(models.CharField(max_length=50))
    rpn_type = ArrayField(models.CharField(max_length=50))
    equipment_power = IntegerRangeField()

    def __str__(self):
        return f'Transformer limit id {self.id}: \n' \
               f'voltage_class: {self.voltage_class} \n' \
               f'normative_doc: {self.normative_doc}'

class oil_PC(models.Model):
    """физико-химическое испытание масла"""

    class Meta:
        ordering: ['-date']
        verbose_name = 'Проведенные анализы ФХ'
        verbose_name_plural = 'Проведенные анализы ФХ'

    analysis_date = models.DateField(default=now, verbose_name='Дата проведения анализа')
    delivery_date = models.DateField(default=now, verbose_name='Дата доставки пробы в лабораторию')
    probe_id = models.ForeignKey(to=ProbeDetailsInfo, on_delete=models.RESTRICT, verbose_name='Проба из отбора',
                                 default=None)
    probe_code = models.CharField(max_length=30, verbose_name='Шифр пробы', default=None)
    description = models.TextField(null=True, blank=True, max_length=266, verbose_name='Заметки')
    employee = models.ForeignKey(to=User, on_delete=models.RESTRICT, verbose_name='Работник')
    client = models.ForeignKey('client_equipment', on_delete=models.RESTRICT, verbose_name='Заказчик - оборудование')

    color_value = models.TextField(max_length=25, verbose_name='Цвет')
    transparency_value = models.TextField(max_length=25, verbose_name='Прозрачность')
    BV_CV_value = models.TextField(null=True, blank=True, max_length=12, verbose_name='Пробивное напряжение/коэффициент')
    acid_number_value = models.FloatField(null=True, blank=True, max_length=12, verbose_name='Кислотное число')
    flash_rate_value = models.TextField(null=True, blank=True, max_length=12, verbose_name='Темп вспышки')
    moisture_value = models.FloatField(null=True, blank=True, max_length=12, verbose_name='Влагосодержание')
    KPC_value = models.FloatField(null=True, blank=True, max_length=12, verbose_name='КПЧ')
    tan_d_value = models.FloatField(null=True, blank=True, max_length=12, verbose_name='тангенс d')
    ph_value = models.FloatField(null=True, blank=True, max_length=12, verbose_name='кисл и щелч')
    ionol_value = models.FloatField(null=True, blank=True, max_length=12, verbose_name='ионол')
    gas_value = models.FloatField(null=True, blank=True, max_length=12, verbose_name='газосодержание')
    furan_value = models.FloatField(null=True, blank=True, max_length=12, verbose_name='фуран')

    sludge_value = models.FloatField(null=True, blank=True, max_length=12, verbose_name='общее содержание шлама')
    solidification_value = models.IntegerField(null=True, blank=True, verbose_name='Температура застывания')
    oxidation_stability_value = models.FloatField(null=True, blank=True, max_length=12, verbose_name='стабильность против окисления')
    sulfur_value = models.FloatField(null=True, blank=True, max_length=12, verbose_name='содержание серы')
    corrosive_sulfur_value = models.FloatField(null=True, blank=True, max_length=12, verbose_name='содержание коррозийной серы')

    protocol_code = models.CharField(max_length=50, verbose_name='Шифр протокола', default=0)
    test_condition_temp = models.TextField(max_length=4, verbose_name='Температура помещения, °C', default=None)
    test_condition_humidity = models.TextField(max_length=4, verbose_name='Влажность, %', default=None)
    test_condition_pressure = models.TextField(max_length=4, verbose_name='Давление, мм.рт.ст.', default=None)

    def __str__(self):
        return f'{self.analysis_date}: {self.client}'


class PC_LimitValues(models.Model):
    """Предельные значения ФХ анализа"""

    class Meta:
        verbose_name = 'Предельные значения ФХ анализа'
        verbose_name_plural = 'Предельные значения ФХ анализа'

    probe_issue = models.ForeignKey(to=OilProbesIssues, on_delete=models.RESTRICT, verbose_name='Причина отбора', default=None)
    normative_doc = models.CharField(max_length=100, verbose_name='Наименование НТД')
    voltage_class = models.IntegerField(verbose_name='Класс напряжения')
    def_type = models.CharField(max_length=100, verbose_name='Тип защиты')
    oil_brand = ArrayField(models.CharField(max_length=50), verbose_name='Марка масла')

    color_limit_value_pd = models.CharField(max_length=25, verbose_name='Цвет', null=True, blank=True)
    color_limit_value_ons = models.CharField(max_length=25, verbose_name='Цвет', null=True, blank=True)

    transparency_limit_value_pd = models.CharField(max_length=25, verbose_name='Прозрачность', null=True, blank=True)
    transparency_limit_value_ons = models.CharField(max_length=25, verbose_name='Прозрачность', null=True, blank=True)

    BV_CV_limit_value_ons = models.CharField(max_length=100, null=True, blank=True)
    BV_CV_limit_value_pd = models.CharField(max_length=100, null=True, blank=True)

    acid_number_limit_value_ons = models.FloatField(null=True, blank=True)
    acid_number_limit_value_pd = models.FloatField(null=True, blank=True)

    flash_rate_limit_value_ons = models.CharField(max_length=100, null=True, blank=True)
    flash_rate_limit_value_pd = models.CharField(max_length=100, null=True, blank=True)

    moisture_limit_value_ons = models.FloatField(null=True, blank=True)
    moisture_limit_value_pd = models.FloatField(null=True, blank=True)

    KPC_limit_value_ons = models.IntegerField(null=True, blank=True)
    KPC_limit_value_pd = models.IntegerField(null=True, blank=True)

    tan_d_limit_value_ons = models.FloatField(null=True, blank=True)
    tan_d_limit_value_pd = models.FloatField(null=True, blank=True)

    ph_limit_value_ons = models.FloatField(null=True, blank=True)
    ph_limit_value_pd = models.FloatField(null=True, blank=True)

    ionol_limit_value_ons = models.FloatField(null=True, blank=True)
    ionol_limit_value_pd = models.FloatField(null=True, blank=True)

    gas_limit_value_ons = models.FloatField(null=True, blank=True)
    gas_limit_value_pd = models.FloatField(null=True, blank=True)

    furan_limit_value_ons = models.FloatField(null=True, blank=True)
    furan_limit_value_pd = models.FloatField(null=True, blank=True)

    sludge_limit_value_ons = models.FloatField(null=True, blank=True)
    sludge_limit_value_pd = models.FloatField(null=True, blank=True)

    solidification_limit_value_ons = models.IntegerField(null=True, blank=True)
    solidification_limit_value_pd = models.IntegerField(null=True, blank=True)

    oxidation_stability_limit_value_ons = models.FloatField(null=True, blank=True)
    oxidation_stability_limit_value_pd = models.FloatField(null=True, blank=True)

    sulfur_limit_value_ons = models.FloatField(null=True, blank=True)
    sulfur_limit_value_pd = models.FloatField(null=True, blank=True)

    corrosive_sulfur_limit_value_ons = models.FloatField(null=True, blank=True)
    corrosive_sulfur_limit_value_pd = models.FloatField(null=True, blank=True)


    def __str__(self):
        return f'Transformer PC limit id {self.id}: \n' \
               f'voltage_class: {self.voltage_class} \n' \
               f'normative_doc: {self.normative_doc}'
