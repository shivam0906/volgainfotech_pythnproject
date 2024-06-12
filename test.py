import unittest
from flask_testing import TestCase
from flask import Flask
from main import app, db, Chef, Recipe

class TestAuthentication(TestCase):
    def create_app(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_register(self):
        # Test registration functionality
        response = self.client.post('/register', data=dict(
            username='test_user',
            password='test_password',
            name='Test User',
            mobile_number='1234567890'
        ), follow_redirects=True)
        self.assertIn(b'Registered successfully', response.data)

    def test_login_logout(self):
        # Test login and logout functionality
        self.client.post('/register', data=dict(
            username='test_user',
            password='test_password',
            name='Test User',
            mobile_number='1234567890'
        ), follow_redirects=True)
        response = self.client.post('/login', data=dict(
            username='test_user',
            password='test_password'
        ), follow_redirects=True)
        self.assertIn(b'Logged in successfully', response.data)
        response = self.client.get('/logout', follow_redirects=True)
        self.assertIn(b'Logged out successfully', response.data)

class TestDatabaseOperations(TestCase):
    def create_app(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        return app

    def setUp(self):
        db.create_all()
        self.user = Chef(username='test_user', name='Test User', mobile_number='1234567890')
        self.user.set_password('test_password')
        db.session.add(self.user)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_add_recipe(self):
        # Test adding a new recipe
        self.client.post('/login', data=dict(
            username='test_user',
            password='test_password'
        ), follow_redirects=True)
        response = self.client.post('/add_recipe', data=dict(
            title='Test Recipe',
            ingredients='Ingredient 1, Ingredient 2',
            instructions='Step 1, Step 2',
            description='Test Description'
        ), follow_redirects=True)
        self.assertIn(b'Recipe added successfully', response.data)
        recipe = Recipe.query.filter_by(title='Test Recipe').first()
        self.assertIsNotNone(recipe)

    def test_edit_recipe(self):
        # Test editing an existing recipe
        self.client.post('/login', data=dict(
            username='test_user',
            password='test_password'
        ), follow_redirects=True)
        recipe = Recipe(title='Test Recipe', ingredients='Ingredient 1, Ingredient 2', instructions='Step 1, Step 2', description='Test Description', created_by=self.user.id)
        db.session.add(recipe)
        db.session.commit()
        response = self.client.post('/recipe/{}/edit'.format(recipe.id), data=dict(
            title='Updated Test Recipe',
            ingredients='Updated Ingredient 1, Updated Ingredient 2',
            instructions='Updated Step 1, Updated Step 2',
            description='Updated Test Description'
        ), follow_redirects=True)
        self.assertIn(b'Recipe updated successfully', response.data)
        updated_recipe = Recipe.query.filter_by(id=recipe.id).first()
        self.assertEqual(updated_recipe.title, 'Updated Test Recipe')

    def test_delete_recipe(self):
        # Test deleting an existing recipe
        self.client.post('/login', data=dict(
            username='test_user',
            password='test_password'
        ), follow_redirects=True)
        recipe = Recipe(title='Test Recipe', ingredients='Ingredient 1, Ingredient 2', instructions='Step 1, Step 2', description='Test Description', created_by=self.user.id)
        db.session.add(recipe)
        db.session.commit()
        response = self.client.post('/recipe/{}/delete'.format(recipe.id), follow_redirects=True)
        self.assertIn(b'Recipe deleted successfully', response.data)
        deleted_recipe = Recipe.query.filter_by(id=recipe.id).first()
        self.assertIsNone(deleted_recipe)

if __name__ == '__main__':
    unittest.main()
