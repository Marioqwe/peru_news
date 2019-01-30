import React from 'react';

import ArticleBoard from './components/ArticleBoard';
import axios from "axios";
import { Link, Route } from 'react-router-dom';

const FilteredArticleBoard = ({ filter }) => (
    <ArticleBoard
        filter={filter}
    />
);

class MainPage extends React.Component {
    constructor(props) {
        super(props);
        this._isMounted = false;
        this.state = {
            sections: [],
            filter: undefined,
            isFetching: false,
            currentSection: 'all',
        };
    }

    componentDidMount() {
        this._isMounted = true;
        this.fetchSections();
    }

    componentWillUnmount() {
        this._isMounted = false;
        this.setState({ isFetching: false });
    }

    fetchSections = () => {
        this.setState({ isFetching: true });
        axios.get('https://api.perunews.xyz/v1/sections/')
            .then((res) => {
                if (!this._isMounted) return;
                this.setState({ isFetching: false });

                const data = res['data'];
                if (data['status'] === 'ok') {
                    this.setState({ sections: ['all', ...data['sections']], });
                }

                // should not happen.
                // if we reach this point then there is
                // something wrong with our restful api.
            })
            .catch((err) => {
                if (!this._isMounted) return;
                this.setState({ isFetching: false });

                // handle error.
            })
    };

    handleSelectSection = name => this.setState({ currentSection: name });

    render() {
        const { sections, isFetching, currentSection } = this.state;
        return (
            <div className="page">
                <div className="page__header">
                    <div className="page__title">
                        Peru News
                    </div>
                    <div className="sections-bar">
                        {sections.map(name => (
                            <Link
                                key={name}
                                to={`/${name}`}
                                onClick={() => this.handleSelectSection(name)}
                                className={currentSection === name ? 'selected-section' : ''}
                            >
                                {name}
                            </Link>
                        ))}
                    </div>
                </div>
                <div className="page__body">
                    {sections.map(name => (
                        <Route
                            key={name}
                            path={`/${name}`}
                            render={props => <FilteredArticleBoard {...props} filter={name} />}
                        />
                    ))}
                </div>
            </div>
        );
    }
}

export default MainPage;
