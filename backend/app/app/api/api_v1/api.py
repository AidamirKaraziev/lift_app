from fastapi import APIRouter

from app.api.api_v1.endpoints import entrance, location, working_specialty, role, vova_test, universal_user, admin,\
    company, client, contact_person, division, foreman, test_api, execution_status


api_router = APIRouter()

api_router.include_router(execution_status.router)

api_router.include_router(universal_user.router)
api_router.include_router(role.router)
api_router.include_router(admin.router)
api_router.include_router(company.router)
api_router.include_router(client.router)
api_router.include_router(contact_person.router)
api_router.include_router(division.router)
api_router.include_router(foreman.router)
api_router.include_router(location.router)
api_router.include_router(working_specialty.router)
api_router.include_router(test_api.router)
api_router.include_router(vova_test.router)

