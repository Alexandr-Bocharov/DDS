from django import forms
from .models import CashFlowRecord, Category, SubCategory, Type, Status


class CashFlowRecordForm(forms.ModelForm):
    class Meta:
        model = CashFlowRecord
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        data = kwargs.get("data")
        instance = kwargs.get("instance")

        super().__init__(*args, **kwargs)

        category_id = None
        if data:
            try:
                category_id = int(data.get("category"))
            except (TypeError, ValueError):
                pass
        elif instance:
            category_id = instance.category_id

        if category_id:
            self.fields["subcategory"].queryset = SubCategory.objects.filter(
                category_id=category_id
            )
        else:
            self.fields["subcategory"].queryset = SubCategory.objects.none()

    def clean(self):
        cleaned_data = super().clean()
        type = cleaned_data.get("type")
        category = cleaned_data.get("category")
        subcategory = cleaned_data.get("subcategory")

        # Проверка: категория должна принадлежать выбранному типу
        if category and type and category.type != type:
            self.add_error(
                "category",
                "Выбранная категория не относится к выбранному типу."
            )

        # Проверка: подкатегория должна принадлежать выбранной категории
        if subcategory and category and subcategory.category != category:
            self.add_error(
                "subcategory",
                "Выбранная подкатегория не относится к выбранной категории."
            )


class StatusForm(forms.ModelForm):
    class Meta:
        model = Status
        fields = '__all__'


class TypeForm(forms.ModelForm):
    class Meta:
        model = Type
        fields = '__all__'


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'


class SubCategoryForm(forms.ModelForm):
    class Meta:
        model = SubCategory
        fields = '__all__'


class CashFlowFilterForm(forms.Form):
    date_from = forms.DateField(
        label="С", required=False,
        widget=forms.DateInput(attrs={"type": "date", "class": "form-control"})
    )
    date_to = forms.DateField(
        label="По", required=False,
        widget=forms.DateInput(attrs={"type": "date", "class": "form-control"})
    )
    status = forms.ModelChoiceField(
        queryset=Status.objects.all(), required=False, label="Статус",
        widget=forms.Select(attrs={"class": "form-select"})
    )
    type = forms.ModelChoiceField(
        queryset=Type.objects.all(), required=False, label="Тип",
        widget=forms.Select(attrs={"class": "form-select"})
    )
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(), required=False, label="Категория",
        widget=forms.Select(attrs={"class": "form-select"})
    )
    subcategory = forms.ModelChoiceField(
        queryset=SubCategory.objects.all(), required=False, label="Подкатегория",
        widget=forms.Select(attrs={"class": "form-select"})
    )
