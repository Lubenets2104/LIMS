from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
import json
from datetime import date
from .forms import TestSampleForm
from .models import TestSample, GOST, MixName, Indicator, TestResult, AsphaltTestResult, ShchPSTestResult, AsphaltCoreTestResult, Crushed8267TestResult, UserProfile
# Безопасный импорт дополнительных моделей
try:
    from .models_extra import BitumenTestResult33133, EmulsionTestResult, MineralPowderTestResult
    EXTRA_MODELS_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ Не удалось импортировать дополнительные модели: {e}")
    EXTRA_MODELS_AVAILABLE = False
    # Создаем заглушки для моделей
    class BitumenTestResult33133:
        pass
    class EmulsionTestResult:
        pass
    class MineralPowderTestResult:
        pass

# Test view for JavaScript debugging
def test_js(request):
    return render(request, 'labtests/test_js.html')

# Debug view
def debug_data(request, pk):
    sample = get_object_or_404(TestSample, pk=pk)
    test_result, created = TestResult.objects.get_or_create(sample=sample)
    return render(request, 'labtests/debug_data.html', {
        'sample': sample,
        'test_result': test_result
    })

@login_required
def sample_list(request):
    # Показываем только образцы текущего пользователя
    samples = TestSample.objects.select_related('material', 'gost', 'mix').filter(
        owner=request.user
    ).order_by('-id')
    return render(request, 'labtests/sample_list.html', {'samples': samples})

@login_required
def add_sample(request):
    if request.method == 'POST':
        form = TestSampleForm(request.POST)
        if form.is_valid():
            sample = form.save(commit=False)
            sample.status = 'in_progress'  # Автоматически устанавливаем статус "В работе"
            sample.owner = request.user  # Привязываем образец к текущему пользователю
            sample.save()
            form.save_m2m()  # Сохраняем many-to-many связи (indicators)
            return redirect('sample_list')
        else:
            # Форма не валидна, но данные сохраняются в form.data
            # ВАЖНО: Восстанавливаем queryset'ы для зависимых полей
            # чтобы форма правильно отобразила введенные значения
            
            # Восстанавливаем queryset для gost на основе выбранного материала
            if 'material' in request.POST:
                try:
                    material_id = int(request.POST.get('material'))
                    form.fields['gost'].queryset = GOST.objects.filter(material_id=material_id)
                    
                    # Восстанавливаем queryset для mix и indicators на основе выбранного ГОСТ
                    if 'gost' in request.POST:
                        gost_id = int(request.POST.get('gost'))
                        form.fields['mix'].queryset = MixName.objects.filter(gost_id=gost_id)
                        form.fields['indicators'].queryset = Indicator.objects.filter(gost_id=gost_id)
                        
                        # Проверяем наличие смесей и делаем поле обязательным если они есть
                        if form.fields['mix'].queryset.exists():
                            form.fields['mix'].required = True
                except (ValueError, TypeError):
                    pass
            
            # Передаем все данные POST в контекст для JavaScript
            # чтобы он мог восстановить состояние полей
            form.preserve_data = True
            
            # Добавляем выбранные показатели в контекст
            form.selected_indicators = request.POST.getlist('indicators')
            
    else:
        form = TestSampleForm()
    return render(request, 'labtests/add_sample.html', {'form': form})

# AJAX Views
def load_gosts(request):
    material_id = request.GET.get('material_id')
    gosts = GOST.objects.filter(material_id=material_id).order_by('number')
    return JsonResponse(list(gosts.values('id', 'number')), safe=False)

def load_mixes(request):
    gost_id = request.GET.get('gost_id')
    mixes = MixName.objects.filter(gost_id=gost_id).order_by('name')
    return JsonResponse(list(mixes.values('id', 'name')), safe=False)

def load_indicators(request):
    gost_id = request.GET.get('gost_id')
    indicators = Indicator.objects.filter(gost_id=gost_id).order_by('name')
    return JsonResponse(list(indicators.values('id', 'name')), safe=False)

# Delete sample
@require_POST
def delete_sample(request, pk):
    sample = get_object_or_404(TestSample, pk=pk)
    sample.delete()
    return JsonResponse({'status': 'success'})

# Update sample status
@require_POST
def update_sample_status(request, pk):
    sample = get_object_or_404(TestSample, pk=pk)
    data = json.loads(request.body)
    new_status = data.get('status')
    
    if new_status in ['draft', 'in_progress', 'completed']:
        sample.status = new_status
        sample.save()
        return JsonResponse({'status': 'success'})
    
    return JsonResponse({'status': 'error', 'message': 'Invalid status'}, status=400)

# Test form view (for 'in_progress' status)
def sample_test_form(request, pk):
    sample = get_object_or_404(TestSample, pk=pk)
    
    # ВАЖНО: Сначала проверяем битум, потом все остальное!
    # Определяем тип материала и перенаправляем на соответствующую форму
    material_name = sample.material.name.lower() if sample.material else ''
    gost_number = sample.gost.number.lower() if sample.gost else ''
    mix_name = sample.mix.name.lower() if sample.mix else ''
    
    print(f"\n=== ОПРЕДЕЛЕНИЕ ТИПА МАТЕРИАЛА ===")
    print(f"Образец ID: {pk}")
    print(f"Материал: {sample.material.name if sample.material else 'None'}")
    print(f"ГОСТ: {sample.gost.number if sample.gost else 'None'}")
    print(f"Смесь/Марка: {sample.mix.name if sample.mix else 'None'}")
    print(f"Материал (lowercase): {material_name}")
    
    # Первым делом проверяем минеральный порошок
    if 'минеральный порошок' in material_name or 'минеральный' in material_name or 'порошок' in material_name or '32761' in gost_number:
        # Для минерального порошка
        print("Определен как: МИНЕРАЛЬНЫЙ ПОРОШОК")
        print("Перенаправляем на форму минерального порошка")
        print("===\n")
        return mineral_powder_test_form(request, pk)
    # Потом проверяем эмульсию
    elif 'эмульсия' in material_name or 'эмульс' in material_name or 'emulsion' in material_name or '58952' in gost_number:
        # Для эмульсии
        print("Определен как: ЭМУЛЬСИЯ")
        print("Перенаправляем на форму эмульсии")
        print("===\n")
        return emulsion_test_form(request, pk)
    # Потом проверяем битум (проверяем и материал, и ГОСТ, и марку)
    elif 'битум' in material_name or 'bitum' in material_name or '33133' in gost_number or 'бнд' in mix_name:
        # Для битума
        print("Определен как: БИТУМ")
        print("Перенаправляем на форму битума")
        print("===\n")
        return bitumen_test_form(request, pk)
    elif 'керн' in material_name or 'kern' in material_name:
        # Для кернов из асфальтобетона
        print("Определен как: КЕРНЫ ИЗ АСФАЛЬТОБЕТОНА")
        print("Перенаправляем на форму кернов")
        print("===\n")
        return asphalt_core_test_form(request, pk)
    elif 'асфальт' in material_name or 'asphalt' in material_name:
        # Для обычного асфальтобетона
        print("Определен как: АСФАЛЬТОБЕТОН")
        print("Перенаправляем на форму асфальтобетона")
        print("===\n")
        test_result, created = AsphaltTestResult.objects.get_or_create(sample=sample)
        return asphalt_test_form(request, pk)
    elif 'щпс' in material_name or 'shchps' in material_name or 'щебень' in material_name or 'shcheben' in material_name:
        # Для ЩПС и щебня используем отдельную view функцию, которая уже определит правильную модель по ГОСТ
        print("Определен как: ЩПС или ЩЕБЕНЬ")
        print("Перенаправляем на форму ЩПС/Щебень (будет выбрана по ГОСТ)")
        print("===\n")
        return shchps_test_form(request, pk)
    else:
        # Для песка и других материалов используем стандартную модель TestResult
        print("Определен как: ПЕСОК или другой материал")
        print("Используем стандартную форму для песка")
        print("===\n")
        test_result, created = TestResult.objects.get_or_create(sample=sample)
    
    # Отладочный вывод загружаемых данных
    print(f"\n=== ЗАГРУЗКА ФОРМЫ для образца {pk} ===")
    print(f"TestResult создан: {created}")
    print(f"TestResult ID: {test_result.id if test_result else 'None'}")
    
    if test_result:
        print(f"grain_initial_weight: {test_result.grain_initial_weight}")
        print(f"grain_8_weight: {test_result.grain_8_weight}")
        print(f"grain_4_weight: {test_result.grain_4_weight}")
        print(f"grain_8_percent: {test_result.grain_8_percent}")
        print(f"grain_4_percent: {test_result.grain_4_percent}")
    else:
        print("TestResult is None!")
    print("===")
    
    if request.method == 'POST':
        # Обработка AJAX автосохранения
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest' or request.POST.get('action') == 'autosave':
            print(f"=== АВТОСОХРАНЕНИЕ для образца {pk} ===")
            
            # Используем ту же логику сохранения
            save_test_result(request, test_result, sample)
            
            return JsonResponse({
                'status': 'success',
                'message': 'Данные автоматически сохранены'
            })
        
        # Обычное сохранение через кнопку
        if request.POST.get('action') == 'save':
            print(f"=== НАЧАЛО СОХРАНЕНИЯ для образца {pk} ===")
            
            save_test_result(request, test_result, sample)
            
            return redirect('sample_list')
    
    return render(request, 'labtests/sample_test_form.html', {
        'sample': sample,
        'test_result': test_result
    })

