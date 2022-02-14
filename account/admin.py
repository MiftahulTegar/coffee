from django.contrib import admin
from .models import UserProfileInfo, Kategori, Produk, Comment

@admin.register(UserProfileInfo)
class UserProfileInfoAdmin(admin.ModelAdmin):
    list_display = ['user', 'nama', 'Tanggal_Lahir', 'telepon', 'foto_profil']

@admin.register(Kategori)
class KategoriAdmin(admin.ModelAdmin):
	list_display = ('nama', 'slug')
	list_filter = ('nama', 'slug')
	search_fields = ('nama', 'slug')
	prepopulated_fields = {'slug': ('nama',)}

@admin.register(Produk)
class ProdukAdmin(admin.ModelAdmin):
	list_display = ('nama', 'slug', 'harga', 'available', 'created', 'updated', 'status')
	list_filter = ('available', 'created', 'updated')
	search_fields = ('nama', 'slug')
	prepopulated_fields = {'slug': ('nama',)}

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('nama', 'body', 'post', 'created', 'updated', 'active', 'post_id')
    list_filter = ('active', 'created', 'updated', 'post_id')
    search_fields = ('nama', 'body')
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(active=True)
