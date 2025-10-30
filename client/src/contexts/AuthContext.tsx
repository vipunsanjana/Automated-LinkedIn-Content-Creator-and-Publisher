import { createContext, useContext, useEffect, useState, ReactNode } from "react";
import axios from "axios";

interface User {
  id: string;
  name: string;
  email: string;
  accessToken: string;
}

interface AuthContextType {
  user: User | null;
  loading: boolean;
  signInWithLinkedIn: () => void;
  signOut: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider = ({ children }: { children: ReactNode }) => {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(false);

  const signInWithLinkedIn = () => {
    const clientId = import.meta.env.VITE_LINKEDIN_CLIENT_ID;
    const redirectUri = import.meta.env.VITE_LINKEDIN_REDIRECT_URI;
    const scope = "openid profile email";
    const state = crypto.randomUUID();

    // Step 1: Redirect user to LinkedIn auth page
    const authUrl = `https://www.linkedin.com/oauth/v2/authorization?response_type=code&client_id=${clientId}&redirect_uri=${encodeURIComponent(
      redirectUri
    )}&scope=${encodeURIComponent(scope)}&state=${state}`;

    localStorage.setItem("linkedin_state", state);
    window.location.href = authUrl;
  };

  const handleLinkedInCallback = async () => {
    const params = new URLSearchParams(window.location.search);
    const code = params.get("code");
    const state = params.get("state");

    if (!code || !state) return;

    const savedState = localStorage.getItem("linkedin_state");
    if (state !== savedState) {
      console.error("Invalid OAuth state");
      return;
    }

    setLoading(true);
    try {
      // Step 2: Exchange code for access token via backend
      const response = await axios.post(`${import.meta.env.VITE_BACKEND_URL}/auth/linkedin/token`, {
        code,
        redirect_uri: import.meta.env.VITE_LINKEDIN_REDIRECT_URI,
      });

      const { access_token } = response.data;

      // Step 3: Get user info from backend (or directly from LinkedIn)
      const userInfo = await axios.get(`${import.meta.env.VITE_BACKEND_URL}/auth/linkedin/me`, {
        headers: { Authorization: `Bearer ${access_token}` },
      });

      setUser({
        id: userInfo.data.id,
        name: userInfo.data.name,
        email: userInfo.data.email,
        accessToken: access_token,
      });

      // Clean up
      localStorage.removeItem("linkedin_state");
      window.history.replaceState({}, document.title, "/");
    } catch (error) {
      console.error("LinkedIn login error:", error);
    } finally {
      setLoading(false);
    }
  };

  const signOut = () => {
    setUser(null);
    localStorage.removeItem("linkedin_state");
  };

  useEffect(() => {
    if (window.location.pathname === "/auth/callback") {
      handleLinkedInCallback();
    }
  }, []);

  return (
    <AuthContext.Provider value={{ user, loading, signInWithLinkedIn, signOut }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
};
