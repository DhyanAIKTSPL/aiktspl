"""
Test script to verify MongoDB integration with Django models.
Tests basic CRUD operations and model relationships.
"""

import os
import sys
import django
from pymongo import MongoClient
from datetime import datetime, date, time
import traceback

# Add the backend directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'office_management.settings')
django.setup()

# Import models after Django setup
from accounts.models import User
from employees.models import Department, EmployeeDetail
from attendance.models import AttendanceRecord, LeaveRequest
from tasks.models import Project, Task, TaskComment
from salary.models import SalaryStructure, EmployeeSalary, Payroll
from learning.models import Course, CourseEnrollment, TrainingSession
from notifications.models import Notification, NotificationPreference, SystemAnnouncement

def test_mongodb_connection():
    """Test MongoDB connection"""
    print("🔍 Testing MongoDB Connection...")
    
    try:
        mongodb_uri = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/office_management')
        client = MongoClient(mongodb_uri)
        db_name = os.getenv('MONGODB_NAME', 'office_management')
        db = client[db_name]
        
        # Test connection
        server_info = client.server_info()
        print(f"  ✅ Connected to MongoDB {server_info['version']}")
        print(f"  ✅ Database: {db_name}")
        
        # List collections
        collections = db.list_collection_names()
        print(f"  ✅ Collections available: {len(collections)}")
        
        client.close()
        return True
        
    except Exception as e:
        print(f"  ❌ MongoDB connection failed: {e}")
        return False

def test_user_model():
    """Test User model CRUD operations"""
    print("\n👤 Testing User Model...")
    
    try:
        # Create test user
        user = User.objects.create(
            username='testuser',
            email='test@example.com',
            first_name='Test',
            last_name='User',
            role='employee'
        )
        print(f"  ✅ Created user: {user}")
        
        # Read user
        retrieved_user = User.objects.get(username='testuser')
        print(f"  ✅ Retrieved user: {retrieved_user}")
        
        # Update user
        retrieved_user.first_name = 'Updated'
        retrieved_user.save()
        print(f"  ✅ Updated user: {retrieved_user}")
        
        # Delete user
        user_id = retrieved_user.id
        retrieved_user.delete()
        print(f"  ✅ Deleted user with ID: {user_id}")
        
        return True
        
    except Exception as e:
        print(f"  ❌ User model test failed: {e}")
        traceback.print_exc()
        return False

def test_department_and_employee():
    """Test Department and EmployeeDetail models"""
    print("\n🏢 Testing Department and Employee Models...")
    
    try:
        # Create user first
        user = User.objects.create(
            username='employee1',
            email='employee1@example.com',
            first_name='John',
            last_name='Doe',
            role='employee'
        )
        
        # Create department
        department = Department.objects.create(
            name='Engineering',
            description='Software Development Team',
            head_id=str(user.id)
        )
        print(f"  ✅ Created department: {department}")
        
        # Create employee detail
        employee = EmployeeDetail.objects.create(
            user_id=str(user.id),
            employee_id='EMP001',
            department_id=str(department.id),
            position='Software Developer',
            hire_date=date.today(),
            salary=75000.00
        )
        print(f"  ✅ Created employee: {employee}")
        
        # Test relationships
        dept_head = department.get_head()
        emp_user = employee.get_user()
        emp_dept = employee.get_department()
        
        print(f"  ✅ Department head: {dept_head}")
        print(f"  ✅ Employee user: {emp_user}")
        print(f"  ✅ Employee department: {emp_dept}")
        
        # Cleanup
        employee.delete()
        department.delete()
        user.delete()
        
        return True
        
    except Exception as e:
        print(f"  ❌ Department/Employee test failed: {e}")
        traceback.print_exc()
        return False

def test_attendance_models():
    """Test Attendance models"""
    print("\n📅 Testing Attendance Models...")
    
    try:
        # Create user
        user = User.objects.create(
            username='attendanceuser',
            email='attendance@example.com',
            first_name='Jane',
            last_name='Smith',
            role='employee'
        )
        
        # Create attendance record
        attendance = AttendanceRecord.objects.create(
            user_id=str(user.id),
            date=date.today(),
            check_in_time=time(9, 0),
            check_out_time=time(17, 30),
            status='present',
            hours_worked=8.5
        )
        print(f"  ✅ Created attendance record: {attendance}")
        
        # Create leave request
        leave_request = LeaveRequest.objects.create(
            user_id=str(user.id),
            leave_type='vacation',
            start_date=date.today(),
            end_date=date.today(),
            reason='Personal vacation'
        )
        print(f"  ✅ Created leave request: {leave_request}")
        
        # Test methods
        duration = leave_request.duration_days
        print(f"  ✅ Leave duration: {duration} days")
        
        # Cleanup
        attendance.delete()
        leave_request.delete()
        user.delete()
        
        return True
        
    except Exception as e:
        print(f"  ❌ Attendance models test failed: {e}")
        traceback.print_exc()
        return False

