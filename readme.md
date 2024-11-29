## Homework 10 : Event Manager Company: Software QA Analyst/Developer Onboarding Assignment

This repository contains fixes for several issues as per instructor videos and course material.

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

The assignment provided an exciting opportunity to approach challenges from a QA perspective. Step by step, I explored the user lifecycle of the event manager application, uncovering bugs and gaining a thorough understanding of the codebase. Each issue presented an opportunity to refine or create functions, which enhanced my coding skills.Tackling the assignment through a QA lens was both engaging and insightful. By breaking down the user lifecycle of the event manager application, I uncovered and resolved several issues, refining my understanding of the codebase. This process involved developing new functions and creatively reusing existing ones to address problems efficiently.The assignment was also an exciting mix of challenges and discoveries. Adopting a QA perspective allowed me to systematically explore the user lifecycle in the event manager application, uncovering issues and refining my problem-solving approach. By leveraging existing functions and developing new ones, I gained a much deeper understanding of the codebase.

One of the most enjoyable aspects was working with Docker Compose. It was fascinating to see how microservices communicate internally and to troubleshoot connectivity with tools like pgAdmin. Writing test cases for the newly implemented logic and improving code coverage pushed me to dive even deeper into the application’s functionality. By the end, I felt confident navigating the code and pinpointing areas for future improvements.
Overall, this experience enhanced my technical and problem-solving skills while reinforcing the value of a structured and detailed approach to development and testing. It also made me appreciate the synergy between QA and development teams in delivering robust applications.



