# Project Report: Lockbox - Building a Secure Web Application

## Abstract
Lockbox is a local web application demonstrating secure registration, authentication and session-based access control using foundational defensive coding practices.

## Problem Statement
Web applications that accept user input and store credentials can be exposed to plaintext password disclosure, SQL injection, CSRF and unauthorised access.

## Objectives
- Implement registration and login.
- Store password hashes rather than plaintext passwords.
- Use parameterized database queries.
- Validate CSRF tokens on state-changing requests.
- Restrict dashboard access to authenticated users.
- Apply secure session settings and response headers.

## Architecture
Browser → Flask routes → validation/authentication → parameterized SQLite queries → session/access checks → protected dashboard.

## Tools
Python, Flask, SQLite, Werkzeug, HTML, CSS and unittest.

## Testing
The included tests cover unauthenticated dashboard redirection, rejection of POST without a CSRF token, and registration/login flow.

## Limitations
This is an educational prototype. It lacks rate limiting, MFA, password reset, email verification, formal security audit and production deployment hardening.

## Future Scope
Add rate limiting, multi-factor authentication, audit logs, password reset, email verification and role-based access control.

## Conclusion
Lockbox demonstrates several important secure-coding practices in a small Flask application. Further hardening is required before real-world deployment.
