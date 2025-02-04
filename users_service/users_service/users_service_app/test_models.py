# from django.test import TestCase
# from users_service_app.models import User, UserSettings, UserConfidentialitySettings, Friend
# from django.core.exceptions import ValidationError
# from django.db import IntegrityError

# class UserModelTestCase(TestCase):
#     def setUp(self):
#         """Create a test user"""
#         self.user = User.objects.create(
#             username="testuser",
#             email="testuser@example.com",
#             token="randomtoken123",
#             fullname="Test User"
#         )

#     def test_user_creation(self):
#         """Test that a user is created successfully"""
#         user = User.objects.get(username="testuser")
#         self.assertEqual(user.email, "testuser@example.com")
#         self.assertEqual(user.token, "randomtoken123")
#         self.assertEqual(str(user), "testuser")

#     def test_duplicate_email_fails(self):
#         """Ensure that duplicate emails raise an error"""
#         with self.assertRaises(IntegrityError):
#             User.objects.create(
#                 username="anotheruser",
#                 email="testuser@example.com",
#                 token="randomtoken456",
#                 fullname="Another User"
#             )

# class UserSettingsModelTestCase(TestCase):
#     def setUp(self):
#         """Create a test user and settings"""
#         self.user = User.objects.create(
#             username="testuser",
#             email="testuser@example.com",
#             token="randomtoken123",
#             fullname="Test User"
#         )
#         self.user_settings = UserSettings.objects.create(
#             user_id=self.user.user_id,
#             display_name="Tester",
#             lang="fr",
#             github="https://github.com/testuser",
#             status_message="Hello World!"
#         )

#     def test_user_settings_creation(self):
#         """Test that user settings are created correctly"""
#         self.assertEqual(self.user_settings.display_name, "Tester")
#         self.assertEqual(self.user_settings.lang, "fr")
#         self.assertEqual(self.user_settings.github, "https://github.com/testuser")
#         self.assertEqual(self.user_settings.status_message, "Hello World!")

#     def test_default_avatar(self):
#         """Check that the default avatar is set correctly"""
#         self.assertEqual(self.user_settings.avatar, "avatars/default_avatar.svg")

# class UserConfidentialitySettingsModelTestCase(TestCase):
#     def setUp(self):
#         """Create a test user and confidentiality settings"""
#         self.user = User.objects.create(
#             username="testuser",
#             email="testuser@example.com",
#             token="randomtoken123",
#             fullname="Test User"
#         )
#         self.confidentiality_settings = UserConfidentialitySettings.objects.create(
#             user_id=self.user.user_id,
#             profile_visibility="private",
#             show_fullname=False,
#             show_email=False
#         )

#     def test_confidentiality_settings(self):
#         """Test that confidentiality settings are saved correctly"""
#         self.assertEqual(self.confidentiality_settings.profile_visibility, "private")
#         self.assertFalse(self.confidentiality_settings.show_fullname)
#         self.assertFalse(self.confidentiality_settings.show_email)

#     def test_invalid_visibility_choice(self):
#         """Ensure an invalid profile visibility choice raises a ValidationError"""
#         with self.assertRaises(ValidationError):
#             invalid_settings = UserConfidentialitySettings(
#                 user_id=self.user.user_id, profile_visibility="unknown"
#             )
#             invalid_settings.full_clean() 

# class FriendModelTestCase(TestCase):
#     def setUp(self):
#         """Create test users and a friendship"""
#         self.user1 = User.objects.create(
#             username="user1",
#             email="user1@example.com",
#             token="token123",
#             fullname="User One"
#         )
#         self.user2 = User.objects.create(
#             username="user2",
#             email="user2@example.com",
#             token="token456",
#             fullname="User Two"
#         )
#         self.friendship = Friend.objects.create(user=self.user1, friend=self.user2)

#     def test_friendship_creation(self):
#         """Test that a friendship is created correctly"""
#         self.assertEqual(str(self.friendship), "user1 is friends with user2")

#     def test_duplicate_friendship_fails(self):
#         """Ensure that duplicate friendships are not allowed"""
#         with self.assertRaises(IntegrityError):
#             Friend.objects.create(user=self.user1, friend=self.user2)

#     def test_reverse_friendship(self):
#         """Ensure that a friendship is not implicitly bidirectional"""
#         with self.assertRaises(IntegrityError):
#             Friend.objects.create(user=self.user2, friend=self.user1)

