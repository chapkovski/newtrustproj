(function(e){function t(t){for(var n,i,s=t[0],l=t[1],c=t[2],d=0,p=[];d<s.length;d++)i=s[d],Object.prototype.hasOwnProperty.call(a,i)&&a[i]&&p.push(a[i][0]),a[i]=0;for(n in l)Object.prototype.hasOwnProperty.call(l,n)&&(e[n]=l[n]);u&&u(t);while(p.length)p.shift()();return r.push.apply(r,c||[]),o()}function o(){for(var e,t=0;t<r.length;t++){for(var o=r[t],n=!0,s=1;s<o.length;s++){var l=o[s];0!==a[l]&&(n=!1)}n&&(r.splice(t--,1),e=i(i.s=o[0]))}return e}var n={},a={main:0},r=[];function i(t){if(n[t])return n[t].exports;var o=n[t]={i:t,l:!1,exports:{}};return e[t].call(o.exports,o,o.exports,i),o.l=!0,o.exports}i.m=e,i.c=n,i.d=function(e,t,o){i.o(e,t)||Object.defineProperty(e,t,{enumerable:!0,get:o})},i.r=function(e){"undefined"!==typeof Symbol&&Symbol.toStringTag&&Object.defineProperty(e,Symbol.toStringTag,{value:"Module"}),Object.defineProperty(e,"__esModule",{value:!0})},i.t=function(e,t){if(1&t&&(e=i(e)),8&t)return e;if(4&t&&"object"===typeof e&&e&&e.__esModule)return e;var o=Object.create(null);if(i.r(o),Object.defineProperty(o,"default",{enumerable:!0,value:e}),2&t&&"string"!=typeof e)for(var n in e)i.d(o,n,function(t){return e[t]}.bind(null,n));return o},i.n=function(e){var t=e&&e.__esModule?function(){return e["default"]}:function(){return e};return i.d(t,"a",t),t},i.o=function(e,t){return Object.prototype.hasOwnProperty.call(e,t)},i.p="/static/vue/";var s=window["webpackJsonp"]=window["webpackJsonp"]||[],l=s.push.bind(s);s.push=t,s=s.slice();for(var c=0;c<s.length;c++)t(s[c]);var u=l;r.push([0,"chunk-vendors"]),o()})({0:function(e,t,o){e.exports=o("56d7")},"56d7":function(e,t,o){"use strict";o.r(t);o("e260"),o("e6cf"),o("cca6"),o("a79d");var n=o("2b0e"),a=function(){var e=this,t=e.$createElement,o=e._self._c||t;return o("div",{attrs:{id:"app"}},[o("TypeAhead")],1)},r=[],i=function(){var e=this,t=e.$createElement,o=e._self._c||t;return o("div",{staticClass:"form-group required"},[o("div",{staticClass:"controls  field-location"},[o("vue-google-autocomplete",{ref:"address",attrs:{id:"id_birthplace",classname:"form-control",placeholder:"Введите название",types:"(cities)",name:"birthplace"},on:{placechanged:e.getAddressData}})],1)])},s=[],l=function(){var e=this,t=e.$createElement,o=e._self._c||t;return o("input",{directives:[{name:"model",rawName:"v-model",value:e.autocompleteText,expression:"autocompleteText"}],ref:"autocomplete",class:e.classname,attrs:{type:"text",id:e.id,placeholder:e.placeholder,required:!0,name:e.name},domProps:{value:e.autocompleteText},on:{focus:function(t){return e.onFocus()},blur:function(t){return e.onBlur()},change:e.onChange,keypress:e.onKeyPress,keyup:e.onKeyUp,input:function(t){t.target.composing||(e.autocompleteText=t.target.value)}}})},c=[],u=(o("99af"),o("caad"),o("2532"),o("b85c")),d={subpremise:"short_name",street_number:"short_name",route:"long_name",locality:"long_name",administrative_area_level_1:"short_name",administrative_area_level_2:"long_name",country:"long_name",postal_code:"short_name"},p=["locality","administrative_area_level_3"],f=["locality","sublocality","postal_code","country","administrative_area_level_1","administrative_area_level_2"],m={name:"VueGoogleAutocomplete",props:{id:{type:String,required:!0},name:String,classname:String,placeholder:{type:String,default:"Start typing"},types:{type:String,default:"address"},country:{type:[String,Array],default:null},enableGeolocation:{type:Boolean,default:!1},geolocationOptions:{type:Object,default:null}},data:function(){return{autocomplete:null,autocompleteText:"",geolocation:{geocoder:null,loc:null,position:null}}},watch:{autocompleteText:function(e,t){this.$emit("inputChange",{newVal:e,oldVal:t},this.id)},country:function(e,t){this.autocomplete.setComponentRestrictions({country:null===this.country?[]:this.country})}},mounted:function(){var e={};this.types&&(e.types=[this.types]),this.country&&(e.componentRestrictions={country:this.country}),this.autocomplete=new google.maps.places.Autocomplete(document.getElementById(this.id),e),this.autocomplete.addListener("place_changed",this.onPlaceChanged)},methods:{onPlaceChanged:function(){var e=this.autocomplete.getPlace();e.geometry?void 0!==e.address_components&&(this.$emit("placechanged",this.formatResult(e),e,this.id),this.autocompleteText=document.getElementById(this.id).value,this.onChange()):this.$emit("no-results-found",e,this.id)},onFocus:function(){this.biasAutocompleteLocation(),this.$emit("focus")},onBlur:function(){this.$emit("blur")},onChange:function(){this.$emit("change",this.autocompleteText)},onKeyPress:function(e){this.$emit("keypress",e)},onKeyUp:function(e){this.$emit("keyup",e)},clear:function(){this.autocompleteText=""},focus:function(){this.$refs.autocomplete.focus()},blur:function(){this.$refs.autocomplete.blur()},update:function(e){this.autocompleteText=e},updateCoordinates:function(e){var t=this;(e||e.lat||e.lng)&&(this.geolocation.geocoder||(this.geolocation.geocoder=new google.maps.Geocoder),this.geolocation.geocoder.geocode({location:e},(function(e,o){"OK"===o?(e=t.filterGeocodeResultTypes(e),e[0]?(t.$emit("placechanged",t.formatResult(e[0]),e[0],t.id),t.update(e[0].formatted_address)):t.$emit("error","no result for provided coordinates")):t.$emit("error","error getting address from coords")})))},geolocate:function(){var e=this;this.updateGeolocation((function(t,o){e.updateCoordinates(t)}))},updateGeolocation:function(){var e=this,t=arguments.length>0&&void 0!==arguments[0]?arguments[0]:null;if(navigator.geolocation){var o={};this.geolocationOptions&&Object.assign(o,this.geolocationOptions),navigator.geolocation.getCurrentPosition((function(o){var n={lat:o.coords.latitude,lng:o.coords.longitude};e.geolocation.loc=n,e.geolocation.position=o,t&&t(n,o)}),(function(t){e.$emit("error","Cannot get Coordinates from navigator",t)}),o)}},biasAutocompleteLocation:function(){var e=this;this.enableGeolocation&&this.updateGeolocation((function(t,o){var n=new google.maps.Circle({center:t,radius:o.coords.accuracy});e.autocomplete.setBounds(n.getBounds())}))},formatResult:function(e){for(var t={},o=0;o<e.address_components.length;o++){var n=e.address_components[o].types[0];if(d[n]){var a=e.address_components[o][d[n]];t[n]=a}}return t["latitude"]=e.geometry.location.lat(),t["longitude"]=e.geometry.location.lng(),t},filterGeocodeResultTypes:function(e){if(!e||!this.types)return e;var t=[],o=[this.types];o.includes("(cities)")&&(o=o.concat(p)),o.includes("(regions)")&&(o=o.concat(f));var n,a=Object(u["a"])(e);try{for(a.s();!(n=a.n()).done;){var r,i=n.value,s=Object(u["a"])(i.types);try{for(s.s();!(r=s.n()).done;){var l=r.value;if(o.includes(l)){t.push(i);break}}}catch(c){s.e(c)}finally{s.f()}}}catch(c){a.e(c)}finally{a.f()}return t}}},h=m,g=o("2877"),y=Object(g["a"])(h,l,c,!1,null,null,null),v=y.exports,_={name:"HelloWorld",components:{VueGoogleAutocomplete:v},data:function(){return{address:"",retrieved_address:""}},methods:{getAddressData:function(e,t){console.debug("PLACE",t.formatted_address),this.address=e,t&&t.formatted_address&&(this.retrieved_address=t.formatted_address)}}},b=_,O=(o("9392"),Object(g["a"])(b,i,s,!1,null,"30335ff8",null)),x=O.exports,$={name:"App",components:{TypeAhead:x}},w=$,T=Object(g["a"])(w,a,r,!1,null,null,null),j=T.exports;n["a"].config.productionTip=!1,new n["a"]({render:function(e){return e(j)}}).$mount("#birthplace_app")},"82a1":function(e,t,o){},9392:function(e,t,o){"use strict";var n=o("82a1"),a=o.n(n);a.a}});