# Выносим логику сохранения в отдельную функцию
def save_test_result(request, test_result, sample):
            
            # Полный список всех полей модели TestResult для сохранения
            fields_mapping = {
                # Класс результата
                'result_class': str,
                
                # Зерновой состав и модуль крупности
                'grain_initial_weight': float,
                'grain_8_weight': float,
                'grain_4_weight': float,
                'grain_8_percent': float,
                'grain_4_percent': float,
                
                # Пылевидные и глинистые частицы
                'dust_initial_weight': float,
                'dust_after_weight': float,
                'dust_percent': float,
                
                # Зерновой состав (сита)
                'sieve_2_weight': float,
                'sieve_1_weight': float,
                'sieve_05_weight': float,
                'sieve_025_weight': float,
                'sieve_0125_weight': float,
                'sieve_2_partial': float,
                'sieve_1_partial': float,
                'sieve_05_partial': float,
                'sieve_025_partial': float,
                'sieve_0125_partial': float,
                'sieve_2_full': float,
                'sieve_1_full': float,
                'sieve_05_full': float,
                'sieve_025_full': float,
                'sieve_0125_full': float,
                
                # Модуль крупности
                'size_module_value': float,
                'size_module_name': str,
                
                # Глина в комках
                'clay_initial_weight': float,
                'clay_weight': float,
                'clay_percent': float,
                
                # Влажность
                'humidity_1_number': str,
                'humidity_1_container': float,
                'humidity_1_with_sand': float,
                'humidity_1_after_dry': float,
                'humidity_1_value': float,
                'humidity_2_number': str,
                'humidity_2_container': float,
                'humidity_2_with_sand': float,
                'humidity_2_after_dry': float,
                'humidity_2_value': float,
                'humidity_average': float,
                
                # Набухание глинистых частиц
                'clay_swell_1_number': str,
                'clay_swell_1_initial': float,
                'clay_swell_1_after': float,
                'clay_swell_1_k': float,
                'clay_swell_2_number': str,
                'clay_swell_2_initial': float,
                'clay_swell_2_after': float,
                'clay_swell_2_k': float,
                'clay_swell_average_k': float,
                'clay_swell_content': float,
                'clay_swell_conclusion': str,
                
                # Насыпная плотность
                'bulk_1_volume': float,
                'bulk_1_empty': float,
                'bulk_1_full': float,
                'bulk_1_density': float,
                'bulk_2_volume': float,
                'bulk_2_empty': float,
                'bulk_2_full': float,
                'bulk_2_density': float,
                'bulk_average_density': float,
                
                # Истинная плотность
                'actual_1_number': str,
                'actual_1_empty': float,
                'actual_1_water': float,
                'actual_1_sand': float,
                'actual_1_full': float,
                'actual_1_density': float,
                'actual_2_number': str,
                'actual_2_empty': float,
                'actual_2_water': float,
                'actual_2_sand': float,
                'actual_2_full': float,
                'actual_2_density': float,
                'actual_average_density': float,
                
                # Пустотность
                'emptiness': float
            }
            
            # Сохраняем все поля с улучшенной обработкой
            saved_data = {}
            errors = []
            
            for field_name, field_type in fields_mapping.items():
                # Получаем значение из POST запроса
                # Так как скрытые поля теперь имеют те же имена что и в базе,
                # просто берем значение по имени поля
                final_value = request.POST.get(field_name, '')
                
                # Для отладки выводим все значения
                if final_value:
                    print(f"Поле {field_name}: значение='{final_value}'")
                else:
                    # Если поле пустое, пробуем получить из всех данных POST
                    all_post_data = dict(request.POST)
                    for key in all_post_data:
                        if field_name in key:
                            print(f"Найдено похожее поле: {key} = {all_post_data[key]}")
                    print(f"Поле {field_name}: пусто")
                
                # Обработка типов данных
                if field_type == float:
                    try:
                        processed_value = float(final_value) if final_value else None
                    except (ValueError, TypeError):
                        processed_value = None
                        if final_value:  # Только если значение не пустое
                            errors.append(f"Неверный формат числа в поле {field_name}: {final_value}")
                elif field_type == str:
                    processed_value = str(final_value) if final_value else ''
                else:
                    processed_value = final_value
                
                # ВАЖНО: Не перезаписываем существующие значения пустыми
                # Исключение: если это поле ввода (не readonly), то сохраняем пустое значение
                # чтобы пользователь мог очистить поле, если нужно
                readonly_fields = [
                    'grain_8_percent', 'grain_4_percent', 'dust_percent',
                    'sieve_2_partial', 'sieve_1_partial', 'sieve_05_partial', 'sieve_025_partial', 'sieve_0125_partial',
                    'sieve_2_full', 'sieve_1_full', 'sieve_05_full', 'sieve_025_full', 'sieve_0125_full',
                    'size_module_value', 'size_module_name', 'clay_percent',
                    'humidity_1_value', 'humidity_2_value', 'humidity_average',
                    'clay_swell_1_k', 'clay_swell_2_k', 'clay_swell_average_k',
                    'clay_swell_content', 'clay_swell_conclusion',
                    'bulk_1_density', 'bulk_2_density', 'bulk_average_density',
                    'actual_1_density', 'actual_2_density', 'actual_average_density',
                    'emptiness'
                ]
                
                if field_name in readonly_fields:
                    # Для readonly полей: не перезаписываем существующие значения пустыми
                    if processed_value is None or processed_value == '':
                        existing_value = getattr(test_result, field_name)
                        if existing_value is not None and existing_value != '':
                            processed_value = existing_value
                            print(f"Сохраняем существующее readonly значение для {field_name}: {existing_value}")
                # Для остальных полей - пользователь может сознательно очистить их
                
                # Устанавливаем значение в модель
                setattr(test_result, field_name, processed_value)
                saved_data[field_name] = processed_value
            
            # Логируем все сохраненные данные
            print("=== СОХРАНЕННЫЕ ДАННЫЕ ===")
            for field_name, value in saved_data.items():
                if value is not None and value != '':
                    print(f"{field_name}: {value}")
            
            if errors:
                print("=== ОШИБКИ ===")
                for error in errors:
                    print(error)
            
            # Сохраняем в базу данных
            try:
                test_result.save()
                print(f"✅ Данные успешно сохранены в БД для образца {sample.pk}")
                
                # Проверяем заполненность основных полей для определения статуса
                required_fields = [
                    'grain_initial_weight', 'dust_initial_weight', 'dust_after_weight',
                    'sieve_2_weight', 'sieve_1_weight', 'sieve_05_weight', 'sieve_025_weight', 'sieve_0125_weight',
                    'bulk_1_volume', 'bulk_1_empty', 'bulk_1_full',
                    'actual_1_empty', 'actual_1_water', 'actual_1_sand', 'actual_1_full'
                ]
                
                all_filled = True
                for field in required_fields:
                    value = getattr(test_result, field)
                    if value is None or value == '':
                        all_filled = False
                        print(f"⚠️ Обязательное поле {field} не заполнено")
                        break
                
                # Обновляем статус образца только если все обязательные поля заполнены
                if all_filled:
                    sample.status = 'completed'
                    sample.completion_date = date.today()
                    print(f"✅ Все обязательные поля заполнены. Статус образца обновлен на 'completed'")
                else:
                    sample.status = 'in_progress'
                    print(f"⚠️ Не все обязательные поля заполнены. Статус остается 'in_progress'")
                
                sample.save()
                
                # Проверяем, что данные действительно сохранились
                saved_test_result = TestResult.objects.get(sample=sample)
                print("=== ПРОВЕРКА СОХРАНЕНИЯ ===")
                
                # Проверяем несколько ключевых readonly полей
                key_readonly_fields = ['grain_8_percent', 'grain_4_percent', 'dust_percent', 
                                     'size_module_value', 'clay_percent', 'humidity_average', 
                                     'bulk_average_density', 'actual_average_density', 'emptiness']
                
                for field in key_readonly_fields:
                    db_value = getattr(saved_test_result, field)
                    if db_value is not None:
                        print(f"✅ {field} в БД: {db_value}")
                    else:
                        print(f"⚠️ {field} в БД: пустое значение")
                
                
            except Exception as e:
                print(f"❌ Ошибка при сохранении в БД: {e}")
                raise e

# Test results view (for 'completed' status)
def sample_test_results(request, pk):
    sample = get_object_or_404(TestSample, pk=pk)
    # Получаем результаты теста
    try:
        test_result = TestResult.objects.get(sample=sample)
    except TestResult.DoesNotExist:
        test_result = None
    
    return render(request, 'labtests/sample_test_results.html', {
        'sample': sample,
        'test_result': test_result
    })

# Автосохранение результатов теста (AJAX) - с улучшенной обработкой
@require_POST
def autosave_test_result(request, pk):
    sample = get_object_or_404(TestSample, pk=pk)
    test_result, created = TestResult.objects.get_or_create(sample=sample)
    
    try:
        # Получаем данные из POST запроса
        data = json.loads(request.body)
        print(f"Ajax автосохранение для образца {pk}: {data}")
        
        # Используем тот же маппинг полей как в основной функции
        fields_mapping = {
            'result_class': str, 'grain_initial_weight': float, 'grain_8_weight': float, 'grain_4_weight': float, 
            'grain_8_percent': float, 'grain_4_percent': float, 'dust_initial_weight': float, 'dust_after_weight': float, 
            'dust_percent': float, 'sieve_2_weight': float, 'sieve_1_weight': float, 'sieve_05_weight': float, 
            'sieve_025_weight': float, 'sieve_0125_weight': float, 'sieve_2_partial': float, 'sieve_1_partial': float, 
            'sieve_05_partial': float, 'sieve_025_partial': float, 'sieve_0125_partial': float, 'sieve_2_full': float, 
            'sieve_1_full': float, 'sieve_05_full': float, 'sieve_025_full': float, 'sieve_0125_full': float, 
            'size_module_value': float, 'size_module_name': str, 'clay_initial_weight': float, 'clay_weight': float, 
            'clay_percent': float, 'humidity_1_number': str, 'humidity_1_container': float, 'humidity_1_with_sand': float,
            'humidity_1_after_dry': float, 'humidity_1_value': float, 'humidity_2_number': str, 'humidity_2_container': float, 
            'humidity_2_with_sand': float, 'humidity_2_after_dry': float, 'humidity_2_value': float, 'humidity_average': float,
            'clay_swell_1_number': str, 'clay_swell_1_initial': float, 'clay_swell_1_after': float, 'clay_swell_1_k': float,
            'clay_swell_2_number': str, 'clay_swell_2_initial': float, 'clay_swell_2_after': float, 'clay_swell_2_k': float,
            'clay_swell_average_k': float, 'clay_swell_content': float, 'clay_swell_conclusion': str, 'bulk_1_volume': float, 
            'bulk_1_empty': float, 'bulk_1_full': float, 'bulk_1_density': float, 'bulk_2_volume': float, 'bulk_2_empty': float, 
            'bulk_2_full': float, 'bulk_2_density': float, 'bulk_average_density': float, 'actual_1_number': str, 
            'actual_1_empty': float, 'actual_1_water': float, 'actual_1_sand': float, 'actual_1_full': float, 'actual_1_density': float,
            'actual_2_number': str, 'actual_2_empty': float, 'actual_2_water': float, 'actual_2_sand': float, 'actual_2_full': float, 
            'actual_2_density': float, 'actual_average_density': float, 'emptiness': float
        }
        
        # Сохраняем данные
        for field_name, field_type in fields_mapping.items():
            if field_name in data:
                value = data[field_name]
                
                if field_type == float:
                    try:
                        processed_value = float(value) if value else None
                    except (ValueError, TypeError):
                        processed_value = None
                elif field_type == int:
                    try:
                        processed_value = int(value) if value else 0
                    except (ValueError, TypeError):
                        processed_value = 0
                elif field_type == str:
                    processed_value = str(value) if value else ''
                else:
                    processed_value = value
                
                setattr(test_result, field_name, processed_value)
        
        test_result.save()
        return JsonResponse({'status': 'success', 'message': 'Данные автосохранены'})
        
    except Exception as e:
        print(f"Ошибка автосохранения: {e}")
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)


