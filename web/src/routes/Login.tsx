import { useAuth0 } from '@auth0/auth0-react';

interface RoleCardProps {
  icon: string;
  title: string;
  description: string;
  features: string[];
  color: string;
  roleType: string;
}

const RoleCard = ({ icon, title, description, features, color, roleType }: RoleCardProps) => {
  const { loginWithRedirect } = useAuth0();

  const handleSignIn = () => {
    loginWithRedirect({
      appState: {
        returnTo: window.location.pathname,
        role: roleType
      },
      authorizationParams: {
        prompt: 'login', // Force login screen every time (no auto-login)
        max_age: 0, // Ignore existing sessions
        screen_hint: 'signup' // Show signup tab by default
      }
    });
  };

  return (
    <div className={`${color} rounded-2xl p-8 shadow-xl flex flex-col items-center text-white min-h-[500px] w-full max-w-sm transform transition-all hover:scale-105 hover:shadow-2xl`}>
      <div className="text-7xl mb-6">{icon}</div>
      
      <h2 className="text-3xl font-bold mb-3">{title}</h2>
      <p className="text-center mb-6 opacity-90 text-lg">{description}</p>
      
      <div className="space-y-3 mb-8 flex-grow w-full">
        {features.map((feature, idx) => (
          <div key={idx} className="flex items-start gap-3">
            <span className="text-xl mt-0.5">✓</span>
            <span className="text-left">{feature}</span>
          </div>
        ))}
      </div>
      
      <button
        onClick={handleSignIn}
        className="w-full bg-white/20 hover:bg-white/30 backdrop-blur-sm text-white font-bold py-4 px-6 rounded-xl transition-all text-lg border-2 border-white/30"
      >
        Sign In as {title}
      </button>
    </div>
  );
};

export default function Login() {
  const { logout, isAuthenticated } = useAuth0();

  const handleClearSession = () => {
    // Clear all Auth0 cache
    Object.keys(localStorage).forEach(key => {
      if (key.startsWith('@@auth0spajs@@')) {
        localStorage.removeItem(key);
      }
    });
    
    // Logout from Auth0
    logout({ 
      logoutParams: { 
        returnTo: window.location.origin 
      } 
    });
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-slate-800 to-gray-900 flex flex-col items-center justify-center p-8">
      {/* Header */}
      <div className="text-center mb-12">
        <div className="text-6xl mb-4">🚨</div>
        <h1 className="text-5xl font-bold text-white mb-3">MediAssist AI</h1>
        <p className="text-xl text-gray-300">Emergency First-Aid Coach with Hospital Integration</p>
        <p className="text-lg text-gray-400 mt-4">Choose how you want to sign in</p>
        
        {/* Clear Session Button (if already logged in) */}
        {isAuthenticated && (
          <div className="mt-4">
            <button
              onClick={handleClearSession}
              className="text-sm text-yellow-400 hover:text-yellow-300 underline"
            >
              🔄 Click here to sign out and choose a different role
            </button>
          </div>
        )}
      </div>

      {/* Role Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-7xl w-full">
        <RoleCard
          icon="👤"
          title="Citizen"
          description="I need emergency first-aid guidance"
          features={[
            'Get AI-powered triage',
            'Step-by-step first-aid instructions',
            'Alert emergency contacts',
            'Find nearest hospitals'
          ]}
          color="bg-gradient-to-br from-blue-500 to-blue-700"
          roleType="citizen"
        />

        <RoleCard
          icon="🏥"
          title="Hospital / ER"
          description="Receive real-time emergency alerts"
          features={[
            'Get notified of nearby emergencies',
            'Webhook integration',
            'View incident dashboard',
            'Prepare for incoming patients'
          ]}
          color="bg-gradient-to-br from-green-500 to-green-700"
          roleType="hospital"
        />

        <RoleCard
          icon="🚑"
          title="First Responder"
          description="CPR/EMT certified volunteer"
          features={[
            'Receive nearby emergency alerts',
            'Update your availability',
            'Track response history',
            'Help save lives in your area'
          ]}
          color="bg-gradient-to-br from-red-500 to-red-700"
          roleType="responder"
        />
      </div>

      {/* Footer */}
      <div className="mt-12 text-center text-gray-400 text-sm max-w-2xl">
        <p className="font-semibold text-red-400 mb-2">⚠️ ALWAYS CALL 911 FIRST</p>
        <p>This app provides guidance while waiting for emergency services. It is not a substitute for professional medical care.</p>
        <p className="mt-4 text-xs">Secure authentication powered by Auth0</p>
      </div>
    </div>
  );
}
