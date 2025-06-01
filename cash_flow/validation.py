import datetime


def validate_category_type_match(category, record_type):
    """
    Валидация на соответствие категории выбранному типу
    """
    if category and record_type and category.type != record_type:
        raise ValueError("Категория не относится к типу")


def validate_subcategory_category_match(subcategory, category):
    """
    Валидация на соответствие подкатегории выбранной категории
    """
    if subcategory and category and subcategory.category != category:
        raise ValueError("Подкатегория не относится к категории")


def validate_custom_date(custom_date):
    """
    Проверка, что дата создания записи - не дата будущего
    """
    date_now = datetime.datetime.now().date()
    if custom_date:
        if custom_date > date_now:
            raise ValueError("Дата создания не может быть в будущем")


def validate_cash_flow_record_amount(amount):
    """
    Валидация суммы из записи.
    Количество денежных средств(amount) не должно быть меньше нуля
    """
    if amount < 0:
        raise ValueError("Количество средств не может быть меньше нуля")