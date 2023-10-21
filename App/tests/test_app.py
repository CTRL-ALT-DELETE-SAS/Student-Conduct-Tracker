import os, tempfile, pytest, logging, unittest
from werkzeug.security import check_password_hash, generate_password_hash

from App.main import create_app
from App.database import db, create_db
from App.models import User, Student, Staff, Admin
from App.controllers import (
    create_user,
    get_all_users_json,
    login
)


LOGGER = logging.getLogger(__name__)

'''
   Unit Tests
'''
class UserUnitTests(unittest.TestCase):

    def test_new_user(self):
        admin = Admin("bob", "boblast",  "bobpass")
        assert admin.firstname == "bob"

    # pure function no side effects or integrations called
    def test_get_json(self):
        user = Admin("bob", "boblast",  "bobpass")
        user_json = user.get_json()
        self.assertDictEqual(user_json, {"id":None, "firstname":"bob"})
    
    def test_hashed_password(self):
        password = "mypass"
        hashed = generate_password_hash(password, method='sha256')
        user = Admin("bob", "boblast",  password)
        assert user.password != password

    def test_check_password(self):
        password = "mypass"
        user = Admin("bob", "boblast",  password)
        assert user.check_password(password)

'''
    Integration Tests
'''

# This fixture creates an empty database for the test and deletes it after the test
# scope="class" would execute the fixture once and resued for all methods in the class
@pytest.fixture(autouse=True, scope="module")
def empty_db():
    app = create_app({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///test.db'})
    create_db()
    yield app.test_client()
    db.drop_all()


def test_authenticate():
    user = create_user("bob","boblast", "bobpass")
    assert login(user.ID, "bobpass") is not None

class UsersIntegrationTests(unittest.TestCase):

    def test_create_user(self):
        user = create_user("rick", "rolast", "bobpass")
        assert user.firstname == "rick"

    def test_get_all_users_json(self):
        users_json = get_all_users_json()
        self.assertListEqual([{"id":1, "username":"bob"}, {"id":2, "username":"rick"}], users_json)

    # Tests data changes in the database
    def test_update_user(self):
        update_user(1, "ronnie")
        user = get_user(1)
        assert user.username == "ronnie"
