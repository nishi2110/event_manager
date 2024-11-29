
## Description and Links to the Closed Issue:

Fixed the Missing test fixtures and mismatched conftest data by creating fixtures to generate user, admin and manager tokens.Also fixed issues with standardization of data in conftest.py

Link : https://github.com/MallikaKasi/IS601-Fall2024-Homework10-event_manager/issues/1

Fixed Pytest Errors with JWT Token and Sendemail by creating a new inbox in Mailtrap.Added the username and password credentials to the .env file.

Link : https://github.com/MallikaKasi/IS601-Fall2024-Homework10-event_manager/issues/1

Fixed the Auto generating nickname mismatch issue. While Registering Nickname is replaced by an auto generated one and getting updated to the database. This issue is resolved by replacing the manually generated nickname that will be passed as an argument to the generate_nickname method.

Link : https://github.com/MallikaKasi/IS601-Fall2024-Homework10-event_manager/issues/2

Fixed the Nickname Duplicate logic: When registering a new user, duplicate Nicknames are allowed. So added the logic to check and make sure Nicknames are unique.

Link : https://github.com/MallikaKasi/IS601-Fall2024-Homework10-event_manager/issues/3

Fixed the Password validation Issue: Added validation for the password to meet the mandatory minimum length and to have at least one upper case, lower case, numbers, and special character.

Link : https://github.com/MallikaKasi/IS601-Fall2024-Homework10-event_manager/issues/6

Added the Additional validation while adding profile urlsand the necessary test case.

Link : https://github.com/MallikaKasi/IS601-Fall2024-Homework10-event_manager/issues/8

Fixed the Email validation missing. Email field doesn't check for invalid email addresses like missing @ or missing username or missing domain name, So added the logic to validate the invalid email addresses. 

Link : https://github.com/MallikaKasi/IS601-Fall2024-Homework10-event_manager/issues/10

## Pytest Code Coverage
![image](https://github.com/user-attachments/assets/25a6fb40-ccaa-442b-af1f-0729de329e1e)

![image](https://github.com/user-attachments/assets/7721d502-cf49-4d73-bd88-94eca4c02a78)


## Link to project image deployed to Dockerhub

![image](https://github.com/user-attachments/assets/aef25a17-f0c3-49a4-9921-1890deb6a965)
![image](https://github.com/user-attachments/assets/5731c9e6-effb-4bcd-8f02-49657e5a2898)

### Learning from this Project

  - Links to the closed issues, providing easy access to your work.
  - Test coverage 
  - Link to project image deployed to Dockerhub.
  - A 2-3 paragraph reflection on what you learned from this assignment, focusing on both technical skills and collaborative processes. Reflect on the challenges you faced, the solutions you implemented, and the insights you gained. This reflection helps solidify your learning and provides valuable feedback for improving the assignment in the future.



