import { useAuth0 } from '@auth0/auth0-react';

export const UserProfile = () => {
  const { user, logout } = useAuth0();

  if (!user) return null;

  return (
    <div className="absolute top-4 right-4 flex items-center gap-4 bg-white rounded-full shadow-lg px-4 py-2">
      <div className="flex items-center gap-3">
        {user.picture && (
          <img 
            src={user.picture} 
            alt={user.name} 
            className="w-10 h-10 rounded-full border-2 border-red-400"
          />
        )}
        <div className="text-left">
          <p className="text-sm font-semibold text-gray-800">{user.name}</p>
          <p className="text-xs text-gray-500">{user.email}</p>
        </div>
      </div>
      <button
        onClick={() => logout({ logoutParams: { returnTo: window.location.origin } })}
        className="text-sm px-4 py-2 bg-red-500 hover:bg-red-600 text-white rounded-full font-medium transition-colors"
      >
        Sign Out
      </button>
    </div>
  );
};
