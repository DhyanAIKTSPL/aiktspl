"""
MongoDB setup script for Office Management System.
Creates necessary collections and indexes for optimal performance.
"""

import os
import sys
import django
from pymongo import MongoClient, ASCENDING, DESCENDING
from pymongo.errors import CollectionInvalid

# Add the backend directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'office_management.settings')
django.setup()

def setup_mongodb():
    """Setup MongoDB collections and indexes"""
    
    # MongoDB connection
    mongodb_uri = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/office_management')
    client = MongoClient(mongodb_uri)
    db_name = os.getenv('MONGODB_NAME', 'office_management')
    db = client[db_name]
    
    print(f"Setting up MongoDB database: {db_name}")
    
    # Collections to create with their indexes
    collections_config = {
        'accounts_user': [
            ('email', ASCENDING),
            ('username', ASCENDING),
            ('is_active', ASCENDING),
            ('role', ASCENDING),
            ('created_at', DESCENDING),
        ],
        'employees_employeedetail': [
            ('user_id', ASCENDING),
            ('employee_id', ASCENDING),
            ('department_id', ASCENDING),
            ('is_active', ASCENDING),
        ],
        'employees_department': [
            ('name', ASCENDING),
            ('is_active', ASCENDING),
        ],
        'attendance_attendancerecord': [
            ('user_id', ASCENDING),
            ('date', DESCENDING),
            ('status', ASCENDING),
            [('user_id', ASCENDING), ('date', DESCENDING)],  # Compound index
        ],
        'attendance_leaverequest': [
            ('user_id', ASCENDING),
            ('status', ASCENDING),
            ('start_date', DESCENDING),
            ('created_at', DESCENDING),
        ],
        'tasks_project': [
            ('manager_id', ASCENDING),
            ('status', ASCENDING),
            ('priority', ASCENDING),
            ('end_date', ASCENDING),
            ('created_at', DESCENDING),
        ],
        'tasks_task': [
            ('assigned_to_id', ASCENDING),
            ('project_id', ASCENDING),
            ('status', ASCENDING),
            ('priority', ASCENDING),
            ('due_date', ASCENDING),
            ('created_at', DESCENDING),
        ],
        'tasks_taskcomment': [
            ('task_id', ASCENDING),
            ('user_id', ASCENDING),
            ('created_at', DESCENDING),
        ],
        'salary_salarystructure': [
            ('name', ASCENDING),
            ('is_active', ASCENDING),
        ],
        'salary_employeesalary': [
            ('user_id', ASCENDING),
            ('is_active', ASCENDING),
            ('effective_from', DESCENDING),
        ],
        'salary_payroll': [
            ('user_id', ASCENDING),
            ('year', DESCENDING),
            ('month', DESCENDING),
            ('status', ASCENDING),
            [('user_id', ASCENDING), ('year', DESCENDING), ('month', DESCENDING)],  # Compound index
        ],
        'learning_course': [
            ('instructor_id', ASCENDING),
            ('category', ASCENDING),
            ('status', ASCENDING),
            ('difficulty_level', ASCENDING),
            ('created_at', DESCENDING),
        ],
        'learning_courseenrollment': [
            ('user_id', ASCENDING),
            ('course_id', ASCENDING),
            ('status', ASCENDING),
            ('enrolled_at', DESCENDING),
            [('user_id', ASCENDING), ('course_id', ASCENDING)],  # Compound index
        ],
        'learning_learningpath': [
            ('is_active', ASCENDING),
            ('is_mandatory', ASCENDING),
            ('name', ASCENDING),
        ],
        'learning_trainingsession': [
            ('instructor_id', ASCENDING),
            ('course_id', ASCENDING),
            ('status', ASCENDING),
            ('start_datetime', ASCENDING),
        ],
        'learning_sessionattendance': [
            ('session_id', ASCENDING),
            ('user_id', ASCENDING),
            ('status', ASCENDING),
            [('session_id', ASCENDING), ('user_id', ASCENDING)],  # Compound index
        ],
        'notifications_notification': [
            ('recipient_id', ASCENDING),
            ('is_read', ASCENDING),
            ('notification_type', ASCENDING),
            ('created_at', DESCENDING),
            [('recipient_id', ASCENDING), ('is_read', ASCENDING)],  # Compound index
        ],
        'notifications_notificationpreference': [
            ('user_id', ASCENDING),
        ],
        'notifications_systemannouncement': [
            ('is_active', ASCENDING),
            ('is_published', ASCENDING),
            ('priority', ASCENDING),
            ('publish_at', ASCENDING),
            ('expire_at', ASCENDING),
            ('created_at', DESCENDING),
        ],
    }
    
    # Create collections and indexes
    for collection_name, indexes in collections_config.items():
        print(f"Setting up collection: {collection_name}")
        
        # Create collection if it doesn't exist
        try:
            db.create_collection(collection_name)
            print(f"  ✓ Created collection: {collection_name}")
        except CollectionInvalid:
            print(f"  ✓ Collection already exists: {collection_name}")
        
        collection = db[collection_name]
        
        # Create indexes
        for index in indexes:
            try:
                if isinstance(index, list):
                    # Compound index
                    collection.create_index(index)
                    index_name = "_".join([f"{field}_{direction}" for field, direction in index])
                    print(f"    ✓ Created compound index: {index_name}")
                else:
                    # Single field index
                    field, direction = index
                    collection.create_index([(field, direction)])
                    print(f"    ✓ Created index: {field}_{direction}")
            except Exception as e:
                print(f"    ⚠ Index creation failed for {index}: {e}")
    
    print("\n✅ MongoDB setup completed successfully!")
    print(f"Database: {db_name}")
    print(f"Collections created: {len(collections_config)}")
    
    # Display collection stats
    print("\nCollection Statistics:")
    for collection_name in collections_config.keys():
        count = db[collection_name].count_documents({})
        print(f"  {collection_name}: {count} documents")
    
    client.close()

if __name__ == "__main__":
    setup_mongodb()
