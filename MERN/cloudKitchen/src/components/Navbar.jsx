import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import Modal from '../Modal';
import Cart from '../screens/Cart';
import { useCartState } from './ContextReducer';

export default function Navbar() {
    const navigate = useNavigate();
    const cartData = useCartState();

    const handleLogout = () => {
        localStorage.removeItem('authToken');
        navigate('./login');
    };

    const [cartView, setCartView] = useState(false);

    return (
        <nav className="navbar navbar-expand-lg navbar-light bg-light">
            <div className="container-fluid">
                <Link className="navbar-brand fs-1 fst-italic" to="/">
                    Cloud Kitchen
                </Link>
                <button className="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
                    <span className="navbar-toggler-icon"></span>
                </button>
                <div className="collapse navbar-collapse" id="navbarSupportedContent">
                    <ul className="navbar-nav me-auto ms-5 mb-2 mb-lg-0">
                        <li className="nav-item">
                            <Link className="nav-link fs-3" to="/">
                                Shop
                            </Link>
                        </li>
                        {localStorage.getItem('authToken') && (
                            <li className="nav-item">
                                <Link className="nav-link fs-3" to="/orders">
                                    Orders
                                </Link>
                            </li>
                        )}
                    </ul>
                </div>
                <div className="d-flex">
                    {localStorage.getItem('authToken') ? (
                        <>
                            <button
                                className="btn btn-primary position-relative me-5"
                                onClick={() => {
                                    setCartView(true);
                                }}
                            >
                                Cart
                                <span className="position-absolute top-0 start-100 translate-middle badge rounded-pill bg-danger">
                                    {cartData.length}
                                    <span className="visually-hidden">Food Items</span>
                                </span>
                            </button>

                            {cartView && (
                                <Modal
                                    onClose={() => {
                                        setCartView(false);
                                    }}
                                >
                                    <Cart />
                                </Modal>
                            )}

                            <button className="btn btn-danger" onClick={handleLogout}>
                                Logout
                            </button>
                        </>
                    ) : (
                        <>
                            <Link className="btn btn-primary me-3" to="/signUp">
                                SignUp
                            </Link>
                            <Link className="btn btn-success" to="/login">
                                Login
                            </Link>
                        </>
                    )}
                </div>
            </div>
        </nav>
    );
}
