import strawberry

@strawberry.type
class Token:
    access_token: str
    token_type: str
    
@strawberry.input
class ForgotPasswordInput:
    email: str


@strawberry.input
class ResetPasswordInput:
    token: str
    new_password: str