# Форма тестирования асфальтобетона
def asphalt_test_form(request, pk):
    from .models import AsphaltTestResult
    
    sample = get_object_or_404(TestSample, pk=pk)
    test_result, created = AsphaltTestResult.objects.get_or_create(sample=sample)
    
    # Отладочный вывод
    if created:
        print(f"Создан новый AsphaltTestResult для образца {pk}")
    else:
        print(f"Загружен существующий AsphaltTestResult для образца {pk}")
    
    if request.method == 'POST':
        if request.POST.get('action') == 'save':
            # Сохраняем данные асфальтобетона
            save_asphalt_test_result(request, test_result, sample)
            # После сохранения перенаправляем на список образцов
            return redirect('sample_list')
    
    # Определяем шаблон в зависимости от ГОСТ
    gost_number = sample.gost.number
    print(f"ГОСТ для асфальтобетона: {gost_number}")
    
    # Выбираем шаблон в зависимости от ГОСТ
    if '58406.2' in gost_number:
        template_name = 'labtests/asphalt_test_form_58406_2.html'
        print("Используем шаблон для ГОСТ 58406.2-2020")
    else:
        # По умолчанию используем шаблон для ГОСТ 58406.1-2020
        template_name = 'labtests/asphalt_test_form.html'
        print("Используем шаблон для ГОСТ 58406.1-2020")
    
    # Передаем test_result в контекст
    return render(request, template_name, {
        'sample': sample,
        'test_result': test_result
    })


def save_asphalt_test_result(request, test_result, sample):
    """Сохраняет результаты тестирования асфальтобетона"""
    
    print(f"\n=== НАЧАЛО СОХРАНЕНИЯ АСФАЛЬТОБЕТОНА для образца {sample.pk} ===")
    
    # Маппинг полей для асфальтобетона
    fields_mapping = {
        # Плотность - 3 образца
        'density_1_number': str, 'density_1_air': float, 'density_1_water': float,
        'density_1_diff_g2g1': float, 'density_1_air_after_water': float, 'density_1_density': float,
        'density_2_number': str, 'density_2_air': float, 'density_2_water': float,
        'density_2_diff_g2g1': float, 'density_2_air_after_water': float, 'density_2_density': float,
        'density_3_number': str, 'density_3_air': float, 'density_3_water': float,
        'density_3_diff_g2g1': float, 'density_3_air_after_water': float, 'density_3_density': float,
        
        # Средние значения
        'average_density': float, 'max_density': float, 'void_volume': float,
        'void_volume_receipt': float, 'void_volume_variance': float, 'void_volume_min': float,
        
        # Гранулометрический состав - 10 фракций
        'partition_31_5_weight': float, 'partition_31_5_cho': float, 'partition_31_5_pp': float,
        'partition_31_5_receipt': float, 'partition_31_5_variance': float,
        'partition_22_4_weight': float, 'partition_22_4_cho': float, 'partition_22_4_pp': float,
        'partition_22_4_receipt': float, 'partition_22_4_variance': float,
        'partition_16_weight': float, 'partition_16_cho': float, 'partition_16_pp': float,
        'partition_16_receipt': float, 'partition_16_variance': float,
        'partition_11_2_weight': float, 'partition_11_2_cho': float, 'partition_11_2_pp': float,
        'partition_11_2_receipt': float, 'partition_11_2_variance': float,
        'partition_8_weight': float, 'partition_8_cho': float, 'partition_8_pp': float,
        'partition_8_receipt': float, 'partition_8_variance': float,
        'partition_5_6_weight': float, 'partition_5_6_cho': float, 'partition_5_6_pp': float,
        'partition_5_6_receipt': float, 'partition_5_6_variance': float,
        'partition_4_weight': float, 'partition_4_cho': float, 'partition_4_pp': float,
        'partition_4_receipt': float, 'partition_4_variance': float,
        'partition_2_weight': float, 'partition_2_cho': float, 'partition_2_pp': float,
        'partition_2_receipt': float, 'partition_2_variance': float,
        'partition_0_125_weight': float, 'partition_0_125_cho': float, 'partition_0_125_pp': float,
        'partition_0_125_receipt': float, 'partition_0_125_variance': float,
        'partition_0_063_weight': float, 'partition_0_063_cho': float, 'partition_0_063_pp': float,
        'partition_0_063_receipt': float, 'partition_0_063_variance': float,
        
        # Максимальная плотность смеси
        'max_mix_density_mix_weight': float, 'max_mix_density_after_vacuum': float,
        'max_mix_density_plate_weight': float,
        
        # Содержание вяжущего
        'viscous_tigle_weight': float, 'viscous_mix_tigle_before': float,
        'viscous_mix_tigle_after': float, 'viscous_bitumen_content': float,
        'viscous_bitumen_receipt': float, 'viscous_bitumen_variance': float,
        
        # Стекание вяжущего
        'binder_empty_glass': float, 'binder_full_glass': float,
        'binder_glass_after': float, 'binder_trickling': float,
        'binder_max_trickling': float,
    }
    
    # Определяем readonly поля
    readonly_fields = [
        'density_1_diff_g2g1', 'density_1_density', 'density_2_diff_g2g1', 'density_2_density',
        'density_3_diff_g2g1', 'density_3_density', 'average_density', 'max_density', 'void_volume',
        'partition_31_5_cho', 'partition_31_5_pp', 'partition_22_4_cho', 'partition_22_4_pp',
        'partition_16_cho', 'partition_16_pp', 'partition_11_2_cho', 'partition_11_2_pp',
        'partition_8_cho', 'partition_8_pp', 'partition_5_6_cho', 'partition_5_6_pp',
        'partition_4_cho', 'partition_4_pp', 'partition_2_cho', 'partition_2_pp',
        'partition_0_125_cho', 'partition_0_125_pp', 'partition_0_063_cho', 'partition_0_063_pp',
        'viscous_bitumen_content', 'binder_trickling'
    ]
    
    # Сохраняем все поля
    saved_fields = {}
    for field_name, field_type in fields_mapping.items():
        value = request.POST.get(field_name, '')
        
        # Логируем полученные значения
        if value:
            print(f"{field_name}: '{value}'")
        
        # Обработка значений
        if field_type == float:
            try:
                # Заменяем запятую на точку перед преобразованием
                if value:
                    value = value.replace(',', '.')
                    processed_value = float(value)
                else:
                    processed_value = None
            except (ValueError, TypeError) as e:
                print(f"Ошибка преобразования {field_name}: {e}")
                processed_value = None
        elif field_type == str:
            processed_value = str(value) if value else ''
        else:
            processed_value = value
        
        # Для readonly полей сохраняем существующие значения, если новые пустые
        if field_name in readonly_fields:
            if processed_value is None or processed_value == '':
                existing_value = getattr(test_result, field_name, None)
                if existing_value is not None and existing_value != '':
                    processed_value = existing_value
                    print(f"  Сохраняем существующее значение для {field_name}: {existing_value}")
        
        # Для полей ввода - сохраняем значения как есть (можно очистить)
        setattr(test_result, field_name, processed_value)
        saved_fields[field_name] = processed_value
    
    # Сохраняем в базу данных
    try:
        test_result.save()
        print(f"\n✅ Данные асфальтобетона сохранены для образца {sample.pk}")
        
        # Логируем сохраненные значения
        print("\n=== СОХРАНЕННЫЕ ЗНАЧЕНИЯ ===")
        non_empty_count = 0
        for field_name, value in saved_fields.items():
            if value is not None and value != '' and value != 0:
                print(f"{field_name}: {value}")
                non_empty_count += 1
        print(f"\nВсего сохранено непустых полей: {non_empty_count}")
        
        # Проверяем заполненность основных полей для определения статуса
        # Определяем ГОСТ для правильного набора обязательных полей
        gost_number = sample.gost.number if sample.gost else ''
        
        # Базовые обязательные поля для всех ГОСТов асфальтобетона
        required_fields = [
            # Плотность - минимум два образца
            'density_1_air', 'density_1_water', 'density_1_air_after_water',
            'density_2_air', 'density_2_water', 'density_2_air_after_water',
            # Гранулометрический состав
            'partition_31_5_weight', 'partition_22_4_weight', 'partition_16_weight',
            'partition_11_2_weight', 'partition_8_weight', 'partition_5_6_weight',
            'partition_4_weight', 'partition_2_weight', 'partition_0_125_weight', 'partition_0_063_weight',
            # Максимальная плотность
            'max_mix_density_mix_weight', 'max_mix_density_after_vacuum', 'max_mix_density_plate_weight',
            # Содержание вяжущего
            'viscous_tigle_weight', 'viscous_mix_tigle_before', 'viscous_mix_tigle_after',
        ]
        
        # Для ГОСТ 58406.1-2020 добавляем стекание вяжущего
        # Для ГОСТ 58406.2-2020 стекание вяжущего НЕ требуется
        if '58406.1' in gost_number:
            required_fields.extend([
                'binder_empty_glass', 'binder_full_glass', 'binder_glass_after'
            ])
        
        all_filled = True
        missing_fields = []
        for field_name in required_fields:
            value = getattr(test_result, field_name, None)
            if value is None or value == '':
                all_filled = False
                missing_fields.append(field_name)
        
        # Обновляем статус образца
        if all_filled:
            sample.status = 'completed'
            sample.completion_date = date.today()
            print(f"\n✅ Все обязательные поля заполнены. Статус образца обновлен на 'Завершено'")
        else:
            sample.status = 'in_progress'
            print(f"\n⚠️ Не все обязательные поля заполнены. Статус остается 'В работе'")
            print(f"   Не заполненные поля: {', '.join(missing_fields[:5])}..." if len(missing_fields) > 5 else f"   Не заполненные поля: {', '.join(missing_fields)}")
        
        sample.save()
        
    except Exception as e:
        print(f"❌ Ошибка при сохранении: {e}")
        raise e


# Форма тестирования битума
def bitumen_test_form(request, pk):
    """Форма для ввода результатов испытаний битума"""
    
    if not EXTRA_MODELS_AVAILABLE:
        # Если модели недоступны, используем стандартную форму
        sample = get_object_or_404(TestSample, pk=pk)
        test_result, created = TestResult.objects.get_or_create(sample=sample)
        return render(request, 'labtests/sample_test_form.html', {
            'sample': sample,
            'test_result': test_result
        })
    
    sample = get_object_or_404(TestSample, pk=pk)
    test_result, created = BitumenTestResult33133.objects.get_or_create(sample=sample)
    
    # Отладочный вывод
    if created:
        print(f"Создан новый BitumenTestResult33133 для образца {pk}")
        # Устанавливаем нормативы для нового образца
        test_result.set_normatives()
        test_result.save()
    else:
        print(f"Загружен существующий BitumenTestResult33133 для образца {pk}")
        # Обновляем нормативы, если они не заполнены
        if not test_result.needle_deep_min:
            test_result.set_normatives()
            test_result.save()
    
    if request.method == 'POST':
        if request.POST.get('action') == 'save':
            # Сохраняем данные битума
            save_bitumen_test_result(request, test_result, sample)
            return redirect('sample_list')
    
    # Передаем test_result в контекст
    return render(request, 'labtests/bitumen_33133_test_form.html', {
        'sample': sample,
        'test_result': test_result
    })


