# Nunua Store | Online Shopping Platform

![Nunua Store Logo](nunua/static/images/logo/Logo.png)

Welcome to Nunua Store, your go-to online shopping platform built with the power of Django Framework.

## Overview

Nunua Store is a fully functional e-commerce platform designed to provide a seamless shopping experience for users and a robust management system for administrators. This project leverages the Django framework's capabilities for handling backend logic, database interactions, and routing, creating a scalable and maintainable web application.

## Features

**For Customers:**

* **Product Browsing:** Easily navigate through a wide range of products categorized for convenient searching.
* **Detailed Product Pages:** View comprehensive information about each product, including descriptions, images, pricing, and availability.
* **User Authentication:** Secure user registration and login to manage profiles and order history.
* **Shopping Cart:** Add, remove, and modify items in a persistent shopping cart.
* **Checkout Process:** A streamlined and secure checkout process with options for shipping and payment e.g. PayPal, Mpesa, and Stripe.
* **Order Tracking:** Receive real-time updates on the status of your order.
* **Order History:** Track past orders and view order details.
* **Search Functionality:** Quickly find products using keywords.

**For Administrators:**

* **Admin Dashboard:** A dedicated interface to manage all aspects of the store.
* **Product Management:** Add, edit, and delete products, including details like name, description, price, images, and category.
* **Category Management:** Create, update, and organize product categories.
* **Order Management:** View, track, and update the status of customer orders.
* **User Management:** Manage user accounts and permissions.

## Technologies Used

* **Django:** The high-level Python web framework that powers the backend.
* **Python:** The programming language used for the Django application.
* **Templates:** (Containing: HTML, the standard markup language for creating web pages, and JavaScript, a programming language used for adding interactivity to web pages).
* **TailwindCSS v.4.1:** Used for styling the look and feel of the entire website.
* **Database:** (for now is SQLite3, but could be switched to PostgreSQL) for storing application data.
* **Payment Gateway Integration:** (Integrated with a payment gateway like e.g. PayPal, Mpesa, and Stripe).

## Getting Started

To run Nunua Store locally, follow these steps:

1. **Clone the repository:**

    ```bash
    git clone
    cd nunua-store
    ```

2. **Create a virtual environment:**

    ```bash
    python -m venv env
    ```

3. **Activate the virtual environment:**
    * **On macOS and Linux:**

        ```bash
        source env/bin/activate
        ```

    * **On Windows:**

        ```bash
        .\env\Scripts\activate
        ```

4. **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

5. **Make migrations:**

    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

6. **Create a superuser (for admin access):**

    ```bash
    python manage.py createsuperuser
    ```

    Follow the prompts to create your admin username and password.

7. **Run the development server:**

    ```bash
    python manage.py runserver
    ```

8. **Open your browser and navigate to `http://127.0.0.1:8000/` to access the store.**
9. **Access the admin panel at `http://127.0.0.1:8000/admin/` and log in with the superuser credentials you created.**

## Contributing

Contributions to Nunua Store are welcome! If you'd like to contribute, please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Make your changes and commit them.
4. Push your changes to your fork.
5. Submit a pull request.

Thank you for checking out Nunua Store!
