(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([["chunk-2d0d2fb1"],{"5b8f":function(e,t,a){"use strict";a.r(t);var r=function(){var e=this,t=e.$createElement,a=e._self._c||t;return a("v-card",{staticClass:"mx-auto",attrs:{"max-width":"1000",raised:""}},[a("v-card-title",[e._v(" Product Items "),a("v-spacer"),a("v-text-field",{attrs:{"append-icon":"mdi-magnify",label:"Search","single-line":"","hide-details":""},model:{value:e.search,callback:function(t){e.search=t},expression:"search"}})],1),a("v-data-table",{attrs:{headers:e.headers,items:e.items,search:e.search}})],1)},s=[],c=a("bc3a"),n=a.n(c),d={data:function(){return{search:"",headers:[{text:"Product Id",align:"start",value:"id"},{text:"Product Type ID",value:"product_type_id"},{text:"Count",value:"count"}],items:[]}},mounted:function(){var e=this;n.a.get("product_items").then((function(t){e.items=t.data.product_items}))}},i=d,l=a("2877"),u=a("6544"),o=a.n(u),h=a("b0af"),p=a("99d9"),f=a("8fea"),m=a("2fa4"),v=a("8654"),b=Object(l["a"])(i,r,s,!1,null,null,null);t["default"]=b.exports;o()(b,{VCard:h["a"],VCardTitle:p["c"],VDataTable:f["a"],VSpacer:m["a"],VTextField:v["a"]})}}]);
//# sourceMappingURL=chunk-2d0d2fb1.f914dff9.js.map