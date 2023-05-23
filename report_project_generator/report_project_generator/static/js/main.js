const clientsDataBox = document.getElementById('clients-data-box');
const clientInput = document.getElementById('clients');

const serialNumberDataBox = document.getElementById('serial-number-box');
const serialNumberInput = document.getElementById('equipment_serial_numbers');

const equipNameBox = document.getElementById('equip-name-box');
const equipSubstationBox = document.getElementById('equip-substation-box');
const equipTypeBox = document.getElementById('equip-type-box');

const testTypeDataBox = document.getElementById('test-type-data-box');
const oilContainerBox = document.getElementById('oil-container-box');

const equipmentTypeFullBox = document.getElementById('equipment-type-full-box');
const testingPartBox = document.getElementById('testing-part-box');
const transformerDetailsBox = document.getElementById('transformer-details-box');
const defTypeBox = document.getElementById('def-type-box');

const normativeDocBox = document.getElementById('normative-doc-box');

// Переменные для создания блока с информацией по отбору на странице добавления анализа
const probeDeterminationBlock = document.getElementById('probe-determination');

const probeDeterminationBlockPH = document.getElementById('probe-determination-PH');
const selectBottleNumberBox = document.getElementById('select-bottle-number-box');

const inputDateBox = document.getElementById('input-date-box');

const selectSyringeNumberBox = document.getElementById('select-syringe-number-box');
const probeIdBox = document.getElementById('probe-id-box');
const probeIdInputBox = document.getElementById('probe-id-input-box');

const issueBoxes = document.getElementById('dynamic-fields-ph');




if (clientsDataBox){
    $.ajax({
        type: 'GET',
        url: '/clients-json/',
        success: function(response){
    //        console.log(response.data)

            const clientsData = response.data
            console.log('clients data list:', clientsData)
            const unique = [...new Set(clientsData.map(item=>item.client_name))]
            console.log('unique:', unique)

            unique.map(item=>{
                const option = document.createElement('option')
                option.textContent = item
                option.setAttribute('class', 'client-item')
                option.setAttribute('data', item)
                option.setAttribute('data-value', '{{ values.client }}')
                clientsDataBox.appendChild(option)
            })
        },
        error: function(error){
            console.log(error)
        }
    })

    clientsDataBox.addEventListener('change', e=>{
        const selectedClient = e.target.value
        serialNumberDataBox.innerHTML = ""

        $.ajax({
            type: 'GET',
            url: `serial-number-json/${selectedClient}/`,
            success: function(response){
    //            console.log(response.data)
                const serialNumberData = response.data
                serialNumberData.map(item=>{
                    const option = document.createElement('option')
                    const hidden_option = document.createElement('option')

                    hidden_option.textContent = 'Выберите'
                    hidden_option.setAttribute('disabled', true)
                    hidden_option.setAttribute('selected', true)
                    hidden_option.setAttribute('hidden', true)
                    hidden_option.setAttribute('value', null)
                    serialNumberDataBox.appendChild(hidden_option)

                    option.textContent = item.equipment_serial_number
                    option.setAttribute('class', 'serial-num-item')
                    option.setAttribute('data-value', item.equipment_serial_number)
                    serialNumberDataBox.appendChild(option)
                });
            },
            error: function(error){
                console.log(error)
            }
        })

        serialNumberInput.addEventListener("change", function(e) {

            console.log('Значение dropdown зав.ном.:', e.target.value)
            console.log('Значение константы', selectedClient)

            equipNameBox.innerHTML = ""
            equipTypeBox.innerHTML = ""
            equipSubstationBox.innerHTML = ""

            var ClientInfoDict = {};
            ClientInfoDict.serial_num = e.target.value;
            ClientInfoDict.client = selectedClient;
            console.log('Словарь для передачи по json', ClientInfoDict)

            $.ajax({
                type: 'POST',
                url: '/equipment-info-json/',
                data: {'data': JSON.stringify([ClientInfoDict])},
                success: function(data){
                    equipNameBox.innerHTML = ""
                    equipTypeBox.innerHTML = ""
                    equipSubstationBox.innerHTML = ""
                    testingPartBox.innerHTML = ""

                    const equipmentInfo = data.data
                    const equipmentParts = data.parts_data

//                  Внесение массива мест отбора для выкидного списка в зависимости от выбранного оборудования
                    equipmentParts.map(item=>{
                        const hidden_option = document.createElement('option')
                        hidden_option.textContent = 'Выберите'
                        hidden_option.setAttribute('disabled', true)
                        hidden_option.setAttribute('selected', true)
                        hidden_option.setAttribute('hidden', true)
                        hidden_option.setAttribute('value', null)
                        testingPartBox.appendChild(hidden_option)

                        const option = document.createElement('option')
                        option.textContent = item
                        option.setAttribute('class', 'part-item')
                        option.setAttribute('data', item)
                        option.setAttribute('data-value', '{{ values.testing_part }}')
                        testingPartBox.appendChild(option)
                    })

//                  Создание формы проверки "Информация по заказчику"
                    equipmentInfo.map(item=>{
                        const option_1 = document.createElement('li')
                        const option_2 = document.createElement('li')
                        const option_3 = document.createElement('li')

                        option_1.textContent = item.equipment_name
                        option_1.setAttribute('class', 'list-group-item')
                        option_1.setAttribute('data-value', item.equipment_name)
                        equipNameBox.appendChild(option_1)

                        option_2.textContent = item.equipment_type
                        option_2.setAttribute('class', 'list-group-item')
                        option_2.setAttribute('data-value', item.equipment_type)
                        equipTypeBox.appendChild(option_2)

                        option_3.textContent = item.substation_name
                        option_3.setAttribute('class', 'list-group-item')
                        option_3.setAttribute('data-value', item.substation_name)
                        equipSubstationBox.appendChild(option_3)
                    })
                }
            })
        })
    })
}


