'use client'
import { useSession, signIn, signOut } from "next-auth/react"

export default function GoogleProvider(){
    const {data: session} = useSession()

    


    // sign in success
    if(session){
        return (
            <div>
                <p>Welcome {session.user?.name}. Signed In As</p>
                <p>{session.user?.email}</p>
                <img src={session.user?.image} alt={session.user?.name} />
                <button onClick={() => signOut()}>Sign out</button>
            </div>
        )
    }
    // not signin
    else{
        return(
            <div>
                <p>Not Signed In</p>
                <button onClick={() => signIn('google')}>Sign in with google</button>
            </div>
        )
    }

}