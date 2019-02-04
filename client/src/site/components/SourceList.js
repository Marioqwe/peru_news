import React from 'react';
import { Link } from 'react-router-dom';

import { LocalStorageManager } from '../storage';

class SourceList extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            selectedSources: LocalStorageManager.getState() || [],
        };
    }

    handleClickSource = (sourceName) => {
        let { selectedSources } = this.state;
        if (selectedSources.includes(sourceName)) {
            selectedSources = selectedSources.filter(item => item !== sourceName);
        } else {
            selectedSources.push(sourceName);
        }

        LocalStorageManager.setState(selectedSources);
        this.setState({ selectedSources, });
    };

    render() {
        const { selectedSources } = this.state;
        return (
            <div className="source-list">
                <div className="source-list__text">
                    Select sources you want to follow.
                </div>
                <div
                    className={`source-list__item ${selectedSources.includes('rpp') ? 'selected' : ''}`}
                    onClick={() => this.handleClickSource('rpp')}
                >
                    RPP
                </div>
                <div
                    className={`source-list__item ${selectedSources.includes('peru21') ? 'selected' : ''}`}
                    onClick={() => this.handleClickSource('peru21')}
                >
                    Peru 21
                </div>
                <Link to="/politica" className="source-list__continue-btn">
                    Continue
                </Link>
            </div>
        );
    }
}

export default SourceList;