if (testTypeDataBox){
//  Получаем элементы (типы анализов из БД и создаем с ними поля option)
    $.ajax({
        type: 'GET',
        url: '/probe_details-json/',
        success: function(response){
            const normative_docs = response.normative_docs

            const oilTestTypeData = response.data
            console.log('probes data list:', oilTestTypeData)

            const unique = [...new Set(oilTestTypeData.map(item=>item.test_type))]
            console.log('unique:', unique)

            unique.map(item=>{
                const option = document.createElement('option')
                option.textContent = item
                option.setAttribute('class', 'test-type')
                option.setAttribute('data', item)
                option.setAttribute('data-value', '{{ values.test_type }}')
                testTypeDataBox.appendChild(option)
            });

//          Создание событий связанных с выбором типа проводимых испытаний
            testTypeDataBox.addEventListener('change', e=>{
                console.log('chosen test:', e.target.value)
                const selectedTestType = e.target.value

                oilContainerBox.innerHTML = ""
                normativeDocBox.innerHTML = ""

                const hidden_option = document.createElement('option')
                hidden_option.textContent = 'Выберите'
                hidden_option.setAttribute('disabled', true)
                hidden_option.setAttribute('selected', true)
                hidden_option.setAttribute('hidden', true)
                hidden_option.setAttribute('value', null)
                normativeDocBox.appendChild(hidden_option)

//             Создание списка нормативных документов в зависимости от выбранного типа испытания
                oilTestTypeData.map(item=>{
                    if (item.test_type == selectedTestType) {

                        normative_doc_id = item.normative_doc_id
                        normative_document = normative_docs.filter(d => d.id === normative_doc_id)[0].normative_doc

                        const option = document.createElement('option')
                        option.textContent = normative_document
                        option.setAttribute('class', 'normative-doc-item')
                        option.setAttribute('data', normative_document)
                        option.setAttribute('data-value', '{{ values.normative_doc }}')
                        normativeDocBox.appendChild(option)
                    }
                })

//              Создания поля используемой тары в зависимости от выбранного типа испытания
                if (selectedTestType == 'ХАРГ') {
                    const label = document.createElement('label')
                    label.textContent = '№ шприца'
                    oilContainerBox.appendChild(label)

                    const input = document.createElement('input')
                    input.setAttribute('class', 'form-control-sm ms-5')
                    input.setAttribute('name', 'container_type')
                    input.setAttribute('data-value', '{{ values.container_type }}')
                    oilContainerBox.appendChild(input)
                    }

                else {
                    const label = document.createElement('label')
                    label.textContent = '№ бутылки'
                    oilContainerBox.appendChild(label)

                    const input = document.createElement('input')
                    input.setAttribute('class', 'form-control-sm ms-5')
                    input.setAttribute('name', 'container_type')
                    input.setAttribute('data-value', '{{ values.container_type }}')
                    oilContainerBox.appendChild(input)
                }
            })
        },

        error: function(error){
            console.log(error)
        }

    });
}

