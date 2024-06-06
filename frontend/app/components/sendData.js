'use client'

import { useSession } from "next-auth/react";
import { useEffect, useState } from 'react';

export default function SendUserDataToLoginAPI(){
    const {data: session, status} = useSession();
    const [response, setResponse] = useState(null);
    const [error, setError] = useState(null);

    useEffect(() => {
        if (session && session.accessToken){
            const sendTokenToBackend = async() => {
                try {
                    const [firstName, lastName] = session.user?.name.split(" ");
                    const userData = {
                        email: session.user?.email,
                        firstName: firstName,
                        lastName: lastName
                    };
                    const response = await fetch ('http://localhost:8000/api/login/', {
                        method: "POST",
                        headers: {
                            'Content-Type': 'application/json',
                            'Authorization': `Bearer ${session.accessToken}`, // Sending token in the Authorization header
                          },
                        body: JSON.stringify({userData}),
                    })

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

    return(
        <div>
            {response && <div>Response from backend: {JSON.stringify(response)}</div>}
        </div>
    )
}