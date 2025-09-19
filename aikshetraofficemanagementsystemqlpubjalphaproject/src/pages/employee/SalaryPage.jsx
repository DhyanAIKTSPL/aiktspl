import React from 'react';
import Header from '../../components/Layout/Header';
import { DollarSign, Download, TrendingUp } from 'lucide-react';
import { faker } from '@faker-js/faker';

function SalaryPage() {
  const salaryHistory = Array.from({ length: 6 }, (_, i) => {
    const date = new Date(2025, 0, 1);
    date.setMonth(date.getMonth() - i);
    return {
      id: faker.string.uuid(),
      month: date.toLocaleString('default', { month: 'long', year: 'numeric' }),
      amount: faker.finance.amount(4500, 5500, 2, '$'),
      status: 'Paid',
    };
  });

  return (
    <div className="min-h-screen bg-gray-50">
      <Header />
      
      <main className="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">Salary Details</h1>
          <p className="text-gray-600 mt-2">View your salary information and history.</p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          <div className="lg:col-span-1">
            <div className="bg-white rounded-xl shadow-sm p-6">
              <h2 className="text-xl font-semibold text-gray-900 mb-4">Current Package</h2>
              <div className="text-4xl font-bold text-blue-600 mb-2">$60,000 / year</div>
              <p className="text-gray-600">Next revision: Jan 2026</p>
              
              <div className="mt-6 border-t pt-4">
                <h3 className="font-semibold text-gray-800 mb-3">Earnings Overview</h3>
                <div className="space-y-2 text-sm">
                  <div className="flex justify-between">
                    <span className="text-gray-600">Basic Salary</span>
                    <span>$4,000</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600">Allowances</span>
                    <span>$500</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600">Bonus</span>
                    <span>$500</span>
                  </div>
                  <div className="flex justify-between font-bold border-t pt-2 mt-1">
                    <span>Gross Monthly</span>
                    <span>$5,000</span>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div className="lg:col-span-2">
            <div className="bg-white rounded-xl shadow-sm">
              <h2 className="text-xl font-semibold text-gray-900 p-6">Salary History</h2>
              <div className="overflow-x-auto">
                <table className="w-full">
                  <thead className="bg-gray-50">
                    <tr className="border-b border-gray-200">
                      <th className="text-left py-3 px-6 font-medium text-gray-700">Month</th>
                      <th className="text-left py-3 px-6 font-medium text-gray-700">Amount</th>
                      <th className="text-left py-3 px-6 font-medium text-gray-700">Status</th>
                      <th className="text-left py-3 px-6 font-medium text-gray-700">Payslip</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-gray-200">
                    {salaryHistory.map((record) => (
                      <tr key={record.id}>
                        <td className="py-4 px-6 font-medium text-gray-900">{record.month}</td>
                        <td className="py-4 px-6 text-gray-700">{record.amount}</td>
                        <td className="py-4 px-6">
                          <span className="px-2 py-1 rounded-full text-xs font-medium bg-green-100 text-green-700">
                            {record.status}
                          </span>
                        </td>
                        <td className="py-4 px-6">
                          <button className="text-blue-600 hover:text-blue-800 flex items-center space-x-1">
                            <Download className="h-4 w-4" />
                            <span>Download</span>
                          </button>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}

export default SalaryPage;
