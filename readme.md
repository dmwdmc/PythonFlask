# Flask Permission Management System

A comprehensive Flask web application with role-based access control (RBAC), user management, and multi-language support.

## 🚀 Features

- **User Authentication & Authorization**: Secure login/logout system with role-based permissions
- **Role Management**: Create, edit, and delete roles with specific permissions
- **User Management**: Assign and manage user roles
- **Multi-language Support**: Internationalization with Flask-Babel
- **Admin Panel**: Comprehensive dashboard for system administration
- **Database Migrations**: Alembic-based database versioning
- **Permission System**: Granular permission control for different operations

## 📋 Prerequisites

- Python 3.7+
- Flask
- SQLAlchemy
- Flask-Login
- Flask-Babel
- Other dependencies listed in `requirements.txt`

## 🛠️ Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd PythonFlask
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   export FLASK_APP=app.py
   export FLASK_ENV=development
   ```

## 🗄️ Database Setup

1. **Initialize the database**
   ```bash
   flask db init
   flask db migrate
   flask db upgrade
   ```

2. **Create admin user**
   - Register a new user through the application
   - Note the user ID for the next step

3. **Set up admin role**
   ```sql
   INSERT INTO public.role (name, description) VALUES ('admin', 'Administrator');
   INSERT INTO public.user_roles VALUES ({admin_user_id}, {admin_role_id});
   ```

## 🌐 Multi-language Support

1. **Compile translations**
   ```bash
   pybabel compile -d translations
   ```

2. **Available languages**
   - English (en)
   - Chinese (zh)

## 🔐 Permission System Setup

1. **Login as admin user**
2. **Access the permission initialization page**
   - Navigate to: `/permission/init_permissions`
   - This will create default permissions and roles:
     - `create_book`
     - `edit_book`
     - `delete_book`
     - `view_books`
     - `admin_panel`
     - `manage_users`
     - `manage_roles`

## 🏃‍♂️ Running the Application

1. **Start the development server**
   ```bash
   flask run
   ```

2. **Access the application**
   - Main application: `http://localhost:5000`
   - Admin panel: `http://localhost:5000/permission/admin`

## 📁 Project Structure

```
PythonFlask/
├── app.py                 # Main application entry point
├── app_factory.py         # Application factory pattern
├── auth/                  # Authentication module
│   ├── forms.py          # Login/register forms
│   ├── models.py         # User model
│   └── views.py          # Auth views
├── book/                  # Book management module
│   ├── forms.py          # Book forms
│   ├── models.py         # Book model
│   └── views.py          # Book views
├── permission/            # Permission management module
│   ├── decorators.py     # Permission decorators
│   ├── forms.py          # Permission forms
│   ├── models.py         # Role/Permission models
│   └── views.py          # Permission views
├── middleware/            # Custom middleware
├── static/               # Static files (CSS, JS)
├── templates/            # HTML templates
├── translations/         # Multi-language files
└── migrations/           # Database migrations
```

## 🔧 Configuration

### Environment Variables
- `FLASK_APP`: Application entry point
- `FLASK_ENV`: Environment (development/production)
- `SECRET_KEY`: Application secret key
- `DATABASE_URL`: Database connection string

### Database Configuration
The application uses SQLite by default. For production, consider using PostgreSQL or MySQL.

## 🚧 Development Notes

- **Redis Integration**: Not yet implemented
- **Testing**: Add comprehensive test suite
- **Documentation**: API documentation needed
- **Security**: Implement additional security measures for production

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For issues and questions:
1. Check the existing issues
2. Create a new issue with detailed description
3. Include error logs and steps to reproduce

---

**Note**: This is a development version. For production deployment, ensure proper security measures and environment configuration.