import unittest
from datetime import datetime, timedelta
from app import create_app, db
from app.models import User, Post
from config import Config


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite://"


class UserModelCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_password_hashing(self):
        u = User(username="johny")
        u.set_password("milkshake")
        self.assertFalse(u.check_password("juice"))
        self.assertTrue(u.check_password("milkshake"))

    def test_avatar(self):
        u = User(username="broman", email="broman@test.com")
        self.assertEqual(
            u.avatar(128),
            (
                "https://www.gravatar.com/avatar/"
                "baf92213d067fd5ec98a7fcd13f45682"
                "?d=identicon&s=128"
            ),
        )

    def test_follow(self):
        u1 = User(username="george", email="george@test.com")
        u2 = User(username="deli", email="deli@test.com")
        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()
        self.assertEqual(u1.followed.all(), [])
        self.assertEqual(u1.followers.all(), [])

        u1.follow(u2)
        db.session.commit()
        self.assertTrue(u1.is_following(u2))
        self.assertEqual(u1.followed.count(), 1)
        self.assertEqual(u1.followed.first().username, "deli")
        self.assertEqual(u2.followers.count(), 1)
        self.assertEqual(u2.followers.first().username, "george")

        u1.unfollow(u2)
        db.session.commit()
        self.assertFalse(u1.is_following(u2))
        self.assertEqual(u1.followed.count(), 0)
        self.assertEqual(u2.followers.count(), 0)

    def test_follow_posts(self):
        u1 = User(username="george", email="george@test.com")
        u2 = User(username="deli", email="deli@test.com")
        u3 = User(username="freya", email="freya@test.com")
        u4 = User(username="io", email="io@test.com")
        db.session.add_all([u1, u2, u3, u4])

        now = datetime.utcnow()
        p1 = Post(
            body="George posted this",
            author=u1,
            timestamp=now + timedelta(seconds=5),
        )
        p2 = Post(
            body="Deli posted this",
            author=u2,
            timestamp=now + timedelta(seconds=10),
        )
        p3 = Post(
            body="Freya posted this",
            author=u3,
            timestamp=now + timedelta(seconds=15),
        )
        p4 = Post(
            body="Io posted this",
            author=u4,
            timestamp=now + timedelta(seconds=20),
        )

        db.session.add_all([p1, p2, p3, p4])
        db.session.commit()

        u1.follow(u2)
        u2.follow(u3)
        u2.follow(u4)
        u3.follow(u4)
        db.session.commit()

        f1 = u1.followed_posts().all()
        f2 = u2.followed_posts().all()
        f3 = u3.followed_posts().all()
        f4 = u4.followed_posts().all()
        self.assertEqual(f1, [p2, p1])
        self.assertEqual(f2, [p4, p3, p2])
        self.assertEqual(f3, [p4, p3])
        self.assertEqual(f4, [p4])


if __name__ == "__main__":
    unittest.main(verbosity=2)
