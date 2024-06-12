import GoogleProvider from "./ui/AuthGoogle";
import ProductAll from "./ui/Products";
import AccessToken from "./components/accessToken";
import SendUserDataToLoginAPI from "./components/sendData";

export default function Home() {
  return (
    <div>
      <ProductAll />
      <SendUserDataToLoginAPI />
    </div>
  );
}
