# 🏠 Real Estate & Property Management Platform

A **real estate and property management web application** built with **Python (Django)** by a team of developers at **SQI College of ICT**.

This platform enables **admins, vendors, and customers** to interact seamlessly in a trusted environment for property listing, management, and transactions.

---

## 👥 Team

* **3 Developers**
* **1 Lead Instructor / Mentor**

---

## 🚀 Features

### Authentication & Authorization

* **SuperAdmin** – Oversees all operations, can manage users and properties.
* **Vendors** – Onboarded to list and manage properties.
* **Customers** – Can browse, search, and interact with properties.

### Property Management

* List, edit, and delete property details (location, type, price, images).
* Categories: Sale / Rent / Lease.
* Property detail pages with descriptions & vendor info.

### User Experience

* Django templating system for frontend.
* REST API endpoints (Django REST Framework) for future integrations.
* Search & filter properties (location, price range, property type).

### Admin Dashboard

* Manage vendors, customers, and property listings.
* Track transactions and platform analytics.

### (Future Extensions / Insights)

* Property verification system.
* Customer favorites & wishlist.
* Messaging between vendors and customers.
* Payment gateway integration.
* Analytics & reporting for vendors and admins.

---

## 🛠️ Tech Stack

* **Backend**: Django (Python)
* **Database**: PostgreSQL (recommended)
* **Authentication**: Django built-in auth + role-based permissions
* **Frontend**: Django Templates (extendable to React in future)
* **API**: Django REST Framework
* **Deployment**: Docker + Render/Heroku/AWS

---

## 📂 Project Setup

### 1. Clone the repository

```bash
git clone https://github.com/SQI-Python-DataScience-Projects/real-estates.git
cd real-estates
```

### 2. Create & activate virtual environment

```bash
python -m venv venv
source venv/bin/activate   # On Mac/Linux
venv\Scripts\activate      # On Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Start development server

```bash
python manage.py runserver
```

---

## 🎯 Project Goals

* Build a **role-based real estate platform**.
* Implement **CRUD operations** for properties.
* Ensure **secure authentication & authorization**.
* Provide a clean **user interface with Django templating**.
* Extend APIs for possible **mobile/web integrations**.

---

## 📌 Roadmap

* [ ] Setup Django project & apps structure
* [ ] Implement user authentication & roles
* [ ] Create property listing module
* [ ] Build templating system & basic UI
* [ ] Develop admin dashboard
* [ ] Expose REST API endpoints
* [ ] Add extra features (verification, messaging, payments, etc.)
