import strawberry
from app.graphql.resolvers.user_queries import UserQuery
from app.graphql.resolvers.user_mutations import UserMutation
from app.graphql.resolvers.auth_mutation import AuthMutation

@strawberry.type
class Mutation(UserMutation, AuthMutation):
    pass

schema = strawberry.Schema(
    query=UserQuery,
    mutation=Mutation,
)
