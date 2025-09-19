"""
Database setup script for the office management system.
Creates initial data and superuser.
"""

import os
import sys
import django
from django.conf import settings

# Add the backend directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'office_management.settings')
django.setup()

from django.contrib.auth import get_user_model
from employees.models import Department, Position
from salary.models import SalaryStructure
from learning.models import Course
from notifications.models import SystemAnnouncement

User = get_user_model()


def create_superuser():
    """Create superuser if it doesn't exist"""
    if not User.objects.filter(is_superuser=True).exists():
        User.objects.create_superuser(
            username='admin',
            email='admin@aikshetra.com',
            password='admin123',
            first_name='System',
            last_name='Administrator',
            role='admin',
            is_approved=True
        )
        print("✓ Superuser created: admin@aikshetra.com / admin123")
    else:
        print("✓ Superuser already exists")


def create_departments():
    """Create initial departments"""
    departments_data = [
        {
            'name': 'Engineering',
            'description': 'Software development and technical operations',
            'location': 'Building A, Floor 3'
        },
        {
            'name': 'Human Resources',
            'description': 'Employee management and organizational development',
            'location': 'Building B, Floor 1'
        },
        {
            'name': 'Marketing',
            'description': 'Brand promotion and customer acquisition',
            'location': 'Building A, Floor 2'
        },
        {
            'name': 'Sales',
            'description': 'Revenue generation and client relations',
            'location': 'Building B, Floor 2'
        },
        {
            'name': 'Finance',
            'description': 'Financial planning and accounting',
            'location': 'Building A, Floor 1'
        }
    ]
    
    for dept_data in departments_data:
        dept, created = Department.objects.get_or_create(
            name=dept_data['name'],
            defaults=dept_data
        )
        if created:
            print(f"✓ Created department: {dept.name}")


def create_positions():
    """Create initial positions"""
    positions_data = [
        # Engineering positions
        {'title': 'Software Engineer', 'department': 'Engineering', 'min_salary': 60000, 'max_salary': 120000},
        {'title': 'Senior Software Engineer', 'department': 'Engineering', 'min_salary': 90000, 'max_salary': 150000},
        {'title': 'Tech Lead', 'department': 'Engineering', 'min_salary': 120000, 'max_salary': 180000},
        {'title': 'DevOps Engineer', 'department': 'Engineering', 'min_salary': 70000, 'max_salary': 130000},
        
        # HR positions
        {'title': 'HR Specialist', 'department': 'Human Resources', 'min_salary': 45000, 'max_salary': 70000},
        {'title': 'HR Manager', 'department': 'Human Resources', 'min_salary': 70000, 'max_salary': 100000},
        
        # Marketing positions
        {'title': 'Marketing Specialist', 'department': 'Marketing', 'min_salary': 40000, 'max_salary': 65000},
        {'title': 'Marketing Manager', 'department': 'Marketing', 'min_salary': 65000, 'max_salary': 95000},
        
        # Sales positions
        {'title': 'Sales Representative', 'department': 'Sales', 'min_salary': 35000, 'max_salary': 60000},
        {'title': 'Sales Manager', 'department': 'Sales', 'min_salary': 60000, 'max_salary': 90000},
        
        # Finance positions
        {'title': 'Accountant', 'department': 'Finance', 'min_salary': 45000, 'max_salary': 70000},
        {'title': 'Finance Manager', 'department': 'Finance', 'min_salary': 70000, 'max_salary': 110000},
    ]
    
    for pos_data in positions_data:
        try:
            department = Department.objects.get(name=pos_data['department'])
            pos, created = Position.objects.get_or_create(
                title=pos_data['title'],
                department=department,
                defaults={
                    'min_salary': pos_data['min_salary'],
                    'max_salary': pos_data['max_salary'],
                    'description': f"{pos_data['title']} in {pos_data['department']} department"
                }
            )
            if created:
                print(f"✓ Created position: {pos.title}")
        except Department.DoesNotExist:
            print(f"✗ Department not found: {pos_data['department']}")


def create_salary_structures():
    """Create initial salary structures"""
    structures_data = [
        {
            'name': 'Junior Level',
            'base_salary': 45000,
            'house_rent_allowance': 9000,
            'transport_allowance': 2400,
            'medical_allowance': 1200,
        },
        {
            'name': 'Mid Level',
            'base_salary': 70000,
            'house_rent_allowance': 14000,
            'transport_allowance': 3600,
            'medical_allowance': 2400,
        },
        {
            'name': 'Senior Level',
            'base_salary': 100000,
            'house_rent_allowance': 20000,
            'transport_allowance': 4800,
            'medical_allowance': 3600,
        },
        {
            'name': 'Management Level',
            'base_salary': 150000,
            'house_rent_allowance': 30000,
            'transport_allowance': 6000,
            'medical_allowance': 6000,
        }
    ]
    
    for struct_data in structures_data:
        struct, created = SalaryStructure.objects.get_or_create(
            name=struct_data['name'],
            defaults=struct_data
        )
        if created:
            print(f"✓ Created salary structure: {struct.name}")


def create_sample_courses():
    """Create sample learning courses"""
    admin_user = User.objects.filter(role='admin').first()
    
    courses_data = [
        {
            'title': 'Python Programming Fundamentals',
            'description': 'Learn the basics of Python programming language',
            'category': 'Programming',
            'difficulty_level': 'beginner',
            'duration_hours': 40,
            'instructor': admin_user,
        },
        {
            'title': 'Project Management Essentials',
            'description': 'Essential skills for effective project management',
            'category': 'Management',
            'difficulty_level': 'intermediate',
            'duration_hours': 30,
            'instructor': admin_user,
        },
        {
            'title': 'Communication Skills Workshop',
            'description': 'Improve your professional communication skills',
            'category': 'Soft Skills',
            'difficulty_level': 'beginner',
            'duration_hours': 20,
            'instructor': admin_user,
        },
        {
            'title': 'Data Analysis with Excel',
            'description': 'Advanced Excel techniques for data analysis',
            'category': 'Data Analysis',
            'difficulty_level': 'intermediate',
            'duration_hours': 25,
            'instructor': admin_user,
        }
    ]
    
    for course_data in courses_data:
        course, created = Course.objects.get_or_create(
            title=course_data['title'],
            defaults=course_data
        )
        if created:
            print(f"✓ Created course: {course.title}")


def create_welcome_announcement():
    """Create welcome system announcement"""
    admin_user = User.objects.filter(role='admin').first()
    
    announcement, created = SystemAnnouncement.objects.get_or_create(
        title='Welcome to Office Management System',
        defaults={
            'content': '''
            Welcome to our new Office Management System! 
            
            This platform will help you manage your daily work activities including:
            - Task management and tracking
            - Attendance recording
            - Leave requests
            - Learning and development
            - Salary and payroll information
            
            If you have any questions, please contact the HR department.
            ''',
            'priority': 'medium',
            'is_published': True,
            'created_by': admin_user,
        }
    )
    
    if created:
        print("✓ Created welcome announcement")


def main():
    """Run all setup functions"""
    print("Setting up Office Management System database...")
    print("=" * 50)
    
    create_superuser()
    create_departments()
    create_positions()
    create_salary_structures()
    create_sample_courses()
    create_welcome_announcement()
    
    print("=" * 50)
    print("✓ Database setup completed successfully!")
    print("\nYou can now:")
    print("1. Access admin panel at: http://localhost:8000/admin/")
    print("2. Login with: admin@aikshetra.com / admin123")
    print("3. Start the development server: python manage.py runserver")


if __name__ == '__main__':
    main()
