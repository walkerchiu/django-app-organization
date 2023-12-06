import graphene

from django_app_organization.graphql.dashboard.organization import OrganizationQuery


class Mutation(
    graphene.ObjectType,
):
    pass


class Query(
    OrganizationQuery,
    graphene.ObjectType,
):
    pass


schema = graphene.Schema(mutation=Mutation, query=Query)
