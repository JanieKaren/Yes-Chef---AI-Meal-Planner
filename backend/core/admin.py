from django.contrib import admin
from .models import Account, Ingredient

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_dietary_preferences', 'get_saved_recipes', 'get_fridge_inventory')
    search_fields = ('user__username', 'user__email')
    list_filter = ('user__is_active',)

    def get_dietary_preferences(self, obj):
        return ', '.join(obj.dietary_preferences) if obj.dietary_preferences else '-'
    get_dietary_preferences.short_description = 'Dietary Preferences'

    def get_saved_recipes(self, obj):
        return len(obj.saved_recipes)
    get_saved_recipes.short_description = 'Saved Recipes'

    def get_fridge_inventory(self, obj):
        return len(obj.fridge_inventory)
    get_fridge_inventory.short_description = 'Fridge Items'

@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'quantity', 'unit', 'expiration_date')
    list_filter = ('category', 'unit')
    search_fields = ('name',)
    date_hierarchy = 'expiration_date'
