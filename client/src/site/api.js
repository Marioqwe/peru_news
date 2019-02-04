import axios from 'axios';

import { API_URL } from './settings';

export function fetchArticles(
    {
        sources,
        section,
        date,
        page,
        pageSize,
    },
    onSuccess,
    onError,
) {
    const params = `source=${sources.join(',')}&section=${section}&pageSize=${pageSize}&page=${page}&date=${date}`;
    axios.get(`${API_URL}/articles/?${params}`)
        .then(res => onSuccess(res))
        .catch(err => onError(err));
}
