from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Material, GOST, Indicator, TestSample, MixName, TestResult, UserProfile

# Безопасный импорт дополнительных моделей
try:
    from .models_extra import BitumenTestResult33133, EmulsionTestResult, MineralPowderTestResult
    EXTRA_MODELS_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ Не удалось импортировать дополнительные модели: {e}")
    EXTRA_MODELS_AVAILABLE = False


@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(GOST)
class GOSTAdmin(admin.ModelAdmin):
    list_display = ('number', 'material')
    list_filter = ('material',)
    search_fields = ('number',)


@admin.register(MixName)
class MixNameAdmin(admin.ModelAdmin):
    list_display = ('name', 'gost')
    list_filter = ('gost',)
    search_fields = ('name',)


@admin.register(Indicator)
class IndicatorAdmin(admin.ModelAdmin):
    list_display = ('name', 'material', 'gost')
    list_filter = ('material', 'gost')
    search_fields = ('name',)


# Inline для профиля пользователя
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Профиль'

# Расширяем админку User
class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)

# Перерегистрируем User модель
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

@admin.register(TestSample)
class TestSampleAdmin(admin.ModelAdmin):
    list_display = ('sample_number', 'material', 'gost', 'status', 'owner')
    list_filter = ('material', 'gost', 'status', 'owner')
    search_fields = ('sample_number', 'customer', 'supplier')


@admin.register(TestResult)
class TestResultAdmin(admin.ModelAdmin):
    list_display = ('sample', 'result_class', 'created_at')
    list_filter = ('result_class', 'created_at')
    search_fields = ('sample__sample_number',)


# Регистрация дополнительных моделей, если они доступны
if EXTRA_MODELS_AVAILABLE:
    # Регистрация модели битума
    @admin.register(BitumenTestResult33133)
    class BitumenTestResult33133Admin(admin.ModelAdmin):
        list_display = ('sample', 'needle_deep', 'softening_temperature', 'created_at')
        list_filter = ('created_at',)
        search_fields = ('sample__sample_number',)

    # Регистрация модели эмульсии
    @admin.register(EmulsionTestResult)
    class EmulsionTestResultAdmin(admin.ModelAdmin):
        list_display = ('sample', 'appearance', 'ph_value', 'created_at')
        list_filter = ('created_at',)
        search_fields = ('sample__sample_number',)
    
    # Регистрация модели минерального порошка
    @admin.register(MineralPowderTestResult)
    class MineralPowderTestResultAdmin(admin.ModelAdmin):
        list_display = ('sample', 'humidity_value', 'real_density_average', 'created_at')
        list_filter = ('created_at',)
        search_fields = ('sample__sample_number',)
