import strawberry

from app.graphql.resolvers.item_queries import ItemQuery
from app.graphql.resolvers.item_mutations import ItemMutation
from app.graphql.resolvers.user_queries import UserQuery
from app.graphql.resolvers.user_mutations import UserMutation
from app.graphql.resolvers.auth_mutation import AuthMutation
from app.graphql.resolvers.health_query import HealthQuery


@strawberry.type
class Query(UserQuery, ItemQuery, HealthQuery):
    pass

@strawberry.type
class Mutation(UserMutation, ItemMutation, AuthMutation):
    pass

schema = strawberry.Schema(query=Query, mutation=Mutation)
