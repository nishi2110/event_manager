### Issue Fixes and Test Scripts

There are 14 test cases written in total. Each branch includes test cases for the necessary changes, which can be verified in the commits named "testcase".

1. **Verify Email Missing UUID**
   - **Cause**: Email was sent before the user was added to the database.
   - **Fix**: Email is now sent after the user is added to the database.

2. **Email ID Update to Existing Email**
   - **Cause**: A success response was given when trying to update to an already existing email.
   - **Fix**: Implemented a check to retrieve data based on email. If the email is already present, an error is thrown.

3. **GitHub and LinkedIn URLs Null in Create User**
   - **Cause**: GitHub and LinkedIn URLs were null in the create user response.
   - **Fix**: Values are now correctly mapped to the response object.

4. **User Role Defaults to Anonymous When Created as Admin**
   - **Cause**: The role defaults to Anonymous and does not change to admin after verification.
   - **Fix**: Code was added to set the role to admin if the user is created as an admin.

5. **Deleting URL Fields Results in an Error**
   - **Cause**: Fields do not accept an empty string to delete the value.
   - **Fix**: A validator was added to set the value to null if the incoming field is empty.

### Feature Implementation

**Feature 9: User Profile Management**
   - **Endpoints**:
     - Update self-profile fields.
     - Upgrade user status to professional.
   - **Functionality**: When the professional field is updated, the user is notified via email about their status update.