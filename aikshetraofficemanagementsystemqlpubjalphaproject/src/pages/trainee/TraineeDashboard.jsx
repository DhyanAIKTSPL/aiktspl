import React from 'react';
import { Link } from 'react-router-dom';
import { Clock, CheckSquare, BookOpen, ArrowRight } from 'lucide-react';
import { motion } from 'framer-motion';
import { useAuth } from '../../contexts/AuthContext';

function TraineeDashboard() {
  const { user } = useAuth();

  const quickActions = [
    { icon: BookOpen, title: 'Learning Dashboard', description: 'Access courses and materials', link: '/trainee/learning', color: 'text-primary' },
    { icon: Clock, title: 'Attendance', description: 'Check in/out and view history', link: '/trainee/attendance', color: 'text-secondary' },
    { icon: CheckSquare, title: 'Tasks', description: 'View and manage your tasks', link: '/trainee/tasks', color: 'text-green-400' },
  ];
  
  const recentActivities = [
    { action: 'Started course: "React Fundamentals"', time: '1 hour ago' },
    { action: 'Checked in for the day', time: '3 hours ago' },
    { action: 'New task assigned: "Setup Development Environment"', time: 'Yesterday' },
  ];

  return (
    <>
      <motion.div 
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
        className="mb-8"
      >
        <h1 className="text-3xl font-bold text-text-primary">Welcome, {user?.name}!</h1>
        <p className="text-text-secondary mt-2">Your training journey starts here. Let's get to work.</p>
      </motion.div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <div className="lg:col-span-2">
          <h2 className="text-xl font-semibold text-text-primary mb-6">Your Tools</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {quickActions.map((action, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5, delay: 0.1 + index * 0.1 }}
              >
                <Link
                  to={action.link}
                  className="block p-6 bg-surface rounded-xl border border-border hover:border-primary transition-colors group hover:shadow-glow h-full"
                >
                  <div className="flex items-center justify-between mb-3">
                    <h3 className="text-lg font-semibold text-text-primary">{action.title}</h3>
                    <action.icon className={`h-8 w-8 ${action.color} transition-colors`} />
                  </div>
                  <p className="text-text-secondary mb-4">{action.description}</p>
                  <div className="flex items-center text-sm text-primary font-medium">
                    <span>Go to {action.title}</span>
                    <ArrowRight className="h-4 w-4 ml-1 transform group-hover:translate-x-1 transition-transform" />
                  </div>
                </Link>
              </motion.div>
            ))}
          </div>
        </div>

        <motion.div
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.5, delay: 0.4 }}
        >
          <h2 className="text-xl font-semibold text-text-primary mb-6">Recent Activities</h2>
          <div className="bg-surface rounded-xl shadow-lg p-6 border border-border">
            <div className="space-y-4">
              {recentActivities.map((activity, index) => (
                <div key={index} className="flex items-start space-x-3">
                  <div className="w-2 h-2 bg-primary rounded-full mt-2 flex-shrink-0"></div>
                  <div className="flex-1">
                    <p className="text-sm font-medium text-text-primary">{activity.action}</p>
                    <p className="text-xs text-text-secondary">{activity.time}</p>
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

export default TraineeDashboard;
