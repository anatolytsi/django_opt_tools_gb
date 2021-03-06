from django.db import models


class ProductCategory(models.Model):
    name = models.CharField(max_length=64, unique=True, db_index=True)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = "Product Categories"

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=256, db_index=True)
    description = models.TextField(blank=True)
    short_description = models.CharField(max_length=64, blank=True, db_index=True)
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0, db_index=True)
    quantity = models.PositiveIntegerField(default=0, db_index=True)
    image = models.ImageField(upload_to="products_images", blank=True)
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    is_active = models.BooleanField(
        verbose_name='активен',
        default=True,
        db_index=True
    )

    def __str__(self):
        return f"{self.name} | {self.category.name}"

    @staticmethod
    def get_items():
        return Product.objects.filter(is_active=True).order_by("category", "name")
