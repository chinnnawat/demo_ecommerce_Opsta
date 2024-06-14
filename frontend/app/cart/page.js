'use client'

import { useSession, signIn } from "next-auth/react";
import { useEffect, useState } from 'react';


export default function Cart() {
    const { data: session, status } = useSession()
    const [cartDetails, setCartDetails] = useState([]); 
    const [error, setError] = useState(null);

    const [sumPrice, setSumPrice] = useState(0);
    const [savings, setSavings] = useState(0);
    const [total, setTotal] = useState(0);
    const [promotion, setPromotion] = useState(0);
    const [notification, setNotification] = useState('');


    useEffect(() => {
        const fetchCartDetails = async () => {
            if (!session || !session.user) {
                console.error('No user session found');
                return;
            }

            const data = {
                email: session?.user?.email  // User email
            };
            try{
                const userIdRespone = await fetch('http://localhost:8000/api/user/get_user_info/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(data),
                });

                if(!userIdRespone.ok){
                    throw new Error('กรุณาเลือกสินค้าครับ');
                }

                const userIdData = await userIdRespone.json();
                const user_id = userIdData.user_id;

                // console.log(user_id);


                const cartResponse = await fetch(`http://localhost:8000/api/show_cart/show_detal_cart/`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({user_id} ), 
                });
                if (!cartResponse.ok) {
                    throw new Error('Failed to fetch cart details');
                }

                const cartData = await cartResponse.json();
                setCartDetails(cartData.cart || []);
                setSumPrice(parseFloat(cartData.sum_price || 0));
                setSavings(parseFloat(cartData.savings || 0));
                setTotal(parseFloat(cartData.total || 0));
                setPromotion(cartData.promotion || '');

                // setCartDetails(cartData);
                console.log(cartData);

            } catch(error){
                setError(error);
            }
        };

        fetchCartDetails()
    }, [session, status]);
    

    if (error) {
        return <div>Error: {error.toString()}</div>;
    }

    if (!Array.isArray(cartDetails) || cartDetails.length === 0) {
        return <div>Loading...</div>;
    }

    const handleQuantityChange = async (product_id, action) => {
        try{
            const userIdRespone = await fetch('http://localhost:8000/api/user/get_user_info/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({email: session?.user?.email}),
            });
            if (!userIdRespone.ok) {
                throw new Error('Failed to fetch user id');
            }
            const userIdData = await userIdRespone.json();


            // api
            let apiEndpoint;
            if (action === 'add') {
                apiEndpoint = 'plus';
            } else if (action === 'remove') {
                apiEndpoint = 'minus';
            } else if (action === 'delete') {
                apiEndpoint = 'remove';
            } else if (action === 'checkout') {
                apiEndpoint = 'checkout';
            }
            
            const response = await fetch(`http://localhost:8000/api/add_cart/${apiEndpoint}/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({user: session?.user?.email, product: product_id}),
            });
            if (!response.ok) {
                throw new Error(`Failed to ${action} product`);
            }

            const result = await response.json();
            // console.log(result);
            setCartDetails(prevDetails => 
                prevDetails.map(cart => {
                    const updatedProducts = cart.cart_products.map(item => {
                        if(item.product.id === product_id){
                            item.quantity = result.quantity;
                        }
                        return item;
                    }).filter(item => item.quantity > 0);
                    return {...cart, cart_products: updatedProducts, totalPrice: result.totalPrice};
                })
            );
            if (result.quantity === 0) {
                window.location.reload(); // Refresh page after removing product
            }
            else if (action === 'add' || action === 'remove') {
                window.location.reload();
            }
            else if (action === 'checkout') {
                setNotification('Order placed successfully!');
                setNotification('Product added to cart successfully!');
                setTimeout(() => {
                    setNotification('');
                }, 1500); // ลบข้อความแจ้งเตือนหลังจาก 3 วินาที
                window.location.assign('/'); // Navigate to home page
            }
        
            // setNotification('Product added to cart successfully!');
            // setTimeout(() => {
            //     setNotification('');
            // }, 1500); // ลบข้อความแจ้งเตือนหลังจาก 3 วินาที


        }
        catch(error){
            setError(error.message); // ใช้ข้อความจาก Error
        }
    }


    console.log(cartDetails);


    return (
        <div>
            {notification && (
                <div className="fixed top-100 left-100 right-0 bg-green-500 text-white text-center p-4">
                    {notification}
                </div>
            )}
            {session && session.user ? (
                <div>
                    <section className="bg-white py-8 antialiased md:py-16">
                        <div className="mx-auto max-w-screen-xl px-4 2xl:px-0">
                            <h2 className="text-xl font-semibold text-gray-900">Shopping Cart</h2>
                            <div className="mt-6 sm:mt-8 md:gap-6 lg:flex lg:items-start xl:gap-8">
                                {cartDetails.map((cart, index) => (
                                    <div key={index}>
                                        {/* map */}
                                        {cart.cart_products.map((productItem, idx) => (
                                            <div className="mx-auto w-full flex-none lg:max-w-2xl xl:max-w-4xl" key={idx}>
                                                <div className="space-y-6">
                                                    <div className="rounded-lg border border-gray-200 bg-white p-4 shadow-sm md:p-6">
                                                        <div className="space-y-4 md:flex md:items-center md:justify-between md:gap-6 md:space-y-0">
                                                            <a href="#" className="shrink-0 md:order-1">
                                                                {/* replace by image url */}
                                                                <img className="h-20 w-20" src={productItem.product.imageUrl} alt="product image"/>
                                                            </a>
                                                            <label htmlFor="counter-input" className="sr-only">Choose quantity:</label>
                                                            <div className="flex items-center justify-between md:order-3 md:justify-end">
                                                                <div className="flex item-center">
                                                                    <button type="button" id="decrement-button" data-input-counter-decrement="counter-input" className="inline-flex h-5 w-5 shrink-0 items-center justify-center rounded-md border border-gray-300 bg-gray-100 hover:bg-gray-200 focus:outline-none focus:ring-2 focus:ring-gray-100" 
                                                                        onClick={() => handleQuantityChange(productItem.product.id, 'remove')}
                                                                    >
                                                                        {/* minus icon */}
                                                                        <svg className="h-2.5 w-2.5 text-gray-900 " aria-hidden="true" fill="none" viewBox="0 0 18 2" xmlns="http://www.w3.org/2000/svg">
                                                                            <path stroke="currentColor" strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M1 1h16" />
                                                                        </svg>
                                                                    </button>
                                                                    <input type="text" id="counter-input" data-input-counter className="w-10 shrink-0 border-0 bg-transparent text-center text-sm font-medium text-gray-900 focus:outline-none focus:ring-0 " placeholder="" value={productItem.quantity} required readOnly />
                                                                    <button type="button" id="increment-button" data-input-counter-increment="counter-input" className="inline-flex h-5 w-5 shrink-0 items-center justify-center rounded-md border border-gray-300 bg-gray-100 hover:bg-gray-200 focus:outline-none focus:ring-2 focus:ring-gray-100"
                                                                        onClick={() => handleQuantityChange(productItem.product.id, 'add')}
                                                                    >
                                                                        {/* plus icon */}
                                                                        <svg className="h-2.5 w-2.5 text-gray-900 " aria-hidden="true" fill="none" viewBox="0 0 18 18" xmlns="http://www.w3.org/2000/svg">
                                                                            <path stroke="currentColor" strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M1 9h16M9 1v16" />
                                                                        </svg>
                                                                    </button>
                                                                </div>
                                                                <div className="text-end md:order-4 md:w-32 pl-4">
                                                                    <p className="text-sm font-bold text-gray-900">{productItem.product.price} per/unit</p>
                                                                </div>
                                                            </div>
                                                            <div className="w-full min-w-0 flex-1 space-y-4 md:order-2 md:max-w-md">
                                                                {/* product name */}
                                                                <a href={{ pathname: '/productDetail/' + productItem.product.id }} className="text-base font-semibold text-gray-900 hover:underline">{productItem.product.name}</a>
                                                                <div className="flex items-center gap-4">
                                                                    <button type="button" className="inline-flex items-center text-sm font-medium gray-900 hover:text-red-500 hover:underline "
                                                                        onClick={() => handleQuantityChange(productItem.product.id, 'delete')}
                                                                    >
                                                                        <svg className="me-1.5 h-5 w-5" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="none" viewBox="0 0 24 24">
                                                                            <path stroke="currentColor" strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M6 18 17.94 6M18 18 6.06 6" />
                                                                        </svg>
                                                                        Remove
                                                                    </button>
                                                                </div>
                                                            </div>
                                                        </div>
                                                    </div>
                                                </div>
                                            </div>
                                        ))}
                                    </div>
                                ))}
                                <div className="mx-auto mt-6 max-w-4xl flex-1 space-y-6 lg:mt-0 lg:w-full">
                                    <div className="space-y-4 rounded-lg border border-gray-200 bg-white p-4 shadow-sm ">
                                        <p className="text-xl font-semibold text-gray-900">Order summary</p>
                                        <div className="space-y-4">
                                            <div className="space-y-2">
                                                <dl className="flex items-center justify-between gap-4">
                                                    <dt className="text-base font-normal text-gray-500">Sum price</dt>
                                                    <dd className="text-base font-medium text-gray-900">{sumPrice}</dd>
                                                </dl>
                                                <dl className="flex items-center justify-between gap-4">
                                                    <dt className="text-base font-normal text-gray-500">Savings *{promotion}</dt>
                                                    <dd className="text-base font-medium text-gray-900">{savings}</dd>
                                                </dl>
                                                <dl className="flex items-center justify-between gap-4 border-t border-gray-200 pt-2">
                                                    <dt className="text-base font-bold text-gray-900">Total</dt>
                                                    <dd className="text-base font-bold text-gray-900">{total}</dd>
                                                </dl>
                                            </div>
                                            <button type="button" className="flex w-full items-center justify-center rounded-lg bg-[#FF7F3E] px-5 py-2.5 text-sm font-medium text-white hover:bg-orange-800 focus:outline-none focus:ring-4 focus:ring-blue-300"
                                                onClick={() => handleQuantityChange(null, 'checkout')}
                                                
                                                >Proceed to Checkout
                                            </button>
                                            <div className="flex items-center justify-center gap-2">
                                                <span className="text-sm font-normal text-gray-500">or</span>
                                                <a href="/" title="" className="inline-flex items-center gap-2 text-sm font-medium text-gray-900 underline hover:no-underline hover:text-[#FF7F3E]">
                                                    Continue Shopping
                                                    <svg className="h-5 w-5" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                                                        <path stroke="currentColor" strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 12H5m14 0-4 4m4-4-4-4"></path>
                                                    </svg>
                                                </a>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </section>
                </div>
            ) : (
                <div className="flex flex-col items-center justify-center h-screen">
                    <p className="text-xl font-semibold mb-4">Please sign in to view your cart</p>
                    <button onClick={() => signIn()} className="px-4 py-2 text-[#e44949] border border-[#f00] rounded hover:bg-[#f00] hover:text-white">
                        Login
                    </button>
                </div>

            )}
        </div>
    )};
