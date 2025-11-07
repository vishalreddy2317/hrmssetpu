# 🏥 Hospital Management System - Backend API
## Powered by FastAPI + Pydantic V2 + PostgreSQL

A comprehensive **FastAPI-based Hospital Management System** with complete floor management, patient records, appointments, billing, inventory, and more.

**Built with:**
- ✅ **FastAPI 0.109+**
- ✅ **Pydantic V2.5+** (Latest validation framework)
- ✅ **PostgreSQL 15+** (Production-grade database)
- ✅ **SQLAlchemy 2.0+** (Modern ORM)
- ✅ **Alembic** (Database migrations)

---

## 📋 **Table of Contents**

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [PostgreSQL Setup](#postgresql-setup)
- [Configuration](#configuration)
- [Database Migrations](#database-migrations)
- [Running the Application](#running-the-application)
- [API Documentation](#api-documentation)
- [Pydantic V2 Features](#pydantic-v2-features)
- [Testing](#testing)
- [Deployment](#deployment)

---

## ✨ **Features**

### **Core Modules**
- ✅ **Floor Management** - Multi-floor building support with elevator/stairs tracking
- ✅ **Patient Management** - Complete patient records with Pydantic V2 validation
- ✅ **Doctor Management** - Doctor profiles, specializations, schedules
- ✅ **Appointment System** - Booking, scheduling, automated reminders
- ✅ **Ward & Room Management** - Floor-wise room allocation
- ✅ **Bed Management** - Real-time bed availability tracking
- ✅ **Admission & Discharge** - Patient admission workflows
- ✅ **Department Management** - Multi-department support

### **Medical Services**
- 🔬 **Lab Tests** - Test orders, results, reports
- 💊 **Pharmacy** - Medicine inventory and dispensing
- 🏥 **Operation Theater** - OT scheduling and management
- 🚑 **Emergency** - Emergency patient handling
- 📊 **Radiology/Imaging** - X-Ray, CT, MRI management
- 💉 **Vaccination** - Vaccine tracking

### **Financial**
- 💰 **Billing** - Invoice generation, payments
- 💳 **Payment Gateway** - Online payment integration
- 📈 **Revenue Tracking** - Financial reports
- 💼 **Payroll** - Staff salary management
- 📋 **Insurance** - Insurance claim processing

### **Staff Management**
- 👨‍⚕️ **Doctors** - Complete doctor profiles
- 👩‍⚕️ **Nurses** - Nurse assignments, shifts
- 👔 **Staff** - Administrative staff
- 📅 **Attendance** - Staff attendance tracking
- 🗓️ **Leave Management** - Leave requests and approvals

---

## 🛠️ **Tech Stack**

| Category | Technology | Version |
|----------|-----------|---------|
| **Framework** | FastAPI | 0.109+ |
| **Language** | Python | 3.11+ |
| **Database** | PostgreSQL | 15+ |
| **ORM** | SQLAlchemy | 2.0+ |
| **Validation** | Pydantic | V2.5+ |
| **Migration** | Alembic | 1.13+ |
| **Authentication** | JWT | - |
| **Caching** | Redis | 7.0+ |
| **Task Queue** | Celery | 5.3+ |
| **Testing** | Pytest | 7.4+ |
| **Container** | Docker | Latest |

---

## 📦 **Prerequisites**

### **Required**
- **Python**: 3.11 or higher
- **PostgreSQL**: 15 or higher
- **pip**: Latest version
- **Git**: Latest version

### **Optional (Recommended)**
- **Redis**: 7.0+ (for caching)
- **Docker**: Latest (for containerization)
- **Docker Compose**: v2.0+

---

## 🚀 **Installation**

### **Step 1: Clone Repository**

```bash
git clone https://github.com/yourusername/hospital-management-backend.git
cd hospital-management-backend