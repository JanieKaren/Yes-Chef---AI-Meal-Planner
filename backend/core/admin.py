from django.contrib import admin
from .models import Account, Ingredient, Recipe

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_dietary_preferences', 'get_saved_recipes', 'get_allergies')
    search_fields = ('user__username', 'user__email')
    list_filter = ('user__is_active',)

    def get_dietary_preferences(self, obj):
        return ', '.join(obj.dietary_preferences) if obj.dietary_preferences else '-'
    get_dietary_preferences.short_description = 'Dietary Preferences'

    def get_saved_recipes(self, obj):
        return len(obj.saved_recipes)
    get_saved_recipes.short_description = 'Saved Recipes'

    def get_allergies(self, obj):
        return len(obj.allergies) if obj.allergies else '-'
    get_allergies.short_description = 'Allergies'

    

@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'quantity', 'unit', 'expiration_date')
    list_filter = ('category', 'unit')
    search_fields = ('name',)
    date_hierarchy = 'expiration_date'

@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'type', 'cuisine', 'time_required', 'nutritional_style', 'created_at')
    list_filter = ('type', 'cuisine', 'time_required', 'nutritional_style', 'created_at')
    search_fields = ('title', 'user__username', 'ingredients')
    readonly_fields = ('created_at', 'updated_at')