def save_bitumen_test_result(request, test_result, sample):
    """Сохраняет результаты тестирования битума"""
    
    if not EXTRA_MODELS_AVAILABLE:
        # Если модели недоступны, ничего не делаем
        return
    
    print(f"\n=== НАЧАЛО СОХРАНЕНИЯ БИТУМА для образца {sample.pk} ===")
    
    # Маппинг полей для битума
    fields_mapping = {
        # Глубина проникания иглы
        'needle_deep': float,
        'needle_deep_min': float,
        'needle_deep_max': float,
        
        # Температура размягчения
        'softening_temperature': float,
        'softening_temperature_min': float,
        
        # Растяжимость
        'extensibility': float,
        'extensibility_min': float,
        
        # Температура хрупкости
        'fragility_temperature': float,
        'fragility_temperature_max': float,
        
        # Температура вспышки
        'flash_temperature': float,
        'flash_temperature_min': float,
        
        # Изменение массы - Контейнер А
        'container_a_weight': float,
        'container_a_bitumen_before': float,
        'container_a_bitumen_after': float,
        'container_a_result': float,
        
        # Изменение массы - Контейнер B
        'container_b_weight': float,
        'container_b_bitumen_before': float,
        'container_b_bitumen_after': float,
        'container_b_result': float,
        
        # Общий итог
        'weight_change': float,
        'weight_change_max': float,
        
        # Изменение температуры размягчения
        'softening_temperature_change': float,
        'softening_temperature_change_max': float,
    }
    
    # Определяем readonly поля (вычисляемые)
    readonly_fields = [
        'container_a_result', 'container_b_result', 'weight_change'
    ]
    
    # Сохраняем все поля
    saved_fields = {}
    for field_name, field_type in fields_mapping.items():
        value = request.POST.get(field_name, '')
        
        # Логируем полученные значения
        if value:
            print(f"{field_name}: '{value}'")
        
        # Обработка значений
        if field_type == float:
            try:
                if value:
                    value = value.replace(',', '.')
                    processed_value = float(value)
                else:
                    processed_value = None
            except (ValueError, TypeError) as e:
                print(f"Ошибка преобразования {field_name}: {e}")
                processed_value = None
        elif field_type == int:
            try:
                processed_value = int(value) if value else 0
            except (ValueError, TypeError):
                processed_value = 0
        elif field_type == str:
            processed_value = str(value) if value else ''
        else:
            processed_value = value
        
        # Для readonly полей сохраняем существующие значения, если новые пустые
        if field_name in readonly_fields:
            if processed_value is None or processed_value == '':
                existing_value = getattr(test_result, field_name, None)
                if existing_value is not None and existing_value != '':
                    processed_value = existing_value
                    print(f"  Сохраняем существующее значение для {field_name}: {existing_value}")
        
        # Сохраняем значение
        setattr(test_result, field_name, processed_value)
        saved_fields[field_name] = processed_value
    
    # Сохраняем в базу данных
    try:
        test_result.save()
        print(f"\n✅ Данные битума сохранены для образца {sample.pk}")
        
        # Проверяем заполненность основных полей для определения статуса
        required_fields = [
            'needle_deep',
            'softening_temperature',
            'extensibility',
            'fragility_temperature',
            'flash_temperature',
            'container_a_weight', 'container_a_bitumen_before', 'container_a_bitumen_after',
            'container_b_weight', 'container_b_bitumen_before', 'container_b_bitumen_after',
            'softening_temperature_change',
        ]
        
        all_filled = True
        missing_fields = []
        for field_name in required_fields:
            value = getattr(test_result, field_name, None)
            if value is None or value == '':
                all_filled = False
                missing_fields.append(field_name)
        
        # Обновляем статус образца
        if all_filled:
            sample.status = 'completed'
            sample.completion_date = date.today()
            print(f"\n✅ Все обязательные поля заполнены. Статус образца обновлен на 'Завершено'")
        else:
            sample.status = 'in_progress'
            print(f"\n⚠️ Не все обязательные поля заполнены. Статус остается 'В работе'")
            if missing_fields:
                print(f"   Не заполненные поля: {', '.join(missing_fields[:5])}..." if len(missing_fields) > 5 else f"   Не заполненные поля: {', '.join(missing_fields)}")
        
        sample.save()
        
    except Exception as e:
        print(f"❌ Ошибка при сохранении: {e}")
        raise e


def save_crushed_8267_test_result(request, test_result, sample):
    """Сохраняет результаты тестирования щебня по ГОСТ 8267-93"""
    
    print(f"\n=== НАЧАЛО СОХРАНЕНИЯ ЩЕБНЯ 8267 для образца {sample.pk} ===")
    
    # Маппинг полей для щебня по ГОСТ 8267-93 (универсальная версия)
    fields_mapping = {
        # Пылевидные и глинистые частицы
        'dust_initial_weight': float,
        'dust_after_weight': float,
        'dust_content': float,
        
        # Масса пробы
        'grain_compound_weight': float,
        
        # Гранулометрический состав (5 партиций)
        'partition_0_weight': float, 'partition_0_partial': float, 'partition_0_passes': float,
        'partition_1_weight': float, 'partition_1_partial': float, 'partition_1_passes': float,
        'partition_2_weight': float, 'partition_2_partial': float, 'partition_2_passes': float,
        'partition_3_weight': float, 'partition_3_partial': float, 'partition_3_passes': float,
        'partition_4_weight': float, 'partition_4_partial': float, 'partition_4_passes': float,
        
        # Лещадность
        'flakiness_weight': float,
        'flakiness_flaky_weight': float,
        'flakiness_value': float,
        'flakiness_mark_type': str,
        
        # Дробимость
        'crushability_type': int,
        'crushability_weight': float,
        'crushability_after_weight': float,
        'crushability_value': float,
        'crushability_mark_type': str,
        
        # Насыпная плотность
        'bulk_density_0_volume': float,
        'bulk_density_0_empty_weight': float,
        'bulk_density_0_weight': float,
        'bulk_density_0_density_value': float,
        'bulk_density_1_volume': float,
        'bulk_density_1_empty_weight': float,
        'bulk_density_1_weight': float,
        'bulk_density_1_density_value': float,
        'bulk_density_average': float,
        
        # Содержание зерен слабых пород
        'weak_rock_initial_weight': float,
        'weak_rock_weight': float,
        'weak_rock_content': float,
        
        # Глина в комках
        'clay_initial_weight': float,
        'clay_weight': float,
        'clay_content': float,
        
        # Средняя плотность
        'average_density_dried_weight': float,
        'average_density_weight_in_air': float,
        'average_density_weight_in_water': float,
        'average_density_empty_basket_weight': float,
        'average_density_value': float,
    }
    
    # Определяем readonly поля (вычисляемые)
    readonly_fields = [
        'dust_content',
        'partition_0_partial', 'partition_0_passes',
        'partition_1_partial', 'partition_1_passes',
        'partition_2_partial', 'partition_2_passes',
        'partition_3_partial', 'partition_3_passes',
        'partition_4_partial', 'partition_4_passes',
        'flakiness_value',
        'crushability_value',
        'bulk_density_0_density_value', 'bulk_density_1_density_value', 'bulk_density_average',
        'weak_rock_content',
        'clay_content',
        'average_density_value',
    ]
    
    # Сохраняем все поля
    saved_fields = {}
    for field_name, field_type in fields_mapping.items():
        value = request.POST.get(field_name, '')
        
        # Логируем полученные значения
        if value:
            print(f"{field_name}: '{value}'")
        
        # Обработка значений
        if field_type == float:
            try:
                if value:
                    value = value.replace(',', '.')
                    processed_value = float(value)
                else:
                    processed_value = None
            except (ValueError, TypeError) as e:
                print(f"Ошибка преобразования {field_name}: {e}")
                processed_value = None
        elif field_type == str:
            processed_value = str(value) if value else ''
        elif field_type == int:
            try:
                processed_value = int(value) if value else 0
            except (ValueError, TypeError):
                processed_value = 0
        else:
            processed_value = value
        
        # Для readonly полей сохраняем существующие значения, если новые пустые
        if field_name in readonly_fields:
            if processed_value is None or processed_value == '':
                existing_value = getattr(test_result, field_name, None)
                if existing_value is not None and existing_value != '':
                    processed_value = existing_value
                    print(f"  Сохраняем существующее значение для {field_name}: {existing_value}")
        
        # Сохраняем значение
        setattr(test_result, field_name, processed_value)
        saved_fields[field_name] = processed_value
    
    # Сохраняем в базу данных
    try:
        test_result.save()
        print(f"\n✅ Данные щебня 8267 сохранены для образца {sample.pk}")
        
        # Проверяем заполненность основных полей для определения статуса
        required_fields = [
            # Гранулометрический состав (хотя бы 3 партиции)
            'grain_compound_weight',
            'partition_0_weight', 'partition_1_weight', 'partition_2_weight',
            # Пылевидные и глинистые
            'dust_initial_weight', 'dust_after_weight',
            # Глина в комках
            'clay_initial_weight', 'clay_weight',
            # Лещадность
            'flakiness_weight', 'flakiness_flaky_weight',
            # Дробимость
            'crushability_weight', 'crushability_after_weight',
        ]
        
        all_filled = True
        missing_fields = []
        for field_name in required_fields:
            value = getattr(test_result, field_name, None)
            if value is None or value == '':
                all_filled = False
                missing_fields.append(field_name)
        
        # Обновляем статус образца
        if all_filled:
            sample.status = 'completed'
            sample.completion_date = date.today()
            print(f"\n✅ Все обязательные поля заполнены. Статус образца обновлен на 'Завершено'")
        else:
            sample.status = 'in_progress'
            print(f"\n⚠️ Не все обязательные поля заполнены. Статус остается 'В работе'")
            if missing_fields:
                print(f"   Не заполненные поля: {', '.join(missing_fields[:5])}..." if len(missing_fields) > 5 else f"   Не заполненные поля: {', '.join(missing_fields)}")
        
        sample.save()
        
    except Exception as e:
        print(f"❌ Ошибка при сохранении: {e}")
        raise e


