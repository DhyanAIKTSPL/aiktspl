import React from 'react';
import { Users, UserCheck, ClipboardList, BarChart, ArrowRight } from 'lucide-react';
import { motion } from 'framer-motion';
import { Link } from 'react-router-dom';

function AdminDashboard() {
  const stats = [
    { icon: Users, title: 'Total Employees', value: '125', link: '/admin/employees', color: 'text-secondary' },
    { icon: UserCheck, title: 'Pending Approvals', value: '3', link: '/admin/approvals', color: 'text-orange-400' },
    { icon: ClipboardList, title: 'Tasks In Progress', value: '28', link: '/admin/tasks', color: 'text-green-400' },
    { icon: BarChart, title: 'Attendance Today', value: '92%', link: '/admin/attendance', color: 'text-primary' }
  ];

  const recentActivities = [
    { user: 'John Doe', action: 'registered as a new employee.', time: '15 mins ago' },
    { user: 'Jane Smith', action: 'submitted a task for review.', time: '1 hour ago' },
    { user: 'Admin', action: 'approved 2 leave requests.', time: '3 hours ago' },
    { user: 'Mike Johnson', action: 'is marked as absent today.', time: '4 hours ago' }
  ];

  return (
    <>
      <motion.div 
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
        className="mb-8"
      >
        <h1 className="text-3xl font-bold text-text-primary">Admin Dashboard</h1>
        <p className="text-text-secondary mt-2">Oversee and manage all office operations.</p>
      </motion.div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        {stats.map((stat, index) => (
          <motion.div
            key={index}
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.5, delay: index * 0.1 }}
          >
            <Link to={stat.link} className="block bg-surface rounded-xl shadow-lg p-6 border border-border hover:border-primary transition-all group hover:shadow-glow">
              <div className="flex items-center justify-between">
                <div className="p-3 rounded-lg bg-background">
                  <stat.icon className={`h-6 w-6 ${stat.color}`} />
                </div>
                <div className="text-right">
                  <p className="text-sm font-medium text-text-secondary">{stat.title}</p>
                  <p className="text-2xl font-bold text-text-primary">{stat.value}</p>
                </div>
              </div>
              <div className="mt-4 flex items-center text-sm text-primary">
                <span>View Details</span>
                <ArrowRight className="h-4 w-4 ml-1 transform group-hover:translate-x-1 transition-transform" />
              </div>
            </Link>
          </motion.div>
        ))}
      </div>

      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 0.4 }}
      >
        <h2 className="text-xl font-semibold text-text-primary mb-6">Recent Activities</h2>
        <div className="bg-surface rounded-xl shadow-lg border border-border">
          <div className="divide-y divide-border">
            {recentActivities.map((activity, index) => (
              <div key={index} className="p-4 flex items-center justify-between hover:bg-background">
                <p className="text-sm text-text-secondary">
                  <span className="font-medium text-text-primary">{activity.user}</span> {activity.action}
                </p>
                <p className="text-xs text-text-secondary">{activity.time}</p>
              </div>
            ))}
          </div>
        </div>
      </motion.div>
    </>
  );
}

export default AdminDashboard;
