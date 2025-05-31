from rest_framework import serializers
from cash_flow.models import Status, Type, Category, SubCategory, CashFlowRecord


class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = '__all__'


class TypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Type
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = '__all__'


class CashFlowRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = CashFlowRecord
        fields = '__all__'
