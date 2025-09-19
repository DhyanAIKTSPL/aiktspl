import React, { useState } from 'react';
import Header from '../../components/Layout/Header';
import { Clock, MapPin, Calendar, FileText, CheckCircle, XCircle } from 'lucide-react';
import { motion } from 'framer-motion';
import { format } from 'date-fns';

function AttendancePage() {
  const [isCheckedIn, setIsCheckedIn] = useState(false);
  const [showLeaveModal, setShowLeaveModal] = useState(false);
  const [leaveForm, setLeaveForm] = useState({
    fromDate: '',
    toDate: '',
    reason: '',
    document: null
  });

  const handleCheckIn = () => {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        (position) => {
          setIsCheckedIn(true);
          alert('Checked in successfully!');
        },
        (error) => {
          alert('GPS permission required for check-in');
        }
      );
    }
  };

  const handleCheckOut = () => {
    setIsCheckedIn(false);
    alert('Checked out successfully!');
  };

  const attendanceHistory = [
    { date: '2025-01-15', checkIn: '9:00 AM', checkOut: '6:00 PM', hours: '9:00', status: 'Present' },
    { date: '2025-01-14', checkIn: '9:15 AM', checkOut: '6:15 PM', hours: '9:00', status: 'Present' },
    { date: '2025-01-13', checkIn: '9:30 AM', checkOut: '6:30 PM', hours: '9:00', status: 'Late' },
    { date: '2025-01-12', checkIn: '-', checkOut: '-', hours: '0:00', status: 'Absent' },
    { date: '2025-01-11', checkIn: '9:00 AM', checkOut: '6:00 PM', hours: '9:00', status: 'Present' }
  ];

  const leaveRequests = [
    { id: 1, dates: 'Jan 20-22, 2025', reason: 'Medical emergency', status: 'Pending', type: 'Sick Leave' },
    { id: 2, dates: 'Jan 10, 2025', reason: 'Personal work', status: 'Approved', type: 'Personal Leave' },
    { id: 3, dates: 'Dec 25-26, 2024', reason: 'Christmas vacation', status: 'Approved', type: 'Holiday' }
  ];

  const handleLeaveSubmit = (e) => {
    e.preventDefault();
    // Handle leave request submission
    alert('Leave request submitted successfully!');
    setShowLeaveModal(false);
    setLeaveForm({ fromDate: '', toDate: '', reason: '', document: null });
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <Header />
      
      <main className="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">Attendance</h1>
          <p className="text-gray-600 mt-2">Manage your attendance and leave requests</p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Check In/Out Section */}
          <div className="lg:col-span-1">
            <div className="bg-white rounded-xl shadow-sm p-6 mb-6">
              <h2 className="text-xl font-semibold text-gray-900 mb-4">Today's Attendance</h2>
              
              <div className="text-center mb-6">
                <div className="text-3xl font-bold text-gray-900 mb-2">
                  {format(new Date(), 'MMM dd, yyyy')}
                </div>
                <div className="text-lg text-gray-600">
                  {format(new Date(), 'EEEE')}
                </div>
              </div>

              <div className="space-y-4">
                {!isCheckedIn ? (
                  <button
                    onClick={handleCheckIn}
                    className="w-full bg-green-600 hover:bg-green-700 text-white py-4 px-6 rounded-lg font-semibold flex items-center justify-center space-x-2"
                  >
                    <Clock className="h-5 w-5" />
                    <span>Check In</span>
                  </button>
                ) : (
                  <div className="space-y-4">
                    <div className="bg-green-50 border border-green-200 rounded-lg p-4">
                      <div className="flex items-center space-x-2 text-green-700">
                        <CheckCircle className="h-5 w-5" />
                        <span className="font-medium">Checked In</span>
                      </div>
                      <p className="text-sm text-green-600 mt-1">9:00 AM</p>
                    </div>
                    
                    <button
                      onClick={handleCheckOut}
                      className="w-full bg-red-600 hover:bg-red-700 text-white py-4 px-6 rounded-lg font-semibold flex items-center justify-center space-x-2"
                    >
                      <Clock className="h-5 w-5" />
                      <span>Check Out</span>
                    </button>
                  </div>
                )}

                <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
                  <div className="flex items-center space-x-2 text-blue-700 mb-2">
                    <MapPin className="h-4 w-4" />
                    <span className="text-sm font-medium">Location Required</span>
                  </div>
                  <p className="text-xs text-blue-600">GPS location is required for attendance marking</p>
                </div>
              </div>
            </div>

            <div className="bg-white rounded-xl shadow-sm p-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">This Month Stats</h3>
              <div className="space-y-3">
                <div className="flex justify-between">
                  <span className="text-gray-600">Present Days</span>
                  <span className="font-semibold">22</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">Absent Days</span>
                  <span className="font-semibold text-red-600">1</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">Late Days</span>
                  <span className="font-semibold text-orange-600">3</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">Total Hours</span>
                  <span className="font-semibold">176</span>
                </div>
              </div>
            </div>
          </div>

          {/* Attendance History & Leave Requests */}
          <div className="lg:col-span-2 space-y-8">
            {/* Leave Request Section */}
            <div className="bg-white rounded-xl shadow-sm p-6">
              <div className="flex justify-between items-center mb-6">
                <h2 className="text-xl font-semibold text-gray-900">Leave Requests</h2>
                <button
                  onClick={() => setShowLeaveModal(true)}
                  className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg font-medium"
                >
                  Apply for Leave
                </button>
              </div>

              <div className="space-y-4">
                {leaveRequests.map((request) => (
                  <div key={request.id} className="border border-gray-200 rounded-lg p-4">
                    <div className="flex items-center justify-between mb-2">
                      <div className="flex items-center space-x-3">
                        <Calendar className="h-5 w-5 text-gray-400" />
                        <span className="font-medium text-gray-900">{request.dates}</span>
                        <span className="px-2 py-1 bg-gray-100 text-gray-700 text-xs rounded-full">
                          {request.type}
                        </span>
                      </div>
                      <div className={`px-3 py-1 rounded-full text-xs font-medium ${
                        request.status === 'Approved' ? 'bg-green-100 text-green-700' :
                        request.status === 'Pending' ? 'bg-yellow-100 text-yellow-700' :
                        'bg-red-100 text-red-700'
                      }`}>
                        {request.status}
                      </div>
                    </div>
                    <p className="text-sm text-gray-600">{request.reason}</p>
                  </div>
                ))}
              </div>
            </div>

            {/* Attendance History */}
            <div className="bg-white rounded-xl shadow-sm p-6">
              <h2 className="text-xl font-semibold text-gray-900 mb-6">Attendance History</h2>
              
              <div className="overflow-x-auto">
                <table className="w-full">
                  <thead>
                    <tr className="border-b border-gray-200">
                      <th className="text-left py-3 px-4 font-medium text-gray-700">Date</th>
                      <th className="text-left py-3 px-4 font-medium text-gray-700">Check In</th>
                      <th className="text-left py-3 px-4 font-medium text-gray-700">Check Out</th>
                      <th className="text-left py-3 px-4 font-medium text-gray-700">Hours</th>
                      <th className="text-left py-3 px-4 font-medium text-gray-700">Status</th>
                    </tr>
                  </thead>
                  <tbody>
                    {attendanceHistory.map((record, index) => (
                      <tr key={index} className="border-b border-gray-100">
                        <td className="py-3 px-4">{record.date}</td>
                        <td className="py-3 px-4">{record.checkIn}</td>
                        <td className="py-3 px-4">{record.checkOut}</td>
                        <td className="py-3 px-4">{record.hours}</td>
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
        </div>

        {/* Leave Application Modal */}
        {showLeaveModal && (
          <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
            <motion.div
              initial={{ opacity: 0, scale: 0.95 }}
              animate={{ opacity: 1, scale: 1 }}
              className="bg-white rounded-xl p-6 w-full max-w-md mx-4"
            >
              <h3 className="text-xl font-semibold text-gray-900 mb-4">Apply for Leave</h3>
              
              <form onSubmit={handleLeaveSubmit} className="space-y-4">
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">From Date</label>
                    <input
                      type="date"
                      value={leaveForm.fromDate}
                      onChange={(e) => setLeaveForm({...leaveForm, fromDate: e.target.value})}
                      className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                      required
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">To Date</label>
                    <input
                      type="date"
                      value={leaveForm.toDate}
                      onChange={(e) => setLeaveForm({...leaveForm, toDate: e.target.value})}
                      className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                      required
                    />
                  </div>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">Reason</label>
                  <textarea
                    value={leaveForm.reason}
                    onChange={(e) => setLeaveForm({...leaveForm, reason: e.target.value})}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    rows="3"
                    placeholder="Enter reason for leave"
                    required
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">Supporting Document (Optional)</label>
                  <input
                    type="file"
                    onChange={(e) => setLeaveForm({...leaveForm, document: e.target.files[0]})}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    accept=".pdf,.jpg,.jpeg,.png"
                  />
                </div>

                <div className="flex space-x-3 pt-4">
                  <button
                    type="submit"
                    className="flex-1 bg-blue-600 hover:bg-blue-700 text-white py-2 px-4 rounded-lg font-medium"
                  >
                    Submit Request
                  </button>
                  <button
                    type="button"
                    onClick={() => setShowLeaveModal(false)}
                    className="flex-1 bg-gray-300 hover:bg-gray-400 text-gray-700 py-2 px-4 rounded-lg font-medium"
                  >
                    Cancel
                  </button>
                </div>
              </form>
            </motion.div>
          </div>
        )}
      </main>
    </div>
  );
}

export default AttendancePage;
