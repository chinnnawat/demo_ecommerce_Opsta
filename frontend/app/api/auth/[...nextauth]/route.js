
// imports
import NextAuth from "next-auth";

// importing providers
import GoogleProvider from "next-auth/providers/google";

const authOptions = NextAuth({
    providers: [
        GoogleProvider({
            clientId: process.env.GOOGLE_CLIENT_ID || '',
            clientSecret: process.env.GOOGLE_CLIENT_SECRET || '',
        })
    ],
    callbacks: {
        async jwt ({ token, account }) {
            if (account) {
                token.accessToken = account.access_token;
            }
            return token;
        },
        async session({ session, token, user }) {
            session.accessToken = token.accessToken;
            return session;
        }
    }
});

export { authOptions as GET, authOptions as POST };








