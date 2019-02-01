import React from 'react';
import { Redirect, Route, Switch } from 'react-router-dom';

import MainPage from './components/MainPage';

const Root = () => (
    <Switch>
        <Route exact path="/" render={() => <Redirect to="/politica" />} />
        <Route path="/:section" component={MainPage} />
    </Switch>
);

export default Root;
