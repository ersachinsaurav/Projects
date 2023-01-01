import React, { useEffect, useState } from "react";
import NewsItem from "./NewsItem";
import Spinner from "./Spinner";
import PropTypes from "prop-types";
import InfiniteScroll from "react-infinite-scroll-component";

const News = (props) => {
  const [articles, setArticles] = useState([]);
  const [loading, setLoading] = useState(true);
  let [page, setPage] = useState(1);
  const [totalResults, setTotalResults] = useState(0);

  const pageIncrement = () => {
    setPage(++page);
  };

  const pageDecrement = () => {
    setPage(--page);
  };

  const capitalize = (word) => {
    return word.charAt(0).toUpperCase() + word.slice(1).toLowerCase();
  };

  document.title = `${capitalize(props.category)} - NewsBilla`;

  const newsData = async () => {
    setLoading(true);
    props.setProgress(10);
    const url = `https://newsapi.org/v2/top-headlines?apiKey=${props.apiKey}&country=${props.country}&category=${props.category}&page=${page}&pageSize=${props.pageSize}`;
    let data = await fetch(url);
    props.setProgress(30);
    let parsedData = await data.json();
    props.setProgress(60);
    setArticles(parsedData.articles);
    setTotalResults(parsedData.totalResults);
    setLoading(false);
    props.setProgress(100);
  };

  useEffect(() => {
    newsData();
  }, []);

  const handlePreviousClick = async () => {
    pageDecrement();
    newsData();
  };

  const handleNextClick = async () => {
    pageIncrement();
    newsData();
  };

  const fetchMoreData = async () => {
    pageIncrement();
    const url = `https://newsapi.org/v2/top-headlines?apiKey=${props.apiKey}&country=${props.country}&category=${props.category}&page=${page}&pageSize=${props.pageSize}`;
    let data = await fetch(url);
    let parsedData = await data.json();
    setArticles(articles.concat(parsedData.articles));
    setTotalResults(parsedData.totalResults);
  };

  return (
    <>
      <div className="container my-3">
        <h1 className="text-center" style={{ marginTop: "90px" }}>
          <img
            src={process.env.PUBLIC_URL + "/newsBilla.jpg"}
            style={{ height: "70px" }}
            alt="logo"
          />
          NewsBilla - Top Headlines From{" "}
          <span className="badge bg-info">{capitalize(props.category)}</span>{" "}
          Category
        </h1>

        {/* Home Page Start */}
        {loading && <Spinner />}

        {props.category === "general" && !loading && (
          <>
            <div className="row">
              {articles.map((element) => {
                return (
                  <div className="col-md-4" key={element.url}>
                    <NewsItem
                      title={element.title ? element.title : "No Title Found"}
                      description={
                        element.description
                          ? element.description
                          : "No Description Found"
                      }
                      imageUrl={
                        element.urlToImage
                          ? element.urlToImage
                          : process.env.PUBLIC_URL + "/newsBilla.jpg"
                      }
                      newsUrl={element.url}
                      author={element.author}
                      date={element.publishedAt}
                      source={element.source.name}
                    />
                  </div>
                );
              })}
            </div>
            <div className="d-flex justify-content-between my-3">
              <button
                type="button"
                className="btn btn-dark"
                disabled={page <= 1}
                onClick={handlePreviousClick}
              >
                &larr; Previous{" "}
              </button>
              <button
                type="button"
                className="btn btn-dark"
                disabled={page > totalResults / props.pageSize}
                onClick={handleNextClick}
              >
                Next &rarr;{" "}
              </button>
            </div>
          </>
        )}
        {/* Home Page End */}

        {/* Other Categories Start */}
        {props.category !== "general" && (
          <InfiniteScroll
            dataLength={articles.length}
            next={fetchMoreData}
            hasMore={articles.length !== totalResults}
            loader={<Spinner />}
          >
            <div className="container">
              <div className="row">
                {articles.map((element) => {
                  return (
                    <div className="col-md-4" key={element.url}>
                      <NewsItem
                        title={element.title ? element.title : "No Title Found"}
                        description={
                          element.description
                            ? element.description
                            : "No Description Found"
                        }
                        imageUrl={
                          element.urlToImage
                            ? element.urlToImage
                            : process.env.PUBLIC_URL + "/newsBilla.jpg"
                        }
                        newsUrl={element.url}
                        author={element.author}
                        date={element.publishedAt}
                        source={element.source.name}
                      />
                    </div>
                  );
                })}
              </div>
            </div>
          </InfiniteScroll>
        )}
        {/* Other Categories End */}
      </div>
    </>
  );
};

export default News;

News.defaultProps = {
  country: "in",
  pageSize: 9,
  category: "general",
};

News.propTypes = {
  country: PropTypes.string,
  pageSize: PropTypes.number,
  category: PropTypes.string,
};