// Появление блока с информацией о типе защиты и РПН страницы добавления клиента в зависимости от выбранного оборудования
if (equipmentTypeFullBox) {
    transformerDetailsBox.style.display = "none"
    const savedData = defTypeBox.innerHTML
    equipmentTypeFullBox.addEventListener('change', e=>{
        console.log('Выбранное оборудование:', e.target.value)
        const selectedEquipment = e.target.value

        if (selectedEquipment == 'Трансформатор') {
            transformerDetailsBox.style.display = ""
            defTypeBox.innerHTML = savedData
        }

        else {
            transformerDetailsBox.style.display = "none"
            defTypeBox.innerHTML = ""
        }
    })
}


if (probeDeterminationBlock) {
// TODO Сюда передать все сущности отборов
    $.ajax({
        type: 'GET',
        url: '/probes-json/',
        success: function(response){
            const probesData = response.probes_data
            const clientsData = response.clients_data
            const voltageClassesData = response.voltage_classes
            const oilBrands = response.oil_brands
            const defTypes = response.def_types
            var chosen_date = ''
            var substation_unique = ''
            var client_unique = ''
            console.log('Probes data list:', probesData)
            console.log('Clients data list:', clientsData)

//          Задаем реакцию на выбор даты, как формирование списка со шприцами, использованными в выбранную дату
            inputDateBox.addEventListener('change', e=>{
                selectSyringeNumberBox.innerHTML = ''
                const hidden_option = document.createElement('option')

                hidden_option.textContent = 'Выберите'
                hidden_option.setAttribute('disabled', true)
                hidden_option.setAttribute('selected', true)
                hidden_option.setAttribute('hidden', true)
                hidden_option.setAttribute('value', null)
                selectSyringeNumberBox.appendChild(hidden_option)

                const date_filtered_probes = probesData.filter(d=>d.probe_date === e.target.value)
                const uniqueSyringes = [...new Set(date_filtered_probes.map(item=>item.syringe_num))]

//              Создаем выкидной список со шприцами
                uniqueSyringes.map(item=>{
                    const option = document.createElement('option')

                    option.textContent = item
                    option.setAttribute('class', 'probe-date-item')
                    option.setAttribute('value', item)
                    option.setAttribute('data-value', '{{ values.probe_date }}')
                    selectSyringeNumberBox.appendChild(option)
                })

    //          Отслеживаем событие выбора номера шприца для дальнейшей фильтрации проб
                selectSyringeNumberBox.addEventListener('change', e=>{
                    let elements = document.getElementsByName('li-insert')
                    const syringe_filtered_probe = date_filtered_probes.filter(d=>d.syringe_num === e.target.value)[0]
                    const gain_client = clientsData.filter(d=>d.id === syringe_filtered_probe.tested_client_id)[0]

                    let probe_id_input_field = document.createElement('input')

                    probeIdBox.textContent = 'Проба из отбора ' + syringe_filtered_probe.id

                    probe_id_input_field.textContent = syringe_filtered_probe.id
                    probe_id_input_field.setAttribute('value', syringe_filtered_probe.id)
                    probe_id_input_field.setAttribute('name', 'probe_id')
                    probe_id_input_field.setAttribute('type', 'hidden')
                    probeIdInputBox.appendChild(probe_id_input_field)

                    probeIdBox
//                  Вносим в информационные поля данные из отфильтрованной пробы
                    for (let elem of elements) {
                        elem.innerHTML = '';
                        const data_value = elem.dataset.param.split('~')
                        const li = document.createElement('li')

                        if (data_value[0] === 'client') {
                            li.textContent = gain_client[data_value[1]]
                        } else if (data_value[0] === 'probe') {
                            li.textContent = syringe_filtered_probe[data_value[1]]
                        } else if (data_value[0] === 'voltage'){
                            let voltageClass = voltageClassesData.filter(d=>d.id === gain_client[data_value[1] + '_id'])[0].voltage_class
                            li.textContent = voltageClass
                        } else if (data_value[0] === 'oil'){
                            let oilBrand = oilBrands.filter(d=>d.id === syringe_filtered_probe[data_value[1] + '_id'])[0].oil_brand
                            li.textContent = oilBrand
                        } else if (data_value[0] === 'def'){
                            let defType = defTypes.filter(d=>d.id === gain_client[data_value[1] + '_id'])[0].def_type
                            li.textContent = defType
                        }

                        li.setAttribute('class', 'list-group-item')
                        elem.appendChild(li)
                    }
                })
            });
        }
    })
}

