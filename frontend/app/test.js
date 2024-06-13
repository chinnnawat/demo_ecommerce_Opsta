'use client';

import { useSession } from "next-auth/react";
import { useEffect, useState } from 'react';

export default function Cart() {
    const { data: session, status } = useSession();
    const [cartDetails, setCartDetails] = useState([]);
    const [sumPrice, setSumPrice] = useState(0);
    const [savings, setSavings] = useState(0);
    const [total, setTotal] = useState(0);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchCartDetails = async () => {
            if (!session || !session.user) {
                console.error('No user session found');
                return;
            }

            const data = {
                email: session?.user?.email  // User email
            };
            try {
                const userIdResponse = await fetch('http://localhost:8000/api/user/get_user_info/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(data),
                });

                if (!userIdResponse.ok) {
                    throw new Error('Failed to fetch user id');
                }

                const userIdData = await userIdResponse.json();
                const user_id = userIdData.user_id;

                const cartResponse = await fetch(`http://localhost:8000/api/show_cart/show_detal_cart/`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ user_id }),
                });
                if (!cartResponse.ok) {
                    throw new Error('Failed to fetch cart details');
                }

                const cartData = await cartResponse.json();
                setCartDetails(cartData.cart || []);
                setSumPrice(parseFloat(cartData.sum_price || 0));
                setSavings(parseFloat(cartData.savings || 0));
                setTotal(parseFloat(cartData.total || 0));

            } catch (error) {
                setError(error.message); // Use error.message instead of the whole error object
            }
        };

        fetchCartDetails();
    }, [session, status]);

    const handleQuantityChange = async (product_id, action) => {
        try {
            const userIdResponse = await fetch('http://localhost:8000/api/user/get_user_info/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ email: session?.user?.email }),
            });

            if (!userIdResponse.ok) {
                throw new Error('Failed to fetch user id');
            }

            const userIdData = await userIdResponse.json();
            const user_id = userIdData.user_id;

            let apiEndpoint;
            if (action === 'add') {
                apiEndpoint = 'plus';
            } else if (action === 'remove') {
                apiEndpoint = 'minus';
            } else if (action === 'delete') {
                apiEndpoint = 'remove';
            }

            const response = await fetch(`http://localhost:8000/api/add_cart/${apiEndpoint}/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ user: session?.user?.email, product: product_id }),
            });

            if (!response.ok) {
                throw new Error(`Failed to ${action} product`);
            }

            const result = await response.json();

            if (action === 'delete' || result.quantity === 0) {
                setCartDetails(prevDetails => 
                    prevDetails.map(cart => {
                        const updatedProducts = cart.cart_products.filter(item => item.product.id !== product_id);
                        return { ...cart, cart_products: updatedProducts, totalPrice: result.totalPrice };
                    })
                );
            } else {
                setCartDetails(prevDetails => 
                    prevDetails.map(cart => {
                        const updatedProducts = cart.cart_products.map(item => {
                            if (item.product.id === product_id) {
                                item.quantity = result.quantity;
                            }
                            return item;
                        });
                        return { ...cart, cart_products: updatedProducts, totalPrice: result.totalPrice };
                    })
                );
            }
        } catch (error) {
            setError(error.message); // Use error.message instead of the whole error object
        }
    };

    const handleRemoveProduct = (product_id) => {
        handleQuantityChange(product_id, 'delete');
    };

    if (error) {
        return <div>Error: {error}</div>;
    }

    if (!cartDetails.length) {
        return <div>Loading...</div>;
    }

    return (
        <div>
            <section className="bg-white py-8 antialiased md:py-16">
                <div className="mx-auto max-w-screen-xl px-4 2xl:px-0">
                    <h2 className="text-xl font-semibold text-gray-900">Shopping Cart</h2>
                    <div className="mt-6 sm:mt-8 md:gap-6 lg:flex lg:items-start xl:gap-8">
                        {cartDetails.map((cart, index) => (
                            <div key={index}>
                                {cart.cart_products.map((productItem, idx) => (
                                    <div key={idx} className="mx-auto w-full flex-none lg:max-w-2xl xl:max-w-4xl">
                                        <div className="space-y-6">
                                            <div className="rounded-lg border border-gray-200 bg-white p-4 shadow-smmd:p-6">
                                                <div className="space-y-4 md:flex md:items-center md:justify-between md:gap-6 md:space-y-0">
                                                    <a href="#" className="shrink-0 md:order-1">
                                                        <img className="h-20 w-20" src={productItem.product.imageUrl} alt="imac image"/>
                                                    </a>

                                                    <label htmlFor="counter-input" className="sr-only">Choose quantity:</label>
                                                    <div className="flex items-center justify-between md:order-3 md:justify-end">
                                                        <div className="flex item-center">
                                                            <button type="button" id="decrement-button" data-input-counter-decrement="counter-input" className="inline-flex h-5 w-5 shrink-0 items-center justify-center rounded-md border border-gray-300 bg-gray-100 hover:bg-gray-200 focus:outline-none focus:ring-2 focus:ring-gray-100" 
                                                                onClick={() => handleQuantityChange(productItem.product.id, 'remove')}
                                                            >
                                                                <svg className="h-2.5 w-2.5 text-gray-900 " aria-hidden="true" fill="none" viewBox="0 0 18 2" xmlns="http://www.w3.org/2000/svg">
                                                                    <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M1 1h16" />
                                                                </svg>
                                                            </button>
                                                            <input type="text" id="counter-input" data-input-counter className="w-10 shrink-0 border-0 bg-transparent text-center text-sm font-medium text-gray-900 focus:outline-none focus:ring-0 " placeholder="" value={productItem.quantity} readOnly/>
                                                            <button type="button" id="increment-button" data-input-counter-increment="counter-input" className="inline-flex h-5 w-5 shrink-0 items-center justify-center rounded-md border border-gray-300 bg-gray-100 hover:bg-gray-200 focus:outline-none focus:ring-2 focus:ring-gray-100"
                                                                onClick={() => handleQuantityChange(productItem.product.id, 'add')}
                                                            >
                                                                <svg className="h-2.5 w-2.5 text-gray-900 " aria-hidden="true" fill="none" viewBox="0 0 18 18" xmlns="http://www.w3.org/2000/svg">
                                                                    <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M1 9h16M9 1v16" />
                                                                </svg>
                                                            </button>
                                                        </div>
                                                        <div className="text-end md:order-4 md:w-32 pl-4">
                                                            <p className="text-sm font-bold text-gray-900">{productItem.product.price} per/unit</p>
                                                        </div>
                                                    </div>
                                                    <div className="w-full min-w-0 flex-1 space-y-4 md:order-2 md:max-w-md">
                                                        <a href={{ pathname: '/productDetail/' + productItem.product.id }} className="text-base font-semibold text-gray-900 hover:underline">{productItem.product.name}</a>

                                                        <div className="flex items-center gap-4">
                                                            <button type="button" onClick={() => handleRemoveProduct(productItem.product.id)} className="inline-flex items-center text-sm font-medium gray-900 hover:text-red-500 hover:underline ">
                                                                <svg className="me-1.5 h-5 w-5" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="none" viewBox="0 0 24 24">
                                                                    <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18 17.94 6M18 18 6.06 6" />
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
                                            <dt className="text-base font-normal text-gray-500">Savings</dt>
                                            <dd className="text-base font-medium text-gray-900">{savings}</dd>
                                        </dl>

                                        <dl className="flex items-center justify-between gap-4 border-t border-gray-200 pt-2">
                                            <dt className="text-base font-bold text-gray-900">Total</dt>
                                            <dd className="text-base font-bold text-gray-900">{total}</dd>
                                        </dl>
                                    </div>

                                    <button type="button" className="flex w-full items-center justify-center rounded-lg bg-[#FF7F3E] px-5 py-2.5 text-sm font-medium text-white hover:bg-orange-800 focus:outline-none focus:ring-4 focus:ring-blue-300">Proceed to Checkout</button>

                                    <div className="flex items-center justify-center gap-2">
                                        <span className="text-sm font-normal text-gray-500">or</span>
                                        <a href="/" title="" className="inline-flex items-center gap-2 text-sm font-medium text-gray-900 underline hover:no-underline hover:text-[#FF7F3E]">
                                            Continue Shopping
                                            <svg className="h-5 w-5" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                                                <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 12H5m14 0-4 4m4-4-4-4"></path>
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
    );
}
