import React from 'react';
import { Link } from 'react-router-dom';

import { SECTIONS } from '../settings';

class SectionBar extends React.Component {
    state = {
        currSection: undefined,
    };

    handleClick = (secName) => {
        this.setState({ currSection: secName, });
    };

    render() {
        const { currSection } = this.state;
        return (
            <div className="sections-bar">
                {SECTIONS.map(secName => (
                    <Link
                        key={secName}
                        to={`/${secName}`}
                        onClick={() => this.handleClick(secName)}
                        className={currSection === secName ? 'selected-section' : ''}
                    >
                        {secName}
                    </Link>
                ))}
            </div>
        );
    }
}

export default SectionBar;
