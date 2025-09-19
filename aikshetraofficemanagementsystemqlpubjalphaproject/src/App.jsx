import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './contexts/AuthContext';
import DashboardLayout from './components/Layout/DashboardLayout';

// Public Pages
import HomePage from './pages/HomePage';
import LoginPage from './pages/LoginPage';
import RegisterPage from './pages/RegisterPage';
import ContactPage from './pages/ContactPage';
import AboutPage from './pages/AboutPage';

// Shared Pages
import ProfilePage from './pages/ProfilePage';

// Employee Pages
import EmployeeDashboard from './pages/employee/EmployeeDashboard';
import AttendancePage from './pages/employee/AttendancePage';
import TasksPage from './pages/employee/TasksPage';
import SalaryPage from './pages/employee/SalaryPage';

// Admin Pages
import AdminDashboard from './pages/admin/AdminDashboard';
import AdminEmployeesPage from './pages/admin/AdminEmployeesPage';
import AdminTasksPage from './pages/admin/AdminTasksPage';
import AdminAttendancePage from './pages/admin/AdminAttendancePage';
import AdminSalaryPage from './pages/admin/AdminSalaryPage';
import LoginApprovalPage from './pages/admin/LoginApprovalPage';
import AdminLearningPage from './pages/admin/AdminLearningPage';

// Trainee Pages
import TraineeDashboard from './pages/trainee/TraineeDashboard';
import LearningDashboard from './pages/trainee/LearningDashboard';


function ProtectedRoute({ children, role }) {
  const { user, isAuthenticated } = useAuth();
  
  if (!isAuthenticated) {
    return <Navigate to="/login" />;
  }
  
  if (role && user?.role !== role) {
    const userHome = user?.role === 'admin' ? '/admin' : user?.role === 'employee' ? '/employee' : '/trainee';
    return <Navigate to={userHome} />;
  }
  
  return children;
}

const ProtectedLayout = ({ role, children }) => {
  return (
    <ProtectedRoute role={role}>
      <DashboardLayout>
        {children}
      </DashboardLayout>
    </ProtectedRoute>
  );
};

function App() {
  return (
    <AuthProvider>
      <Router>
        <Routes>
          {/* Public Routes */}
          <Route path="/" element={<HomePage />} />
          <Route path="/login" element={<LoginPage />} />
          <Route path="/register" element={<RegisterPage />} />
          <Route path="/contact" element={<ContactPage />} />
          <Route path="/about" element={<AboutPage />} />
          
          {/* Employee Routes */}
          <Route path="/employee" element={<ProtectedLayout role="employee"><EmployeeDashboard /></ProtectedLayout>} />
          <Route path="/employee/attendance" element={<ProtectedLayout role="employee"><AttendancePage /></ProtectedLayout>} />
          <Route path="/employee/tasks" element={<ProtectedLayout role="employee"><TasksPage /></ProtectedLayout>} />
          <Route path="/employee/profile" element={<ProtectedLayout role="employee"><ProfilePage /></ProtectedLayout>} />
          <Route path="/employee/salary" element={<ProtectedLayout role="employee"><SalaryPage /></ProtectedLayout>} />
          
          {/* Admin Routes */}
          <Route path="/admin" element={<ProtectedLayout role="admin"><AdminDashboard /></ProtectedLayout>} />
          <Route path="/admin/employees" element={<ProtectedLayout role="admin"><AdminEmployeesPage /></ProtectedLayout>} />
          <Route path="/admin/tasks" element={<ProtectedLayout role="admin"><AdminTasksPage /></ProtectedLayout>} />
          <Route path="/admin/attendance" element={<ProtectedLayout role="admin"><AdminAttendancePage /></ProtectedLayout>} />
          <Route path="/admin/salary" element={<ProtectedLayout role="admin"><AdminSalaryPage /></ProtectedLayout>} />
          <Route path="/admin/approvals" element={<ProtectedLayout role="admin"><LoginApprovalPage /></ProtectedLayout>} />
          <Route path="/admin/learning" element={<ProtectedLayout role="admin"><AdminLearningPage /></ProtectedLayout>} />
          <Route path="/admin/profile" element={<ProtectedLayout role="admin"><ProfilePage /></ProtectedLayout>} />

          {/* Trainee Routes */}
          <Route path="/trainee" element={<ProtectedLayout role="trainee"><TraineeDashboard /></ProtectedLayout>} />
          <Route path="/trainee/attendance" element={<ProtectedLayout role="trainee"><AttendancePage /></ProtectedLayout>} />
          <Route path="/trainee/tasks" element={<ProtectedLayout role="trainee"><TasksPage /></ProtectedLayout>} />
          <Route path="/trainee/learning" element={<ProtectedLayout role="trainee"><LearningDashboard /></ProtectedLayout>} />
          <Route path="/trainee/profile" element={<ProtectedLayout role="trainee"><ProfilePage /></ProtectedLayout>} />

        </Routes>
      </Router>
    </AuthProvider>
  );
}

export default App;