def save_crushed_32703_test_result(request, test_result, sample):
    """Сохраняет результаты тестирования щебня по ГОСТ 32703-2014"""
    
    print(f"\n=== НАЧАЛО СОХРАНЕНИЯ ЩЕБНЯ 32703 для образца {sample.pk} ===")
    
    # Маппинг полей для щебня по ГОСТ 32703-2014
    fields_mapping = {
        # Масса пробы
        'grain_compound_weight': float,
        
        # Гранулометрический состав (5 фракций)
        'sieve_2d_weight': float, 'sieve_2d_partial': float, 'sieve_2d_full': float,
        'sieve_1_4d_weight': float, 'sieve_1_4d_partial': float, 'sieve_1_4d_full': float,
        'sieve_d_weight': float, 'sieve_d_partial': float, 'sieve_d_full': float,
        'sieve_d_small_weight': float, 'sieve_d_small_partial': float, 'sieve_d_small_full': float,
        'sieve_d_2_weight': float, 'sieve_d_2_partial': float, 'sieve_d_2_full': float,
        
        'mark_type': str,
        
        # Лещадность
        'flakiness_weight': float,
        'flakiness_flaky_weight': float,
        'flakiness_value': float,
        'flakiness_mark': str,
        
        # Дробимость
        'crushability_type': int,
        'crushability_weight': float,
        'crushability_after_weight': float,
        'crushability_value': float,
        'crushability_mark': str,
    }
    
    # Определяем readonly поля (вычисляемые)
    readonly_fields = [
        'sieve_2d_partial', 'sieve_2d_full',
        'sieve_1_4d_partial', 'sieve_1_4d_full',
        'sieve_d_partial', 'sieve_d_full',
        'sieve_d_small_partial', 'sieve_d_small_full',
        'sieve_d_2_partial', 'sieve_d_2_full',
        'flakiness_value',
        'crushability_value',
    ]
    
    # Сохраняем все поля
    saved_fields = {}
    for field_name, field_type in fields_mapping.items():
        value = request.POST.get(field_name, '')
        
        # Логируем полученные значения
        if value:
            print(f"{field_name}: '{value}'")
        
        # Обработка значений
        if field_type == float:
            try:
                if value:
                    value = value.replace(',', '.')
                    processed_value = float(value)
                else:
                    processed_value = None
            except (ValueError, TypeError) as e:
                print(f"Ошибка преобразования {field_name}: {e}")
                processed_value = None
        elif field_type == str:
            processed_value = str(value) if value else ''
        elif field_type == int:
            try:
                processed_value = int(value) if value else 0
            except (ValueError, TypeError):
                processed_value = 0
        else:
            processed_value = value
        
        # Для readonly полей сохраняем существующие значения, если новые пустые
        if field_name in readonly_fields:
            if processed_value is None or processed_value == '':
                existing_value = getattr(test_result, field_name, None)
                if existing_value is not None and existing_value != '':
                    processed_value = existing_value
                    print(f"  Сохраняем существующее значение для {field_name}: {existing_value}")
        
        # Сохраняем значение
        setattr(test_result, field_name, processed_value)
        saved_fields[field_name] = processed_value
    
    # Сохраняем в базу данных
    try:
        test_result.save()
        print(f"\n✅ Данные щебня 32703 сохранены для образца {sample.pk}")
        
        # Проверяем заполненность основных полей для определения статуса
        required_fields = [
            # Гранулометрический состав
            'grain_compound_weight',
            'sieve_2d_weight', 'sieve_1_4d_weight', 'sieve_d_weight',
            'sieve_d_small_weight', 'sieve_d_2_weight',
            # Лещадность
            'flakiness_weight', 'flakiness_flaky_weight',
            # Дробимость
            'crushability_weight', 'crushability_after_weight',
        ]
        
        all_filled = True
        missing_fields = []
        for field_name in required_fields:
            value = getattr(test_result, field_name, None)
            if value is None or value == '':
                all_filled = False
                missing_fields.append(field_name)
        
        # Обновляем статус образца
        if all_filled:
            sample.status = 'completed'
            sample.completion_date = date.today()
            print(f"\n✅ Все обязательные поля заполнены. Статус образца обновлен на 'Завершено'")
        else:
            sample.status = 'in_progress'
            print(f"\n⚠️ Не все обязательные поля заполнены. Статус остается 'В работе'")
            if missing_fields:
                print(f"   Не заполненные поля: {', '.join(missing_fields[:5])}..." if len(missing_fields) > 5 else f"   Не заполненные поля: {', '.join(missing_fields)}")
        
        sample.save()
        
    except Exception as e:
        print(f"❌ Ошибка при сохранении: {e}")
        raise e


def save_shchps_70458_test_result(request, test_result, sample):
    """Сохраняет результаты тестирования щебня по ГОСТ 70458-2022"""
    
    print(f"\n=== НАЧАЛО СОХРАНЕНИЯ ЩЕБНЯ 70458 для образца {sample.pk} ===")
    
    # Маппинг полей для щебня по ГОСТ 70458-2022
    fields_mapping = {
        # Масса пробы
        'grain_compound_weight': float,
        
        # Пылевидные и глинистые частицы
        'dust_initial_weight': float,
        'dust_after_weight': float,
        'dust_clay_content': float,
        
        # Гранулометрический состав (9 фракций)
        'sieve_22_4_weight': float, 'sieve_22_4_partial': float, 'sieve_22_4_full': float,
        'sieve_16_weight': float, 'sieve_16_partial': float, 'sieve_16_full': float,
        'sieve_11_2_weight': float, 'sieve_11_2_partial': float, 'sieve_11_2_full': float,
        'sieve_8_weight': float, 'sieve_8_partial': float, 'sieve_8_full': float,
        'sieve_5_6_weight': float, 'sieve_5_6_partial': float, 'sieve_5_6_full': float,
        'sieve_4_weight': float, 'sieve_4_partial': float, 'sieve_4_full': float,
        'sieve_2_weight': float, 'sieve_2_partial': float, 'sieve_2_full': float,
        'sieve_1_weight': float, 'sieve_1_partial': float, 'sieve_1_full': float,
        'sieve_0_5_weight': float, 'sieve_0_5_partial': float, 'sieve_0_5_full': float,
        
        'category_and_mark': str,
        
        # Лещадность
        'flakiness_4_8_initial': float, 'flakiness_4_8_flaky': float, 'flakiness_4_8_value': float,
        'flakiness_8_16_initial': float, 'flakiness_8_16_flaky': float, 'flakiness_8_16_value': float,
        'flakiness_average': float,
        'flakiness_mark': str,
        
        # Дробимость
        'crushability_type': int,
        'crushability_4_8_initial': float, 'crushability_4_8_after': float, 'crushability_4_8_value': float,
        'crushability_8_16_initial': float, 'crushability_8_16_after': float, 'crushability_8_16_value': float,
        'crushability_average': float,
        'crushability_mark': str,
        
        # Насыпная плотность
        'bulk_density_1_volume': float, 'bulk_density_1_empty': float, 
        'bulk_density_1_weight': float, 'bulk_density_1_density': float,
        'bulk_density_2_volume': float, 'bulk_density_2_empty': float,
        'bulk_density_2_weight': float, 'bulk_density_2_density': float,
        'bulk_density_average': float,
        
        # Глина в комках
        'clay_initial_weight': float,
        'clay_weight': float,
        'clay_content': float,
    }
    
    # Определяем readonly поля (вычисляемые)
    readonly_fields = [
        'dust_clay_content',
        'sieve_22_4_partial', 'sieve_22_4_full',
        'sieve_16_partial', 'sieve_16_full',
        'sieve_11_2_partial', 'sieve_11_2_full',
        'sieve_8_partial', 'sieve_8_full',
        'sieve_5_6_partial', 'sieve_5_6_full',
        'sieve_4_partial', 'sieve_4_full',
        'sieve_2_partial', 'sieve_2_full',
        'sieve_1_partial', 'sieve_1_full',
        'sieve_0_5_partial', 'sieve_0_5_full',
        'flakiness_4_8_value', 'flakiness_8_16_value', 'flakiness_average',
        'crushability_4_8_value', 'crushability_8_16_value', 'crushability_average',
        'bulk_density_1_density', 'bulk_density_2_density', 'bulk_density_average',
        'clay_content',
    ]
    
    # Сохраняем все поля
    saved_fields = {}
    for field_name, field_type in fields_mapping.items():
        value = request.POST.get(field_name, '')
        
        # Логируем полученные значения
        if value:
            print(f"{field_name}: '{value}'")
        
        # Обработка значений
        if field_type == float:
            try:
                if value:
                    value = value.replace(',', '.')
                    processed_value = float(value)
                else:
                    processed_value = None
            except (ValueError, TypeError) as e:
                print(f"Ошибка преобразования {field_name}: {e}")
                processed_value = None
        elif field_type == str:
            processed_value = str(value) if value else ''
        elif field_type == int:
            try:
                processed_value = int(value) if value else 0
            except (ValueError, TypeError):
                processed_value = 0
        else:
            processed_value = value
        
        # Для readonly полей сохраняем существующие значения, если новые пустые
        if field_name in readonly_fields:
            if processed_value is None or processed_value == '':
                existing_value = getattr(test_result, field_name, None)
                if existing_value is not None and existing_value != '':
                    processed_value = existing_value
                    print(f"  Сохраняем существующее значение для {field_name}: {existing_value}")
        
        # Сохраняем значение
        setattr(test_result, field_name, processed_value)
        saved_fields[field_name] = processed_value
    
    # Сохраняем в базу данных
    try:
        test_result.save()
        print(f"\n✅ Данные щебня 70458 сохранены для образца {sample.pk}")
        
        # Проверяем заполненность основных полей для определения статуса
        required_fields = [
            # Пылевидные и глинистые
            'dust_initial_weight', 'dust_after_weight',
            # Гранулометрический состав - масса пробы
            'grain_compound_weight',
            # Гранулометрический состав - массы на ситах
            'sieve_22_4_weight', 'sieve_16_weight', 'sieve_11_2_weight',
            'sieve_8_weight', 'sieve_5_6_weight', 'sieve_4_weight',
            'sieve_2_weight', 'sieve_1_weight', 'sieve_0_5_weight',
            # Лещадность (хотя бы одна фракция)
            'flakiness_4_8_initial', 'flakiness_4_8_flaky',
            # Дробимость (хотя бы одна фракция)
            'crushability_4_8_initial', 'crushability_4_8_after',
            # Насыпная плотность
            'bulk_density_1_volume', 'bulk_density_1_empty', 'bulk_density_1_weight',
            # Глина в комках
            'clay_initial_weight', 'clay_weight',
        ]
        
        all_filled = True
        missing_fields = []
        for field_name in required_fields:
            value = getattr(test_result, field_name, None)
            if value is None or value == '':
                all_filled = False
                missing_fields.append(field_name)
        
        # Обновляем статус образца
        if all_filled:
            sample.status = 'completed'
            sample.completion_date = date.today()
            print(f"\n✅ Все обязательные поля заполнены. Статус образца обновлен на 'Завершено'")
        else:
            sample.status = 'in_progress'
            print(f"\n⚠️ Не все обязательные поля заполнены. Статус остается 'В работе'")
            if missing_fields:
                print(f"   Не заполненные поля: {', '.join(missing_fields[:5])}..." if len(missing_fields) > 5 else f"   Не заполненные поля: {', '.join(missing_fields)}")
        
        sample.save()
        
    except Exception as e:
        print(f"❌ Ошибка при сохранении: {e}")
        raise e


