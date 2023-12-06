import graphene

from django_app_organization.graphql.website.organization import OrganizationQuery


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
