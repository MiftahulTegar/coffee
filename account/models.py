from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.urls import reverse

class UserProfileInfo(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    nama = models.CharField(max_length=200, blank=True, null=True)
    Tanggal_Lahir = models.DateField(blank=True, null=True)
    telepon = models.CharField(max_length=15, db_index=True)
    alamat = models.TextField()
    foto_profil = models.ImageField(upload_to='profile_pics',blank=True)

    def __str__(self):
        return self.user.username

class Kategori(models.Model):
    nama = models.CharField(max_length=200, db_index=True)
    slug = models.CharField(max_length=200, db_index=True)
    
    class Meta:
        ordering = ('nama',)

    def __str__(self):
        return self.nama

class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager,
                self).get_queryset()\
                        .filter(status='published')

class Produk(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )

    Kategori = models.ForeignKey(Kategori, on_delete=models.CASCADE, related_name='produk')
    nama = models.CharField(max_length=200, db_index=True)
    slug = models.CharField(max_length=200, db_index=True)
    image = models.ImageField(max_length=255, upload_to='produk', blank=True)
    deskripsi = models.TextField(blank=True)
    harga = models.DecimalField(max_digits=10, decimal_places=0)
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    published = PublishedManager()

    class Meta:
        ordering = ('harga',)

    def __str__(self):
        return self.nama

    def get_absolute_url(self):
        return reverse('account:post_detail', args=[self.slug])

class Comment(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('created', 'Created'),
    )

    nama = models.CharField(max_length=80, default=None)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    post = models.ForeignKey(Produk, on_delete=models.CASCADE, related_name='blog_comments')

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return f'Komentar ditulis oleh {self.nama}'