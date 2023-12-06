import graphene

from django_app_organization.graphql.website.types.organization import OrganizationNode


class OrganizationMutation(graphene.ObjectType):
    pass


class OrganizationQuery(graphene.ObjectType):
    organization = graphene.relay.Node.Field(OrganizationNode)
