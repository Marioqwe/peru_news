import React from 'react';

import ArticleBoard from './ArticleBoard';
import SectionBar from './SectionBar';

const SectionPage = ({ match }) => {
    const { section } = match.params;
    return (
        <React.Fragment>
            <SectionBar section={section} />
            <ArticleBoard key={section} filter={section} />
        </React.Fragment>
    );
};

export default SectionPage;
