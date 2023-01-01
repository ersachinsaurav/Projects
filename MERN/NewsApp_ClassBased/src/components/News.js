import React, { Component } from "react";
import NewsItem from "./NewsItem";
import Spinner from "./Spinner";
import PropTypes from "prop-types";
import InfiniteScroll from "react-infinite-scroll-component";

export class News extends Component {
  static defaultProps = {
    country: "in",
    pageSize: 9,
    category: "general",
  };

  static propTypes = {
    country: PropTypes.string,
    pageSize: PropTypes.number,
    category: PropTypes.string,
  };

  capitalize = (word) => {
    return word.charAt(0).toUpperCase() + word.slice(1).toLowerCase();
  };

  constructor(props) {
    super(props);
    this.state = {
      articles: [],
      loading: true,
      page: 1,
      totalResults: 0
    };
    document.title = `${this.capitalize(props.category)} - NewsBilla`;
  }

  async newsData() {
    this.setState({ loading: true });
    this.props.setProgress(10);
    const url = `https://newsapi.org/v2/top-headlines?apiKey=${this.props.apiKey}&country=${this.props.country}&category=${this.props.category}&page=${this.state.page}&pageSize=${this.props.pageSize}`;
    let data = await fetch(url);
    this.props.setProgress(30);
    let parsedData = await data.json();
    this.props.setProgress(60);
    this.setState({
      articles: parsedData.articles,
      totalResults: parsedData.totalResults,
      loading: false,
    });
    this.props.setProgress(100);
  }

  async componentDidMount() {
    this.newsData();
  }

  handlePreviousClick = async () => {
    this.setState({ page: --this.state.page });
    this.newsData();
  };

  handleNextClick = async () => {
    this.setState({ page: ++this.state.page });
    this.newsData();
  };

  fetchMoreData = async () => {
    this.setState({ page: ++this.state.page });
    const url = `https://newsapi.org/v2/top-headlines?apiKey=${this.props.apiKey}&country=${this.props.country}&category=${this.props.category}&page=${this.state.page}&pageSize=${this.props.pageSize}`;
    let data = await fetch(url);
    let parsedData = await data.json();
    this.setState({
      articles: this.state.articles.concat(parsedData.articles),
      totalResults: parsedData.totalResults,
    });
  };

  render() {
    return (
      <>
        <div className="container my-3">
          <h1 className="text-center" style={{marginTop: "90px"}}>
            <img
              src={process.env.PUBLIC_URL + "/newsBilla.jpg"}
              style={{ height: "70px" }}
              alt="logo"
            />
            NewsBilla - Top Headlines From{" "}
            <span className="badge bg-info">
              {this.capitalize(this.props.category)}
            </span>{" "}
            Category
          </h1>

          {/* Home Page Start */}
          {this.state.loading && <Spinner />}

          {this.props.category === "general" && !this.state.loading && (
            <>
              <div className="row">
                {this.state.articles.map((element) => {
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
                  disabled={this.state.page <= 1}
                  onClick={this.handlePreviousClick}
                >
                  &larr; Previous{" "}
                </button>
                <button
                  type="button"
                  className="btn btn-dark"
                  disabled={
                    this.state.page >
                    this.state.totalResults / this.props.pageSize
                  }
                  onClick={this.handleNextClick}
                >
                  Next &rarr;{" "}
                </button>
              </div>
            </>
          )}
          {/* Home Page End */}

          {/* Other Categories Start */}
          {this.props.category !== "general" && (
            <InfiniteScroll
              dataLength={this.state.articles.length}
              next={this.fetchMoreData}
              hasMore={this.state.articles.length !== this.state.totalResults}
              loader={<Spinner />}
            >
              <div className="container">
                <div className="row">
                  {this.state.articles.map((element) => {
                    return (
                      <div className="col-md-4" key={element.url}>
                        <NewsItem
                          title={
                            element.title ? element.title : "No Title Found"
                          }
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
  }
}

export default News;
