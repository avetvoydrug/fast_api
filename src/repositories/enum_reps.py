from enum import Enum
from .repositories import (OperationRepository, UserRepository,
                           UserDataExtendedRepository)

class RepositoryEnum(Enum):
    operation = OperationRepository
    user = UserRepository
    user_data_extended = UserDataExtendedRepository