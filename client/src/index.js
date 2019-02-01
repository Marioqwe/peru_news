import React from 'react';
import ReactDOM from 'react-dom';
import { BrowserRouter as Router } from 'react-router-dom';

import './styles/index.scss';

import Root from './site';

const render = (Component) => {
    ReactDOM.render(
        <Router>
            <Component />
        </Router>,
        document.getElementById('react-root'),
    );
};

render(Root);

if (module.hot) {
    module.hot.accept('./site', () => { render(Root); });
}
