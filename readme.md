# Event Manager REST API

This project involves the development of a secure, robust REST API that supports JWT token-based OAuth2 authentication. The API includes user and event management features and focuses on testing, validation, and email integration.

---

## Closed Issues

Here are the closed issues addressed during the development of this project:

1. **[User Data Missing Fixtures](https://github.com/chandrA957355/homework-10/tree/user_data_missing_fixtures)**  
   - Issue: Missing user data fixtures for test cases, which resulted in incomplete test scenarios.
   - Resolution: Added comprehensive fixtures to cover diverse user scenarios and improve test reliability.

2. **[JWT Token Validation](https://github.com/chandrA957355/homework-10/tree/jwt_token_validation)**  
   - Issue: JWT token validation and generation were not conforming to OAuth2 standards.
   - Resolution: Refined the token generation logic and implemented strict validation rules to enhance security.

3. **[Password Validation](https://github.com/chandrA957355/homework-10/tree/password_validation)**  
   - Issue: Weak password validation allowed insecure passwords.
   - Resolution: Introduced custom validation logic for passwords to ensure adherence to security best practices.

4. **[SMTP Server Connection Issue](https://github.com/chandrA957355/homework-10/tree/smtp_server_connection_issue)**  
   - Issue: Failure in connecting to the SMTP server for email notifications.
   - Resolution: Configured environment variables for SMTP credentials and implemented robust error handling for email services.

---

## Docker Image

The project has been containerized using Docker. You can find the deployed image on DockerHub:  
[DockerHub Project Image](https://hub.docker.com/repository/docker/chandrA957355/homework-10)

---

## Reflection

Working on this project provided an invaluable learning experience in both technical and collaborative aspects of software development. 

### Technical Skills
- **REST API Development**: I deepened my understanding of building secure and scalable APIs using FastAPI. Implementing JWT-based authentication and user validation enhanced my knowledge of OAuth2 protocols.
- **Testing and Fixtures**: Writing comprehensive unit and integration tests using pytest improved the project's reliability. Addressing edge cases and increasing test coverage provided insights into robust API design.
- **Error Handling and Debugging**: Troubleshooting issues such as SMTP server connections and validation errors taught me how to methodically approach debugging in a distributed system.

### Collaborative Processes
- **Version Control with Git**: Managing branches for each issue and maintaining a structured workflow improved my Git skills. I also learned the importance of clear commit messages and documentation for collaboration.
- **Team-Oriented Development**: Resolving issues through pull requests and addressing feedback during code reviews reinforced the importance of clear communication and teamwork.

This project was challenging but rewarding, as it provided real-world exposure to building and maintaining production-grade systems. The lessons learned will undoubtedly guide my future endeavors in software development.

---
Access the API documentation at http://localhost:8000/docs.
