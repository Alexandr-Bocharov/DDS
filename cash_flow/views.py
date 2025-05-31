from django.db.models.functions import Coalesce
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, UpdateView, DeleteView, CreateView
from rest_framework import viewsets
from django.contrib import messages
from django.db.models import ProtectedError
from django.http import JsonResponse

from .models import CashFlowRecord, Status, Type, Category, SubCategory
from cash_flow.forms import (
    CashFlowRecordForm,
    TypeForm,
    StatusForm,
    CategoryForm,
    SubCategoryForm, CashFlowFilterForm
)
from cash_flow.serializers import (
    StatusSerializer,
    TypeSerializer,
    CategorySerializer,
    SubCategorySerializer,
    CashFlowRecordSerializer
)


class StatusViewSet(viewsets.ModelViewSet):
    """ CRUD для статусов """
    queryset = Status.objects.all()
    serializer_class = StatusSerializer


class TypeViewSet(viewsets.ModelViewSet):
    """ CRUD для типов """
    queryset = Type.objects.all()
    serializer_class = TypeSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    """ CRUD для категорий """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class SubcategoryViewSet(viewsets.ModelViewSet):
    """ CRUD для подкатегорий """
    queryset = SubCategory.objects.all()
    serializer_class = SubCategorySerializer


class CashFlowRecordViewSet(viewsets.ModelViewSet):
    """ CRUD для записей ДДС """
    queryset = CashFlowRecord.objects.all()
    serializer_class = CashFlowRecordSerializer


class CashFlowRecordListView(ListView):
    """
    Список записей ДДС отсортированный по дате добавления в обратном порядке.
    Записи выводятся в зависимости от примененных фильтров.
    """
    model = CashFlowRecord
    template_name = 'cash_flow/cashflow_list.html'
    ordering = ['-created_at']
    context_object_name = "records"

    def get_queryset(self):
        queryset = super().get_queryset()
        form = CashFlowFilterForm(self.request.GET)

        queryset = queryset.annotate(
            effective_date=Coalesce('custom_date', 'created_at')
        )

        if form.is_valid():
            cd = form.cleaned_data
            if cd["date_from"]:
                queryset = queryset.filter(effective_date__gte=cd["date_from"])
            if cd["date_to"]:
                queryset = queryset.filter(effective_date__lte=cd["date_to"])
            if cd["status"]:
                queryset = queryset.filter(status=cd["status"])
            if cd["type"]:
                queryset = queryset.filter(type=cd["type"])
            if cd["category"]:
                queryset = queryset.filter(category=cd["category"])
            if cd["subcategory"]:
                queryset = queryset.filter(subcategory=cd["subcategory"])

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["filter_form"] = CashFlowFilterForm(self.request.GET)
        return context


class CashFlowRecordUpdateView(UpdateView):
    """
    Обновление записи ДДС.
    """
    model = CashFlowRecord
    template_name = "cash_flow/cashflow_form.html"
    form_class = CashFlowRecordForm
    success_url = reverse_lazy("cashflow:cashflow_list")


class CashFlowRecordDeleteView(DeleteView):
    """
    Удаление записи ДДС.
    """
    model = CashFlowRecord
    template_name = "cash_flow/cashflow_confirm_delete.html"
    success_url = reverse_lazy("cashflow:cashflow_list")


class CashFlowRecordCreateView(CreateView):
    """
    Создание записи ДДС.
    """
    model = CashFlowRecord
    template_name = "cash_flow/cashflow_form.html"
    form_class = CashFlowRecordForm
    success_url = reverse_lazy("cashflow:cashflow_list")


class DirectoryView(View):
    """
    Вьюха для сбора типов, статусов, категорий и подкатегорий.
    """
    def get(self, request):
        context = {
            'statuses': Status.objects.all(),
            'types': Type.objects.all(),
            'categories': Category.objects.all(),
            'subcategories': SubCategory.objects.all(),
        }
        return render(request, 'cash_flow/directories.html', context)


class StatusCreateView(CreateView):
    """
    Создание статуса.
    """
    model = Status
    form_class = StatusForm
    template_name = "cash_flow/status_form.html"
    success_url = reverse_lazy("cashflow:directories")


class StatusUpdateView(UpdateView):
    """
    Обновление статуса.
    """
    model = Status
    form_class = StatusForm
    template_name = "cash_flow/status_form.html"
    success_url = reverse_lazy("cashflow:directories")


class StatusDeleteView(DeleteView):
    """
    Удаление статуса.
    """
    model = Status
    template_name = "cash_flow/status_confirm_delete.html"
    success_url = reverse_lazy("cashflow:directories")


