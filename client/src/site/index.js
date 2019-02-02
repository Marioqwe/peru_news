import React from 'react';
import { Link, Route, Switch } from 'react-router-dom';

import SectionPage from './components/SectionPage'
import SourceList from './components/SourceList';

const Root = () => (
    <div className="page">
        <div className="page__header">
            <Link to="/" className="page__title">
                Peru News
            </Link>
        </div>
        <div className="page__body">
            <Switch>
                <Route exact path="/" component={SourceList} />
                <Route exact path="/:section" component={SectionPage} />
            </Switch>
        </div>
    </div>
);

export default Root;
