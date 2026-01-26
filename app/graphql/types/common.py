# app/graphql/types/common.py
import strawberry

@strawberry.type
class MessageResponse:
    message: str
