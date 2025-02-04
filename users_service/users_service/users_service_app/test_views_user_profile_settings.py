# from django.test import TestCase, Client
# from users_service_app.models import User, UserSettings, UserConfidentialitySettings
# from django.core.files.uploadedfile import SimpleUploadedFile


# class UserProfileSettingsTestCase(TestCase):
#     def setUp(self):
#         self.client = Client()

#         self.user = User.objects.create(
#             user_id=1,
#             username="Alice",
#             email="alice@example.com",
#             token="valid_token",
#             fullname="Alice Wonderland"
#         )

#         self.user_settings = UserSettings.objects.create(
#             user_id=self.user.user_id,
#             display_name="Alice",
#             lang="en",
#             github="https://github.com/alice",
#             status_message="Hello World"
#         )

#         self.user_confidentiality = UserConfidentialitySettings.objects.create(
#             user_id=self.user.user_id,
#             profile_visibility="public",
#             show_fullname=True,
#             show_email=True
#         )

#     def test_update_profile_settings_success(self):
#         url = f"https://testserver/api/user/settings/update/{self.user.token}/"
#         response = self.client.post(url, {
#             "display_name": "NewAlice",
#             "github_url": "https://github.com/newalice",
#             "status_message": "Updated status",
#             "lang": "fr"
#         }, secure=True)

#         self.assertEqual(response.status_code, 200)
#         self.user_settings.refresh_from_db()
#         self.assertEqual(self.user_settings.display_name, "NewAlice")
#         self.assertEqual(self.user_settings.github, "https://github.com/newalice")
#         self.assertEqual(self.user_settings.status_message, "Updated status")
#         self.assertEqual(self.user_settings.lang, "fr")

#     def test_update_profile_settings_invalid_token(self):
#         url = "https://testserver/api/user/settings/update/invalid_token/"
#         response = self.client.post(url, secure=True)
#         self.assertEqual(response.status_code, 404)

#     def test_update_profile_settings_too_long_display_name(self):
#         url = f"https://testserver/api/user/settings/update/{self.user.token}/"
#         response = self.client.post(url, {
#             "display_name": "A" * 21
#         }, secure=True)
#         self.assertEqual(response.status_code, 400)

#     def test_update_profile_settings_valid_display_name(self):
#         url = f"https://testserver/api/user/settings/update/{self.user.token}/"
#         long_name = "A" * 20
#         response = self.client.post(url, {"display_name": long_name}, secure=True)
#         self.assertEqual(response.status_code, 200)

#     def test_update_profile_settings_empty_display_name(self):
#         url = f"https://testserver/api/user/settings/update/{self.user.token}/"
#         response = self.client.post(url, {"display_name": ""}, secure=True)
#         self.assertEqual(response.status_code, 200)

#     def test_update_profile_settings_large_avatar(self):
#         url = f"https://testserver/api/user/settings/update/{self.user.token}/"
#         large_file = SimpleUploadedFile("avatar.jpg", b"A" * (2 * 1024 * 1024 + 1))  # 2MB+1 byte
#         response = self.client.post(url, {"avatar": large_file}, secure=True)
#         self.assertEqual(response.status_code, 400)

#     def test_update_profile_settings_invalid_avatar_type(self):
#         url = f"https://testserver/api/user/settings/update/{self.user.token}/"
#         invalid_file = SimpleUploadedFile("avatar.txt", b"Invalid content")
#         response = self.client.post(url, {"avatar": invalid_file}, secure=True)
#         self.assertEqual(response.status_code, 400)

#     def test_update_confidentiality_settings_success(self):
#         url = f"https://testserver/api/user/settings/confidentiality/{self.user.token}/"
#         response = self.client.post(url, {
#             "profile_visibility": "private",
#             "profile_show_fullname": "on",
#             "profile_show_email": ""
#         }, secure=True)

#         self.assertEqual(response.status_code, 200)
#         self.user_confidentiality.refresh_from_db()
#         self.assertEqual(self.user_confidentiality.profile_visibility, "private")
#         self.assertTrue(self.user_confidentiality.show_fullname)
#         self.assertFalse(self.user_confidentiality.show_email)

#     def test_update_confidentiality_settings_invalid_token(self):
#         url = "https://testserver/api/user/settings/confidentiality/invalid_token/"
#         response = self.client.post(url, secure=True)
#         self.assertEqual(response.status_code, 404)

#     def test_delete_account_success(self):
#         url = f"https://testserver/api/user/delete/{self.user.token}/"
#         response = self.client.delete(url, secure=True)
#         self.assertEqual(response.status_code, 200)
#         self.assertFalse(User.objects.filter(user_id=self.user.user_id).exists())

#     def test_delete_account_invalid_token(self):
#         url = "https://testserver/api/user/delete/invalid_token/"
#         response = self.client.delete(url, secure=True)
#         self.assertEqual(response.status_code, 404)
