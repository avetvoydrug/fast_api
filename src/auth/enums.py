from enum import Enum


class SexEnum(Enum):
    male = 'male'
    female = 'female'
    other = 'other'

class RelationshipStatusEnum(Enum):
    single = "Одинок"
    in_a_relationship = "В отношениях"
    married = "Женат"
    engaged = "Обручен, помолвлен"
    it_s_complicated = "Всё сложно"
    separated = "Брошен"
    divorced = "В разводе"
    widowed = "Овдовел"
    open_to_dating = "В активном поиске"
    friend_zone = "Во фрэндзоне"
    looking_for_friends = "Только дружба"
    other = "Не отсюда" 