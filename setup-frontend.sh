#!/bin/bash
# Script to set up the frontend with auth-service integration

# Copy the API utility to the frontend
cp /home/bhumit-singh/Tracklore/auth-service/api-utils.ts /home/bhumit-singh/Tracklore/frontend/src/lib/api-utils.ts

# Update the login page
cat > /home/bhumit-singh/Tracklore/frontend/src/app/login/page.tsx << 'EOF'
"use client";

import React, { useState } from 'react';
import { motion } from 'framer-motion';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import { apiCall } from '@/lib/api-utils';

const LoginPage = () => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const router = useRouter();

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setError('');

        try {
            const res = await apiCall('/auth/login', {
                method: 'POST',
                body: JSON.stringify({ username, password }),
            });

            if (res.ok) {
                const data = await res.json();
                // Store the tokens in localStorage or a secure cookie
                localStorage.setItem('access_token', data.access_token);
                localStorage.setItem('refresh_token', data.refresh_token);
                router.push('/');
            } else {
                const data = await res.json();
                setError(data.detail || 'Something went wrong');
            }
        } catch (error) {
            setError('Something went wrong');
        }
    };

    return (
        <div className="min-h-screen bg-gray-900 text-white flex flex-col justify-center items-center">
            <motion.div
                initial={{ opacity: 0, y: -20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5 }}
                className="w-full max-w-md p-8 space-y-6 bg-gray-800 rounded-xl shadow-lg"
            >
                <div className="text-center">
                    <h1 className="text-3xl font-bold">Log In to Tracklore</h1>
                    <p className="text-gray-400">Welcome back! Please enter your details.</p>
                </div>
                <form className="space-y-6" onSubmit={handleSubmit}>
                    <div>
                        <label className="block text-sm font-medium text-gray-300" htmlFor="username">
                            Username
                        </label>
                        <input
                            className="w-full px-3 py-2 mt-1 text-gray-900 bg-gray-200 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                            id="username"
                            name="username"
                            type="text"
                            autoComplete="username"
                            required
                            value={username}
                            onChange={(e) => setUsername(e.target.value)}
                        />
                    </div>
                    <div>
                        <label className="block text-sm font-medium text-gray-300" htmlFor="password">
                            Password
                        </label>
                        <input
                            className="w-full px-3 py-2 mt-1 text-gray-900 bg-gray-200 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                            id="password"
                            name="password"
                            type="password"
                            autoComplete="current-password"
                            required
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                        />
                    </div>
                    {error && <p className="text-red-500 text-sm">{error}</p>}
                    <button
                        className="w-full py-3 font-semibold text-white bg-blue-600 rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-offset-gray-800 focus:ring-blue-500 transition-colors"
                        type="submit"
                    >
                        Log In
                    </button>
                </form>
                <div className="text-center text-gray-400">
                    <p>
                        Don't have an account?{' '}
                        <Link href="/signup" className="font-medium text-blue-400 hover:text-blue-300">
                            Sign Up
                        </Link>
                    </p>
                </div>
            </motion.div>
        </div>
    );
};

export default LoginPage;
EOF

# Update the signup page
cat > /home/bhumit-singh/Tracklore/frontend/src/app/signup/page.tsx << 'EOF'
"use client";

import React, { useState } from 'react';
import { motion } from 'framer-motion';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import { apiCall } from '@/lib/api-utils';

const SignupPage = () => {
    const [username, setUsername] = useState('');
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const router = useRouter();

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setError('');

        try {
            const res = await apiCall('/auth/signup', {
                method: 'POST',
                body: JSON.stringify({ username, email, password }),
            });

            if (res.ok) {
                router.push('/login');
            } else {
                const data = await res.json();
                setError(data.detail || 'Something went wrong');
            }
        } catch (error) {
            setError('Something went wrong');
        }
    };

    return (
        <div className="min-h-screen bg-gray-900 text-white flex flex-col justify-center items-center">
            <motion.div
                initial={{ opacity: 0, y: -20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5 }}
                className="w-full max-w-md p-8 space-y-6 bg-gray-800 rounded-xl shadow-lg"
            >
                <div className="text-center">
                    <h1 className="text-3xl font-bold">Create an Account</h1>
                    <p className="text-gray-400">Join Tracklore to start your musical journey.</p>
                </div>
                <form className="space-y-6" onSubmit={handleSubmit}>
                    <div>
                        <label className="block text-sm font-medium text-gray-300" htmlFor="username">
                            Username
                        </label>
                        <input
                            className="w-full px-3 py-2 mt-1 text-gray-900 bg-gray-200 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                            id="username"
                            name="username"
                            type="text"
                            autoComplete="username"
                            required
                            value={username}
                            onChange={(e) => setUsername(e.target.value)}
                        />
                    </div>
                    <div>
                        <label className="block text-sm font-medium text-gray-300" htmlFor="email">
                            Email
                        </label>
                        <input
                            className="w-full px-3 py-2 mt-1 text-gray-900 bg-gray-200 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                            id="email"
                            name="email"
                            type="email"
                            autoComplete="email"
                            required
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                        />
                    </div>
                    <div>
                        <label className="block text-sm font-medium text-gray-300" htmlFor="password">
                            Password
                        </label>
                        <input
                            className="w-full px-3 py-2 mt-1 text-gray-900 bg-gray-200 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                            id="password"
                            name="password"
                            type="password"
                            autoComplete="new-password"
                            required
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                        />
                    </div>
                    {error && <p className="text-red-500 text-sm">{error}</p>}
                    <button
                        className="w-full py-3 font-semibold text-white bg-blue-600 rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-offset-gray-800 focus:ring-blue-500 transition-colors"
                        type="submit"
                    >
                        Sign Up
                    </button>
                </form>
                <div className="text-center text-gray-400">
                    <p>
                        Already have an account?{' '}
                        <Link href="/login" className="font-medium text-blue-400 hover:text-blue-300">
                            Log In
                        </Link>
                    </p>
                </div>
            </motion.div>
        </div>
    );
};

export default SignupPage;
EOF

# Create the Dockerfile for frontend
cat > /home/bhumit-singh/Tracklore/frontend/Dockerfile << 'EOF'
# Use Node.js 18 as base image
FROM node:18-alpine

# Set working directory
WORKDIR /app

# Copy package.json and package-lock.json
COPY package*.json ./

# Install dependencies
RUN npm ci

# Copy the rest of the application
COPY . .

# Build the Next.js application
RUN npm run build

# Expose port 3000
EXPOSE 3000

# Start the application
CMD ["npm", "start"]
EOF

echo "Frontend setup completed successfully!"