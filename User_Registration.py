import re


class UserRegistration:
    def __init__(self, test_case):
        self.test_case = test_case
        self.registered_emails = set()

    def register(self, email, password, confirm_password):
        result = {'success': False, 'message': '', 'error': ''}

        # Check for empty email
        if not email:
            result['error'] = "Email cannot be empty"
            return result

        # Check for valid email format
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            result['error'] = "Invalid email format"
            return result

        # Check for email already registered
        if email in self.registered_emails:
            result['error'] = "Email already registered"
            return result

        # Check for empty password
        if not password:
            result['error'] = "Password cannot be empty"
            return result

        # Check for empty confirmation password
        if not confirm_password:
            result['error'] = "Confirmation password cannot be empty"
            return result

        # Check for password mismatch
        if password != confirm_password:
            result['error'] = "Passwords do not match"
            return result

        # Check for strong password
        if len(password) < 8 or not re.search(r"[a-zA-Z]", password) or not re.search(r"[0-9]", password):
            result['error'] = "Password is not strong enough"
            return result

        # If all checks pass, register the user
        self.registered_emails.add(email)
        result['success'] = True
        result['message'] = "Registration successful, confirmation email sent"
        return result


# The test cases remain the same as provided in the question.
# The following lines should be added at the end of the script to run the tests.


# Unit tests for UserRegistration class
import unittest


class TestUserRegistration(unittest.TestCase):

    def setUp(self):
        """
        Set up the test environment by creating an instance of the UserRegistration class.
        This instance will be used across all test cases.
        """
        self.registration = UserRegistration(self)

    def test_successful_registration(self):
        """
        Test case for successful user registration.
        It verifies that a valid email and matching strong password results in successful registration.
        """
        result = self.registration.register("user@example.com", "Password123", "Password123")
        self.assertTrue(result['success'])  # Ensures that registration is successful.
        self.assertEqual(result['message'],
                         "Registration successful, confirmation email sent")  # Checks the success message.

    def test_invalid_email(self):
        """
        Test case for invalid email format.
        It verifies that attempting to register with an incorrectly formatted email results in an error.
        """
        result = self.registration.register("userexample.com", "Password123", "Password123")
        self.assertFalse(result['success'])  # Ensures registration fails due to invalid email.
        self.assertEqual(result['error'], "Invalid email format")  # Checks the specific error message.

    def test_password_mismatch(self):
        """
        Test case for password mismatch.
        It verifies that when the password and confirmation password do not match, registration fails.
        """
        result = self.registration.register("user@example.com", "Password123", "Password321")
        self.assertFalse(result['success'])  # Ensures registration fails due to password mismatch.
        self.assertEqual(result['error'], "Passwords do not match")  # Checks the specific error message.

    def test_weak_password(self):
        """
        Test case for weak password.
        It verifies that a password not meeting the strength requirements results in an error.
        """
        result = self.registration.register("user@example.com", "pass", "pass")
        self.assertFalse(result['success'])  # Ensures registration fails due to a weak password.
        self.assertEqual(result['error'], "Password is not strong enough")  # Checks the specific error message.

    def test_email_already_registered(self):
        """
        Test case for duplicate email registration.
        It verifies that attempting to register an email that has already been registered results in an error.
        """
        self.registration.register("user@example.com", "Password123", "Password123")  # Register a user.
        result = self.registration.register("user@example.com", "Password123", "Password123")
        self.assertFalse(result['success'])  # Ensures registration fails due to the email already being registered.
        self.assertEqual(result['error'], "Email already registered")  # Checks the specific error message.

    def test_registration_with_empty_email(self):
        """
        Test case for empty email field.
        It verifies that attempting to register without an email results in an error.
        """
        result = self.registration.register("", "Password123", "Password123")
        self.assertFalse(result['success'])  # Ensures registration fails due to empty email.
        self.assertEqual(result['error'], "Email cannot be empty")  # Checks the specific error message.

    def test_registration_with_empty_password(self):
        """
        Test case for empty password field.
        It verifies that attempting to register without a password results in an error.
        """
        result = self.registration.register("user@example.com", "", "Password123")
        self.assertFalse(result['success'])  # Ensures registration fails due to empty password.
        self.assertEqual(result['error'], "Password cannot be empty")  # Checks the specific error message.

    def test_registration_with_empty_confirmation_password(self):
        """
        Test case for empty confirmation password field.
        It verifies that attempting to register without a confirmation password results in an error.
        """
        result = self.registration.register("user@example.com", "Password123", "")
        self.assertFalse(result['success'])  # Ensures registration fails due to empty confirmation password.
        self.assertEqual(result['error'], "Confirmation password cannot be empty")  # Checks the specific error message.


if __name__ == '__main__':
    unittest.main()
