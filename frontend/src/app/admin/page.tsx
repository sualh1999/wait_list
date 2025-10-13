"use client";

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import Form from '@/components/Form';

interface WaitlistEntry {
  id: string;
  email: string;
  created_at: string;
}

export default function AdminPage() {
  const [password, setPassword] = useState('');
  const [token, setToken] = useState<string | null>(null);
  const [message, setMessage] = useState('');
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [waitlistEntries, setWaitlistEntries] = useState<WaitlistEntry[]>([]);
  const router = useRouter();

  useEffect(() => {
    const storedToken = sessionStorage.getItem('admin_token');
    if (storedToken) {
      setToken(storedToken);
      fetchWaitlistEntries(storedToken);
    }
  }, []);

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
        setError(errorData.detail || 'Login failed.');
      }
    } catch (err) {
      setError('Network error. Please try again later.');
    } finally {
      setIsLoading(false);
    }
  };

  const fetchWaitlistEntries = async (authToken: string) => {
    setIsLoading(true);
    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/admin/list`, {
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
        setError(errorData.detail || 'Failed to fetch waitlist entries.');
      }
    } catch (err) {
      setError('Network error while fetching entries.');
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
      <main className="flex min-h-screen flex-col items-center justify-center p-24 bg-gray-100">
        <div className="z-10 w-full max-w-md items-center justify-between font-mono text-sm lg:flex flex-col bg-white p-8 rounded-lg shadow-md">
          <h1 className="text-2xl font-bold mb-6 text-center text-gray-800">Admin Login</h1>
          <Form onSubmit={handleLogin}>
            <div className="mb-4">
              <label htmlFor="password" className="block text-gray-700 text-sm font-bold mb-2">
                Password:
              </label>
              <input
                type="password"
                id="password"
                className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                placeholder="Enter admin password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
              />
            </div>
            <button
              type="submit"
              className="bg-green-500 hover:bg-green-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline w-full"
              disabled={isLoading}
            >
              {isLoading ? 'Logging in...' : 'Login'}
            </button>
          </Form>
          {message && <p className="mt-4 text-green-600 text-center">{message}</p>}
          {error && <p className="mt-4 text-red-600 text-center">{typeof error === 'object' && error !== null && 'detail' in error ? (error as any).detail : error}</p>}
        </div>
      </main>
    );
  }

  return (
    <main className="flex min-h-screen flex-col items-center p-24 bg-gray-100">
      <div className="z-10 w-full max-w-3xl items-center justify-between font-mono text-sm lg:flex flex-col bg-white p-8 rounded-lg shadow-md">
        <h1 className="text-2xl font-bold mb-6 text-center text-gray-800">Admin Dashboard</h1>
        <button
          onClick={handleLogout}
          className="bg-red-500 hover:bg-red-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline mb-6"
        >
          Logout
        </button>
        {isLoading && <p>Loading waitlist entries...</p>}
        {error && <p className="text-red-600">{typeof error === 'object' && error !== null && 'detail' in error ? (error as any).detail : error}</p>}
        {!isLoading && !error && waitlistEntries.length === 0 && (
          <p>No waitlist entries found.</p>
        )}
        {!isLoading && !error && waitlistEntries.length > 0 && (
          <div className="overflow-x-auto w-full">
            <table className="min-w-full bg-white border border-gray-200">
              <thead>
                <tr>
                  <th className="py-2 px-4 border-b text-left text-gray-600">Email</th>
                  <th className="py-2 px-4 border-b text-left text-gray-600">Joined At</th>
                </tr>
              </thead>
              <tbody>
                {waitlistEntries.map((entry) => (
                  <tr key={entry.id}>
                    <td className="py-2 px-4 border-b text-gray-800">{entry.email}</td>
                    <td className="py-2 px-4 border-b text-gray-800">{new Date(entry.created_at).toLocaleString()}</td>
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
