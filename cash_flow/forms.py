from django import forms
from .models import CashFlowRecord, Category, SubCategory, Type, Status
from cash_flow.validation import (
    validate_category_type_match,
    validate_subcategory_category_match,
    validate_custom_date,
    validate_cash_flow_record_amount
)


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
        record_type = cleaned_data.get("type")
        category = cleaned_data.get("category")
        subcategory = cleaned_data.get("subcategory")
        custom_date = cleaned_data.get("custom_date")
        amount = cleaned_data.get("amount")

        try:
            validate_category_type_match(category, record_type)
        except ValueError as e:
            self.add_error("category", str(e))

        try:
            validate_subcategory_category_match(subcategory, category)
        except ValueError as e:
            self.add_error("subcategory", str(e))

        try:
            validate_custom_date(custom_date)
        except ValueError as e:
            self.add_error("custom_date", str(e))

        try:
            validate_cash_flow_record_amount(amount)
        except ValueError as e:
            self.add_error("amount", str(e))


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
        queryset=SubCategory.objects.all(),
        required=False,
        label="Подкатегория",
        widget=forms.Select(attrs={"class": "form-select"})
    )
