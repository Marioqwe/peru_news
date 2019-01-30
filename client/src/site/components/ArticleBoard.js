import React from 'react';
import axios from 'axios';
import Article from './Article';

const PAGE_SIZE = 10;

const numberOfPages = (totalResults, pageSize) => Math.ceil(totalResults / pageSize);

class ArticleBoard extends React.Component {
    constructor(props) {
        super(props);
        this._isMounted = false;
        this.state = {
            articles: [],
            isFetching: false,
            currentPage: 0,
            totalResults: 0,
        };
    }

    componentDidMount() {
        this._isMounted = true;
        window.addEventListener('scroll', this.handleScroll, true);
        this.fetchArticles();
    }

    componentWillUnmount() {
        this._isMounted = false;
        window.removeEventListener('scroll', this.handleScroll);
        this.setState({ isFetching: false });
    }

    fetchArticles = () => {
        const { currentPage, totalResults } = this.state;
        if (currentPage !== 0) {
            const nPages = numberOfPages(totalResults, PAGE_SIZE);
            if (currentPage >= nPages) {
                return;
            }
        }

        const nextPage = currentPage + 1;
        const { filter } = this.props;
        const url = `https://api.perunews.xyz/v1/articles/?source=rpp&section=${filter}&pageSize=${PAGE_SIZE}&page=${nextPage}`;

        this.setState({ isFetching: true });
        axios.get(url)
            .then((res) => {
                if (!this._isMounted) return;
                this.setState({ isFetching: false });

                const data = res['data'];
                if (data['status'] === 'ok') {
                    const { articles } = this.state;
                    this.setState({
                        articles: [...articles, ...data['articles']],
                        totalResults: data['totalResults'],
                        currentPage: nextPage,
                    });
                }

                // should not happen.
                // if we reach this point then there is
                // something wrong with our restful api.
            })
            .catch((err) => {
                if (!this._isMounted) return;
                this.setState({ isFetching: false, });

                // handle error.
            });
    };

    handleScroll = (e) => {
        const bottom = e.target.scrollHeight - e.target.scrollTop === e.target.clientHeight;
        if (bottom) {
            const { isFetching } = this.state;
            if (!isFetching) {
                this.fetchArticles();
            }
        }
    };

    render() {
        const { articles, isFetching } = this.state;
        const { filter } = this.props;
        return (
            <div className="article-board">
                {articles.map(a => {
                    if (filter !== undefined
                        && a['section'] !== filter) { return; }
                    return (
                        <Article
                            key={a['headline']}
                            url={a['url']}
                            source={a['source']['name']}
                            title={a['headline']}
                            summary={a['summary']}
                        />
                    );
                })}
                {isFetching && (
                    <div className="article-board__loading-div">
                        LOADING ...
                    </div>
                )}
            </div>
        );
    }
}

export default ArticleBoard;
