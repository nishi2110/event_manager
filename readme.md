
# Event Manager REST API

This project involves the development of a secure, robust REST API that supports JWT token-based OAuth2 authentication. The API includes user and event management features and focuses on testing, validation, and email integration.

---

## Closed Issues

Here are the closed issues addressed during the development of this project:

1. **[User Data Missing Fixtures](https://github.com/chandrA957355/homework-10/issues/1)**  
   - **Issue:** Missing user data fixtures for test cases, which resulted in incomplete test scenarios.
   - **Resolution:** Added comprehensive fixtures to cover diverse user scenarios and improve test reliability.

2. **[JWT Token Validation for Manager and Admin Users](https://github.com/chandrA957355/homework-10/issues/5)**  
   - **Issue:** JWT token validation and generation were not conforming to OAuth2 standards.
   - **Resolution:** Refined the token generation logic and implemented strict validation rules to enhance security.

3. **[Enhance Password Validation and Update Field Checks in User Schemas](https://github.com/chandrA957355/homework-10/issues/4)**  
   - **Issue:** Weak password validation and insufficient field checks in updates.
   - **Resolution:** Introduced custom validation logic for passwords and enforced update field requirements.

4. **[SMTP Server Connection Issue](https://github.com/chandrA957355/homework-10/issues/3)**  
   - **Issue:** Failure in connecting to the SMTP server for email notifications.
   - **Resolution:** Configured environment variables for SMTP credentials and implemented robust error handling for email services.

5. **[Failing Tests Due to Missing or Inconsistent Fixtures](https://github.com/chandrA957355/homework-10/issues/2)**  
   - **Issue:** Missing or inconsistent fixtures in test cases caused failures in database operations.
   - **Resolution:** Enhanced test fixtures with dynamic and realistic data, and addressed edge cases.

---

## Docker Image

The project has been containerized using Docker. You can find the deployed image on DockerHub:  
[DockerHub Project Image](https://hub.docker.com/repository/docker/chandrA957355/homework-10)

---

## Reflection

Working on this project provided an invaluable learning experience in both technical and collaborative aspects of software development. 

### Technical Skills
- **REST API Development**: Deepened understanding of secure, scalable APIs using FastAPI.
- **Testing and Fixtures**: Improved project reliability with pytest and robust test coverage.
- **Error Handling and Debugging**: Learned methodical approaches to troubleshooting distributed systems.

### Collaborative Processes
- **Version Control with Git**: Structured workflows with branches and clear commit messages.
- **Team-Oriented Development**: Enhanced teamwork via pull requests and code reviews.

This project offered real-world exposure to building and maintaining production-grade systems, laying a strong foundation for future software development endeavors.

---

Access the API documentation at http://localhost:8000/docs.
