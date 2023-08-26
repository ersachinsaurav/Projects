import { useState, useRef, useEffect } from 'react';
import { useCartState, useCartDispatch } from './ContextReducer';

export default function Card({ foodItem, capitalize }) {
    const options = foodItem.options[0];
    const priceOptions = Object.keys(options);
    const [quantity, setQuantity] = useState(1);
    const [size, setSize] = useState('');
    const finalPrice = quantity * parseInt(options[size]);

    const priceRef = useRef();

    const dispatch = useCartDispatch();
    const cartData = useCartState();

    const handleAddToCart = async () => {
        let existingCartItem = null;

        for (const cartItem of cartData) {
            if (cartItem.id === foodItem._id && cartItem.size === size) {
                existingCartItem = cartItem;
                break;
            }
        }

        if (existingCartItem) {
            await dispatch({ type: 'UPDATE_ITEM', foodItem: existingCartItem, size, quantity, price: finalPrice });
        } else {
            await dispatch({ type: 'ADD_ITEM', foodItem, quantity, size, price: finalPrice });
        }
    };

    useEffect(() => {
        setSize(priceRef.current.value);
    }, []);

    return (
        <>
            <div className="card m-3" style={{ width: '25rem', maxHeight: '500px' }}>
                <img src={foodItem.img} className="card-img-top" style={{ height: '250px', objectFit: 'fill' }} />
                <div className="card-body">
                    <h5 className="card-title">{foodItem.name}</h5>
                    <div className="container">
                        <select name="" id="" className="m-2 h-100 rounded bg-success" onChange={(e) => setQuantity(e.target.value)}>
                            {Array.from(Array(6), (element, index) => {
                                return (
                                    <option key={index + 1} value={index + 1}>
                                        {index + 1}
                                    </option>
                                );
                            })}
                        </select>

                        <select name="" id="" className="m-2 h-100 rounded bg-success" ref={priceRef} onChange={(e) => setSize(e.target.value)}>
                            {priceOptions.map((option, index) => {
                                return (
                                    <option key={index} value={option}>
                                        {capitalize(option)}
                                    </option>
                                );
                            })}
                        </select>

                        <div className="d-inline h-100 fs-4">₹{finalPrice}</div>
                    </div>
                    <div className="container text-center">
                        <hr />
                        <button className="btn btn-success" onClick={handleAddToCart}>
                            Add To Cart
                        </button>
                    </div>
                </div>
            </div>
        </>
    );
}
