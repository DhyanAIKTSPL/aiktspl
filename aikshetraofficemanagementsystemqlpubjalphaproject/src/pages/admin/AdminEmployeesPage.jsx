import React, { useState, useEffect } from 'react';
import { UserPlus, MoreVertical, Loader, Users, User, Briefcase } from 'lucide-react';
import { faker } from '@faker-js/faker';
import EmployeeProfileModal from '../../components/admin/EmployeeProfileModal';
import { motion } from 'framer-motion';

function AdminEmployeesPage() {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState('all');
  const [selectedUser, setSelectedUser] = useState(null);
  const [isModalOpen, setIsModalOpen] = useState(false);

  useEffect(() => {
    const fetchUsers = () => {
      return new Promise(resolve => {
        setTimeout(() => {
          const fakeUsers = Array.from({ length: 20 }, () => ({
            id: faker.string.uuid(),
            name: faker.person.fullName(),
            email: faker.internet.email(),
            roleType: faker.helpers.arrayElement(['employee', 'trainee']),
            jobTitle: faker.person.jobTitle(),
            status: faker.helpers.arrayElement(['Active', 'On Leave']),
            joinDate: faker.date.past({ years: 2 }).toLocaleDateString(),
            avatar: faker.image.avatar(),
            phone: faker.phone.number(),
            address: faker.location.streetAddress(true),
            dob: faker.date.birthdate().toLocaleDateString(),
          }));
          resolve(fakeUsers);
        }, 1000);
      });
    };

    setLoading(true);
    fetchUsers().then(data => {
      setUsers(data);
      setLoading(false);
    });
  }, []);

  const handleUserClick = (user) => {
    setSelectedUser(user);
    setIsModalOpen(true);
  };

  const filteredUsers = users.filter(user => {
    if (activeTab === 'all') return true;
    return user.roleType === activeTab;
  });

  const tabs = [
    { id: 'all', label: 'All Users', icon: Users },
    { id: 'employee', label: 'Employees', icon: Briefcase },
    { id: 'trainee', label: 'Trainees', icon: User },
  ];

  return (
    <>
      <div className="flex flex-col md:flex-row justify-between items-center mb-8">
        <div>
          <h1 className="text-3xl font-bold text-text-primary">User Management</h1>
          <p className="text-text-secondary mt-2">View, add, and manage all employees and trainees.</p>
        </div>
        <button className="bg-primary hover:bg-primary-hover text-white px-4 py-2 rounded-lg font-medium flex items-center space-x-2 mt-4 md:mt-0">
          <UserPlus className="h-5 w-5" />
          <span>Add User</span>
        </button>
      </div>

      <div className="border-b border-border mb-6">
        <nav className="-mb-px flex space-x-8" aria-label="Tabs">
          {tabs.map((tab) => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm flex items-center space-x-2 transition-colors ${
                activeTab === tab.id
                  ? 'border-primary text-primary'
                  : 'border-transparent text-text-secondary hover:text-text-primary hover:border-gray-600'
              }`}
            >
              <tab.icon className="h-5 w-5" />
              <span>{tab.label}</span>
            </button>
          ))}
        </nav>
      </div>

      <div className="bg-surface rounded-xl shadow-lg border border-border overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead className="bg-background">
              <tr className="border-b border-border">
                <th className="text-left py-3 px-4 font-medium text-text-secondary">Name</th>
                <th className="text-left py-3 px-4 font-medium text-text-secondary">Role</th>
                <th className="text-left py-3 px-4 font-medium text-text-secondary">Status</th>
                <th className="text-left py-3 px-4 font-medium text-text-secondary">Join Date</th>
                <th className="text-left py-3 px-4 font-medium text-text-secondary">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-border">
              {loading ? (
                <tr>
                  <td colSpan="5" className="text-center py-8">
                    <div className="flex justify-center items-center">
                      <Loader className="animate-spin h-8 w-8 text-primary" />
                      <span className="ml-4 text-text-secondary">Loading Users...</span>
                    </div>
                  </td>
                </tr>
              ) : (
                filteredUsers.map((user) => (
                  <tr key={user.id} className="hover:bg-background cursor-pointer" onClick={() => handleUserClick(user)}>
                    <td className="py-3 px-4">
                      <div className="flex items-center space-x-3">
                        <img src={user.avatar} alt={user.name} className="h-10 w-10 rounded-full" />
                        <div>
                          <p className="font-medium text-text-primary">{user.name}</p>
                          <p className="text-sm text-text-secondary">{user.email}</p>
                        </div>
                      </div>
                    </td>
                    <td className="py-3 px-4 text-text-secondary capitalize">{user.roleType === 'employee' ? user.jobTitle : 'Trainee'}</td>
                    <td className="py-3 px-4">
                      <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                        user.status === 'Active' ? 'bg-green-900/50 text-green-300' : 'bg-yellow-900/50 text-yellow-300'
                      }`}>
                        {user.status}
                      </span>
                    </td>
                    <td className="py-3 px-4 text-text-secondary">{user.joinDate}</td>
                    <td className="py-3 px-4">
                      <button onClick={(e) => { e.stopPropagation(); alert('Actions clicked for ' + user.name); }} className="text-text-secondary hover:text-text-primary">
                        <MoreVertical className="h-5 w-5" />
                      </button>
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </div>
      {selectedUser && (
        <EmployeeProfileModal 
          user={selectedUser} 
          isOpen={isModalOpen} 
          onClose={() => setIsModalOpen(false)} 
        />
      )}
    </>
  );
}

export default AdminEmployeesPage;
