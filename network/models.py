# network/models.py
from django.db import models
from django.core.exceptions import ValidationError


class NetworkNode(models.Model):
    """Модель узла сети электроники с иерархической структурой.

    Attributes:
        name (str): Название узла.
        email (str): Электронная почта узла.
        country (str): Страна расположения узла.
        city (str): Город расположения узла.
        street (str): Улица расположения узла.
        house_number (str): Номер дома.
        supplier (NetworkNode): Поставщик в иерархии.
        debt (Decimal): Задолженность перед поставщиком.
        node_type (str): Тип узла (factory/retail/entrepreneur).
        created_at (datetime): Дата создания узла.
        level (int): Уровень в иерархии.
    """

    NODE_TYPES = [
        ("factory", "Factory"),
        ("retail", "Retail Network"),
        ("entrepreneur", "Individual Entrepreneur"),
    ]

    name = models.CharField(max_length=255)
    email = models.EmailField()
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    street = models.CharField(max_length=255)
    house_number = models.CharField(max_length=20)
    supplier = models.ForeignKey(
        "self", on_delete=models.SET_NULL, null=True,
        blank=True, related_name="clients"
    )
    debt = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    node_type = models.CharField(max_length=20, choices=NODE_TYPES)
    level = models.IntegerField(default=0, editable=False)

    class Meta:
        verbose_name = "Network Node"
        verbose_name_plural = "Network Nodes"
        indexes = [
            models.Index(fields=["city"]),
            models.Index(fields=["country"]),
        ]
        ordering = ["-created_at"]

    def clean(self):
        """Валидация модели."""
        if self.pk and self.supplier:
            # Проверка на циклическую ссылку
            current = self.supplier
            while current:
                if current.pk == self.pk:
                    raise ValidationError("Circular reference detected.")
                current = current.supplier

        # Завод не может иметь поставщика
        if self.node_type == "factory" and self.supplier:
            raise ValidationError("A factory cannot have a supplier.")

    def save(self, *args, **kwargs):
        """Сохранение с автоматическим расчетом уровня иерархии."""
        self.clean()
        self.level = self.get_hierarchy_level()
        super().save(*args, **kwargs)

        # Обновление уровня для всех клиентов
        for client in self.clients.all():
            client.save()

    def get_hierarchy_level(self):
        """Рекурсивно вычисляет уровень в иерархии."""
        if not self.supplier:
            return 0
        return self.supplier.get_hierarchy_level() + 1

    def __str__(self):
        return self.name


class Product(models.Model):
    """Модель продукта, связанного с узлами сети.

    Attributes:
        name (str): Название продукта.
        model (str): Модель продукта.
        release_date (date): Дата выпуска продукта.
        price (Decimal): Цена продукта.
        quantity (int): Количество на складе.
        nodes (ManyToManyField): Узлы сети, где доступен продукт.
    """

    name = models.CharField(max_length=255)
    model = models.CharField(max_length=100)
    release_date = models.DateField()
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    quantity = models.PositiveIntegerField(default=0)
    nodes = models.ManyToManyField(NetworkNode, related_name="products")

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"
        indexes = [
            models.Index(fields=["name"]),
            models.Index(fields=["model"]),
        ]

    def __str__(self):
        return f"{self.name} - {self.model}"
