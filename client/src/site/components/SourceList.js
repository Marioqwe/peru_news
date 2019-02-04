import React from 'react';
import { Link } from 'react-router-dom';

import { LocalStorageManager } from '../storage';
import { SOURCES } from '../settings';

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
                {SOURCES.map(src => (
                    <div
                        key={src.id}
                        className={`source-list__item ${selectedSources.includes(src.id) ? 'selected' : ''}`}
                        onClick={() => this.handleClickSource(src.id)}
                    >
                        {src.name}
                    </div>
                ))}
                <Link to="/politica" className="source-list__continue-btn">
                    Continue
                </Link>
            </div>
        );
    }
}

export default SourceList;
