from .base_repository import SQLAlchemyRepository
from models.operation import Operation
from auth.models import User, UserDataExtended


class OperationRepository(SQLAlchemyRepository):
    model = Operation

class UserRepository(SQLAlchemyRepository):
    model = User

class UserDataExtendedRepository(SQLAlchemyRepository):
    model = UserDataExtended
