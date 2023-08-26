import { useState } from 'react';
import { Link } from 'react-router-dom';
import Footer from '../components/Footer';
import Navbar from '../components/Navbar';

export default function SignUp() {
    const [userData, setUserData] = useState({
        name: '',
        location: '',
        email: '',
        password: '',
    });

    const handleChange = (event) => {
        setUserData({ ...userData, [event.target.name]: event.target.value });
    };

    const handleSignUp = async (event) => {
        event.preventDefault();
        const response = await fetch(`http://localhost:5111/api/createUser`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                name: userData.name,
                email: userData.email,
                password: userData.password,
                location: userData.location,
            }),
        });
        const responseData = await response.json();
        // console.log(responseData);
        if (!responseData.success) {
            alert('Some fields were not successfully validated, please try again.');
        } else {
            alert('You have successfully signed up!');
            // window.location.href = '/login';
        }
    };
    return (
        <>
            <Navbar />
            <div className="container">
                <h1 className="mt-5 mb-5">Sign Up</h1>
                <form onSubmit={handleSignUp}>
                    <div className="mb-3">
                        <label htmlFor="name" className="form-label">
                            Name
                        </label>
                        <input type="text" className="form-control" id="name" name="name" value={userData.name} onChange={handleChange} />
                    </div>
                    <div className="mb-3">
                        <label htmlFor="Location" className="form-label">
                            Location
                        </label>
                        <input type="text" className="form-control" id="location" name="location" value={userData.location} onChange={handleChange} />
                    </div>

                    <div className="mb-3">
                        <label htmlFor="email" className="form-label">
                            Email address
                        </label>
                        <input type="email" className="form-control" id="email" name="email" aria-describedby="emailHelp" value={userData.email} onChange={handleChange} />
                        <div id="emailHelp" className="form-text">
                            We'll never share your email with anyone else.
                        </div>
                    </div>
                    <div className="mb-3">
                        <label htmlFor="password" className="form-label">
                            Password
                        </label>
                        <input type="password" className="form-control" id="password" name="password" value={userData.password} onChange={handleChange} />
                    </div>
                    <button type="submit" className="btn btn-primary">
                        Submit
                    </button>
                    <Link to="/login" className="ms-3 btn btn-secondary">
                        Login
                    </Link>
                </form>
            </div>
            <Footer />
        </>
    );
}
