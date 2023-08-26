import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import Footer from '../components/Footer';
import Navbar from '../components/Navbar';

export default function Login() {
    const [userData, setUserData] = useState({ email: '', password: '' });
    const navigate = useNavigate();

    const handleChange = (event) => {
        setUserData({ ...userData, [event.target.name]: event.target.value });
    };

    const handleLogin = async (event) => {
        event.preventDefault();
        const response = await fetch(`http://localhost:5111/api/authUser`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                email: userData.email,
                password: userData.password,
            }),
        });
        const responseData = await response.json();

        // console.log(responseData);

        if (!responseData.success) {
            alert('Some fields were not successfully validated, please try again.');
        } else {
            localStorage.setItem('authToken', responseData.authToken);
            localStorage.setItem('userEmail', userData.email);
            navigate('/');
        }
    };
    return (
        <>
            <Navbar />
            <div className="container">
                <h1 className="mt-5 mb-5">Login</h1>
                <form onSubmit={handleLogin}>
                    <div className="mb-3">
                        <label htmlFor="email" className="form-label">
                            Email address
                        </label>
                        <input type="email" className="form-control" id="email" name="email" value={userData.email} onChange={handleChange} />
                    </div>
                    <div className="mb-3">
                        <label htmlFor="password" className="form-label">
                            Password
                        </label>
                        <input type="password" className="form-control" id="password" name="password" value={userData.password} onChange={handleChange} />
                    </div>
                    <button type="submit" className="btn btn-primary">
                        Login
                    </button>
                    <Link to="/signUp" className="ms-3 btn btn-secondary">
                        New User?
                    </Link>
                </form>
            </div>
            <Footer />
        </>
    );
}
