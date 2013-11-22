/*
* JQuery util functions
* 
* Author: Faraz Masood Khan faraz@fanaticlab.com
* 
* Copyright (c) 2013 FanaticLab  
*/

String.prototype.trim = String.prototype.trim || function () {
    return this.replace(/^\s+|\s+$/g, "");
};

String.prototype.ltrim = String.prototype.ltrim || function () {
    return this.replace(/^\s+/, "");
};

String.prototype.rtrim = String.prototype.rtrim || function () {
    return this.replace(/\s+$/, "");
};

String.prototype.fulltrim = String.prototype.fulltrim || function () {
    return this.replace(/^[\n\s]+|[\s\n]+$/g, "").replace(/\s+/g, " ");
};
