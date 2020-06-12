from django.contrib import admin

# Register your models here.
from STEP_COUNTER_API_APP.models import UserTrener, User, UserDevices, Saverequest, Languages, Page, Translates,\
    Statistics, Follow, PaymentMetod, TrenerRate, ChatMessages, Chat



class TranslatesAdmin(admin.ModelAdmin):
    list_display = ('name_ru','page',)
    list_filter = (str('page'),'name_ru',)


class StatisticsAdmin(admin.ModelAdmin):
    list_display = ('user','created_at',)
    list_filter = (str('created_at'),'user',)



admin.site.register(UserTrener)
admin.site.register(TrenerRate)

admin.site.register(User)
admin.site.register(UserDevices)
admin.site.register(Saverequest)
admin.site.register(Languages)
admin.site.register(Page)
admin.site.register(Follow)
admin.site.register(PaymentMetod)
admin.site.register(ChatMessages)
admin.site.register(Chat)




admin.site.register(Statistics,StatisticsAdmin)



admin.site.register(Translates,TranslatesAdmin)



