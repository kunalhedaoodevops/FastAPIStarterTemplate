import strawberry

@strawberry.input
class LoginInput:
    username: str
    password: str
