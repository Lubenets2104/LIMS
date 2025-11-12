from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
import json
from datetime import date
from .forms import TestSampleForm
from .models import TestSample, GOST, MixName, Indicator, TestResult

def sample_list(request):
    samples = TestSample.objects.select_related('material', 'gost', 'mix').all().order_by('-id')
    return render(request, 'labtests/sample_list.html', {'samples': samples})

def add_sample(request):
    if request.method == 'POST':
        form = TestSampleForm(request.POST)
        if form.is_valid():
            sample = form.save(commit=False)
            sample.status = 'in_progress'  # Автоматически устанавливаем статус "В работе"
            sample.save()
            form.save_m2m()  # Сохраняем many-to-many связи (indicators)
            return redirect('sample_list')
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
    
    # Получаем или создаем результаты испытаний
    test_result, created = TestResult.objects.get_or_create(sample=sample)
    
    if request.method == 'POST':
        if request.POST.get('action') == 'save':
            # Список всех полей модели TestResult для сохранения
            fields_to_save = [
                # Класс результата
                'result_class',
                # Зерновой состав
                'grain_initial_weight', 'grain_8_weight', 'grain_4_weight', 
                'grain_8_percent', 'grain_4_percent',
                # Пылевидные частицы
                'dust_initial_weight', 'dust_after_weight', 'dust_percent',
                # Сита
                'sieve_2_weight', 'sieve_1_weight', 'sieve_05_weight', 
                'sieve_025_weight', 'sieve_0125_weight',
                'sieve_2_partial', 'sieve_1_partial', 'sieve_05_partial', 
                'sieve_025_partial', 'sieve_0125_partial',
                'sieve_2_full', 'sieve_1_full', 'sieve_05_full', 
                'sieve_025_full', 'sieve_0125_full',
                # Модуль крупности
                'size_module_value', 'size_module_name',
                # Глина в комках
                'clay_initial_weight', 'clay_weight', 'clay_percent',
                # Влажность
                'humidity_1_number', 'humidity_1_container', 'humidity_1_with_sand',
                'humidity_1_after_dry', 'humidity_1_value',
                'humidity_2_number', 'humidity_2_container', 'humidity_2_with_sand',
                'humidity_2_after_dry', 'humidity_2_value', 'humidity_average',
                # Набухание глины
                'clay_swell_1_number', 'clay_swell_1_initial', 'clay_swell_1_after', 'clay_swell_1_k',
                'clay_swell_2_number', 'clay_swell_2_initial', 'clay_swell_2_after', 'clay_swell_2_k',
                'clay_swell_average_k', 'clay_swell_content', 'clay_swell_conclusion',
                # Насыпная плотность
                'bulk_1_volume', 'bulk_1_empty', 'bulk_1_full', 'bulk_1_density',
                'bulk_2_volume', 'bulk_2_empty', 'bulk_2_full', 'bulk_2_density',
                'bulk_average_density',
                # Истинная плотность
                'actual_1_number', 'actual_1_empty', 'actual_1_water', 
                'actual_1_sand', 'actual_1_full', 'actual_1_density',
                'actual_2_number', 'actual_2_empty', 'actual_2_water', 
                'actual_2_sand', 'actual_2_full', 'actual_2_density',
                'actual_average_density',
                # Пустотность
                'emptiness'
            ]
            
            # Сохраняем все поля
            for field_name in fields_to_save:
                value = request.POST.get(field_name, '')
                # Числовые поля
                if field_name.endswith(('_weight', '_percent', '_partial', '_full', '_value', 
                                       '_density', '_k', '_content', '_volume', '_empty', 
                                       '_after', '_initial', '_water', '_sand', 'emptiness', 
                                       'size_module_value', '_container', '_with_sand', 
                                       '_after_dry', '_average')):
                    try:
                        value = float(value) if value else None
                    except (ValueError, TypeError):
                        value = None
                # Устанавливаем значение
                setattr(test_result, field_name, value)
            
            test_result.save()
            
            # Обновляем статус образца
            sample.status = 'completed'
            sample.completion_date = date.today()
            sample.save()
            
            return redirect('sample_list')
    
    return render(request, 'labtests/sample_test_form.html', {
        'sample': sample,
        'test_result': test_result
    })

# Test results view (for 'completed' status)
def sample_test_results(request, pk):
    sample = get_object_or_404(TestSample, pk=pk)
    # Here you would load the test results from the database
    return render(request, 'labtests/sample_test_results.html', {'sample': sample})
