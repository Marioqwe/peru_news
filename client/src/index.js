import React from 'react';
import ReactDOM from 'react-dom';

import Root from './site';

const render = (Component) => {
    ReactDOM.render(
        <Component />,
        document.getElementById('react-root'),
    );
};

render(Root);

if (module.hot) {
    module.hot.accept('./site', () => { render(Root); });
}
