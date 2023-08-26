import { useCartState, useCartDispatch } from '../components/ContextReducer';
import trash from '../assets/images/trash.png';

const Cart = () => {
    const cartData = useCartState();
    const dispatch = useCartDispatch();

    if (cartData.length === 0) {
        return <div className="m-5 w-100 text-center fs-3 text-white">Your Cart Is Empty!</div>;
    }

    const capitalize = (str) => {
        return str[0].toUpperCase() + str.slice(1);
    };

    const totalPrice = cartData.reduce((total, foodItem) => total + foodItem.price, 0);

    const handleCheckout = async () => {
        const userEmail = localStorage.getItem('userEmail');
        const orderResponse = await fetch('http://localhost:5111/api/placeOrder', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                orderData: cartData,
                email: userEmail,
                orderDate: new Date().toDateString(),
            }),
        });
        console.log('JSON orderRESPONSE:::::', orderResponse.status);
        if (orderResponse.status === 200) {
            dispatch({ type: 'DROP_CART' });
        }
    };

    return (
        <>
            <div className="container m-auto mt-5 table-responsive table-responsive-md table-responsive-sm">
                <table className="table table-hover table-dark">
                    <thead className="text-success fs-4">
                        <tr>
                            <th scope="col">#</th>
                            <th scope="col">Description</th>
                            <th scope="col">Quantity</th>
                            <th scope="col">Option</th>
                            <th scope="col">Amount</th>
                            <th scope="col"></th>
                        </tr>
                    </thead>
                    <tbody>
                        {cartData.map((cartItem, itemIndex) => (
                            <tr key={itemIndex}>
                                <td scope="row">{itemIndex + 1}</td>
                                <td>{capitalize(cartItem.name)}</td>
                                <td>{cartItem.quantity}</td>
                                <td>{capitalize(cartItem.size)}</td>
                                <td>{cartItem.price}</td>
                                <td>
                                    <button className="btn p-0">
                                        <img
                                            src={trash}
                                            alt="deleteItem"
                                            onClick={() => {
                                                dispatch({ type: 'REMOVE_ITEM', itemIndex: itemIndex });
                                            }}
                                            height={'25px'}
                                        />
                                    </button>
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
                <div className="row align-items-center">
                    <div className="col d-flex justify-content-start">
                        <h1 className="fs-5 text-white">Total Price: {totalPrice}/-</h1>
                    </div>
                    <div className="col d-flex justify-content-end">
                        <button className="btn btn-primary" onClick={handleCheckout}>
                            CheckOut
                        </button>
                    </div>
                </div>
            </div>
        </>
    );
};

export default Cart;
