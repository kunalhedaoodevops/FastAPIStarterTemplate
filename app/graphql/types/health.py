import strawberry

@strawberry.type
class HealthStatus:
    status: str
