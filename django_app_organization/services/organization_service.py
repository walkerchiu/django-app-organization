from typing import Tuple
import uuid

from django.contrib.auth import get_user_model
from django.db import transaction

from django_tenants.utils import schema_context
from safedelete.models import HARD_DELETE

from organization.models import Organization, OrganizationTrans

DJANGO_APP_ACCOUNT_INSTALLED = (
    importlib.util.find_spec("django_app_account") is not None
)
if DJANGO_APP_ACCOUNT_INSTALLED:
    from django_app_account.services.user_service import UserService

DJANGO_APP_ROLE_INSTALLED = importlib.util.find_spec("django_app_role") is not None
if DJANGO_APP_ROLE_INSTALLED:
    from django_app_role.services.role_service import RoleService


class OrganizationService:
    @transaction.atomic
    def initiate_schema(
        self, schema_name: str, organization_name: str, email: str, password: str
    ) -> Tuple[bool, Organization, get_user_model()]:
        with schema_context(schema_name):
            organization = Organization(
                schema_name=schema_name,
            )
            organization.save()
            OrganizationTrans.objects.create(
                organization=organization,
                language_code=organization.language_code,
                name=organization_name,
            )

            if DJANGO_APP_ACCOUNT_INSTALLED and DJANGO_APP_ROLE_INSTALLED:
                result = self.init_default_data(organization)

                if result:
                    user_service = UserService()
                    result, user = user_service.create_user(
                        endpoint="dashboard",
                        email=email,
                        password=password,
                        username="demo",
                    )
                    if result:
                        role_service = RoleService()
                        user = role_service.assign_owner(
                            organization=organization,
                            user=user,
                        )
            else:
                result, user = True, None

            if result:
                return result, organization, user
            else:
                organization.delete(force_policy=HARD_DELETE)
                return result, None, None

    @transaction.atomic
    def init_default_data(self, organization: Organization) -> bool:
        role_service = RoleService()
        result = role_service.init_default_data(organization)

    @transaction.atomic
    def delete_organization(self, schema_name: str, organization_id: uuid) -> bool:
        with schema_context(schema_name):
            try:
                organization = Organization.objects.only("id").get(pk=organization_id)
            except Organization.DoesNotExist:
                return False

            organization.delete()

        return True

    @transaction.atomic
    def undelete_organization(self, schema_name: str, organization_id: uuid) -> bool:
        with schema_context(schema_name):
            try:
                organization = Organization.deleted_objects.only("id").get(
                    pk=organization_id
                )
            except Organization.DoesNotExist:
                return False

            organization.undelete()

        return True
