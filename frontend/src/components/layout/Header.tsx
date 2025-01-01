import ProfilePhotoWrapper from "../layout/ProfilePhotoWrapper";
import Logo from "./Logo.tsx";

const Header = () => {
  return (
    <header className="layout__header">
      <Logo />
      <ProfilePhotoWrapper user={undefined} />
    </header>
  );
};

export default Header;