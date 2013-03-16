from media.models import Photo, Gallery 
from django.contrib import admin

class PhotoAdmin(admin.ModelAdmin):

    fieldsets = (
            (None, {
                'fields': ('name','image','caption','photographer',
                ('publish_date','expiry_date'),
                
                'upload_date',)
            }),
        )
    list_display = ('id','name','caption',"thumb")
    list_filter = ['publish_date']
    search_fields = ['caption']
    #date_hierarchy = 'publish_date'
    

    save_on_top=True
    list_per_page=20

    

admin.site.register(Photo,PhotoAdmin)

admin.site.register(Gallery)