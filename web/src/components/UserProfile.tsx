import { useAuth0 } from '@auth0/auth0-react';
import { useState, useRef, useEffect } from 'react';

export const UserProfile = () => {
  const { user, logout } = useAuth0();
  const [isOpen, setIsOpen] = useState(false);
  const dropdownRef = useRef<HTMLDivElement>(null);

  // Close dropdown when clicking outside
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
        setIsOpen(false);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  const handleLogout = async () => {
    setIsOpen(false);
    
    try {
      // Clear all Auth0 cache
      Object.keys(localStorage).forEach(key => {
        if (key.startsWith('@@auth0spajs@@')) {
          localStorage.removeItem(key);
        }
      });
      
      // Clear session storage too
      sessionStorage.clear();
      
      // Logout from Auth0 and redirect to origin
      await logout({ 
        logoutParams: { 
          returnTo: window.location.origin 
        } 
      });
    } catch (error) {
      console.error('Logout error:', error);
      // If Auth0 logout fails, force redirect to home
      window.location.href = '/';
    }
  };

  if (!user) return null;

  return (
    <div className="relative" ref={dropdownRef}>
      {/* User Avatar Button */}
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="flex items-center gap-2 hover:opacity-80 transition-opacity"
      >
        {user.picture && (
          <img 
            src={user.picture} 
            alt={user.name} 
            className="w-10 h-10 rounded-full border-2 border-red-400"
          />
        )}
        <span className="text-white text-sm font-medium hidden md:inline">{user.name}</span>
        <svg 
          className={`w-4 h-4 text-white transition-transform ${isOpen ? 'rotate-180' : ''}`}
          fill="none" 
          stroke="currentColor" 
          viewBox="0 0 24 24"
        >
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
        </svg>
      </button>

      {/* Dropdown Menu */}
      {isOpen && (
        <div className="absolute right-0 mt-2 w-64 bg-white rounded-lg shadow-xl border border-gray-200 py-2 z-50">
          <div className="px-4 py-3 border-b border-gray-200">
            <p className="text-sm font-semibold text-gray-800">{user.name}</p>
            <p className="text-xs text-gray-500 truncate">{user.email}</p>
          </div>
          <button
            onClick={handleLogout}
            className="w-full text-left px-4 py-2 text-sm text-red-600 hover:bg-red-50 transition-colors flex items-center gap-2"
          >
            <span>🚪</span>
            <span>Sign Out</span>
          </button>
        </div>
      )}
    </div>
  );
};
