import React, { useState } from 'react';
import Header from '../../components/Layout/Header';
import { List, CheckCircle, Clock } from 'lucide-react';
import { faker } from '@faker-js/faker';

function TasksPage() {
  const [activeTab, setActiveTab] = useState('pending');
  const [tasks] = useState(
    Array.from({ length: 8 }, () => ({
      id: faker.string.uuid(),
      title: faker.lorem.sentence(5),
      dueDate: faker.date.future().toLocaleDateString(),
      status: faker.helpers.arrayElement(['Pending', 'Accepted', 'Completed']),
      description: faker.lorem.paragraph(),
    }))
  );

  const filteredTasks = tasks.filter(task => task.status.toLowerCase().includes(activeTab));

  const tabs = [
    { id: 'pending', label: 'Pending', icon: Clock },
    { id: 'accepted', label: 'Accepted', icon: List },
    { id: 'completed', label: 'Completed', icon: CheckCircle },
  ];

  return (
    <div className="min-h-screen bg-gray-50">
      <Header />
      
      <main className="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">My Tasks</h1>
          <p className="text-gray-600 mt-2">View and manage your assigned tasks.</p>
        </div>

        <div className="border-b border-gray-200 mb-6">
          <nav className="-mb-px flex space-x-8" aria-label="Tabs">
            {tabs.map((tab) => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm flex items-center space-x-2 ${
                  activeTab === tab.id
                    ? 'border-blue-500 text-blue-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }`}
              >
                <tab.icon className="h-5 w-5" />
                <span>{tab.label}</span>
              </button>
            ))}
          </nav>
        </div>

        <div className="space-y-4">
          {filteredTasks.length > 0 ? (
            filteredTasks.map((task) => (
              <div key={task.id} className="bg-white rounded-xl shadow-sm p-6">
                <div className="flex justify-between items-start">
                  <div>
                    <h3 className="text-lg font-semibold text-gray-900">{task.title}</h3>
                    <p className="text-sm text-gray-500">Due: {task.dueDate}</p>
                  </div>
                  <span className={`px-3 py-1 rounded-full text-xs font-medium ${
                    task.status === 'Completed' ? 'bg-green-100 text-green-700' :
                    task.status === 'Accepted' ? 'bg-blue-100 text-blue-700' :
                    'bg-yellow-100 text-yellow-700'
                  }`}>
                    {task.status}
                  </span>
                </div>
                <p className="text-gray-600 mt-3">{task.description}</p>
                {task.status !== 'Completed' && (
                  <div className="mt-4 flex space-x-3">
                    <button className="bg-blue-600 text-white px-4 py-2 rounded-lg text-sm">View Details</button>
                    {task.status === 'Pending' && <button className="bg-gray-200 text-gray-800 px-4 py-2 rounded-lg text-sm">Accept Task</button>}
                  </div>
                )}
              </div>
            ))
          ) : (
            <div className="text-center p-8 bg-white rounded-xl shadow-sm">
              <CheckCircle className="h-12 w-12 text-green-500 mx-auto mb-4" />
              <h3 className="text-xl font-semibold text-gray-800">All caught up!</h3>
              <p className="text-gray-500 mt-2">You have no tasks in this category.</p>
            </div>
          )}
        </div>
      </main>
    </div>
  );
}

export default TasksPage;
