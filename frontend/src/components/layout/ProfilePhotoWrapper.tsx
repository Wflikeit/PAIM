import { useState } from 'react';
import Popover from '@mui/material/Popover';
import {red} from "@mui/material/colors";
//
// import { getInitialsFromEmail } from '../reservation/ReservationUtils';
//
// import { useCustomNavigation } from 'src/hooks/NavigationHook';
// import { LoggedInUser, TOKEN_KEY } from 'src/auth/authService';
// import { randomColorFor } from 'src/values/colors';

export interface LoggedInUser {
    email: string;
    role: string;
}
export default function ProfilePhotoWrapper({ user }: { user?: LoggedInUser }) {
    const [anchorEl, setAnchorEl] = useState<HTMLButtonElement | null | undefined>(null);
    // const { navigateToLoginPage } = useCustomNavigation();

    const handleClick = (event: React.MouseEvent<HTMLButtonElement>) => {
        setAnchorEl(event.currentTarget);
    };

    // const handleLogoutClick = () => {
    //     localStorage.removeItem(TOKEN_KEY);
    //     navigateToLoginPage();
    // };

    const handleClose = () => {
        setAnchorEl(null);
    };

    const open = Boolean(anchorEl);
    const id = open ? 'simple-popover' : undefined;

    // const avatarColor = randomColorFor(user?.email as string);

    return (
        <div className="icon__wrapper">
            <button className="photo__wrapper" style={{ backgroundColor: `${red}` }} onClick={handleClick}>
                {user ? "WF" : null}
            </button>

            <Popover
                id={id}
                open={open}
                anchorEl={anchorEl}
                onClose={handleClose}
                anchorOrigin={{
                    vertical: 'bottom',
                    horizontal: 'right',
                }}
                transformOrigin={{
                    vertical: 'top',
                    horizontal: 'right',
                }}
                sx={{
                    marginTop: '1.3rem',
                    borderRadius: '1rem !important',
                }}
            >
                {/*<button className="sign__out__button" onClick={handleLogoutClick}>*/}
                {/*    Sign out*/}
                {/*</button>*/}
                <button className="sign__out__button" >
                    Sign out
                </button>
            </Popover>
        </div>
    );
}
