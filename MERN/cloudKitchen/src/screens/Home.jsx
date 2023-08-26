import { useState, useEffect } from 'react';
import Navbar from '../components/Navbar';
import Footer from '../components/Footer';
import Card from '../components/Card';

export default function Home() {
    const [foodItems, setFoodItems] = useState([]);
    const [foodCategories, setFoodCategories] = useState([]);
    const [searchTerm, setSearchTerm] = useState('');

    const capitalize = (str) => {
        return str[0].toUpperCase() + str.slice(1);
    };

    const loadData = async () => {
        const responseFoodItems = await fetch('http://localhost:5111/api/foodItems', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
        });
        const dataFoodItems = await responseFoodItems.json();
        setFoodItems(dataFoodItems);

        const responseFoodCategories = await fetch('http://localhost:5111/api/foodCategories', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
        });
        const dataFoodCategories = await responseFoodCategories.json();
        setFoodCategories(dataFoodCategories);
    };

    useEffect(() => {
        loadData();
    }, []);

    return (
        <>
            <Navbar />

            {/* Carousel Start */}
            <div id="autoplayingCarousel" className="carousel slide carousel-fade" data-bs-ride="carousel">
                <div className="carousel-indicators">
                    <button data-bs-target="#autoplayingCarousel" data-bs-slide-to="0" className="active" aria-current="true" aria-label="Slide 1"></button>
                    <button data-bs-target="#autoplayingCarousel" data-bs-slide-to="1" aria-label="Slide 2"></button>
                    <button data-bs-target="#autoplayingCarousel" data-bs-slide-to="2" aria-label="Slide 3"></button>*
                </div>
                <div className="carousel-inner" style={{ maxHeight: '520px' }}>
                    <div className="carousel-caption d-md-block" style={{ zIndex: '100' }}>
                        <div className="d-flex justify-content-center" role="search">
                            <input
                                className="form-control me-2"
                                type="text"
                                placeholder="Search"
                                aria-label="Search"
                                value={searchTerm}
                                onChange={(e) => {
                                    setSearchTerm(e.target.value);
                                }}
                            />
                            {/* <button className="btn btn-success" type="submit">Search</button> */}
                        </div>
                    </div>
                    <div className="carousel-item active">
                        <img src="https://source.unsplash.com/random/1200x600/?burger" className="d-block carousel-image" style={{ filter: 'brightness(30%)' }} />
                    </div>
                    <div className="carousel-item">
                        <img src="https://source.unsplash.com/random/1200x600/?pizza" className="d-block carousel-image" style={{ filter: 'brightness(30%)' }} />
                    </div>
                    <div className="carousel-item">
                        <img src="https://source.unsplash.com/random/1200x600/?chowmein" className="d-block carousel-image" style={{ filter: 'brightness(30%)' }} />
                    </div>
                </div>
                <button className="carousel-control-prev" data-bs-target="#autoplayingCarousel" data-bs-slide="prev">
                    <span className="carousel-control-prev-icon" aria-hidden="true"></span>
                    <span className="visually-hidden">Previous</span>
                </button>
                <button className="carousel-control-next" data-bs-target="#autoplayingCarousel" data-bs-slide="next">
                    <span className="carousel-control-next-icon" aria-hidden="true"></span>
                    <span className="visually-hidden">Next</span>
                </button>
            </div>
            {/* Carousel End  */}

            {/* Main Content */}
            {foodCategories.length > 0 &&
                foodCategories.map((foodCategory, categoryIndex) => {
                    return (
                        <div className="row mb-3" key={categoryIndex}>
                            <div className="fs-3 m-3">{foodCategory.CategoryName}</div>
                            <hr />

                            {foodItems.length > 0 &&
                                foodItems
                                    .filter((foodItem) => foodCategory.CategoryName === foodItem.CategoryName && foodItem.name.toLowerCase().includes(searchTerm.toLowerCase()))
                                    .map((foodItem, itemIndex) => {
                                        return (
                                            <div className="col-12 col-md-6 col-lg-3" key={itemIndex}>
                                                <Card foodItem={foodItem} capitalize={capitalize} />
                                            </div>
                                        );
                                    })}
                        </div>
                    );
                })}

            <Footer />
        </>
    );
}
