from fastapi import Request
from strawberry.fastapi import GraphQLRouter

from app.graphql.schema import schema
from app.databases.db import get_db
from app.utils.deps import get_current_user_graphql

async def get_context(request: Request):
    db = next(get_db())
    current_user = await get_current_user_graphql(request, db)

    return {
        "db": db,
        "current_user": current_user,
        "request": request,
    }

graphql_app = GraphQLRouter(
    schema,
    context_getter=get_context,
)
