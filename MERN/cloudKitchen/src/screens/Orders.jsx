import { useEffect, useState } from 'react';
import Footer from '../components/Footer';
import Navbar from '../components/Navbar';

const Orders = () => {
    const [orderData, setOrderData] = useState({});

    const fetchMyOrder = async () => {
        await fetch('http://localhost:5111/api/getOrderData', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                email: localStorage.getItem('userEmail'),
            }),
        }).then(async (res) => {
            let response = await res.json();
            await setOrderData(response);
        });
    };

    useEffect(() => {
        fetchMyOrder();
    }, []);

    return (
        <>
            <Navbar />
            <div className="container mt-5 mb-5">
                <h1>Orders</h1>
                <hr />

                <div className="row">
                    {orderData !== {}
                        ? Array(orderData).map((data) => {
                              return data.orderData
                                  ? data.orderData.orderData
                                        .slice(0)
                                        .reverse()
                                        .map((item) => {
                                            return item.map((arrayData, index) => {
                                                return (
                                                    <div key={index}>
                                                        {arrayData.orderDate ? (
                                                            <div className="m-auto mt-5">
                                                                {(data = arrayData.orderDate)}
                                                                <hr />
                                                            </div>
                                                        ) : (
                                                            <div className="col-12 col-md-6 col-lg-3">
                                                                <div className="card mt-3" style={{ width: '16rem', maxHeight: '360px' }}>
                                                                    <img src={arrayData.img} className="card-img-top" alt="..." style={{ height: '120px', objectFit: 'fill' }} />
                                                                    <div className="card-body">
                                                                        <h5 className="card-title">{arrayData.name}</h5>
                                                                        <div className="container w-100 p-0" style={{ height: '38px' }}>
                                                                            <span className="m-1">{arrayData.qty}</span>
                                                                            <span className="m-1">{arrayData.size}</span>
                                                                            <span className="m-1">{data}</span>
                                                                            <div className=" d-inline ms-2 h-100 w-20 fs-5">₹{arrayData.price}/-</div>
                                                                        </div>
                                                                    </div>
                                                                </div>
                                                            </div>
                                                        )}
                                                    </div>
                                                );
                                            });
                                        })
                                  : '';
                          })
                        : ''}
                </div>
            </div>
            <Footer />
        </>
    );
};

export default Orders;
