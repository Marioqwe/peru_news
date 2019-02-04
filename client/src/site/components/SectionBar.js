import React from 'react';
import { Link } from 'react-router-dom';

import { SECTIONS } from '../settings';

const SectionBar = ({ section }) => (
    <div className="sections-bar">
        {SECTIONS.map(secName => (
            <Link
                key={secName}
                to={`/${secName}`}
                className={section === secName ? 'selected-section' : ''}
            >
                {secName}
            </Link>
        ))}
    </div>
);

export default SectionBar;
