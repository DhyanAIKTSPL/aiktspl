import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { Eye, EyeOff, Mail, Lock, User, Phone, ArrowLeft } from 'lucide-react';
import { motion } from 'framer-motion';

function RegisterPage() {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    phone: '',
    password: '',
    confirmPassword: '',
    role: 'employee'
  });
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);
  const [errors, setErrors] = useState({});
  const [loading, setLoading] = useState(false);
  
  const { register } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setErrors({});

    const newErrors = {};
    if (formData.password !== formData.confirmPassword) {
      newErrors.confirmPassword = 'Passwords do not match';
    }
    if (formData.password.length < 6) {
      newErrors.password = 'Password must be at least 6 characters';
    }

    if (Object.keys(newErrors).length > 0) {
      setErrors(newErrors);
      setLoading(false);
      return;
    }

    try {
      const result = await register(formData);
      if (result.success) {
        if (formData.role === 'employee' || formData.role === 'trainee') {
          alert('Registration successful! Your account is pending admin approval.');
          navigate('/login');
        } else {
          alert('Registration successful! Please log in.');
          navigate('/login');
        }
      } else {
        setErrors({ general: result.error || 'Registration failed.' });
      }
    } catch (error) {
      setErrors({ general: 'An error occurred. Please try again.' });
    } finally {
      setLoading(false);
    }
  };

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  return (
    <div className="min-h-screen bg-background flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
        className="max-w-md w-full"
      >
        <div className="bg-surface rounded-2xl shadow-2xl shadow-black/20 p-8 border border-border">
          <div className="text-center mb-8">
            <Link to="/" className="inline-flex items-center text-primary hover:text-primary-hover mb-4">
              <ArrowLeft className="h-4 w-4 mr-2" />
              Back to Home
            </Link>
            <h1 className="text-3xl font-bold text-text-primary">Create Account</h1>
            <p className="text-text-secondary mt-2">Join AIKSHETRA today</p>
          </div>

          {errors.general && (
            <div className="bg-red-900/50 border border-red-500/50 text-red-300 px-4 py-3 rounded-lg mb-6">
              {errors.general}
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-6">
            <div>
              <label className="block text-sm font-medium text-text-secondary mb-2">
                Register as
              </label>
              <div className="grid grid-cols-3 gap-3">
                <button
                  type="button"
                  onClick={() => setFormData({ ...formData, role: 'employee' })}
                  className={`px-4 py-3 rounded-lg border-2 font-medium transition-colors ${
                    formData.role === 'employee'
                      ? 'border-primary bg-primary/10 text-primary'
                      : 'border-border text-text-secondary hover:border-secondary'
                  }`}
                >
                  Employee
                </button>
                <button
                  type="button"
                  onClick={() => setFormData({ ...formData, role: 'admin' })}
                  className={`px-4 py-3 rounded-lg border-2 font-medium transition-colors ${
                    formData.role === 'admin'
                      ? 'border-primary bg-primary/10 text-primary'
                      : 'border-border text-text-secondary hover:border-secondary'
                  }`}
                >
                  Admin
                </button>
                <button
                  type="button"
                  onClick={() => setFormData({ ...formData, role: 'trainee' })}
                  className={`px-4 py-3 rounded-lg border-2 font-medium transition-colors ${
                    formData.role === 'trainee'
                      ? 'border-primary bg-primary/10 text-primary'
                      : 'border-border text-text-secondary hover:border-secondary'
                  }`}
                >
                  Trainee
                </button>
              </div>
              {(formData.role === 'employee' || formData.role === 'trainee') && (
                <p className="mt-2 text-sm text-yellow-400">
                  Registrations require admin approval.
                </p>
              )}
            </div>

            {['name', 'email', 'phone'].map(field => (
              <div key={field}>
                <label className="block text-sm font-medium text-text-secondary mb-2 capitalize">
                  {field === 'name' ? 'Full Name' : `${field} Address`}
                </label>
                <div className="relative">
                  {field === 'name' && <User className="absolute left-3 top-1/2 -translate-y-1/2 h-5 w-5 text-gray-500" />}
                  {field === 'email' && <Mail className="absolute left-3 top-1/2 -translate-y-1/2 h-5 w-5 text-gray-500" />}
                  {field === 'phone' && <Phone className="absolute left-3 top-1/2 -translate-y-1/2 h-5 w-5 text-gray-500" />}
                  <input
                    type={field === 'email' ? 'email' : field === 'phone' ? 'tel' : 'text'}
                    name={field}
                    value={formData[field]}
                    onChange={handleChange}
                    className="w-full pl-10 pr-4 py-3 bg-background border border-border rounded-lg focus:ring-2 focus:ring-primary text-text-primary"
                    placeholder={`Enter your ${field}`}
                    required
                  />
                </div>
              </div>
            ))}

            <div>
              <label className="block text-sm font-medium text-text-secondary mb-2">Password</label>
              <div className="relative">
                <Lock className="absolute left-3 top-1/2 -translate-y-1/2 h-5 w-5 text-gray-500" />
                <input
                  type={showPassword ? 'text' : 'password'}
                  name="password"
                  value={formData.password}
                  onChange={handleChange}
                  className={`w-full pl-10 pr-12 py-3 bg-background border rounded-lg focus:ring-2 focus:ring-primary text-text-primary ${errors.password ? 'border-red-500' : 'border-border'}`}
                  placeholder="Create a password"
                  required
                />
                <button type="button" onClick={() => setShowPassword(!showPassword)} className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-500"><EyeOff className="h-5 w-5" /></button>
              </div>
              {errors.password && <p className="mt-1 text-sm text-red-400">{errors.password}</p>}
            </div>

            <div>
              <label className="block text-sm font-medium text-text-secondary mb-2">Confirm Password</label>
              <div className="relative">
                <Lock className="absolute left-3 top-1/2 -translate-y-1/2 h-5 w-5 text-gray-500" />
                <input
                  type={showConfirmPassword ? 'text' : 'password'}
                  name="confirmPassword"
                  value={formData.confirmPassword}
                  onChange={handleChange}
                  className={`w-full pl-10 pr-12 py-3 bg-background border rounded-lg focus:ring-2 focus:ring-primary text-text-primary ${errors.confirmPassword ? 'border-red-500' : 'border-border'}`}
                  placeholder="Confirm your password"
                  required
                />
                <button type="button" onClick={() => setShowConfirmPassword(!showConfirmPassword)} className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-500"><EyeOff className="h-5 w-5" /></button>
              </div>
              {errors.confirmPassword && <p className="mt-1 text-sm text-red-400">{errors.confirmPassword}</p>}
            </div>

            <div className="flex items-center">
              <input type="checkbox" required className="rounded border-border bg-secondary text-primary focus:ring-primary" />
              <span className="ml-2 text-sm text-text-secondary">
                I agree to the <a href="#" className="text-primary hover:underline">Terms</a> and <a href="#" className="text-primary hover:underline">Privacy Policy</a>
              </span>
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full bg-primary hover:bg-primary-hover disabled:bg-red-800 text-white py-3 px-4 rounded-lg font-medium transition-colors"
            >
              {loading ? 'Creating Account...' : 'Create Account'}
            </button>
          </form>

          <div className="mt-8 text-center">
            <p className="text-text-secondary">
              Already have an account?{' '}
              <Link to="/login" className="text-primary hover:text-primary-hover font-medium">
                Sign in here
              </Link>
            </p>
          </div>
        </div>
      </motion.div>
    </div>
  );
}

export default RegisterPage;
