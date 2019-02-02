window.fakeStorage = {
    _data: {},
    setItem: function (id, val) {
        return this._data[id] = String(val);
    },
    getItem: function (id) {
        return this._data.hasOwnProperty(id) ? this._data[id] : undefined;
    },
    removeItem: function (id) {
        return delete this._data[id];
    },
    clear: function () {
        return this._data = {};
    }
};

const localStorageSupported = () => {
    const testKey = 'test';
    const storage = window.localStorage;
    try {
        storage.setItem(testKey, '1');
        storage.removeItem(testKey);
        return true;
    } catch (error) {
        return false;
    }
};

class _LocalStorageManager {
    constructor() {
        this.stateKey = 'stateKey';
        this.storage = localStorageSupported() ? window.localStorage : window.fakeStorage;
    }

    getState() {
        const stateJSON = this.storage.getItem(this.stateKey);
        return stateJSON ? JSON.parse(stateJSON) : undefined
    }

    setState(state) {
        this.storage.setItem(this.stateKey, JSON.stringify(state));
    }

    clearState() {
        this.storage.removeItem(this.stateKey);
    }
}

const LocalStorageManager = new _LocalStorageManager();
export { LocalStorageManager };
