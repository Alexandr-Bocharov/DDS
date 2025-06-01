from django.db import models
from utils import NULLABLE


class Status(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name = "статус"
        verbose_name_plural = "статусы"

    def __str__(self):
        return self.name


class Type(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name = "тип"
        verbose_name_plural = "типы"

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=100)
    type = models.ForeignKey(
        Type,
        on_delete=models.CASCADE,
        related_name='categories'
    )

    class Meta:
        unique_together = ('name', 'type')
        verbose_name = "категория"
        verbose_name_plural = "категории"

    def __str__(self):
        return f"{self.name} ({self.type.name})"


class SubCategory(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name='subcategories'
    )

    class Meta:
        unique_together = ('name', 'category')
        verbose_name = "подкатегория"
        verbose_name_plural = "подкатегории"

    def __str__(self):
        return f"{self.name} ({self.category.name})"


class CashFlowRecord(models.Model):
    created_at = models.DateField(
        auto_now_add=True, verbose_name="Дата создания(автоматически)"
    )
    custom_date = models.DateField(
        verbose_name="Дата создания(вручную)", **NULLABLE
    )
    status = models.ForeignKey(Status, on_delete=models.PROTECT, **NULLABLE)
    type = models.ForeignKey(Type, on_delete=models.PROTECT)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    subcategory = models.ForeignKey(SubCategory, on_delete=models.PROTECT)
    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        verbose_name="Количество средств в рублях"
    )
    comment = models.TextField(verbose_name="Комментарий", **NULLABLE)

    class Meta:
        verbose_name = "запись ДДС"
        verbose_name_plural = "записи ДДС"

    def get_effective_date(self):
        return self.custom_date if self.custom_date else self.created_at

    def __str__(self):
        return (f"{self.get_effective_date()} "
                f"| {self.type.name} | {self.amount} руб.")
