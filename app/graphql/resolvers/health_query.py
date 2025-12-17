import strawberry
from app.graphql.types.health import HealthStatus

@strawberry.type
class HealthQuery:

    @strawberry.field
    def health(self) -> HealthStatus:
        # Same logic as REST health_check
        all_systems_operational = True

        if all_systems_operational:
            return HealthStatus(status="healthy")
        return HealthStatus(status="unhealthy")
