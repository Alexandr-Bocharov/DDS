from rest_framework.routers import DefaultRouter

from .apps import CashFlowConfig
from .views import (
    StatusViewSet,
    TypeViewSet,
    CategoryViewSet,
    SubcategoryViewSet,
    CashFlowRecordViewSet
)

app_name = CashFlowConfig.name

router = DefaultRouter()
router.register(r'statuses', StatusViewSet)
router.register(r'types', TypeViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'subcategories', SubcategoryViewSet)
router.register(r'records', CashFlowRecordViewSet)

urlpatterns = router.urls
