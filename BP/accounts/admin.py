from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from accounts.models import Account
from profiles.models import Profile

class AccountAdmin(UserAdmin):
    # 관리자 화면에 보여질 칼럼 지정
    list_display = ('username','name', 'nickname', 'email', 'create_at','last_login','is_admin','is_staff')
    search_fields = ('username','name', 'nickname', 'email')
    readonly_fields = ('id', 'create_at', 'last_login')
 
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
 
admin.site.register(Account, AccountAdmin)
admin.site.register(Profile)