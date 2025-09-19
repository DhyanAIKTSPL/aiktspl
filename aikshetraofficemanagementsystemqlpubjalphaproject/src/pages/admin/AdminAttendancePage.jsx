import React from 'react';
import Header from '../../components/Layout/Header';
import { Calendar, Check, X, AlertTriangle } from 'lucide-react';
import { faker } from '@faker-js/faker';

function AdminAttendancePage() {
  const attendanceData = Array.from({ length: 10 }, () => ({
    id: faker.string.uuid(),
    name: faker.person.fullName(),
    avatar: faker.image.avatar(),
    checkIn: '9:00 AM',
    checkOut: '6:00 PM',
    status: faker.helpers.arrayElement(['Present', 'Late', 'Absent']),
  }));

  const leaveRequests = Array.from({ length: 3 }, () => ({
    id: faker.string.uuid(),
    name: faker.person.fullName(),
    dates: 'Jan 20 - Jan 22, 2025',
    reason: faker.lorem.sentence(),
  }));

  return (
    <div className="min-h-screen bg-gray-50">
      <Header />
      
      <main className="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">Employee Attendance</h1>
          <p className="text-gray-600 mt-2">Monitor daily attendance and manage leave requests.</p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          <div className="lg:col-span-2">
            <div className="bg-white rounded-xl shadow-sm p-6">
              <div className="flex justify-between items-center mb-6">
                <h2 className="text-xl font-semibold text-gray-900">Today's Attendance</h2>
                <input type="date" defaultValue={new Date().toISOString().split('T')[0]} className="border border-gray-300 rounded-lg px-3 py-1" />
              </div>
              <div className="overflow-x-auto">
                <table className="w-full">
                  <thead>
                    <tr className="border-b border-gray-200">
                      <th className="text-left py-3 px-4 font-medium text-gray-700">Employee</th>
                      <th className="text-left py-3 px-4 font-medium text-gray-700">Check In</th>
                      <th className="text-left py-3 px-4 font-medium text-gray-700">Check Out</th>
                      <th className="text-left py-3 px-4 font-medium text-gray-700">Status</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-gray-200">
                    {attendanceData.map((record) => (
                      <tr key={record.id}>
                        <td className="py-3 px-4">
                          <div className="flex items-center space-x-3">
                            <img src={record.avatar} alt={record.name} className="h-10 w-10 rounded-full" />
                            <span className="font-medium text-gray-900">{record.name}</span>
                          </div>
                        </td>
                        <td className="py-3 px-4 text-gray-700">{record.checkIn}</td>
                        <td className="py-3 px-4 text-gray-700">{record.checkOut}</td>
                        <td className="py-3 px-4">
                          <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                            record.status === 'Present' ? 'bg-green-100 text-green-700' :
                            record.status === 'Late' ? 'bg-yellow-100 text-yellow-700' :
                            'bg-red-100 text-red-700'
                          }`}>
                            {record.status}
                          </span>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          </div>
          <div>
            <div className="bg-white rounded-xl shadow-sm p-6">
              <h2 className="text-xl font-semibold text-gray-900 mb-6">Leave Approvals</h2>
              <div className="space-y-4">
                {leaveRequests.map(req => (
                  <div key={req.id} className="border border-gray-200 rounded-lg p-4">
                    <p className="font-medium text-gray-900">{req.name}</p>
                    <p className="text-sm text-gray-500">{req.dates}</p>
                    <p className="text-sm text-gray-600 mt-2">{req.reason}</p>
                    <div className="flex space-x-2 mt-3">
                      <button className="flex-1 bg-green-100 text-green-700 hover:bg-green-200 text-sm py-1 rounded-lg flex items-center justify-center space-x-1">
                        <Check className="h-4 w-4" /><span>Approve</span>
                      </button>
                      <button className="flex-1 bg-red-100 text-red-700 hover:bg-red-200 text-sm py-1 rounded-lg flex items-center justify-center space-x-1">
                        <X className="h-4 w-4" /><span>Reject</span>
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            </div>
            <div className="bg-orange-100 border border-orange-200 text-orange-700 rounded-xl p-4 mt-6 flex items-start space-x-3">
              <AlertTriangle className="h-5 w-5 mt-1" />
              <div>
                <h3 className="font-semibold">Absentees Alert</h3>
                <p className="text-sm">Mike Johnson and 2 others are absent today without prior notice.</p>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}

export default AdminAttendancePage;