def test_task_models():
    """Test Task management models"""
    print("\n📋 Testing Task Models...")
    
    try:
        # Create users
        manager = User.objects.create(
            username='manager1',
            email='manager@example.com',
            first_name='Manager',
            last_name='One',
            role='manager'
        )
        
        employee = User.objects.create(
            username='taskemployee',
            email='taskemployee@example.com',
            first_name='Task',
            last_name='Employee',
            role='employee'
        )
        
        # Create project
        project = Project.objects.create(
            name='Test Project',
            description='A test project',
            manager_id=str(manager.id),
            start_date=date.today(),
            end_date=date.today(),
            status='active'
        )
        print(f"  ✅ Created project: {project}")
        
        # Create task
        task = Task.objects.create(
            title='Test Task',
            description='A test task',
            project_id=str(project.id),
            assigned_to_id=str(employee.id),
            assigned_by_id=str(manager.id),
            due_date=datetime.now(),
            status='todo',
            estimated_hours=8.0
        )
        print(f"  ✅ Created task: {task}")
        
        # Create task comment
        comment = TaskComment.objects.create(
            task_id=str(task.id),
            user_id=str(manager.id),
            comment='This is a test comment'
        )
        print(f"  ✅ Created task comment: {comment}")
        
        # Test relationships
        task_project = task.get_project()
        task_assignee = task.get_assigned_to()
        print(f"  ✅ Task project: {task_project}")
        print(f"  ✅ Task assignee: {task_assignee}")
        
        # Cleanup
        comment.delete()
        task.delete()
        project.delete()
        manager.delete()
        employee.delete()
        
        return True
        
    except Exception as e:
        print(f"  ❌ Task models test failed: {e}")
        traceback.print_exc()
        return False

def test_notification_models():
    """Test Notification models"""
    print("\n🔔 Testing Notification Models...")
    
    try:
        # Create user
        user = User.objects.create(
            username='notifuser',
            email='notif@example.com',
            first_name='Notification',
            last_name='User',
            role='employee'
        )
        
        # Create notification
        notification = Notification.objects.create(
            recipient_id=str(user.id),
            title='Test Notification',
            message='This is a test notification',
            notification_type='info'
        )
        print(f"  ✅ Created notification: {notification}")
        
        # Create notification preference
        preference = NotificationPreference.objects.create(
            user_id=str(user.id),
            email_enabled=True,
            push_enabled=False
        )
        print(f"  ✅ Created notification preference: {preference}")
        
        # Create system announcement
        announcement = SystemAnnouncement.objects.create(
            title='System Maintenance',
            content='The system will be under maintenance',
            priority='high',
            created_by_id=str(user.id)
        )
        print(f"  ✅ Created system announcement: {announcement}")
        
        # Test methods
        notification.mark_as_read()
        print(f"  ✅ Marked notification as read: {notification.is_read}")
        
        should_send = preference.should_send_notification('info', 'email')
        print(f"  ✅ Should send email notification: {should_send}")
        
        # Cleanup
        notification.delete()
        preference.delete()
        announcement.delete()
        user.delete()
        
        return True
        
    except Exception as e:
        print(f"  ❌ Notification models test failed: {e}")
        traceback.print_exc()
        return False

def run_all_tests():
    """Run all MongoDB integration tests"""
    print("🚀 Starting MongoDB Integration Tests")
    print("=" * 50)
    
    tests = [
        test_mongodb_connection,
        test_user_model,
        test_department_and_employee,
        test_attendance_models,
        test_task_models,
        test_notification_models,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            if test():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"  ❌ Test {test.__name__} crashed: {e}")
            failed += 1
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed} passed, {failed} failed")
    
    if failed == 0:
        print("🎉 All tests passed! MongoDB integration is working correctly.")
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
    
    return failed == 0

if __name__ == "__main__":
    run_all_tests()
