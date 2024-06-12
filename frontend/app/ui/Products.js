'use client'

import { useProducts } from "../api/Products";
import Link from 'next/link';
// import { usePathname, useRouter, useSearchParams } from 'next/navigation';

export default function ProductAll() {
  const { products, error, isLoading } = useProducts();
  // const pathname = usePathname();

  if (error) return <div>Failed to load</div>;
  if (isLoading) return <div>Loading...</div>;
  if (!products) return null;

  return (
      <div className="flex flex-wrap justify-center mx-80">
        {products.map((product) => (
          <div key={product.id} className="w-72 h-110 mr-3 mb-2 border-solid border-1 rounded-lg shadow-lg">
            <div>
              <img
                  src={product.imageUrl}
                  className="w-full h-72"
              />
            </div>
            <div className="font-bold text-xl mb-2 px-4 pb-4 pt-3 h-[120px]">
            <Link href={{ pathname: '/productDetail/' + product.id}}>
                {product.name}  
            </Link>
            </div>
            <div className="justify-between flex flex-row">
              <div className="px-6 pt-4 pb-2 justify-between">
                <span className="inline-block bg-gray-200 rounded-full px-3 py-1 text-sm font-semibold text-gray-700 mr-2 mb-2">
                  {product.category}
                </span>
                
              </div>
              <div className="px-6 pt-4 pb-2 justify-between">
                <span className="inline-block bg-gray-200 rounded-full px-3 py-1 text-sm font-semibold text-gray-700 mr-2 mb-2">
                  {product.price}
                </span>
              </div>
            </div>
          </div>
        ))}
      </div>
  );
}
