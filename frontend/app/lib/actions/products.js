'use server'
export async function getProducts(){
    console.log("Hello");
    // try {
    //     let response = await fetch('http://localhost:8000/ecommerce/products/')
    //     let data = await response.json()
    //     return data;
    // } catch (error) {
    //     return error
        
    // }
    let response = await fetch('http://localhost:8000/ecommerce/products/')
    let data = await response.json()
    return data;
  }