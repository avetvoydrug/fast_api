from typing import List
from auth.models import User, FriendShip, FriendRequest, UserDataExtended


class UserWebManager:

    @staticmethod
    async def find_friend_status(request_user_id, user: User):
        """
        friend_flag: if True => users have friendship else False
        follow_flag: if True => user has sent a friend request to request_user
        follower_flag: if True => request_user has sent a friend request to user
        any_flag: if True => previously, users did not perform any actions among themselves
        """
        follows: List[FriendRequest] = user.friend_requests_sent
        follows_ids = [obj.receiver_id for obj in follows]
        followers: List[FriendRequest] = user.friend_requests_received
        followers_id = [obj.sender_id for obj in followers]
        friends1: List[FriendShip] = user.friendships
        friends2: List[FriendShip] = user.friendships2
        friends_ids = [obj.user2_id for obj in friends1]
        for obj in friends2:
            friends_ids.append(obj.user1_id)
        
        friend_flag = True if request_user_id in friends_ids else False
        follow_flag = True if request_user_id in follows_ids else False
        follower_flag = True if request_user_id in followers_id else False
        no_action_flag = True if not(friend_flag) and not(follow_flag) and not(follower_flag) else False
        flags = {"friend_flag": friend_flag, 
                 "follow_flag": follow_flag, 
                 "follower_flag": follower_flag, 
                 "no_action_flag": no_action_flag}
        return flags

    @staticmethod
    async def get_user_data_to_edit(user: User):
        data = {}
        user_data = user.user_data
        data.update({
            "first_name": user_data.first_name,
            "last_name": user_data.last_name,
            "birth_date": user_data.birth_date,
            "sex": user_data.sex,
            "loc": user_data.location,
            "edu": user_data.education,
            "interes": user_data.interests
        })
        return data