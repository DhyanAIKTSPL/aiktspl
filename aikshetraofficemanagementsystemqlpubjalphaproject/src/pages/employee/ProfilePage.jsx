import React, { useState } from 'react';
import Header from '../../components/Layout/Header';
import { User, Mail, Phone, MapPin, Calendar, Briefcase, Banknote, Edit } from 'lucide-react';
import { useAuth } from '../../contexts/AuthContext';
import { faker } from '@faker-js/faker';

function ProfilePage() {
  const { user } = useAuth();
  const [isEditing, setIsEditing] = useState(false);
  const [profileData] = useState({
    name: user?.name || 'John Doe',
    email: user?.email || 'employee@aikshetra.com',
    photo: faker.image.avatar(),
    phone: faker.phone.number(),
    dob: '1990-05-15',
    address: faker.location.streetAddress(true),
    role: 'Software Engineer',
    joiningDate: '2022-01-10',
    bankAccount: faker.finance.accountNumber(),
  });

  return (
    <div className="min-h-screen bg-gray-50">
      <Header />
      
      <main className="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center mb-8">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">My Profile</h1>
            <p className="text-gray-600 mt-2">View and manage your personal information.</p>
          </div>
          <button 
            onClick={() => setIsEditing(!isEditing)}
            className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg font-medium flex items-center space-x-2"
          >
            <Edit className="h-5 w-5" />
            <span>{isEditing ? 'Save Changes' : 'Edit Profile'}</span>
          </button>
        </div>

        <div className="bg-white rounded-xl shadow-sm p-8">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div className="md:col-span-1 flex flex-col items-center">
              <img src={profileData.photo} alt="Profile" className="h-32 w-32 rounded-full mb-4" />
              <h2 className="text-2xl font-bold text-gray-900">{profileData.name}</h2>
              <p className="text-gray-600">{profileData.role}</p>
            </div>

            <div className="md:col-span-2 grid grid-cols-1 sm:grid-cols-2 gap-6">
              <div className="flex items-center space-x-3">
                <Mail className="h-5 w-5 text-gray-400" />
                <span className="text-gray-700">{profileData.email}</span>
              </div>
              <div className="flex items-center space-x-3">
                <Phone className="h-5 w-5 text-gray-400" />
                <span className="text-gray-700">{profileData.phone}</span>
              </div>
              <div className="flex items-center space-x-3">
                <Calendar className="h-5 w-5 text-gray-400" />
                <span className="text-gray-700">DOB: {profileData.dob}</span>
              </div>
              <div className="flex items-center space-x-3">
                <Briefcase className="h-5 w-5 text-gray-400" />
                <span className="text-gray-700">Joined: {profileData.joiningDate}</span>
              </div>
              <div className="flex items-center space-x-3 sm:col-span-2">
                <MapPin className="h-5 w-5 text-gray-400" />
                <span className="text-gray-700">{profileData.address}</span>
              </div>
              <div className="flex items-center space-x-3 sm:col-span-2">
                <Banknote className="h-5 w-5 text-gray-400" />
                <span className="text-gray-700">Bank Acc: {isEditing ? profileData.bankAccount : '************' + profileData.bankAccount.slice(-4)}</span>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}

export default ProfilePage;
