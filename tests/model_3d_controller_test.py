import uuid
import unittest

from src import DBConnectionHandler, DBConnect
from src.internal.model_3d.controllers import Model3dController
from src.internal.model_3d.schemas import Model3D as Model3DEntity

from src.internal.users.schemas import Users as UserEntity
from src.internal.users.controllers import UserController



class TestModel3dData(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestModel3dData, self).__init__(*args, **kwargs)
        engine = DBConnectionHandler().get_engine()
        DBConnect.init_db(engine)

    def test_create_user(self):
        user = UserEntity()
        user.name = "domtry"
        user.pseudo = "domtry"
        user.email = "noreply@gmail.com"
        user.id = str(uuid.uuid4())
        user_saved = UserController.create_user(user)

        model_3d = Model3DEntity()
        model_3d.label = "Casque OVR"
        model_3d.description = "Simple test"
        model_3d.image_path = "https://statusneo.com/wp-content/uploads/2023/02/MicrosoftTeams-image551ad57e01403f080a9df51975ac40b6efba82553c323a742b42b1c71c1e45f1.jpg"
        model_3d.user = user_saved
        model_3d.id = str(uuid.uuid4())

        want = Model3dController.create_model_3d(model_3d)

        self.assertEquals(model_3d.id, want.id)
        self.assertEquals(model_3d.user.id, user_saved.id)