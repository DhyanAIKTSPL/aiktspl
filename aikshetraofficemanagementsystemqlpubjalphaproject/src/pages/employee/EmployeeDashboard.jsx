import React from 'react';
import { Link } from 'react-router-dom';
import { Clock, CheckSquare, User, DollarSign, Calendar, TrendingUp } from 'lucide-react';
import { motion } from 'framer-motion';

function EmployeeDashboard() {
  const quickStats = [
    { icon: Clock, title: 'Today\'s Hours', value: '8.5 hrs', subtitle: 'Check-in: 9:00 AM', color: 'text-secondary' },
    { icon: CheckSquare, title: 'Active Tasks', value: '5', subtitle: '2 due today', color: 'text-green-400' },
    { icon: Calendar, title: 'Month Attendance', value: '22 days', subtitle: 'On time', color: 'text-primary' },
    { icon: TrendingUp, title: 'Performance', value: '95%', subtitle: 'Task completion', color: 'text-orange-400' }
  ];

  const quickActions = [
    { icon: Clock, title: 'Attendance', description: 'Check in/out and view history', link: '/employee/attendance' },
    { icon: CheckSquare, title: 'Tasks', description: 'View and manage your tasks', link: '/employee/tasks' },
    { icon: User, title: 'Profile', description: 'Update your profile information', link: '/employee/profile' },
    { icon: DollarSign, title: 'Salary', description: 'View salary details and history', link: '/employee/salary' }
  ];

  const recentActivities = [
    { action: 'Checked in', time: '9:00 AM', date: 'Today' },
    { action: 'Completed task: Website Redesign', time: '2:30 PM', date: 'Yesterday' },
    { action: 'Applied for leave', time: '11:00 AM', date: '2 days ago' },
    { action: 'Updated profile', time: '4:00 PM', date: '3 days ago' }
  ];

  return (
    <>
      <motion.div 
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
        className="mb-8"
      >
        <h1 className="text-3xl font-bold text-text-primary">Welcome back!</h1>
        <p className="text-text-secondary mt-2">Here's what's happening with your work today.</p>
      </motion.div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        {quickStats.map((stat, index) => (
          <motion.div
            key={index}
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.5, delay: index * 0.1 }}
            className="bg-surface rounded-xl shadow-lg p-6 border border-border"
          >
            <div className="flex items-center">
              <div className={`p-3 rounded-lg bg-background`}>
                <stat.icon className={`h-6 w-6 ${stat.color}`} />
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-text-secondary">{stat.title}</p>
                <p className="text-2xl font-bold text-text-primary">{stat.value}</p>
                <p className="text-sm text-text-secondary">{stat.subtitle}</p>
              </div>
            </div>
          </motion.div>
        ))}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <div className="lg:col-span-2">
          <h2 className="text-xl font-semibold text-text-primary mb-6">Quick Actions</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {quickActions.map((action, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5, delay: 0.4 + index * 0.1 }}
              >
                <Link
                  to={action.link}
                  className="block p-6 bg-surface rounded-xl border border-border hover:border-primary transition-colors group hover:shadow-glow"
                >
                  <action.icon className="h-8 w-8 text-text-secondary group-hover:text-primary mb-3 transition-colors" />
                  <h3 className="text-lg font-semibold text-text-primary mb-2">{action.title}</h3>
                  <p className="text-text-secondary">{action.description}</p>
                </Link>
              </motion.div>
            ))}
          </div>
        </div>

        <motion.div
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.5, delay: 0.6 }}
        >
          <h2 className="text-xl font-semibold text-text-primary mb-6">Recent Activities</h2>
          <div className="bg-surface rounded-xl shadow-lg p-6 border border-border">
            <div className="space-y-4">
              {recentActivities.map((activity, index) => (
                <div key={index} className="flex items-start space-x-3">
                  <div className="w-2 h-2 bg-primary rounded-full mt-2 flex-shrink-0"></div>
                  <div className="flex-1">
                    <p className="text-sm font-medium text-text-primary">{activity.action}</p>
                    <p className="text-xs text-text-secondary">{activity.time} • {activity.date}</p>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </motion.div>
      </div>
    </>
  );
}

export default EmployeeDashboard;
