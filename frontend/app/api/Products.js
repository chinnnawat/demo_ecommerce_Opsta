
import useSWR from 'swr';

const fetcher = (url) => fetch(url).then((res) => res.json());

// get all products
export function useProducts() {
  const { data, error, isLoading } = useSWR(`${process.env.NEXT_PUBLIC_API_URL_PRODUCT_ALL}`, fetcher);

  return {
    products: data,
    isLoading,
    error,
  };
}
