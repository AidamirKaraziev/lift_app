from fastapi import APIRouter

from app.api.api_v1.endpoints import entrance, location, working_specialty, role, vova_test, universal_user,\
     client, contact_person, division, foreman, admin, company, type_contract, cost_type, contract, organization, \
     type_object, factory_model, object, type_act, act_base


api_router = APIRouter()

api_router.include_router(universal_user.router)
api_router.include_router(admin.router)
api_router.include_router(foreman.router)
api_router.include_router(client.router)
api_router.include_router(role.router)
api_router.include_router(division.router)
api_router.include_router(company.router)
api_router.include_router(location.router, tags=['Админ панель / Города'])
api_router.include_router(contact_person.router)
api_router.include_router(type_contract.router)
api_router.include_router(type_act.router)
api_router.include_router(cost_type.router)
api_router.include_router(type_object.router)
api_router.include_router(factory_model.router)
# api_router.include_router(role.router, tags=["Админ панель / Должности"])
# api_router.include_router(working_specialty.router, tags=["Админ панель / Специальности"])
api_router.include_router(vova_test.router)
api_router.include_router(working_specialty.router)
api_router.include_router(contract.router)
api_router.include_router(organization.router)
api_router.include_router(object.router)
api_router.include_router(act_base.router)
