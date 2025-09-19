import React from 'react';
import { Search, Bell } from 'lucide-react';

function Header() {
    return (
        <header className="bg-surface h-16 flex-shrink-0 flex items-center justify-between px-6 border-b border-border">
            <div className="relative">
                <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-5 w-5 text-text-secondary" />
                <input
                    type="text"
                    placeholder="Search..."
                    className="pl-10 pr-4 py-2 w-64 bg-background border border-border rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent text-text-primary"
                />
            </div>
            <div className="flex items-center space-x-4">
                <button className="p-2 text-text-secondary hover:text-text-primary relative">
                    <Bell className="h-5 w-5" />
                    <span className="absolute top-1 right-1 block h-2 w-2 rounded-full bg-secondary ring-2 ring-surface"></span>
                </button>
            </div>
        </header>
    );
}

export default Header;
