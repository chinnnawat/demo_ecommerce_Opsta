// page.js
import GoogleProvider from "./ui/AuthGoogle";
import ProductAll from "./ui/Products";
import AccessToken from "./components/accessToken";

export default function Home() {
  return(
    <div>
      <GoogleProvider/>
      <ProductAll/>
      <AccessToken/>
    </div>
  )
}
