import React, { useState } from 'react';

export default function Auth({ onLoginSuccess }) {
  // 1. Role Toggle State Mapping (Based on Screenshot 2026-06-01 at 8.03.32 PM.jpg options)
  const [userRole, setUserRole] = useState('user'); // 'user' or 'admin'

  // 2. Form Input States
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [rememberMe, setRememberMe] = useState(false);
  const [showPassword, setShowPassword] = useState(false);

  // 3. Status Handling States
  const [isLoading, setIsLoading] = useState(false);
  const [errorMessage, setErrorMessage] = useState('');

  const handleFormSubmit = async (e) => {
    e.preventDefault();

    setIsLoading(true);
    setErrorMessage('');

    try {
      // Use URLSearchParams to send application/x-www-form-urlencoded
      // This is the standard for OAuth2 and more compatible with FastAPI's Form parsing
      const params = new URLSearchParams();
      params.append("username", email); // OAuth2 spec uses 'username'
      params.append("password", password);

      const response = await fetch(
        "http://localhost:8000/api/v1/auth/login/access-token",
        {
          method: "POST",
          body: params,
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.detail || "Invalid credentials"
        );
      }

      // Save token
      localStorage.setItem(
        "access_token",
        data.access_token
      );

      // Save login state
      localStorage.setItem(
        "isAuthenticated",
        "true"
      );

      onLoginSuccess();

    } catch (error) {
      setErrorMessage(
        error.message || "Login failed"
      );
    } finally {
      setIsLoading(false);
    }
  };

  const handleSSOLogin = () => {
    console.log("Redirecting system engine to external Tenant SSO Identity Provider integration route...");
  };

  return (
    <div className="min-h-screen bg-slate-950 text-white flex flex-col md:flex-row items-center justify-center p-6 md:p-12 gap-12">

      {/* LEFT BRAND SECTION METADATA */}
      <div className="w-full md:w-1/2 space-y-6">
        <div className="flex items-center gap-2 text-rose-500 font-bold text-xl">
          <div className="w-4 h-4 bg-rose-500 transform rotate-45"></div>
          <span>Project Hub AI</span>
        </div>

        <div className="space-y-2">
          <span className="text-xs font-semibold tracking-wider text-rose-400 bg-rose-500/10 px-2.5 py-1 rounded">
            AI-POWERED L&D MANAGEMENT
          </span>
          <h2 className="text-4xl font-extrabold tracking-tight md:text-5xl">
            Smarter Learning.<br />
            <span className="text-rose-500">Stronger Teams.</span>
          </h2>
          <p className="text-sm text-slate-400 max-w-sm">
            Unify learning, projects, and performance in one AI-powered platform built for the future.
          </p>
        </div>

        {/* Feature Counters Stats Rows */}
        <div className="grid grid-cols-3 gap-4 max-w-md pt-4">
          <div className="bg-slate-900/60 p-4 rounded-xl border border-slate-800">
            <div className="font-bold text-lg">100+</div>
            <div className="text-xs text-slate-500">Active Users</div>
          </div>
          <div className="bg-slate-900/60 p-4 rounded-xl border border-slate-800">
            <div className="font-bold text-lg">2K+</div>
            <div className="text-xs text-slate-500">Courses Completed</div>
          </div>
          <div className="bg-slate-900/60 p-4 rounded-xl border border-slate-800">
            <div className="font-bold text-lg">98%</div>
            <div className="text-xs text-slate-500">Satisfaction Rate</div>
          </div>
        </div>
      </div>

      {/* RIGHT INTERACTIVE AUTHENTICATION FRAME CONSOLE */}
      <div className="w-full md:w-1/2 max-w-md bg-slate-900/40 p-8 rounded-2xl border border-slate-800/80 backdrop-blur-md">
        <div className="text-center mb-6">
          <h3 className="text-xl font-bold">Welcome back</h3>
          <p className="text-xs text-slate-500">Sign in to continue to Project Hub AI</p>
        </div>

        {/* Functional Role Toggle State Switcher Controller */}
        <div className="flex bg-slate-950 p-1 rounded-lg border border-slate-800 mb-6">
          <button
            type="button"
            onClick={() => setUserRole('user')}
            className={`flex-1 text-center py-2 rounded-md text-xs font-medium transition-all ${userRole === 'user' ? 'bg-slate-800 text-white shadow-sm' : 'text-slate-500 hover:text-slate-300'}`}
          >
            Regular User
          </button>
          <button
            type="button"
            onClick={() => setUserRole('admin')}
            className={`flex-1 text-center py-2 rounded-md text-xs font-medium transition-all ${userRole === 'admin' ? 'bg-rose-500 text-white shadow-sm' : 'text-slate-500 hover:text-slate-300'}`}
          >
            Admin
          </button>
        </div>

        {errorMessage && (
          <div className="bg-rose-500/10 border border-rose-500/20 text-rose-400 p-3 rounded-lg text-xs mb-4">
            {errorMessage}
          </div>
        )}

        <form onSubmit={handleFormSubmit} className="space-y-4">
          <div>
            <label className="block text-xs font-medium text-slate-400 mb-1">Email address</label>
            <input
              type="email"
              required
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="Enter your email"
              className="w-full px-3 py-2 bg-slate-950 border border-slate-800 rounded-lg text-xs focus:outline-none focus:border-rose-500 transition-colors text-white"
            />
          </div>

          <div>
            <label className="block text-xs font-medium text-slate-400 mb-1">Password</label>
            <div className="relative">
              <input
                type={showPassword ? "text" : "password"}
                required
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="Enter your password"
                className="w-full px-3 py-2 bg-slate-950 border border-slate-800 rounded-lg text-xs focus:outline-none focus:border-rose-500 transition-colors text-white pr-10"
              />
              <button
                type="button"
                onClick={() => setShowPassword(!showPassword)}
                className="absolute right-3 top-2.5 text-slate-500 hover:text-slate-300 text-xs"
              >
                {showPassword ? "Hide" : "Show"}
              </button>
            </div>
          </div>

          <div className="flex items-center justify-between text-xs pt-1">
            <label className="flex items-center gap-2 cursor-pointer select-none text-slate-400">
              <input
                type="checkbox"
                checked={rememberMe}
                onChange={(e) => setRememberMe(e.target.checked)}
                className="rounded bg-slate-950 border-slate-800 accent-rose-500 focus:ring-0"
              />
              <span>Remember me</span>
            </label>
            <button type="button" className="text-rose-400 hover:underline">Forgot password?</button>
          </div>

          <button
            type="submit"
            disabled={isLoading}
            className="w-full bg-rose-500 hover:bg-rose-600 disabled:bg-rose-500/50 text-white font-medium text-xs py-2.5 rounded-lg transition-colors flex items-center justify-center gap-2 mt-2 shadow-lg shadow-rose-500/10"
          >
            {isLoading ? "Authenticating Platform Node..." : "Sign in →"}
          </button>
        </form>

        <div className="relative flex py-4 items-center justify-center text-slate-600 text-[10px] uppercase font-bold tracking-wider">
          <div className="flex-grow border-t border-slate-800/80"></div>
          <span className="flex-shrink mx-3">OR</span>
          <div className="flex-grow border-t border-slate-800/80"></div>
        </div>

        {/* SSO Integration Interface Trigger */}
        <button
          type="button"
          onClick={handleSSOLogin}
          className="w-full text-left p-3 bg-slate-950/80 border border-slate-800 rounded-lg hover:border-slate-700 transition-colors flex items-center justify-between"
        >
          <div>
            <div className="text-xs font-medium">Sign in with SSO</div>
            <div className="text-[10px] text-slate-500">Use your organization's single sign on</div>
          </div>
          <span className="text-slate-500 text-sm">→</span>
        </button>

        <div className="text-center mt-6 text-[11px] text-slate-500">
          Need help? <button type="button" className="text-rose-400 hover:underline">Contact your administrator</button>
        </div>
      </div>

    </div>
  );
}