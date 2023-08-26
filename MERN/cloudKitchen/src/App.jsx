import './App.css';
import Home from './screens/Home';
import Login from './screens/Login';
import SignUp from './screens/SignUp';
import { CartProvider } from './components/ContextReducer';

import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Orders from './screens/Orders';

function App() {
    return (
        <>
            <CartProvider>
                <Router>
                    <Routes>
                        <Route path="/" element={<Home />} />
                        <Route path="/login" element={<Login />} />
                        <Route path="/signUp" element={<SignUp />} />
                        <Route path="/orders" element={<Orders />} />
                    </Routes>
                </Router>
            </CartProvider>
        </>
    );
}

export default App;
