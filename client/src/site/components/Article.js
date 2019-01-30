import React from 'react';

const Article = ({
    url,
    source,
    title,
    summary,
}) => (
    <div className="article">
        <div className="article__header">
            <div className="article__title">
                {title}&nbsp;
                <a href={url} className="article__url">
                    [source]
                </a>
            </div>
        </div>
        <div className="article__summary">
            {summary}
        </div>
    </div>
);

export default Article;
