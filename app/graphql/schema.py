import strawberry

from app.graphql.resolvers.item_queries import ItemQuery
from app.graphql.resolvers.item_mutations import ItemMutation
from app.graphql.resolvers.user_queries import UserQuery
from app.graphql.resolvers.user_mutations import UserMutation
from app.graphql.resolvers.auth_mutation import AuthMutation

@strawberry.type
class Query(UserQuery, ItemQuery):
    pass

@strawberry.type
class Mutation(UserMutation, ItemMutation, AuthMutation):
    pass

schema = strawberry.Schema(query=Query, mutation=Mutation)
