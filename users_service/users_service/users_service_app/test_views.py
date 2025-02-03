from django.test import TestCase, Client
from users_service_app.models import User, Friend

class UserViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()

        self.user1 = User.objects.create(user_id=1, username="Alice", email="alice@example.com", token="token1", fullname="Alice Wonderland")
        self.user2 = User.objects.create(user_id=2, username="Bob", email="bob@example.com", token="token2", fullname="Bob Builder")
        self.user3 = User.objects.create(user_id=3, username="Charlie", email="charlie@example.com", token="token3", fullname="Charlie Brown")

        self.friendship = Friend.objects.create(user=self.user1, friend=self.user2)

    def test_authenticate_user(self):
        url = f"https://testserver/api/user/authenticate/{self.user1.token}/"
        response = self.client.get(url, secure=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["user_id"], self.user1.user_id)

    def test_list_friends(self):
        url = f"https://testserver/api/user/friends/{self.user1.user_id}/"
        response = self.client.get(url, secure=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()["friends"]), 1)
        self.assertEqual(response.json()["friends"][0]["user_id"], self.user2.user_id)

    def test_add_friend(self):
        url = f"https://testserver/api/user/friends/{self.user1.user_id}/add/{self.user3.user_id}/"
        response = self.client.post(url, secure=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Friend.objects.filter(user=self.user1, friend=self.user3).exists())

    def test_remove_friend(self):
        url = f"https://testserver/api/user/friends/{self.user1.user_id}/remove/{self.user2.user_id}/"
        response = self.client.delete(url, secure=True)

        self.assertEqual(response.status_code, 200)
        self.assertFalse(Friend.objects.filter(user=self.user1, friend=self.user2).exists())

    def test_is_following(self):
        url = f"https://testserver/api/user/friends/follows/{self.user1.user_id}/{self.user2.user_id}/"
        print(f"Generated URL: {url}")

        response = self.client.get(url, secure=True)
        print(f"Generated response: {response}") 
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()["is_following"])

        url = f"https://testserver/api/user/friends/follows/{self.user1.user_id}/{self.user3.user_id}/"
        response = self.client.get(url, secure=True)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.json()["is_following"])