if (probeDeterminationBlockPH) {
    $.ajax({
        type: 'GET',
        url: '/probes-json/',
        success: function(response){
            const probesData = response.probes_data
            const clientsData = response.clients_data
            const voltageClassesData = response.voltage_classes
            const oilBrands = response.oil_brands
            const defTypes = response.def_types

            const testIssues = response.probe_issues

            var chosen_date = ''
            var substation_unique = ''
            var client_unique = ''
            console.log('Probes data list:', probesData)
            console.log('Clients data list:', clientsData)

//          Задаем реакцию на выбор даты, как формирование списка с бутылками, использованными в выбранную дату
            inputDateBox.addEventListener('change', e=>{
                selectBottleNumberBox.innerHTML = ''
                const hidden_option = document.createElement('option')

                hidden_option.textContent = 'Выберите'
                hidden_option.setAttribute('disabled', true)
                hidden_option.setAttribute('selected', true)
                hidden_option.setAttribute('hidden', true)
                hidden_option.setAttribute('value', null)
                selectBottleNumberBox.appendChild(hidden_option)

                const date_filtered_probes = probesData.filter(d=>d.probe_date === e.target.value)
                const uniqueBottles = [...new Set(date_filtered_probes.map(item=>item.bottle_num))]

//              Создаем выкидной список с бутылками
                uniqueBottles.map(item=>{
                    const option = document.createElement('option')

                    option.textContent = item
                    option.setAttribute('class', 'probe-date-item')
                    option.setAttribute('value', item)
                    option.setAttribute('data-value', '{{ values.probe_date }}')
                    selectBottleNumberBox.appendChild(option)
                })

    //          Отслеживаем событие выбора номера бутылки для дальнейшей фильтрации проб
                selectBottleNumberBox.addEventListener('change', e=>{
                    let elements = document.getElementsByName('li-insert')
                    const bottle_filtered_probe = date_filtered_probes.filter(d=>d.bottle_num === e.target.value)[0]
                    probe_issue = testIssues.filter(d=>d.id ===  bottle_filtered_probe.probe_issue_id)[0].probe_issue_type

                    if(probe_issue == 'Плановый'){

                        var div = document.createElement("div");
                        div.setAttribute('class', 'form-group')
                        issueBoxes.appendChild(div)

                        var lbl = document.createElement('label');
                        lbl.innerHTML = "Общее содержание шлама, % массы, не более";
                        div.appendChild(lbl)

                        const input = document.createElement('input')
                        input.setAttribute('class', 'form-control-sm')
                        input.setAttribute('name', 'sludge')
                        input.setAttribute('type', 'number')
                        input.setAttribute('step', '0.001')

                        div.appendChild(input)

                    }

                    if(probe_issue == 'После ремонта'){

                        var div = document.createElement("div");
                        div.setAttribute('class', 'form-group')
                        issueBoxes.appendChild(div)

                        var lbl = document.createElement('label');
                        lbl.innerHTML = "Температура застывания";
                        div.appendChild(lbl)

                        var input = document.createElement('input')
                        input.setAttribute('class', 'form-control-sm')
                        input.setAttribute('name', 'solid')
                        input.setAttribute('type', 'number')
                        input.setAttribute('step', '0.001')
                        div.appendChild(input)

                        var div1 = document.createElement("div");
                        div1.setAttribute('class', 'form-group')
                        issueBoxes.appendChild(div1)

                        var lbl1 = document.createElement('label');
                        lbl1.innerHTML = "стабильность против окисления";
                        div1.appendChild(lbl1)

                        var input1 = document.createElement('input')
                        input1.setAttribute('class', 'form-control-sm')
                        input1.setAttribute('name', 'oxid')
                        input1.setAttribute('type', 'number')
                        input1.setAttribute('step', '0.001')
                        div1.appendChild(input1)

                        var div2 = document.createElement("div");
                        div2.setAttribute('class', 'form-group')
                        issueBoxes.appendChild(div2)

                        var lbl2 = document.createElement('label');
                        lbl2.innerHTML = "содержание серы";
                        div2.appendChild(lbl2)

                        var input2 = document.createElement('input')
                        input2.setAttribute('class', 'form-control-sm')
                        input2.setAttribute('name', 'sulfur')
                        input2.setAttribute('type', 'number')
                        input2.setAttribute('step', '0.001')
                        div2.appendChild(input2)

                        var div3 = document.createElement("div");
                        div3.setAttribute('class', 'form-group')
                        issueBoxes.appendChild(div3)

                        var lbl3 = document.createElement('label');
                        lbl3.innerHTML = "содержание коррозийной серы";
                        div3.appendChild(lbl3)

                        var input3 = document.createElement('input')
                        input3.setAttribute('class', 'form-control-sm')
                        input3.setAttribute('name', 'corrosion')
                        input3.setAttribute('type', 'number')
                        input3.setAttribute('step', '0.001')
                        div3.appendChild(input3)

                    }

                    if(probe_issue == 'Пусконаладочные работы'){
                        var div = document.createElement("div");
                        div.setAttribute('class', 'form-group')
                        issueBoxes.appendChild(div)

                        var lbl = document.createElement('label');
                        lbl.innerHTML = "Температура застывания";
                        div.appendChild(lbl)

                        var input = document.createElement('input')
                        input.setAttribute('class', 'form-control-sm')
                        input.setAttribute('name', 'solid')
                        input.setAttribute('type', 'number')
                        input.setAttribute('step', '0.001')
                        div.appendChild(input)

                        var div1 = document.createElement("div");
                        div1.setAttribute('class', 'form-group')
                        issueBoxes.appendChild(div1)

                        var lbl1 = document.createElement('label');
                        lbl1.innerHTML = "стабильность против окисления";
                        div1.appendChild(lbl1)

                        var input1 = document.createElement('input')
                        input1.setAttribute('class', 'form-control-sm')
                        input1.setAttribute('name', 'oxid')
                        input1.setAttribute('type', 'number')
                        input1.setAttribute('step', '0.001')
                        div1.appendChild(input1)

                    }

                    const gain_client = clientsData.filter(d=>d.id === bottle_filtered_probe.tested_client_id)[0]

                    let probe_id_input_field = document.createElement('input')

                    probeIdBox.textContent = 'Проба из отбора ' + bottle_filtered_probe.id

                    probe_id_input_field.textContent = bottle_filtered_probe.id
                    probe_id_input_field.setAttribute('value', bottle_filtered_probe.id)
                    probe_id_input_field.setAttribute('name', 'probe_id')
                    probe_id_input_field.setAttribute('type', 'hidden')
                    probeIdInputBox.appendChild(probe_id_input_field)

                    probeIdBox
//                  Вносим в информационные поля данные из отфильтрованной пробы
                    for (let elem of elements) {
                        elem.innerHTML = '';
                        const data_value = elem.dataset.param.split('~')
                        const li = document.createElement('li')

                        if (data_value[0] === 'client') {
                            li.textContent = gain_client[data_value[1]]
                        } else if (data_value[0] === 'probe') {
                            li.textContent = bottle_filtered_probe[data_value[1]]
                        } else if (data_value[0] === 'voltage'){
                            let voltageClass = voltageClassesData.filter(d=>d.id === gain_client[data_value[1] + '_id'])[0].voltage_class
                            li.textContent = voltageClass
                        } else if (data_value[0] === 'oil'){
                            let oilBrand = oilBrands.filter(d=>d.id === bottle_filtered_probe[data_value[1] + '_id'])[0].oil_brand
                            li.textContent = oilBrand
                        } else if (data_value[0] === 'def'){
                            let defType = defTypes.filter(d=>d.id === gain_client[data_value[1] + '_id'])[0].def_type
                            li.textContent = defType
                        }

                        li.setAttribute('class', 'list-group-item')
                        elem.appendChild(li)
                    }
                })
            });
        }
    })
}


