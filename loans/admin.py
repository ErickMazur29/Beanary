from django.contrib import admin
from loans.models import Loan


@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin):
    list_display = ('id', 'book', 'borrowed_at', 'due_date', 'returned_at')
    search_fields = ('book__title',)
