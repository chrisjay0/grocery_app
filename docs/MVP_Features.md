### Minimum Viable Product (MVP) - Features:

1. **User Authentication**:
    - **User Login**: Allows registered users to access their personalized experience and saved lists.
    - **Guest User Access**: Enables quick use of the app without the need for account creation.

2. **User Preferences**:
    - **Stored Zip Code**: For signed-in users, the app remembers their zip code to simplify price checking.
    - **Manual Zip Code Entry**: Guest users always provide their zip code manually each time.
    - **Travel Distance**: When creating an account, users specify their preferred travel distance for store recommendations.
    - **Delete Account**: The user can delete there account. A warning confirmation popup appears to confirm their decision.

3. **List Management**:
    - **Create a List**: Users can type in items and add them to their list with a click.
    - **Edit List**: Options to remove items or adjust quantities.
    - **Load Saved Lists**: Signed-in users can select previously saved lists, which are loaded into the main UI.

4. **Backend Operations**:
    - **Real-Time Price Check**: As users add items to their list, the backend sends API requests to update item prices in the database. This ensures up-to-date data without overloading the system upon the final price comparison.

5. **Price Comparisons**:
    - **Compare Prices Button**: Users submit their list to see the total cost at various stores.
    - **Display Price Comparisons**: Results show the estimated total cost for each store, sorted from cheapest to most expensive.

6. **User Feedback**:
    - **No Matches Notification**: If certain items don't match any store products, users are informed via a red text popup.

7. **List Saving & Prompts**:
    - **Save List Option**: Signed-in users can save their current list to their account.
    - **Signup Prompt for Guest Users**: If a guest user tries to save a list, they're prompted to sign in or create an account.

8. **User Dashboard**:
    - **View Saved Lists**: Signed-in users see their saved lists with options to view, edit, or delete.
    - **User Preferences**: Signed-in users can see their account settings to edit their zipcode, travel distance, or delete their account.

9. **Account Creation**:
    - **New Account Setup**: New users provide their username, password, zip code, and travel distance during account creation.