# Smart Grocery Shopper

Optimize your grocery shopping experience by ensuring you get the most value for your money.

## Description

Grocery shopping can be cumbersome, especially for those mindful of their budgets. 'Smart Grocery Shopper' is designed to simplify this task. Users create their grocery lists within the app, which then scours various grocery store databases to compare item prices. It offers a detailed breakdown of the total cost for the entire list across different stores, helping users decide where to shop for the best savings.

## Table of Contents

- [Features](https://chat.openai.com/c/a006a96a-5a61-45a9-9259-a5a8461ad8b4#features)
- [Technologies](https://chat.openai.com/c/a006a96a-5a61-45a9-9259-a5a8461ad8b4#technologies)
- [Services and Resources](https://chat.openai.com/c/a006a96a-5a61-45a9-9259-a5a8461ad8b4#services-and-resources)

## Features

- **List Management**: Facilitates list creation, and editing.
- **Backend Operations**: Provides real-time price checks as items are added.
- **Price Comparisons**: Enables users to see total costs at various stores, displayed in an organized manner.

## Technologies

### Frontend:

- **Framework**: React
- **Libraries & Components**:
    - `@mui/material`: UI library for React.
    - `@mui/icons-material`: Icons library for React.
    - `axios`: Used for making HTTP requests.

### Backend:

- **Framework**: Flask
- **Libraries**:
    - `flask_cors`: Handles Cross-Origin Resource Sharing.
    - `flask_migrate`: Manages database migrations.
    - `httpx`: Asynchronous HTTP client.
    - `asyncio`: Handles asynchronous operations.
- **Database**: SQLAlchemy (ORM)

## Services and Resources

Currently, the app leverages the publicly available [Kroger API](https://developer.kroger.com/reference/) for data. In the future, there's potential to integrate with additional API services to further enhance the comparison and recommendation capabilities.
