import React from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { X, Mail, Phone, MapPin, Calendar, Briefcase } from 'lucide-react';

function EmployeeProfileModal({ user, isOpen, onClose }) {
  if (!user) return null;

  return (
    <AnimatePresence>
      {isOpen && (
        <div className="fixed inset-0 bg-black bg-opacity-75 flex items-center justify-center z-50 p-4">
          <motion.div
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            exit={{ opacity: 0, scale: 0.9 }}
            transition={{ duration: 0.3 }}
            className="bg-surface rounded-2xl shadow-2xl w-full max-w-2xl border border-border relative"
          >
            <button onClick={onClose} className="absolute top-4 right-4 text-text-secondary hover:text-text-primary">
              <X className="h-6 w-6" />
            </button>

            <div className="p-8">
              <div className="flex flex-col sm:flex-row items-center sm:items-start space-y-4 sm:space-y-0 sm:space-x-6 mb-8">
                <img src={user.avatar} alt={user.name} className="h-24 w-24 rounded-full border-4 border-primary" />
                <div>
                  <h2 className="text-3xl font-bold text-text-primary">{user.name}</h2>
                  <p className="text-lg text-primary">{user.roleType === 'employee' ? user.jobTitle : 'Trainee'}</p>
                   <span className={`mt-2 inline-block px-3 py-1 rounded-full text-sm font-medium ${
                        user.status === 'Active' ? 'bg-green-900/50 text-green-300' : 'bg-yellow-900/50 text-yellow-300'
                      }`}>
                        {user.status}
                      </span>
                </div>
              </div>

              <div className="border-t border-border pt-6 grid grid-cols-1 md:grid-cols-2 gap-6">
                <h3 className="md:col-span-2 text-xl font-semibold text-text-primary mb-2">Contact Information</h3>
                <div className="flex items-center space-x-3">
                  <Mail className="h-5 w-5 text-primary flex-shrink-0" />
                  <span className="text-text-secondary break-all">{user.email}</span>
                </div>
                <div className="flex items-center space-x-3">
                  <Phone className="h-5 w-5 text-primary flex-shrink-0" />
                  <span className="text-text-secondary">{user.phone}</span>
                </div>
                <div className="md:col-span-2 flex items-start space-x-3">
                  <MapPin className="h-5 w-5 text-primary flex-shrink-0 mt-1" />
                  <span className="text-text-secondary">{user.address}</span>
                </div>
                
                <h3 className="md:col-span-2 text-xl font-semibold text-text-primary mt-4 mb-2">Personal & Work Details</h3>
                <div className="flex items-center space-x-3">
                  <Calendar className="h-5 w-5 text-primary flex-shrink-0" />
                  <span className="text-text-secondary">Born on {user.dob}</span>
                </div>
                 <div className="flex items-center space-x-3">
                  <Briefcase className="h-5 w-5 text-primary flex-shrink-0" />
                  <span className="text-text-secondary">Joined on {user.joinDate}</span>
                </div>
              </div>
            </div>
          </motion.div>
        </div>
      )}
    </AnimatePresence>
  );
}

export default EmployeeProfileModal;
