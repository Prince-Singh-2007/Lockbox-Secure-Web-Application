# 🔐 PROJECT REPORT
# LOCKBOX – BUILDING A SECURE WEB APPLICATION

**Project Domain:** Cybersecurity / Web Application Security  
**Project Type:** Defensive Web Application  
**Technology:** Python, Flask, SQLite, HTML, CSS  
**Purpose:** Educational and Academic Project

---

## 1. Abstract

Lockbox is a local web application developed using Python and Flask to demonstrate secure user registration, authentication, and session-based access control.

The project focuses on implementing foundational defensive coding practices to protect user accounts and prevent common web application vulnerabilities.

It incorporates password hashing using Werkzeug's scrypt algorithm, parameterized SQLite queries, Cross-Site Request Forgery (CSRF) protection, secure session management, and browser security headers.

The primary aim of this project is to provide practical knowledge of secure web application development and demonstrate how common security risks can be reduced through appropriate coding techniques.

## 2. Problem Statement

Web applications that accept user input and store account credentials may be vulnerable to several security threats, including:

- Plaintext password disclosure.
- SQL injection attacks.
- Cross-Site Request Forgery (CSRF).
- Unauthorized access to protected pages.
- Session-related security vulnerabilities.

These threats can compromise user accounts and sensitive information.

Therefore, there is a need to demonstrate secure authentication mechanisms and defensive programming practices that help protect web applications against common security risks.

## 3. Objectives

The main objectives of the Lockbox project are:

1. Implement secure user registration and login functionality.
2. Store password hashes instead of plaintext passwords.
3. Use parameterized database queries to reduce SQL injection risks.
4. Validate CSRF tokens on state-changing POST requests.
5. Restrict dashboard access to authenticated users.
6. Implement secure session management.
7. Configure browser security headers and cookie attributes.
8. Perform automated testing to verify application functionality and security controls.

## 4. System Architecture

The Lockbox application follows a simple client-server architecture.

**Application Workflow:**

Browser → Flask Routes → Input Validation → Authentication → Parameterized SQLite Queries → Session Management → Protected Dashboard

### Architecture Components

| Component | Description |
|---|---|
| Browser | Provides the user interface. |
| Flask | Handles HTTP requests and application routing. |
| Validation | Checks user input and password requirements. |
| Authentication | Verifies user credentials. |
| SQLite | Stores user account information. |
| Session Management | Maintains authenticated user sessions. |
| Dashboard | Provides access to protected content. |

## 5. Technologies and Tools Used

| Technology | Purpose |
|---|---|
| Python | Backend programming language |
| Flask | Web application framework |
| SQLite | Database management |
| Werkzeug | Password hashing using scrypt |
| HTML | Web page structure |
| CSS | User interface styling |
| Unittest | Automated application testing |

## 6. Security Implementations

Lockbox demonstrates the following defensive security mechanisms:

### 6.1 Password Hashing

Passwords are hashed using Werkzeug's scrypt-based password hashing functionality.

This prevents plaintext passwords from being stored directly in the database.

### 6.2 SQL Injection Prevention

Parameterized SQLite queries are used to handle user-supplied values safely.

This reduces the risk of SQL injection attacks.

### 6.3 CSRF Protection

Random, session-bound CSRF tokens are generated and validated for POST requests.

Constant-time comparison is used when checking submitted tokens.

### 6.4 Session Security

The application renews the session after successful authentication to reduce session fixation risks.

### 6.5 Protected Dashboard

Only authenticated users can access the dashboard.

Unauthenticated users are redirected to the login page.

### 6.6 Secure Cookies and Headers

The application uses security-related cookie settings and response headers, including:

- HttpOnly
- SameSite
- Secure (optional, when deployed behind HTTPS)
- Content Security Policy (CSP)
- X-Content-Type-Options
- X-Frame-Options
- Referrer-Policy

## 7. Testing

Automated testing is performed using Python's built-in `unittest` framework.

The included test cases verify important application workflows.

| Test Case | Expected Result |
|---|---|
| Dashboard access without login | Redirects to login |
| POST request without CSRF token | Returns HTTP 400 |
| User registration | Successfully registers the user |
| User login | Successfully authenticates the user |
| Dashboard access after login | Displays authenticated session |

### Test Execution

Run the following command from the project root directory:

```bash
python -m unittest discover -s tests -v
```

The tests help verify that the implemented authentication and CSRF controls behave as expected.

## 8. Limitations

Lockbox is an educational prototype and is not designed to serve as a production identity management system.

Current limitations include:

- No login rate limiting.
- No Multi-Factor Authentication (MFA).
- No password reset functionality.
- No email verification.
- No formal security audit.
- No production deployment configuration.
- Limited automated security test coverage.

## 9. Future Scope

The application can be improved by implementing additional security and account management features.

Planned enhancements include:

1. **Rate Limiting:** Reduce automated login attempts and brute-force attacks.
2. **Multi-Factor Authentication:** Add another layer of account security.
3. **Audit Logging:** Record important authentication and account events.
4. **Password Recovery:** Allow users to securely reset forgotten passwords.
5. **Email Verification:** Verify user email addresses during registration.
6. **Role-Based Access Control:** Support different user permissions and access levels.
7. **Security Auditing:** Conduct additional security testing and vulnerability assessments.

## 10. Conclusion

Lockbox successfully demonstrates several important secure-coding practices through a small Python Flask web application.

The project provides practical experience with secure password storage, user authentication, parameterized database queries, CSRF protection, session management, and browser security headers.

It also highlights the importance of defensive programming when developing web applications that handle user credentials.

Although Lockbox provides a foundation for understanding web application security, additional security controls and professional review are necessary before considering real-world deployment.

---

## Project Declaration

**Project Name:** Lockbox – Building a Secure Web Application

**Project Category:** Cybersecurity / Web Development

**Development Environment:** Python and Flask

**Project Purpose:** Educational demonstration of secure authentication and defensive web application development.

**Ethical Statement:** This project is intended strictly for educational and defensive cybersecurity purposes. It should be tested using fictional accounts and must not be used for unauthorized credential collection.
