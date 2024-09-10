from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='children')

    def __str__(self):
        return self.name
        
    

class Products(models.Model):
    name = models.TextField(blank=True, null=True)
    price = models.TextField(blank=True, null=True)
    original_price = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)#to find the deal rating
    current_price = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)# to find deal rating
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True, related_name='products')
    image = models.URLField()
    link = models.URLField()

    def __str__(self):
        return self.name

    def get_deal_rating(self):
        if self.original_price and self.current_price:
            discount = (self.original_price - self.current_price) / self.original_price * 100
            if discount < 10:
                return "Low"
            elif discount < 20:
                return "Medium"
            else:
                return "High"
        return "No discount"