"""
    Tests for models
"""
from unittest.mock import patch
from decimal import Decimal
from django.test import TestCase
from django.contrib.auth import get_user_model
from core import models


class ModelTests(TestCase):
    """Test models."""
    def test_create_user_with_email_successful(self):
        email = 'test@example.com'
        password = 'testpass123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))
    def test_new_user_email_normalized(self):
        sample_email = [
            ['test1@EXAMPLE.com', 'test1@example.com'],
            ['TEST2@Example.com', 'TEST2@example.com'],
            ['Test3@EXAMPLE.COM', 'Test3@example.com'],
            ['test4@example.COM', 'test4@example.com']
        ]
        for email, expected in sample_email:
            user = get_user_model().objects.create_user(email, 'sample123')
            self.assertEqual(user.email, expected)
    def test_new_user_without_email_raise_value_error(self):
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('', 'sample123')
    def test_create_new_superuser(self):
        user = get_user_model().objects.create_superuser(
            'test@example.com', 'test123')
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
    def test_create_recipe(self):
        """test creating a new recipe"""
        user = get_user_model().objects.create_user(
            'testuser@example.com', 'testpass123')
        recipe = models.Recipe.objects.create(
            user=user,
            title='Recipe title',
            time_minutes=5,
            price=Decimal('5.00'),
            description='Recipe description'
        )
        self.assertEqual(str(recipe), recipe.title)
    @patch('core.models.uuid.uuid4')
    def test_recipe_file_name_uuid(self, mock_uuid):
        """Test generatig image path"""
        uuid = 'test-uuid'
        mock_uuid.return_value = uuid
        file_path = models.recipe_image_file_path(None, 'myimage.jpg')
        exp_path = f'uploads/recipe/{uuid}.jpg'
        self.assertEqual(file_path, exp_path)