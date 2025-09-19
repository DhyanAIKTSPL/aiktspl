import React, { useState, useEffect } from 'react';
import Header from '../../components/Layout/Header';
import { Plus, List, CheckCircle, Clock, Loader } from 'lucide-react';
import { faker } from '@faker-js/faker';

function AdminTasksPage() {
  const [activeTab, setActiveTab] = useState('status');
  const [tasks, setTasks] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Simulate fetching data
    const fetchTasks = () => {
      // TODO: Replace with actual API call to Supabase
      return new Promise(resolve => {
        setTimeout(() => {
          const fakeTasks = Array.from({ length: 10 }, () => ({
            id: faker.string.uuid(),
            title: faker.lorem.sentence(4),
            assignee: faker.person.fullName(),
            dueDate: faker.date.future().toLocaleDateString(),
            status: faker.helpers.arrayElement(['In Progress', 'Completed', 'Pending Review']),
            priority: faker.helpers.arrayElement(['High', 'Medium', 'Low']),
          }));
          resolve(fakeTasks);
        }, 1000);
      });
    };

    setLoading(true);
    fetchTasks().then(data => {
      setTasks(data);
      setLoading(false);
    });
  }, []);

  const tabs = [
    { id: 'status', label: 'Task Status', icon: List },
    { id: 'assign', label: 'Assign Task', icon: Plus },
    { id: 'review', label: 'Task Review', icon: CheckCircle },
  ];

  return (
    <div className="min-h-screen bg-background">
      <Header />
      
      <main className="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-text-primary">Task Management</h1>
          <p className="text-text-secondary mt-2">Assign, monitor, and review all tasks.</p>
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

        {activeTab === 'status' && (
          <div className="bg-surface rounded-xl shadow-lg border border-border overflow-hidden">
             <div className="overflow-x-auto">
              <table className="w-full">
                <thead className="bg-secondary/50">
                  <tr className="border-b border-border">
                    <th className="text-left py-3 px-4 font-medium text-text-secondary">Task</th>
                    <th className="text-left py-3 px-4 font-medium text-text-secondary">Assignee</th>
                    <th className="text-left py-3 px-4 font-medium text-text-secondary">Due Date</th>
                    <th className="text-left py-3 px-4 font-medium text-text-secondary">Status</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-border">
                  {loading ? (
                    <tr><td colSpan="4" className="text-center py-8"><Loader className="animate-spin h-8 w-8 text-primary mx-auto" /></td></tr>
                  ) : (
                    tasks.map((task) => (
                      <tr key={task.id} className="hover:bg-secondary/30">
                        <td className="py-3 px-4 font-medium text-text-primary">{task.title}</td>
                        <td className="py-3 px-4 text-text-secondary">{task.assignee}</td>
                        <td className="py-3 px-4 text-text-secondary">{task.dueDate}</td>
                        <td className="py-3 px-4">
                          <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                            task.status === 'Completed' ? 'bg-green-900/50 text-green-300' :
                            task.status === 'In Progress' ? 'bg-blue-900/50 text-blue-300' :
                            'bg-yellow-900/50 text-yellow-300'
                          }`}>
                            {task.status}
                          </span>
                        </td>
                      </tr>
                    ))
                  )}
                </tbody>
              </table>
            </div>
          </div>
        )}

        {activeTab === 'assign' && (
          <div className="bg-surface rounded-xl shadow-lg border border-border p-6">
            <h2 className="text-xl font-semibold text-text-primary mb-6">Assign a New Task</h2>
            <form className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-text-secondary mb-1">Task Title</label>
                <input type="text" className="w-full px-3 py-2 bg-background border border-border rounded-lg" placeholder="e.g., Prepare quarterly report" />
              </div>
              <div>
                <label className="block text-sm font-medium text-text-secondary mb-1">Assign To</label>
                <select className="w-full px-3 py-2 bg-background border border-border rounded-lg">
                  <option>Select Employee</option>
                  <option>John Doe</option>
                  <option>Jane Smith</option>
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium text-text-secondary mb-1">Due Date</label>
                <input type="date" className="w-full px-3 py-2 bg-background border border-border rounded-lg" />
              </div>
              <div>
                <label className="block text-sm font-medium text-text-secondary mb-1">Description</label>
                <textarea rows="3" className="w-full px-3 py-2 bg-background border border-border rounded-lg"></textarea>
              </div>
              <button type="submit" className="bg-primary hover:bg-primary-hover text-white px-4 py-2 rounded-lg">Assign Task</button>
            </form>
          </div>
        )}
        
        {activeTab === 'review' && (
           <div className="text-center p-8 bg-surface rounded-xl shadow-lg border border-border">
             <Clock className="h-12 w-12 text-gray-600 mx-auto mb-4" />
             <h3 className="text-xl font-semibold text-text-primary">No tasks to review</h3>
             <p className="text-text-secondary mt-2">Tasks submitted by employees will appear here for your review.</p>
           </div>
        )}

      </main>
    </div>
  );
}

export default AdminTasksPage;
