from django.contrib import admin


class ImmortalAdmin(admin.ModelAdmin):
    exclude = ('deleted',)


class ImmortalTabularInline(admin.TabularInline):
    exclude = ('deleted',)


class ImmortalStackedInline(admin.StackedInline):
    exclude = ('deleted',)
