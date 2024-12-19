from django.db import models
from pytils.translit import slugify

class Category(models.Model):
    name = models.CharField("Название категории", max_length=191)
    image = models.ImageField("Фото", upload_to='category_images/')
    slug = models.SlugField(unique=True, blank=True, editable=False)

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return f"{self.name}"

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')
    name = models.CharField("Название товара",max_length=191)
    price = models.IntegerField("Цена")
    slug = models.SlugField(unique=True, blank=True, editable=False)
    description = models.TextField("Описание")
    image = models.ImageField("Фото", upload_to='products_images/')

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

    def __str__(self):
        return f"{self.name}"

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class CartItem(models.Model):
    cart_id = models.CharField(max_length=50)
    price = models.IntegerField()
    quantity = models.IntegerField()
    date_added = models.DateTimeField(auto_now_add=True)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)

    def __str__(self):
        return "{}:{}".format(self.product.name, self.id)

    def update_quantity(self, quantity):
        self.quantity = self.quantity + quantity
        self.save()

    def total_cost(self):
        return self.quantity * self.price



class Order(models.Model):
    name = models.CharField("Имя", max_length=191)
    email = models.EmailField("Почта")
    phone = models.CharField("Номер телефона", max_length=15)
    address = models.CharField("Город, адрес", max_length=191)
    date = models.DateTimeField("Дата и время заказа", auto_now_add=True)
    paid = models.BooleanField("Оплачен", default=False)
    delivered = models.BooleanField("Доставлен", default=False)

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

    def __str__(self):
        return "{}:{}".format(self.id, self.email)

    def total_cost(self):
        return sum([ li.cost() for li in self.lineitem_set.all() ] )


class LineItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name='Заказ')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Товар')
    price = models.IntegerField("Цена")
    quantity = models.IntegerField("Количество")
    date_added = models.DateTimeField("Изменение", auto_now_add=True)

    class Meta:
        verbose_name = "Оформленный заказ"
        verbose_name_plural = "Оформленные заказы"

    def __str__(self):
        return "{}:{}".format(self.product.name, self.id)

    def cost(self):
        return self.price * self.quantity