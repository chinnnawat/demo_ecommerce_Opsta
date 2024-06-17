'use client'
import { useSession } from "next-auth/react";
import { useEffect, useState } from 'react';

export default function CArtDetailFromBackend(){
    const { data: session, status } = useSession();
    useEffect(() => {
        if(session && session.accessToken){
            const CArtDetailFromBackend = async() => {
                try {
                    const userData = {
                        email: session.user?.email,
                    };
                    const response = await fetch (`${process.env.NEXT_PUBLIC_API_SHOW_CART}`, {
                        method: "POST",
                        headers: {
                            'Content-Type': 'application/json',
                            'Authorization': `Bearer ${session.accessToken}`, // Sending token in the Authorization header
                          },
                        body: JSON.stringify({userData}),
                    } )

                    const data = await response.json();
                    console.log(data);
                }
                catch(error){
                    setError(error.message);
                    console.error('Error:', error);
                }
            };
            CArtDetailFromBackend
    }}, [session])
}