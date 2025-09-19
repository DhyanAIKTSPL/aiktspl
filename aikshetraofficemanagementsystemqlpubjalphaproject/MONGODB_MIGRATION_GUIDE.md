# MongoDB Migration Guide

This guide explains how to migrate the Office Management System from PostgreSQL to MongoDB using djongo.

## Prerequisites

1. **MongoDB Installation**
   \`\`\`bash
   # Install MongoDB Community Edition
   # Follow official MongoDB installation guide for your OS
   # https://docs.mongodb.com/manual/installation/
   \`\`\`

2. **Python Dependencies**
   \`\`\`bash
   pip install djongo pymongo psycopg2-binary
   \`\`\`

## Migration Steps

### 1. Update Environment Configuration

Copy the new environment template:
\`\`\`bash
cp backend/.env.example backend/.env
\`\`\`

Update your `.env` file with MongoDB settings:
\`\`\`env
# MongoDB Configuration
MONGODB_URI=mongodb://localhost:27017/office_management
MONGODB_NAME=office_management
\`\`\`

### 2. Setup MongoDB Database

Run the MongoDB setup script:
\`\`\`bash
cd scripts
python setup_mongodb.py
\`\`\`

This script will:
- Create necessary collections
- Set up indexes for optimal performance
- Display collection statistics

### 3. Migrate Existing Data (Optional)

If you have existing PostgreSQL data to migrate:

\`\`\`bash
cd scripts
python migrate_to_mongodb.py
\`\`\`

This script will:
- Connect to your existing PostgreSQL database
- Transfer all data to MongoDB
- Convert foreign key relationships
- Handle data type conversions

### 4. Test the Integration

Verify everything is working:
\`\`\`bash
cd scripts
python test_mongodb_integration.py
\`\`\`

This will run comprehensive tests on:
- MongoDB connection
- Model CRUD operations
- Relationship handling
- Custom methods and properties

### 5. Update Django Settings

The Django settings have been automatically updated to use djongo as the database engine. Key changes:

\`\`\`python
DATABASES = {
    'default': {
        'ENGINE': 'djongo',
        'NAME': os.getenv('MONGODB_NAME', 'office_management'),
        'CLIENT': {
            'host': os.getenv('MONGODB_URI', 'mongodb://localhost:27017'),
        }
    }
}
\`\`\`

## Model Changes

All models have been updated to be MongoDB-compatible:

### Foreign Key Handling
- Foreign keys are now stored as string ObjectIds
- Helper methods added to retrieve related objects
- Example:
  \`\`\`python
  # Old PostgreSQL way
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  
  # New MongoDB way
  user_id = models.CharField(max_length=24, help_text="ObjectId reference to User")
  
  def get_user(self):
      return User.objects.get(id=self.user_id)
  \`\`\`

### Many-to-Many Relationships
- Converted to JSONField storing lists of ObjectIds
- Helper methods for retrieving related objects
- Example:
  \`\`\`python
  # Old way
  team_members = models.ManyToManyField(User)
  
  # New way
  team_member_ids = djongo_models.JSONField(default=list)
  
  def get_team_members(self):
      return User.objects.filter(id__in=self.team_member_ids)
  \`\`\`

### JSON Fields
- PostgreSQL JSONField replaced with djongo JSONField
- Maintains same functionality and API

## Performance Considerations

### Indexes Created
The setup script creates indexes on commonly queried fields:
- User email, username, role
- Attendance records by user and date
- Tasks by assignee and due date
- Notifications by recipient and read status

### Query Optimization
- Use `select_related()` equivalent patterns with helper methods
- Consider denormalization for frequently accessed data
- Use MongoDB aggregation pipeline for complex queries

## Troubleshooting

### Common Issues

1. **Connection Errors**
   - Ensure MongoDB is running: `sudo systemctl start mongod`
   - Check MongoDB URI in environment variables
   - Verify network connectivity

2. **Migration Errors**
   - Ensure PostgreSQL credentials are correct
   - Check that all required tables exist
   - Verify data types are compatible

3. **Model Errors**
   - Clear Django migrations: `rm */migrations/0*.py`
   - Create new migrations: `python manage.py makemigrations`
   - Apply migrations: `python manage.py migrate`

### Rollback Plan

If you need to rollback to PostgreSQL:

1. Restore original settings.py
2. Restore original model files
3. Update .env with PostgreSQL settings
4. Run PostgreSQL migrations

## Performance Monitoring

Monitor your MongoDB performance:

\`\`\`bash
# MongoDB shell
mongo office_management

# Check collection stats
db.stats()

# Monitor slow queries
db.setProfilingLevel(2)
db.system.profile.find().sort({ts: -1}).limit(5)
\`\`\`

## Next Steps

1. **Test thoroughly** in development environment
2. **Backup data** before production migration
3. **Monitor performance** after migration
4. **Update documentation** for your team
5. **Consider MongoDB-specific optimizations**

## Support

If you encounter issues:
1. Check the test script output for specific errors
2. Review MongoDB logs: `tail -f /var/log/mongodb/mongod.log`
3. Consult djongo documentation: https://djongo.readthedocs.io/
4. MongoDB documentation: https://docs.mongodb.com/
