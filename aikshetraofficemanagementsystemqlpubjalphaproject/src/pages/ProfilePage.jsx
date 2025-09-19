import React, { useState } from 'react';
import { User, Mail, Phone, MapPin, Calendar, Briefcase, Banknote, Edit } from 'lucide-react';
import { useAuth } from '../contexts/AuthContext';
import { faker } from '@faker-js/faker';
import { motion } from 'framer-motion';

function ProfilePage() {
  const { user } = useAuth();
  const [isEditing, setIsEditing] = useState(false);

  const getRoleDisplay = (role) => {
    switch (role) {
      case 'admin':
        return 'Administrator';
      case 'employee':
        return 'Software Engineer'; // Example role
      case 'trainee':
        return 'Trainee';
      default:
        return 'User';
    }
  };

  const [profileData] = useState({
    name: user?.name || 'User',
    email: user?.email || 'user@aikshetra.com',
    photo: faker.image.avatar(),
    phone: faker.phone.number(),
    dob: '1990-05-15',
    address: faker.location.streetAddress(true),
    role: getRoleDisplay(user?.role),
    joiningDate: '2022-01-10',
    bankAccount: faker.finance.accountNumber(),
  });

  const handleEditToggle = () => {
    if (isEditing) {
      // In a real app, you would save the updated data here.
      alert('Profile changes saved!');
    }
    setIsEditing(!isEditing);
  };

  return (
    <>
      <div className="flex flex-col md:flex-row justify-between items-center mb-8">
        <div>
          <h1 className="text-3xl font-bold text-text-primary">My Profile</h1>
          <p className="text-text-secondary mt-2">View and manage your personal information.</p>
        </div>
        <button 
          onClick={handleEditToggle}
          className="bg-primary hover:bg-primary-hover text-white px-4 py-2 rounded-lg font-medium flex items-center space-x-2 mt-4 md:mt-0"
        >
          <Edit className="h-5 w-5" />
          <span>{isEditing ? 'Save Changes' : 'Edit Profile'}</span>
        </button>
      </div>

      <motion.div 
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
        className="bg-surface rounded-xl shadow-lg border border-border p-8"
      >
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div className="md:col-span-1 flex flex-col items-center text-center">
            <img src={profileData.photo} alt="Profile" className="h-32 w-32 rounded-full mb-4 border-4 border-primary" />
            <h2 className="text-2xl font-bold text-text-primary">{profileData.name}</h2>
            <p className="text-primary capitalize">{user?.role}</p>
          </div>

          <div className="md:col-span-2 grid grid-cols-1 sm:grid-cols-2 gap-6 border-t md:border-t-0 md:border-l border-border pt-6 md:pt-0 md:pl-6">
            <div className="flex items-center space-x-3">
              <Mail className="h-5 w-5 text-primary" />
              <span className="text-text-secondary break-all">{profileData.email}</span>
            </div>
            <div className="flex items-center space-x-3">
              <Phone className="h-5 w-5 text-primary" />
              <span className="text-text-secondary">{profileData.phone}</span>
            </div>
            <div className="flex items-center space-x-3">
              <Calendar className="h-5 w-5 text-primary" />
              <span className="text-text-secondary">DOB: {profileData.dob}</span>
            </div>
            <div className="flex items-center space-x-3">
              <Briefcase className="h-5 w-5 text-primary" />
              <span className="text-text-secondary">Joined: {profileData.joiningDate}</span>
            </div>
            <div className="flex items-start space-x-3 sm:col-span-2">
              <MapPin className="h-5 w-5 text-primary mt-1" />
              <span className="text-text-secondary">{profileData.address}</span>
            </div>
            <div className="flex items-center space-x-3 sm:col-span-2">
              <Banknote className="h-5 w-5 text-primary" />
              <span className="text-text-secondary">Bank Acc: {isEditing ? profileData.bankAccount : '************' + profileData.bankAccount.slice(-4)}</span>
            </div>
          </div>
        </div>
      </motion.div>
    </>
  );
}

export default ProfilePage;
