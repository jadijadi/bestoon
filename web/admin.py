from django.contrib import admin
from .models import Expense, Income, Token, News
# Register your models here.
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'date',)
    list_filter = ('date',)
    search_fields = ('title', 'text',)
    class Meta:
        model = News
class TokenAdmin(admin.ModelAdmin):
    search_fields = ('user',)
    class Meta:
        model = Token
class IncomeAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount',)
    list_filter = ('date',)
    search_fields = ('title', 'text','amount',)
    class Meta:
        model = Income
class ExpenseAdmin(admin.ModelAdmin):
    list_filter = ('date',)
    search_fields = ('text', 'user','amount',)
    class Meta:
        model = Expense

admin.site.register(Expense,ExpenseAdmin)
admin.site.register(Income, IncomeAdmin)
admin.site.register(Token, TokenAdmin)
admin.site.register(News, NewsAdmin)
