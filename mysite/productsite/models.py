from django.db import models

# Create your models here

class Products(models.Model):
    name = models.TextField(blank=True, null=True)
    price = models.TextField(blank=True, null=True)
    categories = models.TextField(blank=True, null=True)
    image = models.URLField()
    link = models.URLField()

    class Meta:
        managed = False
        db_table = 'products'

class Category(models.Model):
    name = models.CharField(max_length=100)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='children')

    class Meta:
        unique_together = ('name', 'parent',)  #makes unique subcategories within each category
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name