import { useNavigate, useLocation } from 'react-router-dom';
import { UserProfile } from './UserProfile';

export const Navbar = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const isHomePage = location.pathname === '/';

  return (
    <nav className="fixed top-0 left-0 right-0 z-50 bg-gray-900/95 backdrop-blur-sm border-b border-gray-800 shadow-lg">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Logo/Brand */}
          <div 
            onClick={() => navigate('/')}
            className="flex items-center gap-3 cursor-pointer hover:opacity-80 transition-opacity"
          >
            <span className="text-3xl">🚨</span>
            <div>
              <h1 className="text-xl font-bold text-white">MediAssist AI</h1>
              <p className="text-xs text-gray-400">Emergency First-Aid Coach</p>
            </div>
          </div>

          {/* Navigation Links */}
          <div className="flex items-center gap-6">
            {!isHomePage && (
              <button
                onClick={() => navigate('/')}
                className="flex items-center gap-2 px-4 py-2 bg-red-500 hover:bg-red-600 text-white rounded-lg font-medium transition-colors"
              >
                <span>🏠</span>
                <span>Home</span>
              </button>
            )}

            <button
              onClick={() => navigate('/contacts')}
              className={`flex items-center gap-2 px-4 py-2 rounded-lg font-medium transition-colors ${
                location.pathname === '/contacts'
                  ? 'bg-blue-500 text-white'
                  : 'text-gray-300 hover:text-white hover:bg-gray-800'
              }`}
            >
              <span>👥</span>
              <span className="hidden sm:inline">Contacts</span>
            </button>

            {/* User Profile */}
            <UserProfile />
          </div>
        </div>
      </div>
    </nav>
  );
};
