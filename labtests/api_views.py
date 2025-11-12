from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

from .models import Material, GOST, MixName, Indicator, TestSample
from .serializers import (
    MaterialSerializer, GOSTSerializer, MixNameSerializer, 
    IndicatorSerializer, TestSampleListSerializer, 
    TestSampleDetailSerializer, TestSampleCreateSerializer
)


class MaterialViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Material.objects.all()
    serializer_class = MaterialSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['name']
    ordering = ['name']


class GOSTViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = GOST.objects.select_related('material')
    serializer_class = GOSTSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['material']
    search_fields = ['number', 'material__name']
    ordering_fields = ['number', 'material__name']
    ordering = ['number']


class MixNameViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = MixName.objects.select_related('gost', 'gost__material')
    serializer_class = MixNameSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['gost', 'gost__material']
    search_fields = ['name', 'gost__number']
    ordering_fields = ['name']
    ordering = ['name']


class IndicatorViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Indicator.objects.select_related('material', 'gost')
    serializer_class = IndicatorSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['material', 'gost']
    search_fields = ['name', 'material__name', 'gost__number']
    ordering_fields = ['name']
    ordering = ['name']


class TestSampleViewSet(viewsets.ModelViewSet):
    queryset = TestSample.objects.select_related(
        'material', 'gost', 'mix'
    ).prefetch_related('indicators')
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['material', 'gost', 'status', 'customer', 'supplier']
    search_fields = [
        'sample_number', 'customer', 'supplier', 'object_name',
        'material__name', 'gost__number'
    ]
    ordering_fields = [
        'sample_number', 'sampling_date', 'received_date', 
        'completion_date', 'status'
    ]
    ordering = ['-sampling_date']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return TestSampleListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return TestSampleCreateSerializer
        else:
            return TestSampleDetailSerializer
    
    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Статистика по образцам"""
        queryset = self.get_queryset()
        
        total_samples = queryset.count()
        status_stats = {}
        for status_code, status_name in TestSample.STATUS_CHOICES:
            count = queryset.filter(status=status_code).count()
            status_stats[status_code] = {
                'name': status_name,
                'count': count
            }
        
        material_stats = {}
        for material in Material.objects.all():
            count = queryset.filter(material=material).count()
            if count > 0:
                material_stats[material.name] = count
        
        return Response({
            'total_samples': total_samples,
            'status_stats': status_stats,
            'material_stats': material_stats
        })
    
    @action(detail=True, methods=['post'])
    def change_status(self, request, pk=None):
        """Изменение статуса образца"""
        sample = self.get_object()
        new_status = request.data.get('status')
        
        if new_status not in dict(TestSample.STATUS_CHOICES):
            return Response(
                {'error': 'Недопустимый статус'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        sample.status = new_status
        sample.save()
        
        serializer = self.get_serializer(sample)
        return Response(serializer.data)