class TypeCreateView(CreateView):
    """
    Создание типа.
    """
    model = Type
    form_class = TypeForm
    template_name = "cash_flow/type_form.html"
    success_url = reverse_lazy("cashflow:directories")


class TypeUpdateView(UpdateView):
    """
    Обновление типа.
    """
    model = Type
    form_class = TypeForm
    template_name = "cash_flow/type_form.html"
    success_url = reverse_lazy("cashflow:directories")


class TypeDeleteView(DeleteView):
    """
    Удаление типа.
    Если существует запись с типом, который пытаемся удалить -
    выведется сообщение из метода post.
    """
    model = Type
    template_name = "cash_flow/type_confirm_delete.html"
    success_url = reverse_lazy("cashflow:directories")

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        try:
            return super().post(request, *args, **kwargs)
        except ProtectedError:
            messages.error(
                request,
                "Нельзя удалить тип, так как он используется в записях."
            )
            return redirect(self.success_url)


class CategoryCreateView(CreateView):
    """
    Создание категории.
    """
    model = Category
    template_name = "cash_flow/category_form.html"
    form_class = CategoryForm
    success_url = reverse_lazy("cashflow:directories")


class CategoryUpdateView(UpdateView):
    """
    Редактирование категории.
    """
    model = Category
    form_class = CategoryForm
    template_name = "cash_flow/category_form.html"
    success_url = reverse_lazy("cashflow:directories")


class CategoryDeleteView(DeleteView):
    """
    Удаление категории.
    Если существует запись с категорией, которую пытаемся удалить -
    выведется сообщение из метода post.
    """
    model = Category
    template_name = "cash_flow/category_confirm_delete.html"
    success_url = reverse_lazy("cashflow:directories")

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        try:
            return super().post(request, *args, **kwargs)
        except ProtectedError:
            messages.error(
                request,
                "Нельзя удалить категорию, так как она используется в записях."
            )
            return redirect(self.success_url)


class SubCategoryCreateView(CreateView):
    """
    Создание подкатегории.
    """
    model = SubCategory
    template_name = "cash_flow/subcategory_form.html"
    form_class = SubCategoryForm
    success_url = reverse_lazy("cashflow:directories")


class SubCategoryUpdateView(UpdateView):
    """
    Редактирование подкатегории.
    """
    model = SubCategory
    form_class = SubCategoryForm
    template_name = "cash_flow/subcategory_form.html"
    success_url = reverse_lazy("cashflow:directories")


class SubCategoryDeleteView(DeleteView):
    """
    Удаление подкатегории.
    Если существует запись с подкатегорией, которую пытаемся удалить -
    выведется сообщение из метода post.
    """
    model = SubCategory
    template_name = "cash_flow/subcategory_confirm_delete.html"
    success_url = reverse_lazy("cashflow:directories")

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        try:
            return super().post(request, *args, **kwargs)
        except ProtectedError:
            messages.error(
                request,
                "Нельзя удалить подкатегорию, так как она используется в записях."
            )
            return redirect(self.success_url)


def load_subcategories(request):
    """
    Возвращает список подкатегорий, относящихся к заданной категории.

    Получает параметр `category_id` из GET-запроса и фильтрует подкатегории по этому идентификатору.
    Результат возвращается в формате JSON, содержащем список подкатегорий с их идентификаторами и названиями.

    Args:
        request (HttpRequest): HTTP-запрос, содержащий параметр `category_id`.

    Returns:
        JsonResponse: JSON-ответ с подкатегориями, например:
                      {"subcategories": [{"id": 1, "name": "Подкатегория 1"}, ...]}
    """
    category_id = request.GET.get("category_id")
    subcategories = SubCategory.objects.filter(category_id=category_id).values("id", "name")
    return JsonResponse({"subcategories": list(subcategories)})


def load_categories(request):
    """
    Возвращает список категорий, относящихся к заданному типу.

    Получает параметр `type_id` из GET-запроса и фильтрует категории по этому идентификатору.
    Результат возвращается в формате JSON, содержащем список категорий с их идентификаторами и названиями.

    Args:
        request (HttpRequest): HTTP-запрос, содержащий параметр `type_id`.

    Returns:
        JsonResponse: JSON-ответ с категориями, например:
                {"categories": [{"id": 1, "name": "Категория 1"}, ...]}
    """
    type_id = request.GET.get("type_id")
    categories = Category.objects.filter(type_id=type_id).values("id", "name")
    return JsonResponse({"categories": list(categories)})
