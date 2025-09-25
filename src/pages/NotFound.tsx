import { useLocation, NavLink } from "react-router-dom";
import { useEffect } from "react";

const NotFound = () => {
  const location = useLocation();

  useEffect(() => {
    console.error("404 Error: User attempted to access non-existent route:", location.pathname);
  }, [location.pathname]);

  return (
    <div className="flex min-h-screen items-center justify-center bg-background">
      <div className="text-center medical-card p-8 max-w-md">
        <h1 className="mb-4 text-4xl font-bold">404</h1>
        <p className="mb-4 text-xl text-muted-foreground">Oops! Page not found</p>
        <NavLink to="/" className="inline-block">
          <button className="bg-gradient-primary text-primary-foreground px-6 py-2 rounded-lg hover:opacity-90 transition-opacity">
            Return to Home
          </button>
        </NavLink>
      </div>
    </div>
  );
};

export default NotFound;
