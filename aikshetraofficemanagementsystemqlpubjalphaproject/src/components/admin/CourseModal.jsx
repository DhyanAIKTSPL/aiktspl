import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { X, Plus, Trash2, Video, FileText, Edit } from 'lucide-react';
import { faker } from '@faker-js/faker';

function CourseModal({ isOpen, onClose, onSave, course }) {
  const [formData, setFormData] = useState({ id: null, title: '', description: '', modules: [] });

  useEffect(() => {
    if (course) {
      setFormData(course);
    } else {
      setFormData({ id: null, title: '', description: '', modules: [] });
    }
  }, [course, isOpen]);

  const handleSave = () => {
    onSave(formData);
    onClose();
  };

  const addModule = () => {
    const newModule = {
      id: faker.string.uuid(),
      title: 'New Module',
      materials: [],
    };
    setFormData({ ...formData, modules: [...formData.modules, newModule] });
  };

  const deleteModule = (moduleId) => {
    setFormData({ ...formData, modules: formData.modules.filter(m => m.id !== moduleId) });
  };
  
  const addMaterial = (moduleId) => {
    const newMaterial = {
      id: faker.string.uuid(),
      title: 'New Material',
      type: 'document'
    };
    const updatedModules = formData.modules.map(m => 
      m.id === moduleId ? { ...m, materials: [...m.materials, newMaterial] } : m
    );
    setFormData({ ...formData, modules: updatedModules });
  };

  const deleteMaterial = (moduleId, materialId) => {
    const updatedModules = formData.modules.map(m => 
      m.id === moduleId ? { ...m, materials: m.materials.filter(mat => mat.id !== materialId) } : m
    );
    setFormData({ ...formData, modules: updatedModules });
  };

  const handleModuleTitleChange = (moduleId, newTitle) => {
    const updatedModules = formData.modules.map(m => 
      m.id === moduleId ? { ...m, title: newTitle } : m
    );
    setFormData({ ...formData, modules: updatedModules });
  };

  return (
    <AnimatePresence>
      {isOpen && (
        <div className="fixed inset-0 bg-black bg-opacity-75 flex items-center justify-center z-50 p-4">
          <motion.div
            initial={{ opacity: 0, y: 50 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -50 }}
            className="bg-surface rounded-2xl shadow-2xl w-full max-w-3xl border border-border relative flex flex-col max-h-[90vh]"
          >
            <div className="p-6 border-b border-border flex-shrink-0">
              <h2 className="text-2xl font-bold text-text-primary">{course ? 'Edit Course' : 'Add New Course'}</h2>
            </div>
            
            <div className="p-6 space-y-6 overflow-y-auto">
              <div>
                <label className="block text-sm font-medium text-text-secondary mb-2">Course Title</label>
                <input
                  type="text"
                  value={formData.title}
                  onChange={(e) => setFormData({ ...formData, title: e.target.value })}
                  className="w-full px-4 py-2 bg-background border border-border rounded-lg focus:ring-2 focus:ring-primary text-text-primary"
                  placeholder="e.g., Introduction to React"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-text-secondary mb-2">Description</label>
                <textarea
                  value={formData.description}
                  onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                  rows="3"
                  className="w-full px-4 py-2 bg-background border border-border rounded-lg focus:ring-2 focus:ring-primary text-text-primary"
                  placeholder="A brief summary of the course"
                />
              </div>

              <div>
                <div className="flex justify-between items-center mb-4">
                  <h3 className="text-lg font-semibold text-text-primary">Modules</h3>
                  <button onClick={addModule} className="bg-secondary/50 hover:bg-secondary/80 text-white px-3 py-1 rounded-lg text-sm flex items-center space-x-1">
                    <Plus className="h-4 w-4" />
                    <span>Add Module</span>
                  </button>
                </div>
                <div className="space-y-4">
                  {formData.modules.map(module => (
                    <div key={module.id} className="bg-background rounded-lg border border-border p-4">
                      <div className="flex justify-between items-center mb-3">
                        <input 
                          type="text"
                          value={module.title}
                          onChange={(e) => handleModuleTitleChange(module.id, e.target.value)}
                          className="bg-transparent font-semibold text-text-primary w-full focus:outline-none focus:ring-0"
                        />
                        <button onClick={() => deleteModule(module.id)} className="text-text-secondary hover:text-primary"><Trash2 className="h-4 w-4" /></button>
                      </div>
                      <div className="space-y-2">
                        {module.materials.map(material => (
                          <div key={material.id} className="flex items-center justify-between bg-surface p-2 rounded">
                            <div className="flex items-center space-x-2">
                              {material.type === 'video' ? <Video className="h-4 w-4 text-primary" /> : <FileText className="h-4 w-4 text-green-400" />}
                              <span className="text-sm text-text-secondary">{material.title}</span>
                            </div>
                            <button onClick={() => deleteMaterial(module.id, material.id)} className="text-text-secondary hover:text-primary"><Trash2 className="h-4 w-4" /></button>
                          </div>
                        ))}
                      </div>
                      <button onClick={() => addMaterial(module.id)} className="text-primary hover:text-primary-hover text-sm mt-3 flex items-center space-x-1">
                        <Plus className="h-4 w-4" />
                        <span>Add Material</span>
                      </button>
                    </div>
                  ))}
                </div>
              </div>
            </div>

            <div className="p-6 border-t border-border flex justify-end space-x-4 flex-shrink-0">
              <button onClick={onClose} className="px-6 py-2 rounded-lg text-text-primary bg-surface hover:bg-background border border-border">Cancel</button>
              <button onClick={handleSave} className="px-6 py-2 rounded-lg text-white bg-primary hover:bg-primary-hover">Save Course</button>
            </div>
          </motion.div>
        </div>
      )}
    </AnimatePresence>
  );
}

export default CourseModal;
