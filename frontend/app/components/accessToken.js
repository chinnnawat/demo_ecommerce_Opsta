'use client';

import { useSession } from "next-auth/react";
import { useEffect, useState } from 'react';


export default function AccessToken() {

  // send token
  const { data: session, status } = useSession();
  const [response, setResponse] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (session && session.accessToken) {
      const sendTokenToBackend = async () => {
        try {
            const response = await fetch(`http://localhost:8000/get_user_info/`, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
              'Authorization': `Bearer ${session.accessToken}`, // Sending token in the Authorization header
            },
            body: JSON.stringify({}),
          });

          // if (!response.ok) {
          //   throw new Error('Failed to send access token');
          // }

          const data = await response.json();
          setResponse(data);
        } catch (error) {
          setError(error.message);
          console.error('Error:', error);
        }
      };

      sendTokenToBackend();
    }
  }, [session]);

  if (status === 'loading') {
    return <div>Loading...</div>;
  }

  if (!session) {
    return <div>You need to be authenticated to view this content.</div>;
  }


  // send data user to backend <name, lastname, email>
  


  return (
    <div>
      <p>Access Token: {session.accessToken}</p>
      {error && <div>Error: {error}</div>}
      {response && <div>Response from backend: {JSON.stringify(response)}</div>}
      {session.user?.email}
    </div>
  );
}
