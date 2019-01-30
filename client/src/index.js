import React from 'react';
import ReactDOM from 'react-dom';
import { BrowserRouter as Router } from 'react-router-dom';

import './styles/index.scss';

import MainPage from './site';

const render = (Component) => {
    ReactDOM.render(
        <Router>
            <Component />
        </Router>,
        document.getElementById('react-root'),
    );
};

render(MainPage);

if (module.hot) {
    module.hot.accept('./site', () => { render(MainPage); });
}
