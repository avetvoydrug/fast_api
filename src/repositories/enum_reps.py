from enum import Enum
from .repositories import (OperationRepository, UserRepository,
                           UserDataExtendedRepository, FriendRequestRepository,
                           FriendShipRepository)

class RepositoryEnum(Enum):
    operation = OperationRepository
    user = UserRepository
    user_data_extended = UserDataExtendedRepository
    friend_request = FriendRequestRepository
    friend_ship = FriendShipRepository