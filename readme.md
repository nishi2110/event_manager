# Event Manager Project

## Overview
This repository hosts the source code for the Event Manager project, a web application built with FastAPI, PostgreSQL, and Docker for managing events. The project integrates various features such as user authentication, role management, and email notifications.

This document details the progress made on the project, highlights resolved and unresolved issues, and provides insights into the learning process during the development journey.

## Github Links
**Closed Issues**: 
1. [Issue#1](https://github.com/Livia-1212/event_manager/issues/1)
3. [Issue#3](https://github.com/Livia-1212/event_manager/issues/3)

**Dockerhub Image**: Dockerhub Image


## Reflections

**Technical Challenges**
Throughout this assignment, I encountered several complex issues, including schema validation errors, SMTP connection problems, and difficulties integrating role-based permissions. While I resolved many problems, such as implementing mock SMTP clients for testing and updating fixtures for better schema validation, some challenges persisted. For instance, despite creating robust test fixtures and configurations, the UserRole enum type and table-related issues in PostgreSQL reappeared intermittently, even after dropping and recreating the database.

The process of debugging these errors enhanced my skills in database migrations with Alembic, mocking services, and writing clean, reusable test fixtures. I also deepened my understanding of the FastAPI ecosystem and learned the importance of maintaining a modular structure in services like email_service and user_service.

**Collaborative and Process-Oriented Insights**
This project reinforced the importance of version control and GitHub issue tracking. Each branch focused on a single feature or bug fix, and I diligently documented issues to streamline troubleshooting and progress tracking. However, resolving merge conflicts and ensuring compatibility across branches was more challenging than anticipated. These challenges taught me the value of clear communication, detailed commit messages, and incremental development.

Moreover, I kept setting up Dockerized environments for PostgreSQL and FastAPI, which was one of the most benefiting experience from this class that I've learnt for managing dependencies and ensuring the reproducibility of the project across different systems. While Docker simplified deployment, debugging services running in containers introduced additional complexity, such as verifying inter-service communication in docker-compose.

**Remaining Issues**
>Despite extensive efforts, a few issues remain unresolved:
>1. Certain tests for the email service and user APIs fail due to subtle configuration mismatches in fixtures or dependency injection.
>2. Failed SMTPServerDisconnected error persists: 'smtplib.SMTPServerDisconnected: Connection unexpectedly closed'

Moving forward, I plan to investigate alternative testing strategies, refine dependency management, and explore advanced database schema handling techniques.