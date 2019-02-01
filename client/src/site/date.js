export function getTodayDate() {
    return new Date();
}

export function getPrevDateFromDate(date) {
    const ms = date.setDate(date.getDate() - 1);
    return new Date(ms);
}

function normalize(num) {
    if (num < 10) {
        return `0${num}`;
    }

    return num;
}

export function toStrFormat(date) {
    const yyyy = date.getFullYear();
    const mm = normalize(date.getMonth() + 1); // month starts at 0.
    const dd = normalize(date.getDate());

    return `${yyyy}-${mm}-${dd}`;
}

export function prettyStrFormat(strDate) {
    const dateArray = strDate.split('-');
    // see stackoverflow.com/questions/2488313/
    const date = new Date(
        parseInt(dateArray[0]),
        parseInt(dateArray[1]) - 1,
        parseInt(dateArray[2])
    );
    return date.toDateString();
}
