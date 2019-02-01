import React from 'react';

import Article from './Article';
import * as date from '../date';
import * as api from '../api';
import * as utils from '../utils';
import { PAGE_SIZE } from '../settings';

class ArticleBoard extends React.Component {

    constructor(props) {
        super(props);
        this._isMounted = false;
        const today= date.getTodayDate();
        this.state = {
            articles: {[date.toStrFormat(today)]: []},
            currentDate: today,
            isFetching: false,
            currentPage: 0,
            totalResults: 0,
        };
    }

    componentDidMount() {
        this._isMounted = true;
        this.fetchArticles();
    }

    componentWillUnmount() {
        this._isMounted = false;
        this.setState({ isFetching: false });
    }

    fetchArticles = () => {
        const { currentPage, totalResults } = this.state;
        let { currentDate } = this.state;
        let strDate = date.toStrFormat(currentDate);
        let prevDate;
        if (currentPage !== 0) {
            const nPages = utils.calcNumPages(totalResults, PAGE_SIZE);
            if (currentPage >= nPages) {
                prevDate = date.getPrevDateFromDate(currentDate);
                strDate = date.toStrFormat(prevDate);
            }
        }

        if (prevDate !== undefined) currentDate = prevDate;

        const nextPage = prevDate !== undefined ? 1 : currentPage + 1;
        const { filter } = this.props;

        this.setState({ isFetching: true, currentDate }, () => {
            api.fetchArticles({
                source: 'rpp',
                section: filter,
                date: strDate,
                page: nextPage,
                pageSize: PAGE_SIZE,
            },
                (res) => {
                    if (!this._isMounted) return;

                    const data = res['data'];
                    if (data['status'] === 'ok') {
                        const { articles } = this.state;
                        if (articles[strDate] === undefined) articles[strDate] = [];
                        this.setState({
                            articles: {
                                ...articles,
                                [strDate]: [...articles[strDate],
                                    ...data['articles']],
                            },
                            totalResults: data['totalResults'],
                            currentPage: nextPage,
                            isFetching: false,
                        });
                    }

                    // should not happen.
                    // if we reach this point then there is
                    // something wrong with our restful api.
                },
                (err) => {
                    if (!this._isMounted) return;

                    this.setState({ isFetching: false, });

                    // handle error.
                }
            )
        });
    };

    handleLoadMore = (e) => {
        const { isFetching } = this.state;
        if (this._isMounted && !isFetching) {
            this.fetchArticles();
        }
    };

    render() {
        const { articles, isFetching } = this.state;
        const { filter } = this.props;
        return (
            <div className="article-board">
                {Object.keys(articles).map((d) => {
                    const items = articles[d];
                    return (
                        <React.Fragment key={d}>
                            <div className="article-board__chunk-header">
                                {date.prettyStrFormat(d)}
                            </div>
                            {items.map(a => {
                                if (filter !== undefined
                                    && a['section'] !== filter) { return; }
                                return (
                                    <Article
                                        key={a['headline']}
                                        url={a['url']}
                                        source={a['source']['name']}
                                        title={a['headline']}
                                    />
                                );
                            })}
                        </React.Fragment>
                    )
                })}

                <button
                    onClick={this.handleLoadMore}
                    className="article-board__load-btn"
                >
                    <i className={`fa fa-refresh fa-spin ${!isFetching && 'hidden'}`} />LOAD MORE
                </button>
            </div>
        );
    }
}

export default ArticleBoard;
