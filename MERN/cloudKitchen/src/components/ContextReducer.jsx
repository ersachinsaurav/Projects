import { createContext, useReducer, useContext } from 'react';

const CartStateContext = createContext();
const CartDispatchContext = createContext();

let newCartData;

const reducer = (state, action) => {
    newCartData = [...state];

    switch (action.type) {
        case 'ADD_ITEM':
            return [...state, { id: action.foodItem._id, name: action.foodItem.name, quantity: action.quantity, size: action.size, price: action.price }];

        case 'REMOVE_ITEM':
            newCartData.splice(action.itemIndex, 1);
            return newCartData;

        case 'UPDATE_ITEM':
            return newCartData.map((cartItem) => {
                if (cartItem.id === action.foodItem.id && cartItem.size == action.size) {
                    return {
                        ...cartItem,
                        quantity: parseInt(action.quantity) + parseInt(cartItem.quantity),
                        price: action.price + cartItem.price,
                    };
                }
                return cartItem;
            });

        case 'DROP_CART':
            return [];

        default:
            console.log('Error in reducer action');
    }
};

export const CartProvider = ({ children }) => {
    const [state, dispatch] = useReducer(reducer, []);
    return (
        <CartDispatchContext.Provider value={dispatch}>
            <CartStateContext.Provider value={state}>{children}</CartStateContext.Provider>
        </CartDispatchContext.Provider>
    );
};
export const useCartState = () => useContext(CartStateContext);
export const useCartDispatch = () => useContext(CartDispatchContext);
