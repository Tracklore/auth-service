// Utility function to get the API base URL
export function getApiBaseUrl(): string {
  // In browser environment, use the window location
  if (typeof window !== 'undefined') {
    // For development, use localhost
    if (process.env.NODE_ENV === 'development') {
      return 'http://localhost:8000';
    }
    // For production, you might want to use a relative path or a configured URL
    return '/api';
  }
  
  // In server environment (SSR), use the service name
  // This will work when running in Docker with the same network
  return process.env.NEXT_PUBLIC_API_URL || 'http://auth-service:8000';
}

// Utility function to make API calls
export async function apiCall(endpoint: string, options: RequestInit = {}) {
  const baseUrl = getApiBaseUrl();
  const url = `${baseUrl}${endpoint}`;
  
  const defaultOptions: RequestInit = {
    headers: {
      'Content-Type': 'application/json',
    },
  };
  
  const mergedOptions = {
    ...defaultOptions,
    ...options,
    headers: {
      ...defaultOptions.headers,
      ...options.headers,
    },
  };
  
  try {
    const response = await fetch(url, mergedOptions);
    return response;
  } catch (error) {
    console.error(`API call failed for ${url}:`, error);
    throw error;
  }
}