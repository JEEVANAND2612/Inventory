from fastapi import APIRouter
from api.v1.auth.auth_routes import router as auth_router
from api.v1.categories.category_routes import router as category_router
from api.v1.stock.stock_routes import router as stock_router
from api.v1.suppliers.supplier_routes import router as supplier_router
from api.v1.reports.report_routes import router as report_router
from api.v1.users.user_routes import router as user_router
from api.v1.organization.organization_routes import router as organization_router
from api.v1.warehouses.warehouse_routes import router as warehouse_router

api_router = APIRouter(prefix="/api/v1")

# ✅ include routers
api_router.include_router(auth_router)
api_router.include_router(category_router)
api_router.include_router(stock_router)
api_router.include_router(supplier_router)
api_router.include_router(report_router)
api_router.include_router(user_router)
api_router.include_router(organization_router)
api_router.include_router(warehouse_router)
