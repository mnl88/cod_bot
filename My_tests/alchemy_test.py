import unittest
from alchemy import Person, TG_Account
from alchemy import DB


class TestDb(unittest.TestCase):
    def setUp(self):
        DB.init_app('sqlite://')
        DB.create_all()
        DB.session.add(User(name='Cristian'))
        DB.commit()

    def test_it(self):
        user = User.query.filter_by(name='Cristian')
        assert user is not None

    def tearDown(self):
        # TODO: clean up your test