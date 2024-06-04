'use client';

import { useSession, signIn, signOut } from "next-auth/react";

export default function AccessToken() {
  const { data: session } = useSession();

  if (!session) {
    return <div>Loading...</div>;
  }

  const { accessToken, refreshToken } = session;

  return <div>
    <p>Access Token: {accessToken}</p>
    {/* <p>Refresh Token: {refreshToken}</p>  */}
    </div>;
}
