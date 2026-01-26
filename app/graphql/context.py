from typing import Optional
from sqlalchemy.orm import Session
# from strawberry.fastapi import BaseContext

class GraphQLContext:
    def __init__(self, db: Session, current_user):
        self.db = db
        self.current_user = current_user
