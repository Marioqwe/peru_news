export function normalizeUrl(url) {
    return url.replace(/^https?:\/\/w*.?/, '').split('/', 1)[0];
}

export function calcNumPages(totalResults, pageSize) {
    return Math.ceil(totalResults / pageSize);
}
