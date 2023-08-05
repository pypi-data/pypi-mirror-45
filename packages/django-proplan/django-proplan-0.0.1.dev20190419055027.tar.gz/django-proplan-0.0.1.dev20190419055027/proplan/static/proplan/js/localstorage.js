/*
 * localstorage.js
 * 
 * Handlers for localStorage.
 * 
 */

/* Check if localStorage and JSON converter can be executed. */
function checkLocalStorage() {
    if (!window.localStorage || !window.JSON || !window.JSON.stringify) {
        console.error('localStorage or JSON.stringify is undefined');
        return false
    }
    return true
}

/* Function to add settings to localStorage.
 * `fkey` - full key to value. If it defined then the `key` not used.
 */
function toLocalStorage(key, val, fkey) {
    if (!checkLocalStorage()) return;
    var k = fkey || window.SETTINGS_KEY + key,
        v = JSON.stringify(val);
    localStorage.setItem(k, v);
    return [k, v]
}

/* Function to get settings from localStorage.
 * `fkey` - full key to value. If it defined then the `key` not used.
 */
function fromLocalStorage(key, fkey) {
    if (!checkLocalStorage()) return;
    var val = localStorage.getItem(fkey || window.SETTINGS_KEY + key);
    try {
        return JSON.parse(val)
    } catch (e) {
        return val
    }
}
