### User Flow 1: New User Registration and First Use

1. **Landing Page**:
   - New user chooses "Sign Up".
2. **Account Creation**:
   - User provides username, password, zip code, and travel distance.
3. **Dashboard**:
   - User is greeted and prompted to create their first list.
4. **Create a List**:
   - User types in items and adds them to the list.
5. **Compare Prices**:
   - User clicks the "Compare Prices" button.
6. **Display Results**:
   - The cheapest options are presented.
7. **End of Journey**:
   - User is prompted to save the list or start a new one.

### User Flow 2: Returning User Accessing Saved Lists

1. **Landing Page**:
   - User chooses "Login" and enters credentials.
2. **Dashboard**:
   - User sees saved lists and selects one.
3. **List Management**:
   - The selected list is loaded. User makes modifications if needed.
4. **Compare Prices**:
   - User clicks the "Compare Prices" button.
5. **Display Results**:
   - Updated price comparisons are shown.

### User Flow 3: Guest User Experience

1. **Landing Page**:
   - Guest user starts creating a list without logging in.
2. **Create a List**:
   - User types in items and adds them to the list.
3. **Enter Zip Code**:
   - Guest user manually enters their zip code.
4. **Compare Prices**:
   - User clicks the "Compare Prices" button.
5. **Display Results**:
   - The cheapest options are presented.
6. **Prompt to Save**:
   - User tries to save the list and is prompted to sign in or create an account.

### User Flow 4: Updating User Preferences

1. **Landing Page**:
   - Returning user logs in.
2. **Dashboard**:
   - User navigates to "User Preferences".
3. **Edit Preferences**:
   - User updates their zip code, travel distance, or both.
4. **Confirmation**:
   - Changes are saved, and a confirmation message is displayed.

### User Flow 5: Deleting an Account

1. **Landing Page**:
   - Returning user logs in.
2. **Dashboard**:
   - User navigates to "User Preferences".
3. **Delete Account**:
   - User selects "Delete Account" and confirms via a warning popup.
4. **End of Journey**:
   - Account is deleted, and user is redirected to the landing page with a message confirming the deletion.

### User Flow 6: Handling No Matches

1. **Landing Page**:
   - User (guest or signed-in) starts creating a list.
2. **Create a List**:
   - User adds items, some of which might not have matches in stores.
3. **Compare Prices**:
   - User clicks the "Compare Prices" button.
4. **Display Results**:
   - The cheapest options are presented.
5. **No Matches Notification**:
   - Red text popup informs the user about items that couldn't be matched.