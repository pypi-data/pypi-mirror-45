parcelRequire=function(e,r,t,n){var i,o="function"==typeof parcelRequire&&parcelRequire,u="function"==typeof require&&require;function f(t,n){if(!r[t]){if(!e[t]){var i="function"==typeof parcelRequire&&parcelRequire;if(!n&&i)return i(t,!0);if(o)return o(t,!0);if(u&&"string"==typeof t)return u(t);var c=new Error("Cannot find module '"+t+"'");throw c.code="MODULE_NOT_FOUND",c}p.resolve=function(r){return e[t][1][r]||r},p.cache={};var l=r[t]=new f.Module(t);e[t][0].call(l.exports,p,l,l.exports,this)}return r[t].exports;function p(e){return f(p.resolve(e))}}f.isParcelRequire=!0,f.Module=function(e){this.id=e,this.bundle=f,this.exports={}},f.modules=e,f.cache=r,f.parent=o,f.register=function(r,t){e[r]=[function(e,r){r.exports=t},{}]};for(var c=0;c<t.length;c++)try{f(t[c])}catch(e){i||(i=e)}if(t.length){var l=f(t[t.length-1]);"object"==typeof exports&&"undefined"!=typeof module?module.exports=l:"function"==typeof define&&define.amd?define(function(){return l}):n&&(this[n]=l)}if(parcelRequire=f,i)throw i;return f}({"y60x":[function(require,module,exports) {
"use strict";module.exports=function(){var r,t=Object.assign;return"function"==typeof t&&(t(r={foo:"raz"},{bar:"dwa"},{trzy:"trzy"}),r.foo+r.bar+r.trzy==="razdwatrzy")};
},{}],"gq3z":[function(require,module,exports) {
"use strict";module.exports=function(){try{return Object.keys("primitive"),!0}catch(t){return!1}};
},{}],"qYbH":[function(require,module,exports) {
"use strict";module.exports=function(){};
},{}],"f648":[function(require,module,exports) {
"use strict";var n=require("../function/noop")();module.exports=function(r){return r!==n&&null!==r};
},{"../function/noop":"qYbH"}],"3cwc":[function(require,module,exports) {
"use strict";var e=require("../is-value"),r=Object.keys;module.exports=function(t){return r(e(t)?Object(t):t)};
},{"../is-value":"f648"}],"nhVq":[function(require,module,exports) {
"use strict";module.exports=require("./is-implemented")()?Object.keys:require("./shim");
},{"./is-implemented":"gq3z","./shim":"3cwc"}],"XtTh":[function(require,module,exports) {
"use strict";var e=require("./is-value");module.exports=function(r){if(!e(r))throw new TypeError("Cannot use null or undefined");return r};
},{"./is-value":"f648"}],"ojUF":[function(require,module,exports) {
"use strict";var r=require("../keys"),e=require("../valid-value"),t=Math.max;module.exports=function(a,i){var o,u,c,n=t(arguments.length,2);for(a=Object(e(a)),c=function(r){try{a[r]=i[r]}catch(e){o||(o=e)}},u=1;u<n;++u)i=arguments[u],r(i).forEach(c);if(void 0!==o)throw o;return a};
},{"../keys":"nhVq","../valid-value":"XtTh"}],"flj+":[function(require,module,exports) {
"use strict";module.exports=require("./is-implemented")()?Object.assign:require("./shim");
},{"./is-implemented":"y60x","./shim":"ojUF"}],"1uac":[function(require,module,exports) {

"use strict";var r=require("./is-value"),e=Array.prototype.forEach,t=Object.create,c=function(r,e){var t;for(t in r)e[t]=r[t]};module.exports=function(n){var o=t(null);return e.call(arguments,function(e){r(e)&&c(Object(e),o)}),o};
},{"./is-value":"f648"}],"az0W":[function(require,module,exports) {
"use strict";module.exports=function(t){return"function"==typeof t};
},{}],"753d":[function(require,module,exports) {
"use strict";var n="razdwatrzy";module.exports=function(){return"function"==typeof n.contains&&(!0===n.contains("dwa")&&!1===n.contains("foo"))};
},{}],"3RK5":[function(require,module,exports) {
"use strict";var t=String.prototype.indexOf;module.exports=function(r){return t.call(this,r,arguments[1])>-1};
},{}],"z+/R":[function(require,module,exports) {
"use strict";module.exports=require("./is-implemented")()?String.prototype.contains:require("./shim");
},{"./is-implemented":"753d","./shim":"3RK5"}],"iAJW":[function(require,module,exports) {
"use strict";var e,l=require("es5-ext/object/assign"),r=require("es5-ext/object/normalize-options"),n=require("es5-ext/object/is-callable"),t=require("es5-ext/string/#/contains");(e=module.exports=function(e,n){var i,u,a,o,c;return arguments.length<2||"string"!=typeof e?(o=n,n=e,e=null):o=arguments[2],null==e?(i=a=!0,u=!1):(i=t.call(e,"c"),u=t.call(e,"e"),a=t.call(e,"w")),c={value:n,configurable:i,enumerable:u,writable:a},o?l(r(o),c):c}).gs=function(e,i,u){var a,o,c,s;return"string"!=typeof e?(c=u,u=i,i=e,e=null):c=arguments[3],null==i?i=void 0:n(i)?null==u?u=void 0:n(u)||(c=u,u=void 0):(c=i,i=u=void 0),null==e?(a=!0,o=!1):(a=t.call(e,"c"),o=t.call(e,"e")),s={get:i,set:u,configurable:a,enumerable:o},c?l(r(c),s):s};
},{"es5-ext/object/assign":"flj+","es5-ext/object/normalize-options":"1uac","es5-ext/object/is-callable":"az0W","es5-ext/string/#/contains":"z+/R"}],"N9bW":[function(require,module,exports) {
"use strict";module.exports=function(t){if("function"!=typeof t)throw new TypeError(t+" is not a function");return t};
},{}],"PR/g":[function(require,module,exports) {
"use strict";var e,t,r,l,i,n,c,s=require("d"),o=require("es5-ext/object/valid-callable"),_=Function.prototype.apply,a=Function.prototype.call,h=Object.create,u=Object.defineProperty,f=Object.defineProperties,p=Object.prototype.hasOwnProperty,b={configurable:!0,enumerable:!1,writable:!0};t=function(t,l){var i,n;return o(l),n=this,e.call(this,t,i=function(){r.call(n,t,i),_.call(l,this,arguments)}),i.__eeOnceListener__=l,this},i={on:e=function(e,t){var r;return o(t),p.call(this,"__ee__")?r=this.__ee__:(r=b.value=h(null),u(this,"__ee__",b),b.value=null),r[e]?"object"==typeof r[e]?r[e].push(t):r[e]=[r[e],t]:r[e]=t,this},once:t,off:r=function(e,t){var r,l,i,n;if(o(t),!p.call(this,"__ee__"))return this;if(!(r=this.__ee__)[e])return this;if("object"==typeof(l=r[e]))for(n=0;i=l[n];++n)i!==t&&i.__eeOnceListener__!==t||(2===l.length?r[e]=l[n?0:1]:l.splice(n,1));else l!==t&&l.__eeOnceListener__!==t||delete r[e];return this},emit:l=function(e){var t,r,l,i,n;if(p.call(this,"__ee__")&&(i=this.__ee__[e]))if("object"==typeof i){for(r=arguments.length,n=new Array(r-1),t=1;t<r;++t)n[t-1]=arguments[t];for(i=i.slice(),t=0;l=i[t];++t)_.call(l,this,n)}else switch(arguments.length){case 1:a.call(i,this);break;case 2:a.call(i,this,arguments[1]);break;case 3:a.call(i,this,arguments[1],arguments[2]);break;default:for(r=arguments.length,n=new Array(r-1),t=1;t<r;++t)n[t-1]=arguments[t];_.call(i,this,n)}}},n={on:s(e),once:s(t),off:s(r),emit:s(l)},c=f({},n),module.exports=exports=function(e){return null==e?h(c):f(Object(e),n)},exports.methods=i;
},{"d":"iAJW","es5-ext/object/valid-callable":"N9bW"}],"xsaR":[function(require,module,exports) {
"use strict";var e=n(require("event-emitter"));function n(e){return e&&e.__esModule?e:{default:e}}var t={socket:null,events:(0,e.default)(),connect:function(){var e=this,n=window.ShuupAdminConfig.settings.adminChannelUrl;n&&(this.socket=new WebSocket("ws://".concat(window.location.host).concat(n)),this.socket.onmessage=function(n){var t=JSON.parse(n.data);e.onReceive(t)},this.socket.onclose=function(e){console.error("Channel socket closed unexpectedly")})},send:function(e){this.socket.send(JSON.stringify(e))},onReceive:function(e){this.events.emit("received",e)}};window.ShuupAdminChannelConfig.connectOnLoad&&t.connect(),window.ShuupAdminChannel=t,t.events.on("received",function(e){"alert"===e.command&&Messages.enqueue({tags:e.level,text:e.message})});
},{"event-emitter":"PR/g"}]},{},["xsaR"], null)
//# sourceMappingURL=shuup-admin-channel.js.map