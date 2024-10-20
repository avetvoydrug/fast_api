from repositories.enum_reps import RepositoryEnum
from services.operation import OperationService
from services.user import (UserService, UserDataExtendedService,
                           FriendRequestService, FriendShipService)


def operation_service():
    return OperationService(RepositoryEnum.operation.value)

def user_service():
    return UserService(RepositoryEnum.user.value)

def user_data_service():
    return UserDataExtendedService(
        RepositoryEnum.user_data_extended.value)

def friends_requests_service():
    return FriendRequestService(
        RepositoryEnum.friend_request.value
    )

def friend_ship_service():
    return FriendShipService(
        RepositoryEnum.friend_ship.value
    )