def save_asphalt_core_test_result(request, test_result, sample):
    """Сохраняет результаты тестирования кернов из асфальтобетона"""
    
    print(f"\n=== НАЧАЛО СОХРАНЕНИЯ КЕРНОВ для образца {sample.pk} ===")
    
    # Маппинг полей для кернов
    fields_mapping = {
        # Слой 1
        'layer1_type': str,
        'layer1_mix_name': str,
        
        # Образец 1
        'layer1_sample1_number': str,
        'layer1_sample1_actual_thickness': float,
        'layer1_sample1_project_thickness': float,
        'layer1_sample1_g': float,
        'layer1_sample1_g1': float,
        'layer1_sample1_g2g1': float,
        'layer1_sample1_g2': float,
        'layer1_sample1_density': float,
        
        # Образец 2
        'layer1_sample2_number': str,
        'layer1_sample2_actual_thickness': float,
        'layer1_sample2_project_thickness': float,
        'layer1_sample2_g': float,
        'layer1_sample2_g1': float,
        'layer1_sample2_g2g1': float,
        'layer1_sample2_g2': float,
        'layer1_sample2_density': float,
        
        # Средние и итоговые значения
        'layer1_average_density': float,
        'layer1_max_density': float,
        'layer1_void_volume': float,
    }
    
    # Определяем readonly поля (вычисляемые)
    readonly_fields = [
        'layer1_sample1_g2g1', 'layer1_sample1_density',
        'layer1_sample2_g2g1', 'layer1_sample2_density',
        'layer1_average_density', 'layer1_void_volume'
    ]
    
    # Сохраняем все поля
    saved_fields = {}
    for field_name, field_type in fields_mapping.items():
        value = request.POST.get(field_name, '')
        
        # Логируем полученные значения
        if value:
            print(f"{field_name}: '{value}'")
        
        # Обработка значений
        if field_type == float:
            try:
                # Заменяем запятую на точку перед преобразованием
                if value:
                    value = value.replace(',', '.')
                    processed_value = float(value)
                else:
                    processed_value = None
            except (ValueError, TypeError) as e:
                print(f"Ошибка преобразования {field_name}: {e}")
                processed_value = None
        elif field_type == str:
            processed_value = str(value) if value else ''
        else:
            processed_value = value
        
        # Для readonly полей сохраняем существующие значения, если новые пустые
        if field_name in readonly_fields:
            if processed_value is None or processed_value == '':
                existing_value = getattr(test_result, field_name, None)
                if existing_value is not None and existing_value != '':
                    processed_value = existing_value
                    print(f"  Сохраняем существующее значение для {field_name}: {existing_value}")
        
        # Сохраняем значение
        setattr(test_result, field_name, processed_value)
        saved_fields[field_name] = processed_value
    
    # Сохраняем в базу данных
    try:
        test_result.save()
        print(f"\n✅ Данные кернов сохранены для образца {sample.pk}")
        
        # Логируем сохраненные значения
        print("\n=== СОХРАНЕННЫЕ ЗНАЧЕНИЯ ===")
        non_empty_count = 0
        for field_name, value in saved_fields.items():
            if value is not None and value != '' and value != 0:
                print(f"{field_name}: {value}")
                non_empty_count += 1
        print(f"\nВсего сохранено непустых полей: {non_empty_count}")
        
        # Проверяем заполненность основных полей для определения статуса
        # Для кернов обязательные поля менее строгие - достаточно основных измерений
        required_fields = [
            'layer1_type', 'layer1_mix_name',
            'layer1_sample1_g', 'layer1_sample1_g1', 'layer1_sample1_g2',
            'layer1_max_density'
        ]
        
        all_filled = True
        missing_fields = []
        for field_name in required_fields:
            value = getattr(test_result, field_name, None)
            if value is None or value == '':
                all_filled = False
                missing_fields.append(field_name)
        
        # Обновляем статус образца
        if all_filled:
            sample.status = 'completed'
            sample.completion_date = date.today()
            print(f"\n✅ Все обязательные поля заполнены. Статус образца обновлен на 'Завершено'")
        else:
            sample.status = 'in_progress'
            print(f"\n⚠️ Не все обязательные поля заполнены. Статус остается 'В работе'")
            if missing_fields:
                print(f"   Не заполненные поля: {', '.join(missing_fields)}")
        
        sample.save()
        
    except Exception as e:
        print(f"❌ Ошибка при сохранении: {e}")
        raise e


# Форма тестирования кернов из асфальтобетона
def asphalt_core_test_form(request, pk):
    """Форма для ввода результатов испытаний кернов"""
    from .models import AsphaltCoreTestResult
    
    sample = get_object_or_404(TestSample, pk=pk)
    test_result, created = AsphaltCoreTestResult.objects.get_or_create(sample=sample)
    
    # Отладочный вывод
    if created:
        print(f"Создан новый AsphaltCoreTestResult для образца {pk}")
    else:
        print(f"Загружен существующий AsphaltCoreTestResult для образца {pk}")
    
    if request.method == 'POST':
        if request.POST.get('action') == 'save':
            # Сохраняем данные кернов
            save_asphalt_core_test_result(request, test_result, sample)
            return redirect('sample_list')
    
    # Передаем test_result в контекст
    return render(request, 'labtests/asphalt_core_test_form.html', {
        'sample': sample,
        'test_result': test_result
    })


# Форма тестирования ЩПС
def shchps_test_form(request, pk):
    """Форма для ввода результатов испытаний ЩПС"""
    
    sample = get_object_or_404(TestSample, pk=pk)
    
    # Определяем ГОСТ для выбора правильной модели и шаблона
    gost_number = sample.gost.number if sample.gost else ''
    material_name = sample.material.name if sample.material else ''
    print(f"\n=== ОПРЕДЕЛЕНИЕ ТИПА МАТЕРИАЛА ===")
    print(f"Образец ID: {pk}")
    print(f"ГОСТ: {gost_number}")
    print(f"Материал: {material_name}")
    
    # Для ГОСТ 8267-93 (щебень стандартный)
    if '8267' in gost_number:
        from .models import Crushed8267TestResult
        test_result, created = Crushed8267TestResult.objects.get_or_create(sample=sample)
        template_name = 'labtests/crushed_8267_test_form.html'
        print("Используем модель Crushed8267TestResult для ГОСТ 8267-93")
    # Для ГОСТ 32703-2014 (щебень узких фракций)
    elif '32703' in gost_number:
        from .models import Crushed32703TestResult
        test_result, created = Crushed32703TestResult.objects.get_or_create(sample=sample)
        template_name = 'labtests/crushed_32703_test_form.html'
        print("Используем модель Crushed32703TestResult для ГОСТ 32703-2014")
    # Для ГОСТ 70458-2022 (щебень/ЩПС)
    elif '70458' in gost_number:
        from .models import ShchPS70458TestResult
        test_result, created = ShchPS70458TestResult.objects.get_or_create(sample=sample)
        template_name = 'labtests/shchps_70458_test_form.html'
        print("Используем модель ShchPS70458TestResult для ГОСТ 70458-2022")
    else:
        # Для ГОСТ 25607-2009 (ЩПС) - по умолчанию
        test_result, created = ShchPSTestResult.objects.get_or_create(sample=sample)
        template_name = 'labtests/shchps_test_form.html'
        print("Используем модель ShchPSTestResult для ГОСТ 25607-2009")
    
    # Отладочный вывод
    if created:
        print(f"Создан новый результат для образца {pk}")
    else:
        print(f"Загружен существующий результат для образца {pk}")
    
    if request.method == 'POST':
        if request.POST.get('action') == 'save':
            # Определяем какую функцию сохранения использовать
            if '8267' in gost_number:
                save_crushed_8267_test_result(request, test_result, sample)
            elif '32703' in gost_number:
                save_crushed_32703_test_result(request, test_result, sample)
            elif '70458' in gost_number:
                save_shchps_70458_test_result(request, test_result, sample)
            else:
                save_shchps_test_result(request, test_result, sample)
            # После сохранения перенаправляем на список образцов
            return redirect('sample_list')
    
    # Передаем test_result в контекст
    return render(request, template_name, {
        'sample': sample,
        'test_result': test_result
    })


# Форма тестирования эмульсии
def emulsion_test_form(request, pk):
    """Форма для ввода результатов испытаний эмульсии"""
    
    if not EXTRA_MODELS_AVAILABLE:
        # Если модели недоступны, используем стандартную форму
        sample = get_object_or_404(TestSample, pk=pk)
        test_result, created = TestResult.objects.get_or_create(sample=sample)
        return render(request, 'labtests/sample_test_form.html', {
            'sample': sample,
            'test_result': test_result
        })
    
    sample = get_object_or_404(TestSample, pk=pk)
    test_result, created = EmulsionTestResult.objects.get_or_create(sample=sample)
    
    # Отладочный вывод
    if created:
        print(f"Создан новый EmulsionTestResult для образца {pk}")
        print(f"EmulsionTestResult ID: {test_result.id}")
    else:
        print(f"Загружен существующий EmulsionTestResult для образца {pk}")
        print(f"EmulsionTestResult ID: {test_result.id}")
        print(f"Данные в объекте:")
        print(f"  apply_area: {test_result.apply_area}")
        print(f"  decay_index_w1: {test_result.decay_index_w1}")
        print(f"  decay_index_w2: {test_result.decay_index_w2}")
        print(f"  decay_index_w3: {test_result.decay_index_w3}")
        print(f"  decay_index_value: {test_result.decay_index_value}")
        print(f"  binder_content_value: {test_result.binder_content_value}")
        print(f"  remaining_value: {test_result.remaining_value}")
        print(f"  resistance_after7_value: {test_result.resistance_after7_value}")
    
    if request.method == 'POST':
        if request.POST.get('action') == 'save':
            # Сохраняем данные эмульсии
            save_emulsion_test_result(request, test_result, sample)
            return redirect('sample_list')
    
    # Передаем test_result в контекст
    return render(request, 'labtests/emulsion_58952_test_form.html', {
        'sample': sample,
        'test_result': test_result
    })


