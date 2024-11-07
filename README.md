# Database Theories Final Project

Welcome to the Database Theories Final Project repository. This project showcases various concepts and implementations related to database theories.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Folder Structure](#folder-structure)
- [Contributing](#contributing)
- [License](#license)

## Introduction

This project contains code and resources developed as part of a final project for a course on database theories. The repository demonstrates the design and implementation of a database application, providing functionalities like user authentication, data manipulation, and administrative capabilities.

## Features

- User authentication (login, logout)
- Data definition and manipulation scripts
- Administrative tools for managing the database
- UI for interacting with the database
- Util functions to support various operations

## Installation

Follow these steps to set up and run the project locally:

1. **Clone the Repository**:
    ```sh
    git clone https://github.com/paddy41601/Database-Theories-Final.git
    cd Database-Theories-Final
    ```

2. **Create a virtual environment**:
    ```sh
    python -m venv venv
    ```

3. **Activate the virtual environment**:
   - On Windows:
     ```sh
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```sh
     source venv/bin/activate
     ```

4. **Install the dependencies**:
    ```sh
    pip install -r requirements.txt
    ```

5. **Run the application**:
    ```sh
    python app.py
    ```

## Usage

After setting up the project, you can start the application using the command mentioned above. The application provides a web interface for interaction. Open your web browser and navigate to `http://localhost:5000` to access the application. 

You can use the interface to manage user authentication, perform administrative tasks, and run various database operations.

## Folder Structure

Here's a brief description of the structure of this repository:

- **DDL/** - Contains SQL scripts for creating and managing database schemas.
- **admin/** - Administrative tools and scripts.
- **auth/** - User authentication related code (login, logout, session management).
- **static/** - Static files (e.g., CSS, JavaScript, images).
- **templates/** - HTML templates for UI rendering.
- **user/** - User management functionalities.
- **utils/** - Utility functions.
- **.gitignore** - Git ignore file.
- **app.py** - Main application script.
- **requirements.txt** - List of project dependencies.

## Contributing

Contributions are welcome! Please follow these steps to contribute:

1. Fork the repository.
2. Create your feature branch (`git checkout -b feature/AmazingFeature`).
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`).
4. Push to the branch (`git push origin feature/AmazingFeature`).
5. Open a pull request.

## License

This project is licensed under the MIT License. See the `LICENSE` file for more information.

---

Happy coding! If you have any questions or suggestions, feel free to open an issue or create a pull request.
