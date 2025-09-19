import React from 'react';
import Header from '../../components/Layout/Header';
import { DollarSign, Send, Download } from 'lucide-react';
import { faker } from '@faker-js/faker';

function AdminSalaryPage() {
  const employees = Array.from({ length: 8 }, () => ({
    id: faker.string.uuid(),
    name: faker.person.fullName(),
    avatar: faker.image.avatar(),
    salary: faker.finance.amount(3000, 8000, 2, '$'),
    lastPaid: 'Dec 2024',
    status: faker.helpers.arrayElement(['Paid', 'Pending']),
  }));

  return (
    <div className="min-h-screen bg-gray-50">
      <Header />
      
      <main className="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center mb-8">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">Salary Management</h1>
            <p className="text-gray-600 mt-2">Manage and distribute employee salaries.</p>
          </div>
          <button className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg font-medium flex items-center space-x-2">
            <Send className="h-5 w-5" />
            <span>Pay All Pending</span>
          </button>
        </div>

        <div className="bg-white rounded-xl shadow-sm overflow-hidden">
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead className="bg-gray-50">
                <tr className="border-b border-gray-200">
                  <th className="text-left py-3 px-4 font-medium text-gray-700">Employee</th>
                  <th className="text-left py-3 px-4 font-medium text-gray-700">Salary</th>
                  <th className="text-left py-3 px-4 font-medium text-gray-700">Last Paid</th>
                  <th className="text-left py-3 px-4 font-medium text-gray-700">Status</th>
                  <th className="text-left py-3 px-4 font-medium text-gray-700">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-200">
                {employees.map((employee) => (
                  <tr key={employee.id}>
                    <td className="py-3 px-4">
                      <div className="flex items-center space-x-3">
                        <img src={employee.avatar} alt={employee.name} className="h-10 w-10 rounded-full" />
                        <span className="font-medium text-gray-900">{employee.name}</span>
                      </div>
                    </td>
                    <td className="py-3 px-4 text-gray-700">{employee.salary}</td>
                    <td className="py-3 px-4 text-gray-700">{employee.lastPaid}</td>
                    <td className="py-3 px-4">
                       <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                        employee.status === 'Paid' ? 'bg-green-100 text-green-700' : 'bg-yellow-100 text-yellow-700'
                      }`}>
                        {employee.status}
                      </span>
                    </td>
                    <td className="py-3 px-4">
                      <div className="flex space-x-2">
                        <button className="text-blue-600 hover:text-blue-800"><DollarSign className="h-5 w-5" /></button>
                        <button className="text-gray-500 hover:text-gray-700"><Download className="h-5 w-5" /></button>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </main>
    </div>
  );
}

export default AdminSalaryPage;
