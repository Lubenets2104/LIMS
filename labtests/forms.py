from django import forms
from .models import TestSample, GOST, MixName, Indicator

class TestSampleForm(forms.ModelForm):
    class Meta:
        model = TestSample
        exclude = ['status']  # Исключаем поле status из формы
        widgets = {
            'sampling_date': forms.DateInput(attrs={'type': 'date'}),
            'received_date': forms.DateInput(attrs={'type': 'date'}),
            'completion_date': forms.DateInput(attrs={'type': 'date'}),
            'indicators': forms.SelectMultiple(attrs={'size': 5, 'id': 'id_indicators'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['gost'].queryset = GOST.objects.none()
        self.fields['mix'].queryset = MixName.objects.none()
        self.fields['indicators'].queryset = Indicator.objects.none()
        
        # По умолчанию поле mix необязательное
        self.fields['mix'].required = False

        if 'material' in self.data:
            try:
                material_id = int(self.data.get('material'))
                self.fields['gost'].queryset = GOST.objects.filter(material_id=material_id)
            except (ValueError, TypeError):
                pass

        if 'gost' in self.data:
            try:
                gost_id = int(self.data.get('gost'))
                mix_queryset = MixName.objects.filter(gost_id=gost_id)
                self.fields['mix'].queryset = mix_queryset
                # Делаем поле обязательным, если есть доступные смеси
                if mix_queryset.exists():
                    self.fields['mix'].required = True
                self.fields['indicators'].queryset = Indicator.objects.filter(gost_id=gost_id)
            except (ValueError, TypeError):
                pass
    
    def clean(self):
        cleaned_data = super().clean()
        gost = cleaned_data.get('gost')
        mix = cleaned_data.get('mix')
        
        # Проверяем, если для выбранного ГОСТа есть смеси, то смесь обязательна
        if gost:
            mixes_exist = MixName.objects.filter(gost=gost).exists()
            if mixes_exist and not mix:
                # Добавляем ошибку к полю mix, но НЕ очищаем другие данные
                self.add_error('mix', 'Для выбранного ГОСТа необходимо выбрать смесь.')
                # НЕ вызываем raise ValidationError, чтобы не потерять введенные данные
        
        return cleaned_data
