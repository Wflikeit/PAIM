import { useEffect } from "react";
import { checkTokenValidity } from "./authService.ts";
import useUnauthorizedRedirect from "../hooks/useUnathorizedRedirect.tsx";
import { useCustomNavigation } from "../hooks/useCustomNavigation.ts";

export const EnsureAuth = () => {
  const { navigateToLoginPage } = useCustomNavigation();

  useEffect(() => {
    // Start token validity checking loop.
    console.log("checkTokenValidity(navigateToLoginPage)");
    checkTokenValidity(navigateToLoginPage);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  // Add axios interceptor for 401 responses.
  useUnauthorizedRedirect();

  return <></>;
};