import React from 'react';

import { normalizeUrl } from '../utils';

const Article = ({
    url,
    source,
    title,
}) => (
    <div className="article">
        <div className="article__header">
            <a href={url} className="article__title">
                {title}&nbsp;
            </a>
            <span className="article__url">
                ({normalizeUrl(url)})
            </span>
        </div>
    </div>
);

export default Article;
