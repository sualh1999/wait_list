'use client';

import { useState, useEffect, useCallback } from 'react';

interface WaitlistEntry {
  id: string;
  email: string;
  first_name?: string;
  last_name?: string;
  country?: string;
  created_at: string;
}

type ErrorWithMessage = {
  detail: string;
};

function isErrorWithMessage(error: unknown): error is ErrorWithMessage {
  return (
    typeof error === 'object' &&
    error !== null &&
    'detail' in error &&
    typeof (error as Record<string, unknown>).detail === 'string'
  );
}

export default function AdminPage() {
  const [password, setPassword] = useState('');
  const [token, setToken] = useState<string | null>(null);
  const [message, setMessage] = useState('');
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [waitlistEntries, setWaitlistEntries] = useState<WaitlistEntry[]>([]);
  const [filterEmail, setFilterEmail] = useState('');
  const [filterFirstName, setFilterFirstName] = useState('');
  const [filterLastName, setFilterLastName] = useState('');
  const [filterCountry, setFilterCountry] = useState('');
  const [searchQuery, setSearchQuery] = useState('');

  const fetchWaitlistEntries = useCallback(async (authToken: string) => {
    setIsLoading(true);
    setError('');
    try {
      const params = new URLSearchParams();
      if (filterEmail) params.append('email', filterEmail);
      if (filterFirstName) params.append('first_name', filterFirstName);
      if (filterLastName) params.append('last_name', filterLastName);
      if (filterCountry) params.append('country', filterCountry);
      if (searchQuery) params.append('search', searchQuery);

      const queryString = params.toString();
      const url = `${process.env.NEXT_PUBLIC_API_URL}/admin/list${queryString ? `?${queryString}` : ''}`;

      const response = await fetch(url, {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${authToken}`,
        },
      });

      if (response.ok) {
        const data: WaitlistEntry[] = await response.json();
        setWaitlistEntries(data);
      } else if (response.status === 401) {
        setError('Unauthorized. Please log in again.');
        setToken(null);
        sessionStorage.removeItem('admin_token');
      } else {
        const errorData = await response.json();
        if (isErrorWithMessage(errorData)) {
          setError(errorData.detail);
        } else {
          setError('Failed to fetch waitlist entries.');
        }
      }
    } catch (error) {
      console.error(error);
      setError('Network error while fetching entries.');
    } finally {
      setIsLoading(false);
    }
  }, [filterEmail, filterFirstName, filterLastName, filterCountry, searchQuery]);

  useEffect(() => {
    const storedToken = sessionStorage.getItem('admin_token');
    if (storedToken) {
      setToken(storedToken);
      fetchWaitlistEntries(storedToken);
    }
  }, [fetchWaitlistEntries]);

  const handleLogin = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setMessage('');
    setError('');

    if (!password) {
      setError('Password cannot be empty.');
      return;
    }

    setIsLoading(true);

    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/admin/login`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ password }),
      });

      if (response.ok) {
        const data = await response.json();
        sessionStorage.setItem('admin_token', data.access_token);
        setToken(data.access_token);
        setMessage('Login successful!');
        setPassword('');
        fetchWaitlistEntries(data.access_token);
      } else {
        const errorData = await response.json();
        if (isErrorWithMessage(errorData)) {
          setError(errorData.detail);
        } else {
          setError('Login failed.');
        }
      }
    } catch (error) {
      console.error(error);
      setError('Network error. Please try again later.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleLogout = () => {
    setToken(null);
    sessionStorage.removeItem('admin_token');
    setWaitlistEntries([]);
    setMessage('Logged out successfully.');
  };

  if (!token) {
    return (
      <main className="flex min-h-screen flex-col items-center justify-center p-4 bg-gray-50 transition-colors duration-300">
        <div className="w-full max-w-md p-8 bg-white rounded-xl shadow-lg border border-gray-100 transform hover:scale-105 transition-all duration-300 ease-in-out">
          <h1 className="text-3xl font-bold mb-6 text-center text-gray-800">Admin Login</h1>
          <p className="text-center text-gray-600 mb-8">Access the waitlist management dashboard.</p>
          <form onSubmit={handleLogin}>
            <div className="mb-6">
              <label htmlFor="password" className="block text-gray-700 text-sm font-medium mb-2">
                Password:
              </label>
              <input
                type="password"
                id="password"
                className="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-indigo-500 focus:border-transparent outline-none transition-all duration-200 text-gray-800"
                placeholder="Enter admin password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
              />
            </div>
            <button
              type="submit"
              className="w-full bg-indigo-600 hover:bg-indigo-700 text-white font-semibold py-2 px-4 rounded-md focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:bg-gray-400 transition-all duration-200 flex items-center justify-center gap-2"
              disabled={isLoading}
            >
              {isLoading ? (
                <span className="flex items-center justify-center">
                  <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                  Logging in...
                </span>
              ) : (
                'Login'
              )}
            </button>
          </form>
          {message && <p className="mt-4 text-green-600 text-center text-sm">{message}</p>}
          {error && <p className="mt-4 text-red-600 text-center text-sm">{error}</p>}
        </div>
      </main>
    );
  }

  return (
    <main className="flex min-h-screen flex-col items-center p-4 bg-gray-50 transition-colors duration-300">
      <div className="w-full max-w-5xl p-8 bg-white rounded-xl shadow-lg border border-gray-100">
        <div className="flex justify-between items-center mb-6">
          <h1 className="text-3xl font-bold text-gray-800">Admin Dashboard</h1>
          <button
            onClick={handleLogout}
            className="bg-red-500 hover:bg-red-600 text-white font-semibold py-2 px-4 rounded-md focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500 transition-all duration-200"
          >
            Logout
          </button>
        </div>

        <div className="w-full mb-6 p-6 bg-gray-50 rounded-lg shadow-inner border border-gray-200">
          <h2 className="text-xl font-semibold mb-4 text-gray-800">Filter & Search</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 mb-4">
            <div>
              <label htmlFor="filterEmail" className="block text-gray-700 text-sm font-medium mb-2">Email:</label>
              <input
                type="text"
                id="filterEmail"
                className="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-indigo-500 focus:border-transparent outline-none transition-all duration-200 text-gray-800"
                value={filterEmail}
                onChange={(e) => setFilterEmail(e.target.value)}
                placeholder="Filter by email"
              />
            </div>
            <div>
              <label htmlFor="filterFirstName" className="block text-gray-700 text-sm font-medium mb-2">First Name:</label>
              <input
                type="text"
                id="filterFirstName"
                className="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-indigo-500 focus:border-transparent outline-none transition-all duration-200 text-gray-800"
                value={filterFirstName}
                onChange={(e) => setFilterFirstName(e.target.value)}
                placeholder="Filter by first name"
              />
            </div>
            <div>
              <label htmlFor="filterLastName" className="block text-gray-700 text-sm font-medium mb-2">Last Name:</label>
              <input
                type="text"
                id="filterLastName"
                className="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-indigo-500 focus:border-transparent outline-none transition-all duration-200 text-gray-800"
                value={filterLastName}
                onChange={(e) => setFilterLastName(e.target.value)}
                placeholder="Filter by last name"
              />
            </div>
            <div>
              <label htmlFor="filterCountry" className="block text-gray-700 text-sm font-medium mb-2">Country:</label>
              <input
                type="text"
                id="filterCountry"
                className="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-indigo-500 focus:border-transparent outline-none transition-all duration-200 text-gray-800"
                value={filterCountry}
                onChange={(e) => setFilterCountry(e.target.value)}
                placeholder="Filter by country"
              />
            </div>
            <div className="md:col-span-2 lg:col-span-1">
              <label htmlFor="searchQuery" className="block text-gray-700 text-sm font-medium mb-2">General Search:</label>
              <input
                type="text"
                id="searchQuery"
                className="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-indigo-500 focus:border-transparent outline-none transition-all duration-200 text-gray-800"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                placeholder="Search all fields"
              />
            </div>
          </div>
          <button
            onClick={() => fetchWaitlistEntries(token!)}
            className="w-full bg-indigo-600 hover:bg-indigo-700 text-white font-semibold py-2 px-4 rounded-md focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 transition-all duration-200 flex items-center justify-center gap-2"
            disabled={isLoading}
          >
            {isLoading ? (
              <span className="flex items-center justify-center">
                <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                Applying Filters...
              </span>
            ) : (
              'Apply Filters'
            )}
          </button>
        </div>

        {isLoading && <p className="text-gray-700 flex items-center justify-center"><svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-gray-700" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"><circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle><path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path></svg>Loading waitlist entries...</p>}
        {error && <p className="text-red-600 animate-fade-in">{error}</p>}
        {!isLoading && !error && waitlistEntries.length === 0 && (
          <p className="text-gray-700">No waitlist entries found.</p>
        )}
        {!isLoading && !error && waitlistEntries.length > 0 && (
          <div className="overflow-x-auto w-full">
            <table className="min-w-full bg-white border border-gray-200 rounded-lg shadow-sm">
              <thead>
                <tr>
                  <th className="py-3 px-4 border-b border-gray-200 text-left text-sm font-semibold text-gray-700">Email</th>
                  <th className="py-3 px-4 border-b border-gray-200 text-left text-sm font-semibold text-gray-700">First Name</th>
                  <th className="py-3 px-4 border-b border-gray-200 text-left text-sm font-semibold text-gray-700">Last Name</th>
                  <th className="py-3 px-4 border-b border-gray-200 text-left text-sm font-semibold text-gray-700">Country</th>
                  <th className="py-3 px-4 border-b border-gray-200 text-left text-sm font-semibold text-gray-700">Joined At</th>
                </tr>
              </thead>
              <tbody>
                {waitlistEntries.map((entry) => (
                  <tr key={entry.id} className="hover:bg-gray-50 transition-colors duration-150">
                    <td className="py-2 px-4 border-b border-gray-200 text-gray-800">{entry.email}</td>
                    <td className="py-2 px-4 border-b border-gray-200 text-gray-800">{entry.first_name || 'N/A'}</td>
                    <td className="py-2 px-4 border-b border-gray-200 text-gray-800">{entry.last_name || 'N/A'}</td>
                    <td className="py-2 px-4 border-b border-gray-200 text-gray-800">{entry.country || 'N/A'}</td>
                    <td className="py-2 px-4 border-b border-gray-200 text-gray-800">{new Date(entry.created_at).toLocaleString()}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </main>
  );
}
