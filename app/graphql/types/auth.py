import strawberry

@strawberry.type
class Token:
    access_token: str
    token_type: str
