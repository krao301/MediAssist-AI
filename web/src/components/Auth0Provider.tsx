import { Auth0Provider as Auth0ProviderSDK } from '@auth0/auth0-react';
import { ReactNode } from 'react';

interface Auth0ProviderProps {
  children: ReactNode;
}

export const Auth0Provider = ({ children }: Auth0ProviderProps) => {
  const domain = import.meta.env.VITE_AUTH0_DOMAIN;
  const clientId = import.meta.env.VITE_AUTH0_CLIENT_ID;
  const redirectUri = window.location.origin;
  const audience = import.meta.env.VITE_AUTH0_AUDIENCE;

  if (!domain || !clientId) {
    console.error('Auth0 configuration missing. Please set VITE_AUTH0_DOMAIN and VITE_AUTH0_CLIENT_ID in .env file');
    return <div className="flex items-center justify-center min-h-screen bg-red-50">
      <div className="text-center p-8 bg-white rounded-lg shadow-lg">
        <h2 className="text-2xl font-bold text-red-600 mb-4">⚠️ Auth0 Configuration Missing</h2>
        <p className="text-gray-700 mb-2">Please configure Auth0 in your .env file:</p>
        <pre className="text-left bg-gray-100 p-4 rounded mt-4 text-sm">
          VITE_AUTH0_DOMAIN=your-tenant.auth0.com{'\n'}
          VITE_AUTH0_CLIENT_ID=your-client-id{'\n'}
          VITE_AUTH0_AUDIENCE=https://api.mediassistai
        </pre>
      </div>
    </div>;
  }

  return (
    <Auth0ProviderSDK
      domain={domain}
      clientId={clientId}
      authorizationParams={{
        redirect_uri: redirectUri,
        audience: audience,
        scope: 'openid profile email'
      }}
      useRefreshTokens
      cacheLocation="localstorage"
    >
      {children}
    </Auth0ProviderSDK>
  );
};
