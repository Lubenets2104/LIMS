from rest_framework import serializers
from .models import Material, GOST, MixName, Indicator, TestSample


class MaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = ['id', 'name']


class GOSTSerializer(serializers.ModelSerializer):
    material_name = serializers.CharField(source='material.name', read_only=True)
    
    class Meta:
        model = GOST
        fields = ['id', 'number', 'material', 'material_name']


class MixNameSerializer(serializers.ModelSerializer):
    gost_number = serializers.CharField(source='gost.number', read_only=True)
    
    class Meta:
        model = MixName
        fields = ['id', 'name', 'gost', 'gost_number']


class IndicatorSerializer(serializers.ModelSerializer):
    material_name = serializers.CharField(source='material.name', read_only=True)
    gost_number = serializers.CharField(source='gost.number', read_only=True)
    
    class Meta:
        model = Indicator
        fields = ['id', 'name', 'material', 'material_name', 'gost', 'gost_number']


class TestSampleListSerializer(serializers.ModelSerializer):
    material_name = serializers.CharField(source='material.name', read_only=True)
    gost_number = serializers.CharField(source='gost.number', read_only=True)
    mix_name = serializers.CharField(source='mix.name', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = TestSample
        fields = [
            'id', 'sample_number', 'sampling_date', 'received_date', 
            'completion_date', 'customer', 'supplier', 'object_name',
            'material', 'material_name', 'gost', 'gost_number', 
            'mix', 'mix_name', 'status', 'status_display'
        ]


class TestSampleDetailSerializer(serializers.ModelSerializer):
    material_name = serializers.CharField(source='material.name', read_only=True)
    gost_number = serializers.CharField(source='gost.number', read_only=True)
    mix_name = serializers.CharField(source='mix.name', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    indicators_list = IndicatorSerializer(source='indicators', many=True, read_only=True)
    
    class Meta:
        model = TestSample
        fields = [
            'id', 'sample_number', 'sampling_date', 'received_date', 
            'completion_date', 'customer', 'supplier', 'object_name',
            'material', 'material_name', 'gost', 'gost_number', 
            'mix', 'mix_name', 'status', 'status_display',
            'indicators', 'indicators_list'
        ]


class TestSampleCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestSample
        fields = [
            'sample_number', 'sampling_date', 'received_date', 
            'completion_date', 'customer', 'supplier', 'object_name',
            'material', 'gost', 'mix', 'status', 'indicators'
        ]
    
    def validate(self, data):
        # Проверяем что GОСТ соответствует материалу
        if data.get('gost') and data.get('material'):
            if data['gost'].material != data['material']:
                raise serializers.ValidationError(
                    "ГОСТ должен соответствовать выбранному материалу"
                )
        
        # Проверяем что смесь соответствует ГОСТу
        if data.get('mix') and data.get('gost'):
            if data['mix'].gost != data['gost']:
                raise serializers.ValidationError(
                    "Смесь должна соответствовать выбранному ГОСТу"
                )
        
        return data
