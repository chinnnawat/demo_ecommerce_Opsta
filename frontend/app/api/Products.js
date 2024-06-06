
import useSWR from 'swr';

const fetcher = (url) => fetch(url).then((res) => res.json());

// get all products
export function useProducts() {
  const { data, error, isLoading } = useSWR("http://localhost:8000/api/product/", fetcher);

  return {
    products: data,
    isLoading,
    error,
  };
}
