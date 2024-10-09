from django.test import TestCase, Client
from django.urls import reverse
from .models import Profile



class HomePageTestCase(TestCase):
    def test_home_page_view(self):
        response = self.client.get(reverse('student:home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'student/home.html')  # Replace with the actual template name

class ProfileListViewTestCase(TestCase):
    def test_profile_list_view(self):
        response = self.client.get(reverse('student:profile_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'student/profile_list.html')  # Replace with the actual template name

class ProfileDetailViewTestCase(TestCase):
    def setUp(self):
        self.profile = Profile.objects.create( 
            first_name = 'John',
            last_name = 'Doe',
            email = 'johndoe@example.com',
            phone_number = '1234567890',
            date_of_birth = '2000-01-01',
            address = '123 Main St',
            enrollment_date = '2020-09-01',
            major = 'Computer Science',
            status = 'active'
        )

            


    def test_profile_detail_view(self):
        response = self.client.get(reverse('student:profile_detail', args=[self.profile.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.profile.first_name)

class ProfileCreateViewTestCase(TestCase):
    def test_profile_create_view_get(self):
        response = self.client.get(reverse('student:profile_create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'student/profile_form.html')  # Replace with the actual template name

    def test_profile_create_view_post(self):
        data = {'first_name': 'Jane Doe', 'email': 'janedoe@example.com'}
        response = self.client.post(reverse('student:profile_create'), data)
        self.assertEqual(response.status_code, 302)  # Redirect to the profile list page
        self.assertTrue(Profile.objects.filter(first_name='Jane', email='janedoe@example.com').exists())

# class ProfileUpdateViewTestCase(TestCase):
#     def setUp(self):
#         self.profile = Profile.objects.create(name='John Doe', email='johndoe@example.com')

#     def test_profile_update_view_get(self):
#         response = self.client.get(reverse('student:profile_update', args=[self.profile.pk]))
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'student/profile_form.html')  # Replace with the actual template name

#     def test_profile_update_view_post(self):
#         data = {'name': 'Jane Doe', 'email': 'janedoe@example.com'}
#         response = self.client.post(reverse('student:profile_update', args=[self.profile.pk]), data)
#         self.assertEqual(response.status_code, 302)  # Redirect to the profile list page
#         self.profile.refresh_from_db()
#         self.assertEqual(self.profile.name, 'Jane Doe')
#         self.assertEqual(self.profile.email, 'janedoe@example.com')

# class ProfileDeleteViewTestCase(TestCase):
#     def setUp(self):
#         self.profile = Profile.objects.create(name='John Doe', email='johndoe@example.com')

#     def test_profile_delete_view(self):
#         response = self.client.get(reverse('student:profile_delete', args=[self.profile.pk]))
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'student/profile_confirm_delete.html')  # Replace with the actual template name

#     def test_profile_delete_view_post(self):
#         response = self.client.post(reverse('student:profile_delete', args=[self.profile.pk]))
#         self.assertEqual(response.status_code, 302)  # Redirect to the profile list page
#         self.assertFalse(Profile.objects.filter(pk=self.profile.pk).exists())