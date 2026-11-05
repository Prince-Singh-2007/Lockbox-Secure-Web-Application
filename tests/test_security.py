import os
import tempfile
import unittest

import app as module


class SecurityTests(unittest.TestCase):

    def setUp(self):
        # Create a temporary database for testing
        self.tmp = tempfile.NamedTemporaryFile(delete=False)
        self.tmp.close()

        self.old_db = module.DB
        module.DB = self.tmp.name

        module.init_db()

        # Configure Flask for testing
        module.app.config.update(
            TESTING=True,
            SECRET_KEY='test-secret'
        )

        self.client = module.app.test_client()

    def tearDown(self):
        # Restore original database configuration
        module.DB = self.old_db

        # Remove temporary database
        os.unlink(self.tmp.name)

    def token(self):
        # Retrieve CSRF token from session
        with self.client.session_transaction() as s:
            return s['csrf']

    def test_dashboard_requires_login(self):
        # Verify dashboard redirects unauthenticated users
        response = self.client.get('/dashboard')

        self.assertEqual(response.status_code, 302)

    def test_post_requires_csrf(self):
        # Verify POST requests without CSRF tokens are rejected
        response = self.client.post(
            '/login',
            data={'username': 'x'}
        )

        self.assertEqual(response.status_code, 400)

    def test_register_login_dashboard(self):
        # Register a new test user
        response = self.client.post(
            '/register',
            data={
                'csrf': self.token(),
                'username': 'demo_user',
                'password': 'StrongPass123!'
            },
            follow_redirects=True
        )

        self.assertEqual(response.status_code, 200)

        # Log in using registered credentials
        response = self.client.post(
            '/login',
            data={
                'csrf': self.token(),
                'username': 'demo_user',
                'password': 'StrongPass123!'
            },
            follow_redirects=True
        )

        # Verify successful dashboard access
        self.assertIn(b'Session active', response.data)


if __name__ == '__main__':
    unittest.main()
