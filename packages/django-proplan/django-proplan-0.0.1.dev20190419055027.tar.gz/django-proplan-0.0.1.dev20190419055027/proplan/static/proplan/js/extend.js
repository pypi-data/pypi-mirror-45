/*
 * extend.js
 *
 * Extending standard JavaScript objects.
 *
 */


/* Check the beginning of the string. */
if (!String.prototype.startsWith) {
    String.prototype.startsWith = function(test) {
        return this.IndexOf(test) == 0
    }
}


/* Check the ending of the string */
if (!String.prototype.endsWith) {
    String.prototype.endsWith = function(test) {
        return this.lastIndexOf(test) + test.length == this.length
    }
}


/* Uppercase translation of the first letter of the text. */
if (!String.prototype.capFirst) {
    String.prototype.capFirst = function() {
        if (this.length == 0) return this;
        return this[0].toUpperCase() + this.slice(1)
    }
}


/* Trim the string to the specified number of characters.
 * If the second parameter is true, no ellipsis is added.
 */
if (!String.prototype.truncateChars) {
    String.prototype.truncateChars = function(l, d) {
        var s = this;
        if (s && l && s.length > l) return s.slice(0, l) + (d ? '' : '...');
        return s
    }
}


/* Trim the string to the specified number of words.
 * If the second parameter is true, no ellipsis is added.
 */
if (!String.prototype.truncateWords) {
    String.prototype.truncateWords = function(l, d) {
        var s = this;
        if (!s) return s;
        s = s.split(/\s+/);
        if (l && s.length > l) return s.slice(0, l).join(' ') + (d ? '' : '...');
        return s.join(' ')
    }
}


/* Padding lines on the left (spaces by default). */
if (!String.prototype.leftPad) {
    String.prototype.leftPad = function(l, c) {
        var s = '',
            c = c || ' ',
            l = (l || 2) - this.length;
        while (s.length < l) s += c;
        return s + this;
    }
}


/* Convert numbers to strings with padding (default is zero). */
if (!Number.prototype.leftPad) {
    Number.prototype.leftPad = function(l, c) {
        return String(this).leftPad(l, c || '0');
    }
}


/* Rounding numbers. */
if (!Number.prototype.round) {
    Number.prototype.round = function(c) {
        c = c || 0;
        return Math.round(this * Math.pow(10, c)) / Math.pow(10, c);
    }
}


/* The sum of the values of the list. */
if (!Array.prototype.sum) {
    Array.prototype.sum = function() {
        return this.reduce(function(p, c) {return p + c}, 0);
    }
}


/* The average value from the list. */
if (!Array.prototype.avg) {
    Array.prototype.avg = function() {
        return this.sum() / (this.length || 1);
    }
}
