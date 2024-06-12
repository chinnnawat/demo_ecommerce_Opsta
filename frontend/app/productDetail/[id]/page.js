'use client';

import { useEffect, useState } from 'react';
import { useSession } from 'next-auth/react';

export default function ProductDetail({ params }) {
    const productId = params.id;
    const [product, setProduct] = useState(null);
    const [quantity, setQuantity] = useState(1);
    const [error, setError] = useState(null);
    const [isLoading, setIsLoading] = useState(true);

    const { data: session, status } = useSession();

    useEffect(() => {
        const fetchProductDetail = async () => {
            try {
                const response = await fetch(`http://localhost:8000/api/product/${productId}/getProduct_detail/`);
                if (!response.ok) {
                    throw new Error('Failed to fetch product detail');
                }
                const data = await response.json();
                setProduct(data);
                setQuantity(data.quantity || 1); // Set initial quantity
            } catch (error) {
                setError(error);
            } finally {
                setIsLoading(false);
            }
        };

        fetchProductDetail();
    }, [productId]);

    if (isLoading) return <div>Loading...</div>;
    if (error) return <div>Failed to load</div>;
    if (!product) return null;
    if (status === 'loading') return <div>Loading session...</div>;

    const handleQuantityChange = (e) => {
        const value = parseInt(e.target.value, 10);
        if (isNaN(value) || value < 1) {
            setQuantity(1);
        } else if (value > product.stock) {
            setQuantity(product.stock);
        } else {
            setQuantity(value);
        }
    };

    const handleAddToCart = async () => {
        if (!session || !session.user) {
            console.error('No user session found');
            return;
        }

        // const [firstName, lastName] = session.user?.name.split(" ");
        const cartData = {
            user: session.user?.email,
            product: product.id,
            quantity: quantity,
            // firstName: firstName,
            // lastName: lastName
            // price: product.price,
        };

        console.log('Sending cart data:', cartData);

        // console.log("hi");

        try {
            const response = await fetch('http://localhost:8000/api/add_cart/add_to_cart/', {
            // const response = await fetch('https://www.google.co.uk/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${session.accessToken}`, // ถ้ามีการใช้ token
                },
                body: JSON.stringify(cartData),
            });


            if (!response.ok) {
                throw new Error('Failed to add to cart');
            }
            const data = await response.json();
            console.log('Success:', data);
        } catch (error) {
            console.error('Error:', error);
        }

        // const response = await fetch('http://localhost:8000/api/add_cart/');
        // console.log(response);
    };

    return (
        <div className='font-sans bg-white'>
            <div className='p-6 lg:max-w-7xl max-w-4xl mx-auto'>
                <div className='grid items-start grid-cols-1 lg:grid-cols-5 gap-12 shadow-[0_2px_10px_-3px_rgba(6,81,237,0.3)] p-6'>
                    <div className='lg:col-span-3 w-full lg:sticky top-0 text-center'>
                        <div className='px-4 py-10 rounded-xl shadow-[0_2px_10px_-3px_rgba(6,81,237,0.3)] relative'>
                            <img src={product.imageUrl} alt={product.name} className='h-[640px] min-w-[640px]' />
                            <button type='button' className='absolute top-4 right-4'>
                                <svg xmlns="http://www.w3.org/2000/svg" width="20px" fill="#ccc" className="mr-1 hover:fill-[#333]" viewBox="0 0 64 64">
                                    <path d="M45.5 4A18.53 18.53 0 0 0 32 9.86 18.5 18.5 0 0 0 0 22.5C0 40.92 29.71 59 31 59.71a2 2 0 0 0 2.06 0C34.29 59 64 40.92 64 22.5A18.52 18.52 0 0 0 45.5 4ZM32 55.64C26.83 52.34 4 36.92 4 22.5a14.5 14.5 0 0 1 26.36-8.33 2 2 0 0 0 3.27 0A14.5 14.5 0 0 1 60 22.5c0 14.41-22.83 29.83-28 33.14Z" data-original="#000000"></path>
                                </svg>
                            </button>
                        </div>
                    </div>
                    <div className='lg:col-span-2'>
                        <h2 className='text-2xl font-extrabold text-[#333]'>{product.name} | {product.category}</h2>
                        <div className='flex flex-wrap gap-4 mt-4'>
                            <p className='text-[#333] text-3xl font-bold'>{product.price}</p>
                        </div>
                        <div className='min-h-[200px]'>
                            <p className='text-[#333] mt-2'>{product.description}</p>
                        </div>
                        <div className='flex flex-wrap gap-4 mt-4'>
                            <p className='text-[#333]'>In stock: {product.stock}</p>
                            <p className='text-[#333]'>Quantity:
                                <input
                                    type="number"
                                    value={quantity}
                                    min="1"
                                    max={product.stock}
                                    onChange={handleQuantityChange}
                                    className="border border-gray-300 rounded px-2 py-1 ml-2"
                                    disabled={product.stock === 0}
                                />
                            </p>
                        </div>
                        <div className="flex flex-wrap gap-4 mt-10">
                            <button type="button" onClick={handleAddToCart} className="min-w-[200px] px-4 py-2.5 border border-[#333] bg-transparent hover:bg-[#FF7F3E] text-[#333] text-sm font-semibold rounded hover:text-white hover:border-white" disabled={product.stock === 0}>Add to cart</button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}
