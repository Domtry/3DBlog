import uuid
import unittest

from src import DBConnectionHandler, DBConnect
from src.internal.users.controllers import UserController
from src.internal.users.schemas import Users as UserEntity


class TestUserData(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestUserData, self).__init__(*args, **kwargs)
        engine = DBConnectionHandler().get_engine()
        DBConnect.init_db(engine)

    def test_create_user(self):
        user = UserEntity()
        user.name = "domtry"
        user.pseudo = "domtry"
        user.email = "noreply@gmail.com"
        user.id = str(uuid.uuid4())

        want = UserController.create_user(user)

        self.assertEquals(user.id, want.id)
        self.assertEquals(user.pseudo, want.pseudo)

    def test_update_user(self):
        user = UserEntity()
        user.name = "domtry"
        user.pseudo = "domtry"
        user.email = "noreply@gmail.com"
        user.id = str(uuid.uuid4())

        got = UserController.create_user(user)
        user.pseudo = "socrate"

        want = UserController.update(user.id, user)

        self.assertEquals(got.id, want.id)
        self.assertEquals(got.email, want.email)
        self.assertNotEquals(got.pseudo, want.pseudo)

    def test_get_user_by_id(self):
        user = UserEntity()
        user.name = "domtry"
        user.pseudo = "domtry"
        user.email = "noreply@gmail.com"
        user.id = str(uuid.uuid4())

        got = UserController.create_user(user)
        user.pseudo = "socrate"

        want = UserController.get_user(user.id)

        self.assertEquals(got.id, want.id)
        self.assertEquals(got.email, want.email)
        self.assertEquals(got.pseudo, want.pseudo)