def save_emulsion_test_result(request, test_result, sample):
    """Сохраняет результаты тестирования эмульсии"""
    
    if not EXTRA_MODELS_AVAILABLE:
        # Если модели недоступны, ничего не делаем
        return
    
    print(f"\n=== НАЧАЛО СОХРАНЕНИЯ ЭМУЛЬСИИ для образца {sample.pk} ===")
    
    # Маппинг полей для эмульсии
    fields_mapping = {
        # Область применения
        'apply_area': int,
        
        # Внешний вид
        'appearance': str,
        
        # Индекс распада
        'decay_index_w1': float,
        'decay_index_w2': float,
        'decay_index_w3': float,
        'decay_index_value': float,
        'decay_index_min': float,
        'decay_index_max': float,
        
        # Условная вязкость
        'viscosity_time': float,
        'viscosity_value': float,
        
        # pH
        'ph_value': float,
        
        # Массовая доля остатка на сите
        'sieve_08_container_weight': float,
        'sieve_08_container_with_residue': float,
        'sieve_08_emulsion_weight': float,
        'sieve_08_residue_percent': float,
        
        'sieve_014_container_weight': float,
        'sieve_014_container_with_residue': float,
        'sieve_014_emulsion_weight': float,
        'sieve_014_residue_percent': float,
        
        # Содержание вяжущего с эмульгатором
        'binder_content_w1': float,
        'binder_content_w2': float,
        'binder_content_w3': float,
        'binder_content_value': float,
        'binder_content_min': float,
        'binder_content_max': float,
        
        # Остаток на сите 0.14
        'remaining_w1': float,
        'remaining_w2': float,
        'remaining_w3': float,
        'remaining_w4': float,
        'remaining_w5': float,
        'remaining_value': float,
        'remaining_max': float,
        
        # Остаток на сите 0.14 после 7 суток
        'remaining_after7_w1': float,
        'remaining_after7_w2': float,
        'remaining_after7_w3': float,
        'remaining_after7_w4': float,
        'remaining_after7_w5': float,
        'remaining_after7_value': float,
        'remaining_after7_max': float,
        
        # Устойчивость к расслоению
        'resistance_cylinder1_volume': float,
        'resistance_cylinder1_volume_after7': float,
        'resistance_cylinder1_delamination': float,
        'resistance_cylinder2_volume': float,
        'resistance_cylinder2_volume_after7': float,
        'resistance_cylinder2_delamination': float,
        'resistance_after7_value': float,
        'resistance_after7_max': float,
        
        # Адгезия к минеральному материалу
        'mineral_material_adhesion': float,
        'visual_quality': int,
        
        # Массовая доля вяжущего (дополнительные пробы)
        'binder_1_container_weight': float,
        'binder_1_emulsion_before': float,
        'binder_1_after_evaporation': float,
        'binder_1_content': float,
        
        'binder_2_container_weight': float,
        'binder_2_emulsion_before': float,
        'binder_2_after_evaporation': float,
        'binder_2_content': float,
        
        'binder_average': float,
        
        # Устойчивость при хранении
        'stability_7_container_weight': float,
        'stability_7_sample_weight': float,
        'stability_7_residue_weight': float,
        'stability_7_percent': float,
        
        'stability_30_container_weight': float,
        'stability_30_sample_weight': float,
        'stability_30_residue_weight': float,
        'stability_30_percent': float,
        
        # Устойчивость к перемешиванию
        'mixing_container_weight': float,
        'mixing_sample_weight': float,
        'mixing_residue_weight': float,
        'mixing_stability_percent': float,
        
        # Устойчивость при транспортировании
        'transport_stability': str,
        
        # Сцепление
        'adhesion': str,
        
        # Глубина проникания иглы
        'needle_penetration_1': float,
        'needle_penetration_2': float,
        'needle_penetration_3': float,
        'needle_penetration_average': float,
        
        # Температура размягчения
        'softening_temp_1': float,
        'softening_temp_2': float,
        'softening_temp_average': float,
        
        # Эластичность
        'elasticity_1': float,
        'elasticity_2': float,
        'elasticity_3': float,
        'elasticity_average': float,
    }
    
    # Определяем readonly поля (вычисляемые)
    readonly_fields = [
        'decay_index_value',
        'viscosity_value',
        'binder_content_value',
        'remaining_value',
        'remaining_after7_value',
        'resistance_cylinder1_delamination',
        'resistance_cylinder2_delamination',
        'resistance_after7_value',
        'mineral_material_adhesion',
        'sieve_08_residue_percent', 'sieve_014_residue_percent',
        'binder_1_content', 'binder_2_content', 'binder_average',
        'stability_7_percent', 'stability_30_percent',
        'mixing_stability_percent',
        'needle_penetration_average',
        'softening_temp_average',
        'elasticity_average',
    ]
    
    # Сохраняем все поля
    saved_fields = {}
    for field_name, field_type in fields_mapping.items():
        value = request.POST.get(field_name, '')
        
        # Логируем полученные значения
        if value:
            print(f"{field_name}: '{value}'")
        
        # Обработка значений
        if field_type == float:
            try:
                if value:
                    # Заменяем запятую на точку для корректного преобразования
                    value = str(value).replace(',', '.')
                    processed_value = float(value)
                else:
                    processed_value = None
            except (ValueError, TypeError) as e:
                print(f"Ошибка преобразования {field_name}: {e}")
                processed_value = None
        elif field_type == int:
            try:
                processed_value = int(value) if value else 0
            except (ValueError, TypeError):
                processed_value = 0
        elif field_type == str:
            processed_value = str(value) if value else ''
        else:
            processed_value = value
        
        # Для readonly полей сохраняем существующие значения, если новые пустые
        if field_name in readonly_fields:
            if processed_value is None or processed_value == '':
                existing_value = getattr(test_result, field_name, None)
                if existing_value is not None and existing_value != '':
                    processed_value = existing_value
                    print(f"  Сохраняем существующее значение для {field_name}: {existing_value}")
        
        # Сохраняем значение
        setattr(test_result, field_name, processed_value)
        saved_fields[field_name] = processed_value
    
    # Сохраняем в базу данных
    try:
        test_result.save()
        print(f"\n✅ Данные эмульсии сохранены для образца {sample.pk}")
        
        # Проверяем заполненность основных полей для определения статуса
        # Используем только те поля, которые реально есть в форме эмульсии
        required_fields = [
            # Индекс распада
            'decay_index_w1', 'decay_index_w2', 'decay_index_w3',
            # Содержание вяжущего с эмульгатором
            'binder_content_w1', 'binder_content_w2', 'binder_content_w3',
            # Остаток на сите 0.14
            'remaining_w1', 'remaining_w2', 'remaining_w3', 'remaining_w4', 'remaining_w5',
            # Остаток на сите 0.14 после 7 суток
            'remaining_after7_w1', 'remaining_after7_w2', 'remaining_after7_w3', 
            'remaining_after7_w4', 'remaining_after7_w5',
            # Устойчивость к расслоению
            'resistance_cylinder1_volume', 'resistance_cylinder1_volume_after7',
            'resistance_cylinder2_volume', 'resistance_cylinder2_volume_after7',
            # Визуальная оценка качества
            'visual_quality'
        ]
        
        all_filled = True
        missing_fields = []
        for field_name in required_fields:
            value = getattr(test_result, field_name, None)
            if value is None or value == '':
                all_filled = False
                missing_fields.append(field_name)
        
        # Обновляем статус образца
        if all_filled:
            sample.status = 'completed'
            sample.completion_date = date.today()
            print(f"\n✅ Все обязательные поля заполнены. Статус образца обновлен на 'Завершено'")
        else:
            sample.status = 'in_progress'
            print(f"\n⚠️ Не все обязательные поля заполнены. Статус остается 'В работе'")
            if missing_fields:
                print(f"   Не заполненные поля: {', '.join(missing_fields[:5])}..." if len(missing_fields) > 5 else f"   Не заполненные поля: {', '.join(missing_fields)}")
        
        sample.save()
        
    except Exception as e:
        print(f"❌ Ошибка при сохранении: {e}")
        raise e


# Форма тестирования минерального порошка
def mineral_powder_test_form(request, pk):
    """Форма для ввода результатов испытаний минерального порошка"""
    
    if not EXTRA_MODELS_AVAILABLE:
        # Если модели недоступны, используем стандартную форму
        sample = get_object_or_404(TestSample, pk=pk)
        test_result, created = TestResult.objects.get_or_create(sample=sample)
        return render(request, 'labtests/sample_test_form.html', {
            'sample': sample,
            'test_result': test_result
        })
    
    sample = get_object_or_404(TestSample, pk=pk)
    test_result, created = MineralPowderTestResult.objects.get_or_create(sample=sample)
    
    # Отладочный вывод
    if created:
        print(f"Создан новый MineralPowderTestResult для образца {pk}")
    else:
        print(f"Загружен существующий MineralPowderTestResult для образца {pk}")
    
    if request.method == 'POST':
        if request.POST.get('action') == 'save':
            # Сохраняем данные минерального порошка
            save_mineral_powder_test_result(request, test_result, sample)
            return redirect('sample_list')
    
    # Передаем test_result в контекст
    return render(request, 'labtests/mineral_powder_32761_test_form.html', {
        'sample': sample,
        'test_result': test_result
    })


def save_mineral_powder_test_result(request, test_result, sample):
    """Сохраняет результаты тестирования минерального порошка"""
    
    if not EXTRA_MODELS_AVAILABLE:
        # Если модели недоступны, ничего не делаем
        return
    
    print(f"\n=== НАЧАЛО СОХРАНЕНИЯ МИНЕРАЛЬНОГО ПОРОШКА для образца {sample.pk} ===")
    
    # Маппинг полей для минерального порошка
    fields_mapping = {
        # Гранулометрический состав
        'sample_weight': float,
        'sieve_2_0125_weight': float,
        'sieve_0125_weight': float,
        'sieve_0063_weight': float,
        'sieve_less_0063_weight': float,
        'sieve_2_0125_remainder': float,
        'sieve_0125_remainder': float,
        'sieve_0063_remainder': float,
        'sieve_less_0063_remainder': float,
        'sieve_2_0125_full_remainder': float,
        'sieve_0125_full_remainder': float,
        'sieve_0063_full_remainder': float,
        'sieve_less_0063_full_remainder': float,
        'sieve_2_0125_passes': float,
        'sieve_0125_passes': float,
        'sieve_0063_passes': float,
        'sieve_less_0063_passes': float,
        
        # Влажность
        'humidity_plate_weight_before': float,
        'humidity_plate_weight_after': float,
        'humidity_plate_weight': float,
        'humidity_value': float,
        
        # Истинная плотность
        'real_density_1_weight_with_powder': float,
        'real_density_1_empty_weight': float,
        'real_density_1_weight_with_water': float,
        'real_density_1_weight_with_powder_and_water': float,
        'real_density_1_value': float,
        'real_density_2_weight_with_powder': float,
        'real_density_2_empty_weight': float,
        'real_density_2_weight_with_water': float,
        'real_density_2_weight_with_powder_and_water': float,
        'real_density_2_value': float,
        'real_density_average': float,
        
        # Средняя плотность
        'average_density_bottom_weight_with_powder': float,
        'average_density_bottom_weight': float,
        'average_density_volume': float,
        'average_density_value': float,
        'porosity': float,
        
        # Битумоемкость
        'bitumen_capacity_weight': float,
        'bitumen_capacity_weight_after': float,
        'bitumen_capacity_oil_weight': float,
        'bitumen_capacity_real_density': float,
        'bitumen_capacity_value': float,
    }
    
    # Определяем readonly поля (вычисляемые)
    readonly_fields = [
        'sieve_2_0125_remainder', 'sieve_0125_remainder', 'sieve_0063_remainder', 'sieve_less_0063_remainder',
        'sieve_2_0125_full_remainder', 'sieve_0125_full_remainder', 'sieve_0063_full_remainder', 'sieve_less_0063_full_remainder',
        'sieve_2_0125_passes', 'sieve_0125_passes', 'sieve_0063_passes', 'sieve_less_0063_passes',
        'humidity_value',
        'real_density_1_value', 'real_density_2_value', 'real_density_average',
        'average_density_value', 'porosity',
        'bitumen_capacity_value',
    ]
    
    # Сохраняем все поля
    saved_fields = {}
    for field_name, field_type in fields_mapping.items():
        value = request.POST.get(field_name, '')
        
        # Логируем полученные значения
        if value:
            print(f"{field_name}: '{value}'")
        
        # Обработка значений
        if field_type == float:
            try:
                if value:
                    value = value.replace(',', '.')
                    processed_value = float(value)
                else:
                    processed_value = None
            except (ValueError, TypeError) as e:
                print(f"Ошибка преобразования {field_name}: {e}")
                processed_value = None
        elif field_type == str:
            processed_value = str(value) if value else ''
        else:
            processed_value = value
        
        # Для readonly полей сохраняем существующие значения, если новые пустые
        if field_name in readonly_fields:
            if processed_value is None or processed_value == '':
                existing_value = getattr(test_result, field_name, None)
                if existing_value is not None and existing_value != '':
                    processed_value = existing_value
                    print(f"  Сохраняем существующее значение для {field_name}: {existing_value}")
        
        # Сохраняем значение
        setattr(test_result, field_name, processed_value)
        saved_fields[field_name] = processed_value
    
    # Сохраняем в базу данных
    try:
        test_result.save()
        print(f"\n✅ Данные минерального порошка сохранены для образца {sample.pk}")
        
        # Проверяем заполненность основных полей для определения статуса
        required_fields = [
            # Гранулометрический состав
            'sample_weight',
            'sieve_2_0125_weight', 'sieve_0125_weight', 'sieve_0063_weight', 'sieve_less_0063_weight',
            # Влажность
            'humidity_plate_weight_before', 'humidity_plate_weight_after', 'humidity_plate_weight',
            # Истинная плотность (хотя бы одно измерение)
            'real_density_1_weight_with_powder', 'real_density_1_empty_weight',
            'real_density_1_weight_with_water', 'real_density_1_weight_with_powder_and_water',
            # Средняя плотность
            'average_density_bottom_weight_with_powder', 'average_density_bottom_weight', 'average_density_volume',
            # Битумоемкость
            'bitumen_capacity_weight', 'bitumen_capacity_weight_after', 'bitumen_capacity_oil_weight',
        ]
        
        all_filled = True
        missing_fields = []
        for field_name in required_fields:
            value = getattr(test_result, field_name, None)
            if value is None or value == '':
                all_filled = False
                missing_fields.append(field_name)
        
        # Обновляем статус образца
        if all_filled:
            sample.status = 'completed'
            sample.completion_date = date.today()
            print(f"\n✅ Все обязательные поля заполнены. Статус образца обновлен на 'Завершено'")
        else:
            sample.status = 'in_progress'
            print(f"\n⚠️ Не все обязательные поля заполнены. Статус остается 'В работе'")
            if missing_fields:
                print(f"   Не заполненные поля: {', '.join(missing_fields[:5])}..." if len(missing_fields) > 5 else f"   Не заполненные поля: {', '.join(missing_fields)}")
        
        sample.save()
        
    except Exception as e:
        print(f"❌ Ошибка при сохранении: {e}")
        raise e


