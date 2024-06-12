'use client'
import { useSession, signIn, signOut } from "next-auth/react"
import { useState } from 'react'


// async function getUserID() {
//     const res = await fetch('https://api.example.com/...')
//     // The return value is *not* serialized
//     // You can return Date, Map, Set, etc.
   
//     if (!res.ok) {
//       // This will activate the closest `error.js` Error Boundary
//       throw new Error('Failed to fetch data')
//     }
   
//     return res.json()
//   }


export default function NavBar() {
    const { data: session } = useSession()
    const [dropdownOpen, setDropdownOpen] = useState(false)
    const [activeLink, setActiveLink] = useState('')

    const toggleDropdown = () => {
        setDropdownOpen(!dropdownOpen)
    }


    


    const handleLinkClick = (link) => {
        setActiveLink(link)
    }

    const handleToCart = async () => {
        // console.log("hi");
        if (!session || !session.user) {
            console.error('No user session found');
            return;
        }

        const data = {
            user: session.user?.email,  // User email
        };
        console.log(data);

        try {
            const response = await fetch('http://localhost:8000/api/show_cart/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data),
            });
            if (!response.ok) {
                throw new Error('Failed to show cart');
            }

            const dataUser = await response.json();
            console.log('Success:', dataUser);
        } catch (error) {
            console.error('Error:', error);
        }
        
        
    }

    return (
        <nav className="bg-[#FF7F3E] border-gray-200">
            <div className="max-w-screen-xl flex flex-wrap items-center justify-between mx-auto p-4 mb-3">
                <a href="/" className="flex items-center space-x-3 rtl:space-x-reverse">
                    <img src="https://www.urbanbrush.net/web/wp-content/uploads/edd/2021/06/urbanbrush-20210617095846219755.jpg" alt="duck-logo" className="h-8" />
                    <span className="self-center text-2xl font-semibold whitespace-nowrap"></span>
                </a>

                <form className="w-[600px]">
                        <label for="default-search" className="mb-2 text-sm font-medium text-gray-900 sr-only">Search</label>
                        <div className="relative">
                            <div className="absolute inset-y-0 start-0 flex items-center ps-3 pointer-events-none">
                                <svg className="w-4 h-4 text-gray-500" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 20 20">
                                    <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="m19 19-4-4m0-7A7 7 0 1 1 1 8a7 7 0 0 1 14 0Z" />
                                </svg>
                            </div>
                        <input type="search" id="default-search" class="block w-full p-4 ps-10 text-sm text-gray-900 border border-gray-300 rounded-lg bg-gray-50 focus:ring-blue-500 focus:border-blue-500 " placeholder="Search Mockups, Logos..." required />
                        {/* <button type="submit" class="text-white absolute end-2.5 bottom-2.5 bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-sm px-4 py-2 ">Search</button> */}
                    </div>
                </form>
                
                {session ? (
                    <div className="flex items-center md:order-2 space-x-3 md:space-x-0 rtl:space-x-reverse relative">
                        <button 
                            type="button" 
                            className="flex text-sm bg-gray-800 rounded-full md:me-0 focus:ring-4 focus:ring-gray-300" 
                            id="user-menu-button" 
                            aria-expanded={dropdownOpen ? "true" : "false"} 
                            onClick={toggleDropdown}
                        >
                            <span className="sr-only">Open user menu</span>
                            <img className="w-8 h-8 rounded-full" src={session.user?.image} alt="user photo" />
                        </button>

                        <div className="absolute top-12 right-0 z-50 my-4 text-base list-none bg-white divide-y divide-gray-100 rounded-lg shadow" id="user-dropdown">
                            {/* Dropdown Menu */}
                            {dropdownOpen && (
                                <div>
                                    <div className="px-4 py-3 text-left">
                                        <span className="block text-sm text-gray-900">{session.user?.name}</span>
                                        <span className="block text-sm text-gray-500 truncate dark:text-gray-400">{session.user?.email}</span>
                                    </div>
                                    <div className="py-2">
                                        <li>
                                            <a href="/profile" className="block px-4 py-2 text-sm text-gray-700  hover:bg-[#FF7F3E] hover:text-white">
                                                Profile
                                            </a>
                                        </li>
                                        <li>
                                            <button 
                                                onClick={() => signOut()} 
                                                className="block w-full px-4 py-2 text-sm text-gray-700 hover:bg-[#FF7F3E] hover:text-white text-left"
                                            >
                                                Sign out
                                            </button>
                                        </li>
                                    </div>
                                </div>
                            )}
                        </div>
                        
                    </div>
                ) : (
                    <div className="flex items-center md:order-2 space-x-3 md:space-x-0 rtl:space-x-reverse relative">
                        <button onClick={() => signIn()} className="text-[#e4c549]">
                            Login
                        </button>
                    </div>
                )}
                <div className="item-center justify-between hidden w-full md:flex md:w-auto md:order-1" id="navbar-user">
                    <ul className="flex flex-col font-medium p-4 md:p-0 mt-4 border border-gray-100 rounded-lg  md:space-x-8 rtl:space-x-reverse md:flex-row md:mt-0 md:border-0 text-white">
                        <li>
                            <a 
                                href="/" 
                                className={`block py-2 px-3 text-white rounded md:bg-transparent md:p-0 ${activeLink === 'home' ? 'text-yellow-300' : ''}`} 
                                onClick={() => handleLinkClick('home')}
                                aria-current="page"
                            >
                                Home
                            </a>
                        </li>
                        <li>
                            <a 
                                href="#" 
                                className={`block py-2 px-3 hover:bg-yellow-300 md:hover:bg-transparent md:hover:text-yellow-300 md:p-0 ${activeLink === 'about' ? 'text-yellow-300' : ''}`} 
                                onClick={() => handleLinkClick('about')}
                            >
                                About
                            </a>
                        </li>
                        <li>
                            <a 
                                href="#" 
                                className={`block py-2 px-3 hover:bg-yellow-300 md:hover:bg-transparent md:hover:text-yellow-300 md:p-0 ${activeLink === 'promotion' ? 'text-yellow-300' : ''}`} 
                                onClick={() => handleLinkClick('promotion')}
                            >
                                Promotion
                            </a>
                        </li>
                        <li>
                            <a 
                                href="#" 
                                className={`block py-2 px-3 hover:bg-yellow-300 md:hover:bg-transparent md:hover:text-yellow-300 md:p-0 ${activeLink === 'contact' ? 'text-yellow-300' : ''}`} 
                                onClick={() => handleLinkClick('contact')}
                            >
                                Contact
                            </a>
                        </li>
                        <li>
                            <a 
                                href="/cart" 
                                className={`block py-2 px-3 hover:bg-yellow-300 md:hover:bg-transparent md:hover:text-yellow-300 md:p-0 ${activeLink === 'cart' ? 'text-yellow-300' : ''}`} 
                                onClick={handleToCart}
                            >
                                Cart
                            </a>
                        </li>

                    </ul>
                </div>
            </div>
        </nav>
    )
}
