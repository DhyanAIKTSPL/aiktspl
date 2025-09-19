import React from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { Users, Clock, CheckSquare, TrendingUp, ArrowRight, Shield, Globe, Zap } from 'lucide-react';
import { motion } from 'framer-motion';

function HomePage() {
  const { isAuthenticated, user } = useAuth();

  const features = [
    {
      icon: Clock,
      title: 'Attendance Management',
      description: 'GPS-enabled check-in/out system with real-time tracking and leave management.'
    },
    {
      icon: CheckSquare,
      title: 'Task Assignment',
      description: 'Streamlined task allocation, tracking, and approval workflow for teams.'
    },
    {
      icon: Users,
      title: 'Employee Management',
      description: 'Comprehensive employee profiles, onboarding, and approval processes.'
    },
    {
      icon: TrendingUp,
      title: 'Analytics & Reports',
      description: 'Detailed insights on attendance, productivity, and performance metrics.'
    }
  ];

  const benefits = [
    { icon: Shield, text: 'Secure & Reliable' },
    { icon: Globe, text: 'GPS Integration' },
    { icon: Zap, text: 'Real-time Updates' }
  ];

  return (
    <div className="min-h-screen bg-background text-text-primary">
      {/* Header */}
      <header className="bg-surface/50 backdrop-blur-lg sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <h1 className="text-2xl font-bold text-primary">AIKSHETRA</h1>
            <div className="flex items-center space-x-4">
              {isAuthenticated ? (
                <Link
                  to={user?.role === 'admin' ? '/admin' : '/employee'}
                  className="bg-primary hover:bg-primary-hover text-white px-6 py-2 rounded-lg font-medium transition-colors"
                >
                  Go to Dashboard
                </Link>
              ) : (
                <>
                  <Link
                    to="/login"
                    className="text-text-secondary hover:text-text-primary px-4 py-2 font-medium"
                  >
                    Login
                  </Link>
                  <Link
                    to="/register"
                    className="bg-primary hover:bg-primary-hover text-white px-6 py-2 rounded-lg font-medium transition-colors"
                  >
                    Register
                  </Link>
                </>
              )}
            </div>
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <section className="relative py-20 px-4 sm:px-6 lg:px-8 overflow-hidden">
        <div className="absolute inset-0 bg-grid-pattern opacity-10"></div>
        <div className="relative max-w-7xl mx-auto">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            className="text-center"
          >
            <h1 className="text-4xl md:text-6xl font-bold text-text-primary mb-6">
              The Future of Office
              <span className="text-primary"> Management</span>
            </h1>
            <p className="text-xl text-text-secondary mb-8 max-w-3xl mx-auto">
              Streamline your workplace with our comprehensive office management system. 
              Handle attendance, tasks, and employee management all in one place.
            </p>
            
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              {!isAuthenticated && (
                <>
                  <Link
                    to="/register"
                    className="bg-primary hover:bg-primary-hover text-white px-8 py-4 rounded-lg font-semibold text-lg transition-transform hover:scale-105 inline-flex items-center justify-center"
                  >
                    Get Started
                    <ArrowRight className="ml-2 h-5 w-5" />
                  </Link>
                  <Link
                    to="/about"
                    className="border-2 border-primary text-primary hover:bg-primary hover:text-white px-8 py-4 rounded-lg font-semibold text-lg transition-all"
                  >
                    Learn More
                  </Link>
                </>
              )}
            </div>

            <div className="flex flex-wrap justify-center items-center gap-8 mt-12 text-sm text-text-secondary">
              {benefits.map((benefit, index) => (
                <div key={index} className="flex items-center gap-2">
                  <benefit.icon className="h-4 w-4 text-primary" />
                  <span>{benefit.text}</span>
                </div>
              ))}
            </div>
          </motion.div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-20 bg-surface">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold text-text-primary mb-4">
              Powerful Features
            </h2>
            <p className="text-xl text-text-secondary max-w-2xl mx-auto">
              Everything you need to manage your office efficiently and effectively.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
            {features.map((feature, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ duration: 0.6, delay: index * 0.1 }}
                className="text-center p-6 rounded-xl bg-background border border-border hover:border-primary transition-colors"
              >
                <div className="w-16 h-16 bg-secondary rounded-full flex items-center justify-center mx-auto mb-4">
                  <feature.icon className="h-8 w-8 text-primary" />
                </div>
                <h3 className="text-xl font-semibold text-text-primary mb-3">
                  {feature.title}
                </h3>
                <p className="text-text-secondary">
                  {feature.description}
                </p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 bg-primary">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h2 className="text-3xl md:text-4xl font-bold text-white mb-4">
            Ready to Transform Your Office?
          </h2>
          <p className="text-xl text-red-100 mb-8 max-w-2xl mx-auto">
            Join thousands of companies using AIKSHETRA to streamline their operations.
          </p>
          {!isAuthenticated && (
            <Link
              to="/register"
              className="bg-white text-primary hover:bg-gray-200 px-8 py-4 rounded-lg font-semibold text-lg transition-colors inline-flex items-center"
            >
              Start Free Trial
              <ArrowRight className="ml-2 h-5 w-5" />
            </Link>
          )}
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-black text-white py-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
            <div>
              <h3 className="text-xl font-bold text-primary mb-4">AIKSHETRA</h3>
              <p className="text-text-secondary">
                Modern office management solutions for the digital workplace.
              </p>
            </div>
            <div>
              <h4 className="font-semibold mb-4">Quick Links</h4>
              <div className="space-y-2">
                <Link to="/about" className="block text-text-secondary hover:text-white">About Us</Link>
                <Link to="/contact" className="block text-text-secondary hover:text-white">Contact</Link>
              </div>
            </div>
            <div>
              <h4 className="font-semibold mb-4">Support</h4>
              <div className="space-y-2">
                <a href="#" className="block text-text-secondary hover:text-white">Help Center</a>
                <a href="#" className="block text-text-secondary hover:text-white">Documentation</a>
              </div>
            </div>
            <div>
              <h4 className="font-semibold mb-4">Connect</h4>
              <div className="space-y-2">
                <a href="#" className="block text-text-secondary hover:text-white">LinkedIn</a>
                <a href="#" className="block text-text-secondary hover:text-white">Twitter</a>
              </div>
            </div>
          </div>
          <div className="border-t border-border mt-8 pt-8 text-center text-text-secondary">
            <p>&copy; 2025 AIKSHETRA. All rights reserved.</p>
          </div>
        </div>
      </footer>
    </div>
  );
}

export default HomePage;
