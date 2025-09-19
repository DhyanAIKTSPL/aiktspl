import React from 'react';
import { Check, X, User, Mail, Phone } from 'lucide-react';
import { faker } from '@faker-js/faker';

function LoginApprovalPage() {
  const pendingApprovals = Array.from({ length: 3 }, () => ({
    id: faker.string.uuid(),
    name: faker.person.fullName(),
    email: faker.internet.email(),
    phone: faker.phone.number(),
    avatar: faker.image.avatar(),
    role: faker.helpers.arrayElement(['Employee', 'Trainee']),
    date: faker.date.recent().toLocaleDateString(),
  }));

  return (
    <>
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-text-primary">Login Approvals</h1>
        <p className="text-text-secondary mt-2">Review and approve new user registrations.</p>
      </div>

      <div className="space-y-6">
        {pendingApprovals.length > 0 ? (
          pendingApprovals.map((user) => (
            <div key={user.id} className="bg-surface rounded-xl shadow-lg border border-border p-6">
              <div className="flex flex-col md:flex-row md:items-center md:justify-between">
                <div className="flex items-center space-x-4">
                  <img src={user.avatar} alt={user.name} className="h-16 w-16 rounded-full" />
                  <div>
                    <p className="text-lg font-bold text-text-primary">{user.name}</p>
                    <p className="text-sm text-text-secondary">Applied on: {user.date}</p>
                  </div>
                </div>
                <div className="mt-4 md:mt-0 flex space-x-4">
                  <button className="flex-1 w-full md:w-auto bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded-lg font-medium flex items-center justify-center space-x-2">
                    <Check className="h-5 w-5" />
                    <span>Approve</span>
                  </button>
                  <button className="flex-1 w-full md:w-auto bg-red-600 hover:bg-red-700 text-white px-4 py-2 rounded-lg font-medium flex items-center justify-center space-x-2">
                    <X className="h-5 w-5" />
                    <span>Reject</span>
                  </button>
                </div>
              </div>
              <div className="border-t border-border mt-4 pt-4 grid grid-cols-1 sm:grid-cols-3 gap-4 text-sm">
                <div className="flex items-center space-x-2 text-text-secondary">
                  <User className="h-4 w-4" />
                  <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                      user.role === 'Employee' ? 'bg-blue-900/50 text-blue-300' : 'bg-purple-900/50 text-purple-300'
                    }`}>{user.role}</span>
                </div>
                <div className="flex items-center space-x-2 text-text-secondary">
                  <Mail className="h-4 w-4" />
                  <span>{user.email}</span>
                </div>
                <div className="flex items-center space-x-2 text-text-secondary">
                  <Phone className="h-4 w-4" />
                  <span>{user.phone}</span>
                </div>
              </div>
            </div>
          ))
        ) : (
          <div className="text-center p-8 bg-surface rounded-xl shadow-lg border border-border">
            <Check className="h-12 w-12 text-green-500 mx-auto mb-4" />
            <h3 className="text-xl font-semibold text-text-primary">All Clear!</h3>
            <p className="text-text-secondary mt-2">There are no pending registration approvals.</p>
          </div>
        )}
      </div>
    </>
  );
}

export default LoginApprovalPage;
