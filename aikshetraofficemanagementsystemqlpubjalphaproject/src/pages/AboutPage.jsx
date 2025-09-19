import React from 'react';
import { Link } from 'react-router-dom';
import { ArrowLeft, Target, Users, Zap, Shield } from 'lucide-react';
import { motion } from 'framer-motion';

function AboutPage() {
  const features = [
    {
      icon: Target,
      title: 'Mission-Driven',
      description: 'To revolutionize workplace management with innovative technology solutions.'
    },
    {
      icon: Users,
      title: 'People-Focused',
      description: 'Built by teams, for teams. We understand the challenges of modern workplaces.'
    },
    {
      icon: Zap,
      title: 'Innovation',
      description: 'Cutting-edge features like GPS attendance and real-time task management.'
    },
    {
      icon: Shield,
      title: 'Reliable',
      description: 'Enterprise-grade security and 99.9% uptime guarantee.'
    }
  ];

  const team = [
    {
      name: 'Sarah Johnson',
      role: 'CEO & Founder',
      image: 'https://img-wrapper.vercel.app/image?url=https://placehold.co/150x150'
    },
    {
      name: 'Michael Chen',
      role: 'CTO',
      image: 'https://img-wrapper.vercel.app/image?url=https://placehold.co/150x150'
    },
    {
      name: 'Emily Rodriguez',
      role: 'Head of Product',
      image: 'https://img-wrapper.vercel.app/image?url=https://placehold.co/150x150'
    },
    {
      name: 'David Kim',
      role: 'Lead Developer',
      image: 'https://img-wrapper.vercel.app/image?url=https://placehold.co/150x150'
    }
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-indigo-50">
      {/* Header */}
      <header className="bg-white shadow-lg">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <Link to="/" className="text-2xl font-bold text-blue-600">AIKSHETRA</Link>
            <Link
              to="/"
              className="inline-flex items-center text-blue-600 hover:text-blue-700"
            >
              <ArrowLeft className="h-4 w-4 mr-2" />
              Back to Home
            </Link>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto py-12 px-4 sm:px-6 lg:px-8">
        {/* Hero Section */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          className="text-center mb-16"
        >
          <h1 className="text-4xl md:text-5xl font-bold text-gray-900 mb-6">
            About AIKSHETRA
          </h1>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            We're on a mission to transform how organizations manage their workforce, 
            making office operations more efficient, transparent, and employee-friendly.
          </p>
        </motion.div>

        {/* Story Section */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.2 }}
          className="bg-white rounded-2xl shadow-xl p-8 md:p-12 mb-16"
        >
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
            <div>
              <h2 className="text-3xl font-bold text-gray-900 mb-6">Our Story</h2>
              <div className="space-y-4 text-gray-600">
                <p>
                  AIKSHETRA was born out of a simple observation: traditional office management 
                  systems were failing to meet the needs of modern, dynamic workplaces. Founded 
                  in 2023, we set out to create a comprehensive solution that would streamline 
                  attendance tracking, task management, and employee engagement.
                </p>
                <p>
                  Our team of experienced developers and workplace experts came together with 
                  a shared vision: to build technology that empowers both employees and 
                  administrators to work more effectively and transparently.
                </p>
                <p>
                  Today, AIKSHETRA serves hundreds of organizations worldwide, helping them 
                  manage their workforce with unprecedented efficiency and insight.
                </p>
              </div>
            </div>
            <div className="flex justify-center">
              <img 
                src="https://img-wrapper.vercel.app/image?url=https://placehold.co/500x400" 
                alt="AIKSHETRA Office" 
                className="rounded-xl shadow-lg"
              />
            </div>
          </div>
        </motion.div>

        {/* Values Section */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.4 }}
          className="mb-16"
        >
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold text-gray-900 mb-4">Our Values</h2>
            <p className="text-xl text-gray-600 max-w-2xl mx-auto">
              The principles that guide everything we do at AIKSHETRA.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
            {features.map((feature, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.6, delay: 0.4 + index * 0.1 }}
                className="bg-white rounded-xl shadow-lg p-6 text-center"
              >
                <div className="w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-4">
                  <feature.icon className="h-8 w-8 text-blue-600" />
                </div>
                <h3 className="text-xl font-semibold text-gray-900 mb-3">
                  {feature.title}
                </h3>
                <p className="text-gray-600">
                  {feature.description}
                </p>
              </motion.div>
            ))}
          </div>
        </motion.div>

        {/* Team Section */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.6 }}
          className="mb-16"
        >
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold text-gray-900 mb-4">Meet Our Team</h2>
            <p className="text-xl text-gray-600 max-w-2xl mx-auto">
              The passionate individuals behind AIKSHETRA's success.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
            {team.map((member, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.6, delay: 0.6 + index * 0.1 }}
                className="bg-white rounded-xl shadow-lg p-6 text-center"
              >
                <img
                  src={member.image}
                  alt={member.name}
                  className="w-24 h-24 rounded-full mx-auto mb-4 object-cover"
                />
                <h3 className="text-lg font-semibold text-gray-900 mb-1">
                  {member.name}
                </h3>
                <p className="text-blue-600 font-medium">
                  {member.role}
                </p>
              </motion.div>
            ))}
          </div>
        </motion.div>

        {/* Statistics */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.8 }}
          className="bg-blue-600 rounded-2xl shadow-xl p-8 md:p-12 text-white"
        >
          <div className="text-center mb-8">
            <h2 className="text-3xl font-bold mb-4">AIKSHETRA by the Numbers</h2>
            <p className="text-blue-100 text-lg">
              Our impact in the workplace management space.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-4 gap-8 text-center">
            <div>
              <div className="text-4xl font-bold mb-2">500+</div>
              <div className="text-blue-100">Companies</div>
            </div>
            <div>
              <div className="text-4xl font-bold mb-2">50K+</div>
              <div className="text-blue-100">Employees</div>
            </div>
            <div>
              <div className="text-4xl font-bold mb-2">99.9%</div>
              <div className="text-blue-100">Uptime</div>
            </div>
            <div>
              <div className="text-4xl font-bold mb-2">24/7</div>
              <div className="text-blue-100">Support</div>
            </div>
          </div>
        </motion.div>

        {/* CTA Section */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 1.0 }}
          className="text-center mt-16"
        >
          <h2 className="text-3xl font-bold text-gray-900 mb-4">
            Ready to Transform Your Workplace?
          </h2>
          <p className="text-xl text-gray-600 mb-8 max-w-2xl mx-auto">
            Join thousands of organizations that trust AIKSHETRA for their office management needs.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link
              to="/register"
              className="bg-blue-600 hover:bg-blue-700 text-white px-8 py-4 rounded-lg font-semibold text-lg transition-colors"
            >
              Get Started Today
            </Link>
            <Link
              to="/contact"
              className="border-2 border-blue-600 text-blue-600 hover:bg-blue-600 hover:text-white px-8 py-4 rounded-lg font-semibold text-lg transition-colors"
            >
              Contact Sales
            </Link>
          </div>
        </motion.div>
      </main>
    </div>
  );
}

export default AboutPage;
