import React, { useState, useEffect } from 'react';
import { BookOpen, Plus, MoreVertical, Loader, Edit, Trash2 } from 'lucide-react';
import { faker } from '@faker-js/faker';
import CourseModal from '../../components/admin/CourseModal';

function AdminLearningPage() {
  const [courses, setCourses] = useState([]);
  const [loading, setLoading] = useState(true);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [selectedCourse, setSelectedCourse] = useState(null);

  useEffect(() => {
    const fetchCourses = () => {
      return new Promise(resolve => {
        setTimeout(() => {
          const fakeCourses = Array.from({ length: 4 }, () => ({
            id: faker.string.uuid(),
            title: `Mastering ${faker.company.buzzNoun()}`,
            description: faker.lorem.paragraph(),
            modules: Array.from({ length: faker.number.int({ min: 3, max: 5 }) }, () => ({
              id: faker.string.uuid(),
              title: `Module: ${faker.lorem.words(3)}`,
              materials: Array.from({ length: faker.number.int({ min: 2, max: 4 }) }, () => ({
                id: faker.string.uuid(),
                title: faker.lorem.sentence(4),
                type: faker.helpers.arrayElement(['video', 'document']),
              })),
            })),
            trainees: faker.number.int({ min: 5, max: 20 }),
            lastUpdated: faker.date.recent().toLocaleDateString(),
          }));
          resolve(fakeCourses);
        }, 1000);
      });
    };

    if (courses.length === 0) {
        setLoading(true);
        fetchCourses().then(data => {
            setCourses(data);
            setLoading(false);
        });
    } else {
        setLoading(false);
    }
  }, [courses.length]);

  const handleSaveCourse = (courseData) => {
    if (courseData.id) {
      // Update existing course
      setCourses(courses.map(c => c.id === courseData.id ? courseData : c));
    } else {
      // Add new course
      const newCourse = {
        ...courseData,
        id: faker.string.uuid(),
        trainees: 0,
        lastUpdated: new Date().toLocaleDateString(),
      };
      setCourses([newCourse, ...courses]);
    }
  };

  const handleDeleteCourse = (courseId) => {
    if (window.confirm('Are you sure you want to delete this course?')) {
      setCourses(courses.filter(c => c.id !== courseId));
    }
  };

  const openAddModal = () => {
    setSelectedCourse(null);
    setIsModalOpen(true);
  };

  const openEditModal = (course) => {
    setSelectedCourse(course);
    setIsModalOpen(true);
  };

  return (
    <>
      <div className="flex flex-col md:flex-row justify-between items-center mb-8">
        <div>
          <h1 className="text-3xl font-bold text-text-primary flex items-center">
            <BookOpen className="mr-3 h-8 w-8 text-primary" />
            Learning Management
          </h1>
          <p className="text-text-secondary mt-2">Create, assign, and manage training courses.</p>
        </div>
        <button onClick={openAddModal} className="bg-primary hover:bg-primary-hover text-white px-4 py-2 rounded-lg font-medium flex items-center space-x-2 mt-4 md:mt-0">
          <Plus className="h-5 w-5" />
          <span>Add New Course</span>
        </button>
      </div>

      <div className="bg-surface rounded-xl shadow-lg border border-border overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead className="bg-background">
              <tr className="border-b border-border">
                <th className="text-left py-3 px-4 font-medium text-text-secondary">Course Title</th>
                <th className="text-left py-3 px-4 font-medium text-text-secondary">Modules</th>
                <th className="text-left py-3 px-4 font-medium text-text-secondary">Enrolled</th>
                <th className="text-left py-3 px-4 font-medium text-text-secondary">Last Updated</th>
                <th className="text-left py-3 px-4 font-medium text-text-secondary">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-border">
              {loading ? (
                <tr>
                  <td colSpan="5" className="text-center py-8">
                    <div className="flex justify-center items-center">
                      <Loader className="animate-spin h-8 w-8 text-primary" />
                      <span className="ml-4 text-text-secondary">Loading Courses...</span>
                    </div>
                  </td>
                </tr>
              ) : (
                courses.map((course) => (
                  <tr key={course.id} className="hover:bg-background">
                    <td className="py-3 px-4 font-medium text-text-primary">{course.title}</td>
                    <td className="py-3 px-4 text-text-secondary">{course.modules.length}</td>
                    <td className="py-3 px-4 text-text-secondary">{course.trainees}</td>
                    <td className="py-3 px-4 text-text-secondary">{course.lastUpdated}</td>
                    <td className="py-3 px-4">
                      <div className="flex items-center space-x-4">
                        <button onClick={() => openEditModal(course)} className="text-text-secondary hover:text-primary" title="Edit">
                          <Edit className="h-5 w-5" />
                        </button>
                        <button onClick={() => handleDeleteCourse(course.id)} className="text-text-secondary hover:text-red-500" title="Delete">
                          <Trash2 className="h-5 w-5" />
                        </button>
                      </div>
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </div>
      <CourseModal
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        onSave={handleSaveCourse}
        course={selectedCourse}
      />
    </>
  );
}

export default AdminLearningPage;