# Функция для диагностики данных эмульсии
def check_emulsion_data(request):
    """Страница проверки данных эмульсии в БД"""
    
    # Получаем все образцы эмульсии
    emulsion_samples = TestSample.objects.filter(
        material__name__icontains='эмульс'
    ) | TestSample.objects.filter(
        gost__number__icontains='58952'
    )
    
    samples_data = []
    for sample in emulsion_samples:
        data = {'id': sample.id, 'sample_number': sample.sample_number, 'result': None}
        
        if EXTRA_MODELS_AVAILABLE:
            try:
                result = EmulsionTestResult.objects.get(sample=sample)
                data['result'] = result
            except EmulsionTestResult.DoesNotExist:
                pass
        
        samples_data.append(data)
    
    return render(request, 'labtests/check_emulsion_data.html', {
        'samples': samples_data
    })


# Функции для работы с профилем пользователя
@login_required
def profile_view(request):
    """Просмотр и редактирование профиля пользователя"""
    user = request.user
    profile, created = UserProfile.objects.get_or_create(user=user)
    
    if request.method == 'POST':
        # Обновляем данные пользователя
        user.email = request.POST.get('email', '')
        user.first_name = request.POST.get('first_name', '')
        user.last_name = request.POST.get('last_name', '')
        user.save()
        
        # Обновляем данные профиля
        profile.department = request.POST.get('department', '')
        profile.position = request.POST.get('position', '')
        profile.phone = request.POST.get('phone', '')
        profile.save()
        
        messages.success(request, 'Профиль успешно обновлен')
        return redirect('profile')
    
    # Получаем статистику по образцам
    total_samples = TestSample.objects.filter(owner=user).count()
    in_progress_samples = TestSample.objects.filter(owner=user, status='in_progress').count()
    completed_samples = TestSample.objects.filter(owner=user, status='completed').count()
    
    # Последние образцы
    recent_samples = TestSample.objects.filter(owner=user).select_related(
        'material', 'gost'
    ).order_by('-id')[:5]
    
    context = {
        'user': user,
        'profile': profile,
        'total_samples': total_samples,
        'in_progress_samples': in_progress_samples,
        'completed_samples': completed_samples,
        'recent_samples': recent_samples,
    }
    
    return render(request, 'labtests/profile/profile.html', context)


def register_view(request):
    """Регистрация нового пользователя"""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, f'Аккаунт {username} успешно создан!')
            return redirect('sample_list')
    else:
        form = UserCreationForm()
    
    return render(request, 'registration/register.html', {'form': form})


def save_shchps_test_result(request, test_result, sample):
    """Сохраняет результаты тестирования ЩПС"""
    
    print(f"\n=== НАЧАЛО СОХРАНЕНИЯ ЩПС для образца {sample.pk} ===")
    
    # Маппинг полей для ЩПС
    fields_mapping = {
        # Содержание пылевидных и глинистых частиц
        'dust_initial_weight': float,
        'dust_after_wash_weight': float,
        'dust_clay_content': float,
        
        # Зерновой состав (8 фракций)
        'sieve_40_weight': float,
        'sieve_40_partial': float,
        'sieve_40_full': float,
        
        'sieve_20_weight': float,
        'sieve_20_partial': float,
        'sieve_20_full': float,
        
        'sieve_10_weight': float,
        'sieve_10_partial': float,
        'sieve_10_full': float,
        
        'sieve_5_weight': float,
        'sieve_5_partial': float,
        'sieve_5_full': float,
        
        'sieve_2_5_weight': float,
        'sieve_2_5_partial': float,
        'sieve_2_5_full': float,
        
        'sieve_0_63_weight': float,
        'sieve_0_63_partial': float,
        'sieve_0_63_full': float,
        
        'sieve_0_16_weight': float,
        'sieve_0_16_partial': float,
        'sieve_0_16_full': float,
        
        'sieve_0_05_weight': float,
        'sieve_0_05_partial': float,
        'sieve_0_05_full': float,
        
        # Дробимость (4 фракции)
        'fragility_40_70_initial': float,
        'fragility_40_70_after': float,
        'fragility_40_70_value': float,
        
        'fragility_20_40_initial': float,
        'fragility_20_40_after': float,
        'fragility_20_40_value': float,
        
        'fragility_10_20_initial': float,
        'fragility_10_20_after': float,
        'fragility_10_20_value': float,
        
        'fragility_5_10_initial': float,
        'fragility_5_10_after': float,
        'fragility_5_10_value': float,
        
        'fragility_summary': float,
        
        # Лещадность (4 фракции)
        'flakiness_40_70_initial': float,
        'flakiness_40_70_flaky': float,
        'flakiness_40_70_value': float,
        
        'flakiness_20_40_initial': float,
        'flakiness_20_40_flaky': float,
        'flakiness_20_40_value': float,
        
        'flakiness_10_20_initial': float,
        'flakiness_10_20_flaky': float,
        'flakiness_10_20_value': float,
        
        'flakiness_5_10_initial': float,
        'flakiness_5_10_flaky': float,
        'flakiness_5_10_value': float,
        
        'flakiness_summary': float,
    }
    
    # Определяем readonly поля (вычисляемые)
    readonly_fields = [
        'dust_clay_content',
        'sieve_40_partial', 'sieve_40_full',
        'sieve_20_partial', 'sieve_20_full',
        'sieve_10_partial', 'sieve_10_full',
        'sieve_5_partial', 'sieve_5_full',
        'sieve_2_5_partial', 'sieve_2_5_full',
        'sieve_0_63_partial', 'sieve_0_63_full',
        'sieve_0_16_partial', 'sieve_0_16_full',
        'sieve_0_05_partial', 'sieve_0_05_full',
        'fragility_40_70_value', 'fragility_20_40_value',
        'fragility_10_20_value', 'fragility_5_10_value',
        'fragility_summary',
        'flakiness_40_70_value', 'flakiness_20_40_value',
        'flakiness_10_20_value', 'flakiness_5_10_value',
        'flakiness_summary',
    ]
    
    # Сохраняем все поля
    saved_fields = {}
    for field_name, field_type in fields_mapping.items():
        value = request.POST.get(field_name, '')
        
        # Логируем полученные значения
        if value:
            print(f"{field_name}: '{value}'")
        
        # Обработка значений
        if field_type == float:
            try:
                # Заменяем запятую на точку перед преобразованием
                if value:
                    value = value.replace(',', '.')
                    processed_value = float(value)
                else:
                    processed_value = None
            except (ValueError, TypeError) as e:
                print(f"Ошибка преобразования {field_name}: {e}")
                processed_value = None
        elif field_type == str:
            processed_value = str(value) if value else ''
        else:
            processed_value = value
        
        # Для readonly полей сохраняем существующие значения, если новые пустые
        if field_name in readonly_fields:
            if processed_value is None or processed_value == '':
                existing_value = getattr(test_result, field_name, None)
                if existing_value is not None and existing_value != '':
                    processed_value = existing_value
                    print(f"  Сохраняем существующее значение для {field_name}: {existing_value}")
        
        # Сохраняем значение
        setattr(test_result, field_name, processed_value)
        saved_fields[field_name] = processed_value
    
    # Сохраняем в базу данных
    try:
        test_result.save()
        print(f"\n✅ Данные ЩПС сохранены для образца {sample.pk}")
        
        # Логируем сохраненные значения
        print("\n=== СОХРАНЕННЫЕ ЗНАЧЕНИЯ ===")
        non_empty_count = 0
        for field_name, value in saved_fields.items():
            if value is not None and value != '' and value != 0:
                print(f"{field_name}: {value}")
                non_empty_count += 1
        print(f"\nВсего сохранено непустых полей: {non_empty_count}")
        
        # Проверяем заполненность основных полей для определения статуса
        required_fields = [
            # Пылевидные и глинистые
            'dust_initial_weight', 'dust_after_wash_weight',
            # Зерновой состав
            'sieve_40_weight', 'sieve_20_weight', 'sieve_10_weight',
            'sieve_5_weight', 'sieve_2_5_weight', 'sieve_0_63_weight',
            'sieve_0_16_weight', 'sieve_0_05_weight',
            # Дробимость (хотя бы две фракции)
            'fragility_20_40_initial', 'fragility_20_40_after',
            'fragility_10_20_initial', 'fragility_10_20_after',
            # Лещадность (хотя бы две фракции)
            'flakiness_20_40_initial', 'flakiness_20_40_flaky',
            'flakiness_10_20_initial', 'flakiness_10_20_flaky',
        ]
        
        all_filled = True
        missing_fields = []
        for field_name in required_fields:
            value = getattr(test_result, field_name, None)
            if value is None or value == '':
                all_filled = False
                missing_fields.append(field_name)
        
        # Обновляем статус образца
        if all_filled:
            sample.status = 'completed'
            sample.completion_date = date.today()
            print(f"\n✅ Все обязательные поля заполнены. Статус образца обновлен на 'Завершено'")
        else:
            sample.status = 'in_progress'
            print(f"\n⚠️ Не все обязательные поля заполнены. Статус остается 'В работе'")
            if missing_fields:
                print(f"   Не заполненные поля: {', '.join(missing_fields[:5])}..." if len(missing_fields) > 5 else f"   Не заполненные поля: {', '.join(missing_fields)}")
        
        sample.save()
        
    except Exception as e:
        print(f"❌ Ошибка при сохранении: {e}")
        raise e
