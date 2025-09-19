"""
Migration script to transfer data from PostgreSQL to MongoDB.
Run this script after setting up MongoDB to migrate existing data.
"""

import os
import sys
import django
from pymongo import MongoClient
import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime
import json

# Add the backend directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'office_management.settings')
django.setup()

def migrate_data():
    """Migrate data from PostgreSQL to MongoDB"""
    
    # PostgreSQL connection
    pg_config = {
        'host': os.getenv('DB_HOST', 'localhost'),
        'port': os.getenv('DB_PORT', '5432'),
        'database': os.getenv('DB_NAME', 'office_management'),
        'user': os.getenv('DB_USER', 'postgres'),
        'password': os.getenv('DB_PASSWORD', ''),
    }
    
    # MongoDB connection
    mongodb_uri = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/office_management')
    client = MongoClient(mongodb_uri)
    db_name = os.getenv('MONGODB_NAME', 'office_management')
    db = client[db_name]
    
    print("Starting data migration from PostgreSQL to MongoDB...")
    
    try:
        # Connect to PostgreSQL
        pg_conn = psycopg2.connect(**pg_config)
        pg_cursor = pg_conn.cursor(cursor_factory=RealDictCursor)
        
        # Tables to migrate (in dependency order)
        tables_to_migrate = [
            'auth_user',
            'employees_department',
            'employees_employeedetail',
            'attendance_attendancerecord',
            'attendance_leaverequest',
            'tasks_project',
            'tasks_task',
            'tasks_taskcomment',
            'salary_salarystructure',
            'salary_employeesalary',
            'salary_payroll',
            'learning_course',
            'learning_courseenrollment',
            'learning_learningpath',
            'learning_trainingsession',
            'learning_sessionattendance',
            'notifications_notification',
            'notifications_notificationpreference',
            'notifications_systemannouncement',
        ]
        
        # Mapping of PostgreSQL tables to MongoDB collections
        table_mapping = {
            'auth_user': 'accounts_user',
            'employees_department': 'employees_department',
            'employees_employeedetail': 'employees_employeedetail',
            'attendance_attendancerecord': 'attendance_attendancerecord',
            'attendance_leaverequest': 'attendance_leaverequest',
            'tasks_project': 'tasks_project',
            'tasks_task': 'tasks_task',
            'tasks_taskcomment': 'tasks_taskcomment',
            'salary_salarystructure': 'salary_salarystructure',
            'salary_employeesalary': 'salary_employeesalary',
            'salary_payroll': 'salary_payroll',
            'learning_course': 'learning_course',
            'learning_courseenrollment': 'learning_courseenrollment',
            'learning_learningpath': 'learning_learningpath',
            'learning_trainingsession': 'learning_trainingsession',
            'learning_sessionattendance': 'learning_sessionattendance',
            'notifications_notification': 'notifications_notification',
            'notifications_notificationpreference': 'notifications_notificationpreference',
            'notifications_systemannouncement': 'notifications_systemannouncement',
        }
        
        total_migrated = 0
        
        for pg_table in tables_to_migrate:
            if pg_table not in table_mapping:
                continue
                
            mongo_collection = table_mapping[pg_table]
            
            try:
                # Get data from PostgreSQL
                pg_cursor.execute(f"SELECT * FROM {pg_table}")
                rows = pg_cursor.fetchall()
                
                if not rows:
                    print(f"  ✓ {pg_table}: No data to migrate")
                    continue
                
                # Convert rows to MongoDB documents
                documents = []
                for row in rows:
                    doc = dict(row)
                    
                    # Convert datetime objects to ISO format
                    for key, value in doc.items():
                        if isinstance(value, datetime):
                            doc[key] = value.isoformat()
                    
                    # Handle foreign key conversions for MongoDB
                    doc = convert_foreign_keys(doc, pg_table)
                    
                    documents.append(doc)
                
                # Insert into MongoDB
                collection = db[mongo_collection]
                if documents:
                    collection.insert_many(documents)
                    total_migrated += len(documents)
                    print(f"  ✓ {pg_table} → {mongo_collection}: {len(documents)} records")
                
            except Exception as e:
                print(f"  ✗ Error migrating {pg_table}: {e}")
        
        print(f"\n✅ Migration completed! Total records migrated: {total_migrated}")
        
    except Exception as e:
        print(f"❌ Migration failed: {e}")
    
    finally:
        if 'pg_conn' in locals():
            pg_conn.close()
        client.close()

def convert_foreign_keys(doc, table_name):
    """Convert foreign key fields to ObjectId references"""
    
    # Mapping of foreign key fields to their new names
    fk_mappings = {
        'employees_employeedetail': {
            'user_id': 'user_id',
            'department_id': 'department_id',
        },
        'attendance_attendancerecord': {
            'user_id': 'user_id',
            'approved_by_id': 'approved_by_id',
        },
        'attendance_leaverequest': {
            'user_id': 'user_id',
            'approved_by_id': 'approved_by_id',
        },
        'tasks_project': {
            'manager_id': 'manager_id',
        },
        'tasks_task': {
            'project_id': 'project_id',
            'assigned_to_id': 'assigned_to_id',
            'assigned_by_id': 'assigned_by_id',
        },
        'tasks_taskcomment': {
            'task_id': 'task_id',
            'user_id': 'user_id',
        },
        'salary_employeesalary': {
            'user_id': 'user_id',
            'salary_structure_id': 'salary_structure_id',
        },
        'salary_payroll': {
            'user_id': 'user_id',
            'processed_by_id': 'processed_by_id',
        },
        'learning_course': {
            'instructor_id': 'instructor_id',
        },
        'learning_courseenrollment': {
            'user_id': 'user_id',
            'course_id': 'course_id',
        },
        'learning_trainingsession': {
            'course_id': 'course_id',
            'instructor_id': 'instructor_id',
        },
        'learning_sessionattendance': {
            'session_id': 'session_id',
            'user_id': 'user_id',
        },
        'notifications_notification': {
            'recipient_id': 'recipient_id',
        },
        'notifications_notificationpreference': {
            'user_id': 'user_id',
        },
        'notifications_systemannouncement': {
            'created_by_id': 'created_by_id',
        },
    }
    
    if table_name in fk_mappings:
        for old_field, new_field in fk_mappings[table_name].items():
            if old_field in doc and doc[old_field] is not None:
                # Convert to string representation of ObjectId
                doc[new_field] = str(doc[old_field])
                if old_field != new_field:
                    del doc[old_field]
    
    return doc

if __name__ == "__main__":
    migrate_data()
