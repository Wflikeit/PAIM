import React, {useEffect, useMemo} from "react";
import UserActionsWrapper from "./UserActionsWrapper.tsx";
import Logo from "./Logo.tsx";
import HeaderLink from "./HeaderLink.tsx";
import {getUserFromToken} from "../../auth/authService.ts";

const Header: React.FC = () => {
    // const [user, setUser] = useState<LoggedInUser | undefined>();
    //
    // useEffect(() => {
    //     const token = localStorage.getItem("access_token");
    //     const role = localStorage.getItem("user_role");
    //     const fullname = localStorage.getItem("fullname");
    //
    //     if (token && role && fullname) {
    //         setUser({ token, role, fullname });
    //     }
    // }, []);
  const user = useMemo(() => getUserFromToken(), []);
    useEffect(() => {
      console.log(user)

    }, [user]);


    return (
        <header className="layout__header">
            <Logo />
            <div
                style={{
                    display: "flex",
                    color: "blue",
                    gap: "2rem",
                    alignItems: "center",
                }}
            >
                <HeaderLink to="/" text="Home" />
                <HeaderLink to="/contact" text="Contact" />
                <HeaderLink to="/about" text="About" />
                <HeaderLink to="/" text="Products" />
            </div>
            <UserActionsWrapper user={user} />
        </header>
    );
};

export default Header;
