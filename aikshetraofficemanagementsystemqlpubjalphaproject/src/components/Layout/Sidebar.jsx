import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { useAuth } from '../../contexts/AuthContext';
import { User, LogOut, LayoutDashboard, Users, ClipboardList, BarChart, UserCheck, DollarSign, Clock, CheckSquare, BookOpen } from 'lucide-react';

function Sidebar() {
  const { user, logout } = useAuth();
  const location = useLocation();

  const isEmployee = user?.role === 'employee';
  const isAdmin = user?.role === 'admin';
  const isTrainee = user?.role === 'trainee';

  const employeeNavItems = [
    { path: '/employee', label: 'Dashboard', icon: LayoutDashboard },
    { path: '/employee/attendance', label: 'Attendance', icon: Clock },
    { path: '/employee/tasks', label: 'Tasks', icon: CheckSquare },
    { path: '/employee/profile', label: 'Profile', icon: User },
    { path: '/employee/salary', label: 'Salary', icon: DollarSign }
  ];

  const adminNavItems = [
    { path: '/admin', label: 'Dashboard', icon: LayoutDashboard },
    { path: '/admin/employees', label: 'Employees', icon: Users },
    { path: '/admin/tasks', label: 'Tasks', icon: ClipboardList },
    { path: '/admin/attendance', label: 'Attendance', icon: BarChart },
    { path: '/admin/salary', label: 'Salary', icon: DollarSign },
    { path: '/admin/approvals', label: 'Approvals', icon: UserCheck },
    { path: '/admin/learning', label: 'Learning', icon: BookOpen },
    { path: '/admin/profile', label: 'Profile', icon: User }
  ];

  const traineeNavItems = [
    { path: '/trainee', label: 'Dashboard', icon: LayoutDashboard },
    { path: '/trainee/attendance', label: 'Attendance', icon: Clock },
    { path: '/trainee/tasks', label: 'Tasks', icon: CheckSquare },
    { path: '/trainee/learning', label: 'Learning', icon: BookOpen },
    { path: '/trainee/profile', label: 'Profile', icon: User }
  ];

  const navItems = isEmployee ? employeeNavItems : isAdmin ? adminNavItems : isTrainee ? traineeNavItems : [];

  return (
    <aside className="w-64 bg-surface flex flex-col p-4 border-r border-border flex-shrink-0">
      <div className="flex items-center mb-8">
        <Link to="/" className="flex-shrink-0">
          <h1 className="text-2xl font-bold text-secondary">AIKSHETRA</h1>
        </Link>
      </div>
      
      <nav className="flex-1 space-y-2">
        {navItems.map((item) => (
          <Link
            key={item.path}
            to={item.path}
            className={`flex items-center space-x-3 px-3 py-2 rounded-md text-sm font-medium transition-colors ${
              location.pathname.startsWith(item.path) && (item.path !== '/employee' && item.path !== '/admin' && item.path !== '/trainee' || location.pathname === item.path)
                ? 'text-accent bg-primary/20'
                : 'text-text-secondary hover:text-text-primary hover:bg-background'
            }`}
          >
            <item.icon className="h-5 w-5" />
            <span>{item.label}</span>
          </Link>
        ))}
      </nav>

      <div className="mt-auto">
        <div className="p-3 rounded-lg bg-background">
            <div className="flex items-center space-x-3">
                <div className="w-10 h-10 bg-surface rounded-full flex items-center justify-center border-2 border-primary">
                    <User className="h-5 w-5 text-secondary" />
                </div>
                <div className="flex-1 min-w-0">
                    <p className="text-sm font-medium text-text-primary truncate">{user?.name}</p>
                    <p className="text-xs text-text-secondary truncate">{user?.email}</p>
                </div>
                <button
                    onClick={logout}
                    className="p-2 text-text-secondary hover:text-primary"
                    title="Logout"
                >
                    <LogOut className="h-5 w-5" />
                </button>
            </div>
        </div>
      </div>
    </aside>
  );
}

export default Sidebar;
