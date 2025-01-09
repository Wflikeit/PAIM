import React, {useEffect, useMemo} from 'react';

import { UserRole } from './UserRole';
import {LoggedInUser, getUserFromToken, checkTokenValidity} from './authService';
import NotFound from "../pages/NotFound.tsx";
import {useCustomNavigation} from "../hooks/useCustomNavigation.ts";
import useUnauthorizedRedirect from "../hooks/useUnathorizedRedirect.tsx";

type ProtectedRouteWrapperProps = {
  allowedRoles: UserRole[];
  children: React.ReactElement;
};

export const ProtectedRouteWrapper: React.FC<ProtectedRouteWrapperProps> = ({ allowedRoles, children }) => {
  const user: LoggedInUser | undefined = useMemo(() => getUserFromToken(), []);

  const { navigateToLoginPage } = useCustomNavigation();

  useEffect(() => {
    // Start token validity checking loop.
    console.log("checkTokenValidity(navigateToLoginPage)");
    checkTokenValidity(navigateToLoginPage);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  // Add axios interceptor for 401 responses.
  useUnauthorizedRedirect();


  const hasValidRole: boolean = useMemo(() => {
    if (!user) {
      navigateToLoginPage();
      return false;
    }
    return allowedRoles.includes(user?.role as UserRole);
  }, [navigateToLoginPage, allowedRoles, user]);

  if (!hasValidRole) {
    return <NotFound />;
  }

  return children;
};

export const EnsureAuth = () => {

};