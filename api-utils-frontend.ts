// Utility function to get the API base URL
export function getApiBaseUrl(): string {
  // In browser environment, use localhost:8000 for the auth service
  if (typeof window !== 'undefined') {
    return 'http://localhost:8000';
  }
  
  // In server environment (SSR), also use localhost:8000
  return 'http://localhost:8000';
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