from fastapi import Depends
from fastapi_users import FastAPIUsers
from fastapi_users.authentication import CookieTransport, AuthenticationBackend
from fastapi_users.authentication import JWTStrategy

from .manager import get_user_manager
from .models import User 
from config import SECRET_AUTH

# транспорт: то как токен будет передаваться по запросам
# Bearer предлагают для мобилок, 
# Легко читается и устанавливается в каждом запросе.
# Необходимо сохранить вручную где-нибудь в клиенте.
# Cookie для вэба 
# Автоматически сохраняется и безопасно отправляется веб-браузерами при каждом запросе.
# Автоматически удаляется веб-браузерами по истечении срока действия.
# Для максимальной безопасности требуется защита CSRF.
# Сложнее работать вне браузера, например, с мобильным приложением или сервером.
cookie_transport = CookieTransport(cookie_name='bonds', cookie_max_age=3600)

# стратегия: то как генерируется и защищается токен
# JWT(quick), Database and Redis(Custom, secure and performant)
def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET_AUTH, lifetime_seconds=3600)

# при проверке аут вызываются методы один за другим,
# первый метод вернувший пользователя выигрывает,
# если ни один не вернул пользователя вызывается ошибка
auth_backend = AuthenticationBackend(
    name='jwt',
    transport=cookie_transport,
    get_strategy=get_jwt_strategy,
)

# возвращает юзера и проверяет аут
fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

# можно прикалываться с зависимостями
current_user = fastapi_users.current_user()

async def check_auth(user: User = Depends(fastapi_users.current_user())):
    print("something here")
    return user