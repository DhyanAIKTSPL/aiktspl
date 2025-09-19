import React, { useState, useEffect } from 'react';
import { BookOpen, Video, FileText, ChevronDown, Loader, CheckCircle, PlayCircle } from 'lucide-react';
import { faker } from '@faker-js/faker';
import { motion, AnimatePresence } from 'framer-motion';

function LearningDashboard() {
  const [courses, setCourses] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedCourse, setSelectedCourse] = useState(null);

  useEffect(() => {
    const fetchCourses = () => {
      return new Promise(resolve => {
        setTimeout(() => {
          const fakeCourses = Array.from({ length: 4 }, () => ({
            id: faker.string.uuid(),
            title: `Mastering ${faker.company.buzzNoun()}`,
            description: faker.lorem.paragraph(),
            progress: faker.number.int({ min: 20, max: 100 }),
            modules: Array.from({ length: faker.number.int({ min: 3, max: 5 }) }, () => ({
              id: faker.string.uuid(),
              title: `Module: ${faker.lorem.words(3)}`,
              materials: Array.from({ length: faker.number.int({ min: 2, max: 4 }) }, () => ({
                id: faker.string.uuid(),
                title: faker.lorem.sentence(4),
                type: faker.helpers.arrayElement(['video', 'document']),
                completed: faker.datatype.boolean(),
              })),
            })),
          }));
          resolve(fakeCourses);
        }, 1500);
      });
    };

    setLoading(true);
    fetchCourses().then(data => {
      setCourses(data);
      setSelectedCourse(data[0]); // Select the first course by default
      setLoading(false);
    });
  }, []);

  return (
    <>
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-text-primary flex items-center">
          <BookOpen className="mr-3 h-8 w-8 text-primary" />
          Learning Dashboard
        </h1>
        <p className="text-text-secondary mt-2">Your assigned courses and learning materials.</p>
      </div>

      {loading ? (
        <div className="flex justify-center items-center h-64">
          <Loader className="animate-spin h-10 w-10 text-primary" />
          <span className="ml-4 text-text-secondary text-lg">Loading Courses...</span>
        </div>
      ) : (
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          <div className="lg:col-span-1">
            <h2 className="text-xl font-semibold text-text-primary mb-4">Your Courses</h2>
            <div className="space-y-3">
              {courses.map(course => (
                <motion.div
                  key={course.id}
                  whileHover={{ scale: 1.03 }}
                  onClick={() => setSelectedCourse(course)}
                  className={`p-4 rounded-lg cursor-pointer border-2 transition-all ${selectedCourse?.id === course.id ? 'bg-surface border-primary' : 'bg-surface border-border hover:border-secondary'}`}
                >
                  <h3 className="font-semibold text-text-primary">{course.title}</h3>
                  <div className="w-full bg-background rounded-full h-1.5 mt-2">
                    <div className="bg-primary h-1.5 rounded-full" style={{ width: `${course.progress}%` }}></div>
                  </div>
                  <p className="text-xs text-text-secondary text-right mt-1">{course.progress}% complete</p>
                </motion.div>
              ))}
            </div>
          </div>
          <div className="lg:col-span-2">
            <AnimatePresence mode="wait">
              <motion.div
                key={selectedCourse ? selectedCourse.id : 'empty'}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -20 }}
                transition={{ duration: 0.3 }}
                className="bg-surface rounded-xl shadow-lg border border-border p-6"
              >
                {selectedCourse ? (
                  <>
                    <h2 className="text-2xl font-bold text-text-primary mb-2">{selectedCourse.title}</h2>
                    <p className="text-text-secondary text-sm mb-6">{selectedCourse.description}</p>
                    <div className="space-y-4">
                      {selectedCourse.modules.map(module => (
                        <div key={module.id} className="bg-background p-4 rounded-lg">
                          <h4 className="font-semibold text-text-primary mb-3">{module.title}</h4>
                          <ul className="space-y-3">
                            {module.materials.map(material => (
                              <li key={material.id} className="flex items-center justify-between text-sm text-text-secondary hover:text-text-primary cursor-pointer p-2 rounded-md hover:bg-surface">
                                <div className="flex items-center">
                                  {material.type === 'video' ? <Video className="h-4 w-4 mr-3 text-primary" /> : <FileText className="h-4 w-4 mr-3 text-green-400" />}
                                  <span>{material.title}</span>
                                </div>
                                {material.completed ? (
                                    <CheckCircle className="h-5 w-5 text-green-500" />
                                ) : (
                                    <PlayCircle className="h-5 w-5 text-text-secondary" />
                                )}
                              </li>
                            ))}
                          </ul>
                        </div>
                      ))}
                    </div>
                  </>
                ) : (
                  <div className="text-center py-12">
                    <BookOpen className="h-12 w-12 text-text-secondary mx-auto mb-4" />
                    <h3 className="text-xl font-semibold text-text-primary">Select a course</h3>
                    <p className="text-text-secondary mt-2">Choose a course from the list to see its details.</p>
                  </div>
                )}
              </motion.div>
            </AnimatePresence>
          </div>
        </div>
      )}
    </>
  );
}

export default LearningDashboard;
