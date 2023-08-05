(window.webpackJsonp=window.webpackJsonp||[]).push([[7],{1720:function(e,t,r){"use strict";r.r(t);var a=r(2),n=r(1674),i=r(1259),o=r.n(i),l=r(45);const s=o()(n.a),c=e=>{return{"=":">",">":"<","<":"="}[e]},m=l.c.div`
  width: 100%;
`,p=e=>{const{filterState:t,filterName:r,updateFunction:n,onChange:i}=e,o=t[r]||"=";return a.createElement("form",{style:{border:"1px solid gray",background:"white",borderRadius:"5px",width:"100%"}},a.createElement("input",{type:"text",id:"name",name:"user_name",style:{width:"calc(100% - 30px)",border:"none"},onChange:e=>{i(e.currentTarget.value)},placeholder:"number"}),a.createElement("button",{onClick:()=>{n({[r]:c(o)})}},o))},h=(e,t,r)=>({onChange:n})=>a.createElement(p,{onChange:n,filterState:e,filterName:t,updateFunction:r}),d=(e="=")=>(t,r)=>{const a=Number(t.value);return"="===e?r[t.id]===a:"<"===e?r[t.id]<a:">"===e?r[t.id]>a:r[t.id]},u={integer:h,number:h,string:()=>({onChange:e})=>a.createElement("form",null,a.createElement("input",{type:"text",id:"string-filter",name:"string-filter",onChange:t=>{e(t.currentTarget.value)},placeholder:"string"}))},y={integer:d,number:d,string:()=>(e,t)=>-1!==t[e.id].toLowerCase().indexOf(e.value.toLowerCase())};class g extends a.PureComponent{constructor(e){super(e),this.state={filters:{},showFilters:!1}}render(){const{data:{data:e,schema:t},height:r}=this.props,{filters:n,showFilters:i}=this.state,{primaryKey:o=[]}=t,l=t.fields.map(e=>"string"===e.type||"number"===e.type||"integer"===e.type?{Header:e.name,accessor:e.name,fixed:-1!==o.indexOf(e.name)&&"left",filterMethod:(t,r)=>{if("string"===e.type||"number"===e.type||"integer"===e.type)return y[e.type](n[e.name])(t,r)},Filter:u[e.type](n,e.name,e=>{this.setState({filters:Object.assign({},n,e)})})}:{Header:e.name,accessor:e.name,fixed:-1!==o.indexOf(e.name)&&"left"});return a.createElement(m,null,a.createElement("button",{onClick:()=>this.setState({showFilters:!i})},i?"Hide":"Show"," Filters"),a.createElement(s,{data:e,columns:l,style:{height:`${r}px`},className:"-striped -highlight",filterable:i}))}}g.defaultProps={metadata:{},height:500};var b=g,f=r(361),x=r(227),E=r(1352);const k=l.c.div`
  & {
    margin: 30px 0;
    padding: 30px;
    border: 1px solid #ccc;
    border-radius: 5px;
    position: relative;
  }
  .close {
    position: absolute;
    top: 15px;
    right: 15px;
    cursor: pointer;
    opacity: 0.5;
    font-size: 40px;
    line-height: 22px;
  }
  .close:hover {
    opacity: 1;
  }
  .grid-wrapper {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    grid-gap: 20px;
  }
  h3 {
    margin: 0 0 20px;
  }
  .box {
    cursor: pointer;
    width: 30px;
    height: 30px;
    border-radius: 5px;
    display: inline-block;
    margin: 0 20px 20px 0;
  }
  textarea {
    height: 184px;
    width: 100%;
    box-sizing: border-box;
    margin-bottom: 20px;
    padding: 5px;
    font-size: 14px;
    border-color: #ccc;
  }
`,v=l.c.div`
   {
    width: 225px;
  }
`,w=l.c.div`
   {
    margin-top: 30px;
  }
`,C=l.c.button`
  & {
    margin: 0 20px 10px 0;
    -webkit-appearance: none;
    padding: 5px 15px;
    background: white;
    border: 1px solid #bbb;
    border-radius: 3px;
    cursor: pointer;
    text-transform: uppercase;
    font-size: 14px;
    color: #555;
  }
  &:hover {
    border-color: #888;
    color: #222;
  }
`;class T extends a.PureComponent{constructor(e){super(e),this.openClose=(()=>{this.setState({open:!this.state.open,colors:this.props.colors.join(",\n")})}),this.handleChange=((e,t)=>{this.setState({selectedColor:e,selectedPosition:t})}),this.pickerChange=(e=>{const{colors:t}=this.props;t[this.state.selectedPosition]=e.hex,this.props.updateColor(t),this.setState({selectedColor:e.hex,colors:t.join(",\n")})}),this.colorsFromTextarea=(()=>{const e=this.state.colors.replace(/\"/g,"").replace(/ /g,"").replace(/\[/g,"").replace(/\]/g,"").replace(/\r?\n|\r/g,"").split(",");this.props.updateColor(e)}),this.updateTextArea=(e=>{this.setState({colors:e.target.value})}),this.state={open:!1,selectedColor:e.colors[0],selectedPosition:0,colors:e.colors.join(",\n")}}render(){if(!this.state.open)return a.createElement("div",{style:{display:"inline-block"}},a.createElement(C,{onClick:this.openClose},"Adjust Palette"));const{colors:e}=this.props;return a.createElement(k,null,a.createElement("div",{className:"close",role:"button",tabIndex:0,onClick:this.openClose,onKeyPress:e=>{13===e.keyCode&&this.openClose()}},"×"),a.createElement("div",{className:"grid-wrapper"},a.createElement("div",null,a.createElement("h3",null,"Select Color"),e.map((e,t)=>a.createElement("div",{key:`color-${t}`,className:"box",style:{background:e},role:"button",tabIndex:0,onKeyPress:r=>{13===r.keyCode&&this.handleChange(e,t)},onClick:()=>this.handleChange(e,t)}))),a.createElement("div",null,a.createElement("h3",null,"Adjust Color"),a.createElement(v,null,a.createElement(E.ChromePicker,{color:this.state.selectedColor,onChangeComplete:this.pickerChange}))),a.createElement("div",null,a.createElement("h3",null,"Paste New Colors"),a.createElement("textarea",{value:this.state.colors,onChange:this.updateTextArea}),a.createElement(C,{onClick:this.colorsFromTextarea},"Update Colors"))),a.createElement(w,null,a.createElement("a",{href:`http://projects.susielu.com/viz-palette?colors=[${e.map(e=>`"${e}"`).join(",")}]&backgroundColor="white"&fontColor="black"`},"Evaluate This Palette with VIZ PALETTE")))}}T.defaultProps={metadata:{},height:500};var M=T;const S=l.c.span`
  & {
    display: inline-block;
    width: 20px;
    height: 20px;
    margin-right: 5px;
    border-radius: 20px;
    margin-bottom: -5px;
  }
`,O=l.c.span`
  & {
    display: inline-block;
    min-width: 80px;
    margin: 5px;
  }
`,j=l.c.div`
  & {
    margin-top: 20px;
  }
`;var $=({values:e,colorHash:t,valueHash:r,colors:n=[],setColor:i})=>{return a.createElement(j,null,(e.length>18?[...e.filter((e,t)=>t<18),"Other"]:e).map((e,n)=>t[e]&&a.createElement(O,{key:`legend-item-${n}`},a.createElement(S,{style:{background:t[e]}}),a.createElement("span",{className:"html-legend-item"},e),r[e]&&r[e]>1&&`(${r[e]})`||"")),i&&a.createElement(M,{colors:n,updateColor:e=>{i(e)}}))};var P=l.c.div.attrs(e=>({style:{transform:`translate(\n      ${e.x<200?"0px":"calc(-50% + 7px)"},\n      ${e.y<200?"10px":"calc(-100% - 10px)"}\n    )`}}))`
  color: black;
  padding: 10px;
  z-index: 999999;
  min-width: 120px;
  background: white;
  border: 1px solid #888;
  border-radius: 5px;
  position: relative;

  & p {
    font-size: 14px;
  }

  & h3 {
    margin: 0 0 10px;
  }

  &:before {
    ${e=>e.x<200?null:e.y<200?'\n      border-left: inherit;\n      border-top: inherit;\n      top: -8px;\n      left: calc(50% - 15px);\n      background: inherit;\n      content: "";\n      padding: 0px;\n      transform: rotate(45deg);\n      width: 15px;\n      height: 15px;\n      position: absolute;\n      z-index: 99;\n    ':'\n    border-right: inherit;\n    border-bottom: inherit;\n    bottom: -8px;\n    left: calc(50% - 15px);\n    background: inherit;\n    content: "";\n    padding: 0px;\n    transform: rotate(45deg);\n    width: 15px;\n    height: 15px;\n    position: absolute;\n    z-index: 99;\n  '}
  }
`,A=r(1444),G=r.n(A);function L(e){let t="0.[00]a";return 0===e?"0":(e>1e14||e<1e-5?t="0.[000]e+0":e<1&&(t="0.[0000]a"),G()(e).format(t))}const D=l.c.p`
  margin: 20px 0 5px;
`,F=l.c.g`
  & text {
    text-anchor: end;
  }

  & :first-child {
    fill: white;
    stroke: white;
    opacity: 0.75;
    stroke-width: 2;
  }
`,z=[40,380];class N extends a.Component{constructor(e){super(e),this.brushing=((e,t)=>{const r=this.state.columnExtent;r[t]=e,this.setState({columnExtent:r})});const{options:t,data:r,schema:a}=this.props,{primaryKey:n}=t,i=function(e,t,r,a){const n={},i={};t.forEach(t=>{const r=[Math.min(...e.map(e=>e[t.name])),Math.max(...e.map(e=>e[t.name]))],a=Object(x.a)().domain(r).range([0,1]);n[t.name]=a;const o=Object(x.a)().domain(r).range([380,0]);i[t.name]=o});const o=[];return e.forEach(e=>{t.forEach(t=>{const i={metric:t.name,rawvalue:e[t.name],pctvalue:n[t.name](e[t.name])};r.forEach(t=>{"string"===t.type&&(i[t.name]=e[t.name])}),a.forEach(t=>{i[t]=e[t]}),o.push(i)})}),{dataPieces:o,scales:i}}(r,t.metrics,a.fields,n);this.state={filterMode:!0,data:i.dataPieces,dataScales:i.scales,columnExtent:t.metrics.reduce((e,t)=>(e[t.name]=[-1/0,1/0],e),{})}}shouldComponentUpdate(){return!0}render(){const{options:e,data:t}=this.props,{primaryKey:r,metrics:n,chart:i,colors:o,setColor:l}=e,{dim1:s}=i,{columnExtent:c,filterMode:m}=this.state,p=new Map;Object.keys(c).forEach(e=>{const t=c[e].sort((e,t)=>e-t);this.state.data.filter(r=>r.metric===e&&(r.pctvalue<t[0]||r.pctvalue>t[1])).forEach(e=>{p.set(r.map(t=>e[t]).join(","),!0)})});const h={},d=t.filter(e=>!p.get(r.map(t=>e[t]).join(","))),u=d.map(e=>r.map(t=>e[t]).join(" - ")),y={Other:"grey"};if(s&&"none"!==s){const{uniqueValues:e,valueHash:r}=d.reduce((e,t)=>{const r=t[s];return e.valueHash[r]=e.valueHash[r]&&e.valueHash[r]+1||1,e.uniqueValues=!e.uniqueValues.find(e=>e===r)&&[...e.uniqueValues,r]||e.uniqueValues,e},{uniqueValues:[],valueHash:{}});t.reduce((e,t)=>-1===e.indexOf(t[s])?[...e,t[s]]:e,[]).forEach((e,t)=>{y[e]=o[t%o.length]}),h.afterElements=e.length<=18?a.createElement($,{values:e,colorHash:y,valueHash:r,setColor:l}):a.createElement(D,null,u.length," items")}return m||(h.annotations=n.map(e=>({label:"",metric:e.name,type:"enclose-rect",color:"green",disable:["connector"],coordinates:[{metric:e.name,pctvalue:c[e.name][0]},{metric:e.name,pctvalue:c[e.name][1]}]})).filter(e=>0!==e.coordinates[0].pctvalue||1!==e.coordinates[1].pctvalue)),a.createElement("div",null,a.createElement("div",null,a.createElement("button",{className:`button-text ${m?"selected":""}`,onClick:()=>this.setState({filterMode:!0})},"Filter"),a.createElement("button",{className:`button-text ${m?"":"selected"}`,onClick:()=>this.setState({filterMode:!1})},"Explore")),a.createElement(f.ResponsiveOrdinalFrame,Object.assign({data:this.state.data,oAccessor:"metric",rAccessor:"pctvalue",type:{type:"point",r:2},connectorType:e=>r.map(t=>e[t]).join(","),style:e=>({fill:p.get(r.map(t=>e[t]).join(","))?"lightgray":y[e[s]],opacity:p.get(r.map(t=>e[t]).join(","))?.15:.99}),connectorStyle:e=>({stroke:p.get(r.map(t=>e.source[t]).join(","))?"gray":y[e.source[s]],strokeWidth:p.get(r.map(t=>e.source[t]).join(","))?1:1.5,strokeOpacity:p.get(r.map(t=>e.source[t]).join(","))?.1:1}),responsiveWidth:!0,margin:{top:20,left:20,right:20,bottom:100},oPadding:40,pixelColumnWidth:80,interaction:m?{columnsBrush:!0,during:this.brushing,extent:Object.keys(this.state.columnExtent)}:null,pieceHoverAnnotation:!m,tooltipContent:e=>{const t=p.get(r.map(t=>e[t]).join(","))?"grey":y[e[s]];return a.createElement(P,{x:e.x,y:e.y},a.createElement("h3",null,r.map(t=>e[t]).join(", ")),e[s]&&a.createElement("h3",{style:{color:t}},s,": ",e[s]),a.createElement("p",null,e.metric,": ",e.rawvalue))},canvasPieces:!0,canvasConnectors:!0,oLabel:e=>a.createElement("g",null,a.createElement("text",{transform:"rotate(45)"},e),a.createElement("g",{transform:"translate(-20,-395)"},a.createElement(f.Axis,{scale:this.state.dataScales[e],size:z,orient:"left",ticks:5,tickFormat:e=>a.createElement(F,null,a.createElement("text",null,L(e)),a.createElement("text",null,L(e)))})))},h)))}}N.defaultProps={metadata:{},height:500};var H=N;function B(e,t){return"function"==typeof t?t(e):e[t]}const V=(e,t,r,a)=>{const n={};let i=[];return a.forEach(r=>{const a=B(r,e);n[a]||(n[a]={array:[],value:0,label:a},i.push(n[a])),n[a].array.push(r),n[a].value+=B(r,t)}),i=i.sort((e,t)=>t.value===e.value?e.label<t.label?-1:(e.label,t.label,1):t.value-e.value),"none"!==r&&i.forEach(e=>{e.array=e.array.sort((e,t)=>B(t,r)-B(e,r))}),i.reduce((e,t)=>[...e,...t.array],[])};var Z=r(133),R=r(59);const W=(e,t)=>t=e.parent?W(e.parent,[e.key,...t]):["root",...t],K=(e,t)=>{if(0===t.depth)return"white";if(1===t.depth)return e[t.key];let r=t;for(let e=t.depth;e>1;e--)r=r.parent;return Object(R.interpolateLab)("white",e[r.key])(Math.max(0,t.depth/6))};var I=r(81);const U=Object(x.a)().domain([5,30]).range([8,16]).clamp(!0),X={force:e=>t=>({fill:e[t.source.id],stroke:e[t.source.id],strokeOpacity:.25}),sankey:e=>t=>({fill:e[t.source.id],stroke:e[t.source.id],strokeOpacity:.25}),matrix:e=>t=>({fill:e[t.source.id],stroke:"none"}),arc:e=>t=>({fill:"none",stroke:e[t.source.id],strokeWidth:t.weight||1,strokeOpacity:.75})},Y={force:e=>t=>({fill:e[t.id],stroke:e[t.id],strokeOpacity:.5}),sankey:e=>t=>({fill:e[t.id],stroke:e[t.id],strokeOpacity:.5}),matrix:e=>e=>({fill:"none",stroke:"#666",strokeOpacity:1}),arc:e=>t=>({fill:e[t.id],stroke:e[t.id],strokeOpacity:.5})},q=[{type:"frame-hover"},{type:"highlight",style:{stroke:"red",strokeOpacity:.5,strokeWidth:5,fill:"none"}}],J={force:q,sankey:q,matrix:[{type:"frame-hover"},{type:"highlight",style:{fill:"red",fillOpacity:.5}}],arc:q},_={none:!1,static:!0,scaled:e=>!e.nodeSize||e.nodeSize<5?null:a.createElement("text",{textAnchor:"middle",y:U(e.nodeSize)/2,fontSize:`${U(e.nodeSize)}px`},e.id)},Q=Object(x.a)().domain([8,25]).range([14,8]).clamp(!0),ee=l.c.div`
  font-size: 14px;
  text-transform: uppercase;
  margin: 5px;
  font-weight: 900;
`,te=l.c.div`
  fontsize: 12px;
  texttransform: uppercase;
  margin: 5px;
`,re={heatmap:f.heatmapping,hexbin:f.hexbinning},ae=Object(x.b)().domain([.01,.2,.4,.6,.8]).range(["none","#FBEEEC","#f3c8c2","#e39787","#ce6751","#b3331d"]);const ne=(e,t,r,n="scatterplot")=>{const i=r.height-150||500,{chart:o,primaryKey:l,colors:s,setColor:c,dimensions:m,trendLine:p,marginalGraphics:h}=r,{dim1:d,dim2:u,dim3:y,metric1:g,metric2:b,metric3:f}=o,E=e.filter(e=>e[g]&&e[b]&&(!f||"none"===f||e[f]));let k=()=>5;const v={Other:"grey"},w={};let C;if(u&&"none"!==u){const e=[...E].sort((e,t)=>t[g]-e[g]).filter((e,t)=>t<3),t=[...E].sort((e,t)=>t[b]-e[b]).filter(t=>-1===e.indexOf(t)).filter((e,t)=>t<3);C=function(e,t,r){const a=[],n={};return[...e,...t].forEach(e=>{const t=n[e[r]];if(t){const a=t.coordinates&&[...t.coordinates,e]||[e,t];Object.keys(n[e[r]]).forEach(t=>{delete n[e[r]][t]}),n[e[r]].id=e[r],n[e[r]].label=e[r],n[e[r]].type="react-annotation",n[e[r]].coordinates=a}else n[e[r]]=Object.assign({type:"react-annotation",label:e[r],id:e[r],coordinates:[]},e),a.push(n[e[r]])}),a}(e,t,u)}if(C=void 0,f&&"none"!==f){const e=Math.min(...E.map(e=>e[f])),t=Math.max(...E.map(e=>e[f]));k=Object(x.a)().domain([e,t]).range([2,20])}const T=V(g,"none"!==f&&f||b,"none",e);if(("scatterplot"===n||"contour"===n)&&d&&"none"!==d){const e=T.reduce((e,t)=>!e.find(e=>e===t[d].toString())&&[...e,t[d].toString()]||e,[]);e.forEach((e,t)=>{v[e]=t>18?"grey":s[t%s.length]}),w.afterElements=a.createElement($,{valueHash:{},values:e,colorHash:v,setColor:c,colors:s})}let M=[];if("heatmap"===n||"hexbin"===n||"contour"===n&&"none"===y){if(M=[{coordinates:E}],"contour"!==n){const e=re[n]({summaryType:{type:n,bins:10},data:{coordinates:E.map(e=>Object.assign({},e,{x:e[g],y:e[b]}))},size:[i,i]});M=e;const t=[.2,.4,.6,.8,1].map(t=>Math.floor(e.binMax*t)).reduce((e,t)=>0===t||-1!==e.indexOf(t)?e:[...e,t],[]),r=[0,...t],o=[];r.forEach((e,t)=>{const a=r[t+1];a&&o.push(`${e+1} - ${a}`)});const l=["#FBEEEC","#f3c8c2","#e39787","#ce6751","#b3331d"],m={};o.forEach((e,t)=>{m[e]=l[t]}),ae.domain([.01,...t]).range(["none",...l.filter((e,r)=>r<t.length)]),w.afterElements=a.createElement($,{valueHash:{},values:o,colorHash:m,colors:s,setColor:c})}}else if("contour"===n){const e={};M=[],E.forEach(t=>{e[t[d]]||(e[t[d]]={label:t[d],color:v[t[d]],coordinates:[]},M.push(e[t[d]])),e[t[d]].coordinates.push(t)})}const S=("scatterplot"===n||"contour"===n)&&e.length>999;let O,j=[];"none"!==h&&"scatterplot"===n&&(j=[{orient:"right",tickLineGenerator:()=>a.createElement("g",null),tickFormat:()=>"",marginalSummaryType:{type:h,showPoints:!S}},{orient:"top",tickLineGenerator:()=>a.createElement("g",null),tickFormat:()=>"",marginalSummaryType:{type:h,showPoints:!S}}]),"scatterplot"===n&&"none"!==p?O={type:"trendline",regressionType:p}:"scatterplot"!==n&&(O={type:n,bins:10,thresholds:"none"===y?6:3});const A=Object.assign({xAccessor:"hexbin"===n||"heatmap"===n?"x":g,yAccessor:"hexbin"===n||"heatmap"===n?"y":b,axes:[{orient:"left",ticks:6,label:b,tickFormat:L,baseline:"scatterplot"===n,tickSize:"heatmap"===n?0:void 0},{orient:"bottom",ticks:6,label:g,tickFormat:L,footer:"heatmap"===n,baseline:"scatterplot"===n,tickSize:"heatmap"===n?0:void 0},...j],points:("scatterplot"===n||"contour"===n)&&e,canvasPoints:S,summaryType:O,summaryStyle:e=>"scatterplot"===n?{stroke:"darkred",strokeWidth:2,fill:"none"}:{fill:"contour"===n?"none":ae((e.binItems||e.data).length),stroke:"contour"!==n?void 0:"none"===y?"#BBB":e.parentSummary.color,strokeWidth:"contour"===n?2:1},pointStyle:e=>({r:S?2:"contour"===n?3:k(e[f]),fill:v[e[d]]||"black",fillOpacity:.75,stroke:S?"none":"contour"===n?"white":"black",strokeWidth:"contour"===n?.5:1,strokeOpacity:.9}),hoverAnnotation:!0,responsiveWidth:!1,size:[i+105,i+80],margin:{left:75,bottom:50,right:30,top:30},annotations:"scatterplot"===n&&C||void 0,annotationSettings:{layout:{type:"marginalia",orient:"right",marginOffset:30}},tooltipContent:("hexbin"===n||"heatmap"===n)&&(e=>{const t=e.binItems||e.data||[];return 0===t.length?null:a.createElement(P,{x:e.x,y:e.y},a.createElement(ee,null,"ID, ",g,", ",b),t.map((e,t)=>{const r=m.map(t=>e[t.name].toString&&e[t.name].toString()||e[t.name]).join(",");return a.createElement(te,{key:r+t},r,", ",e[g],", ",e[b])}))})||(e=>a.createElement(P,{x:e.x,y:e.y},a.createElement("h3",null,l.map(t=>e[t]).join(", ")),m.map(t=>a.createElement("p",{key:`tooltip-dim-${t.name}`},t.name,":"," ",e[t.name].toString&&e[t.name].toString()||e[t.name])),a.createElement("p",null,g,": ",e[g]),a.createElement("p",null,b,": ",e[b]),f&&"none"!==f&&a.createElement("p",null,f,": ",e[f])))},w);return"scatterplot"!==n&&(A.areas=M),A},ie={line:{Frame:f.ResponsiveXYFrame,controls:"switch between linetype",chartGenerator:(e,t,r)=>{let n;const{chart:i,selectedMetrics:o,lineType:l,metrics:s,primaryKey:c,colors:m}=r,{timeseriesSort:p}=i,h=t.fields.find(e=>e&&e.name===p),d="array-order"===p?"integer":h&&h.type?h.type:null,u=e=>"datetime"===d?e.toLocaleString().split(",")[0]:L(e),y="datetime"===d?Object(x.c)():Object(x.a)();return n=s.map((t,r)=>{const a="array-order"===p?e:e.sort((e,t)=>e[p]-t[p]);return{color:m[r%m.length],label:t.name,type:t.type,coordinates:a.map((e,a)=>({value:e[t.name],x:"array-order"===p?a:e[p],label:t.name,color:m[r%m.length],originalData:e}))}}).filter(e=>0===o.length||o.some(t=>t===e.label)),{lineType:{type:l,interpolator:I.curveMonotoneX},lines:n,xScaleType:y,renderKey:(e,t)=>e.coordinates?`line-${e.label}`:`linepoint=${e.label}-${t}`,lineStyle:e=>({fill:"line"===l?"none":e.color,stroke:e.color,fillOpacity:.75}),pointStyle:e=>({fill:e.color,fillOpacity:.75}),axes:[{orient:"left",tickFormat:L},{orient:"bottom",ticks:5,tickFormat:e=>{const t=u(e),r=t.length>4?"45":"0",n=t.length>4?"start":"middle";return a.createElement("text",{transform:`rotate(${r})`,textAnchor:n},t)}}],hoverAnnotation:!0,xAccessor:"x",yAccessor:"value",showLinePoints:"line"===l,margin:{top:20,right:200,bottom:"datetime"===d?80:40,left:50},legend:{title:"Legend",position:"right",width:200,legendGroups:[{label:"",styleFn:e=>({fill:e.color}),items:n}]},tooltipContent:e=>a.createElement(P,{x:e.x,y:e.y},a.createElement("p",null,e.parentLine&&e.parentLine.label),a.createElement("p",null,e.value&&e.value.toLocaleString()||e.value),a.createElement("p",null,p,": ",u(e.x)),c.map((t,r)=>a.createElement("p",{key:`key-${r}`},t,":"," ",e.originalData[t].toString&&e.originalData[t].toString()||e.originalData[t])))}}},scatter:{Frame:f.ResponsiveXYFrame,controls:"switch between modes",chartGenerator:ne},hexbin:{Frame:f.ResponsiveXYFrame,controls:"switch between modes",chartGenerator:(e,t,r)=>ne(e,t,r,r.areaType)},bar:{Frame:f.ResponsiveOrdinalFrame,controls:"switch between modes",chartGenerator:(e,t,r)=>{const{selectedDimensions:n,chart:i,colors:o,setColor:l,barGrouping:s}=r,{dim1:c,metric1:m,metric3:p,metric4:h}=i,d=0===n.length?c:e=>n.map(t=>e[t]).join(","),u=m,y={},g={Other:"grey"},b=V(d,"none"!==p&&p||u,c,e);let f;p&&"none"!==p&&(y.dynamicColumnWidth=p),"Clustered"===s&&h&&"none"!==h&&(y.rExtent=[Math.min(...e.map(e=>e[m]-e[h])),Math.max(...e.map(e=>e[m]+e[h]))],f=((e,t,r)=>{const n=Math.abs(r.rScale(e[m])-r.rScale(e[m]+e[h]));return a.createElement("g",null,a.createElement("rect",{width:r.width,height:r.height,style:r.styleFn(e)}),a.createElement("g",{transform:`translate(${r.width/2},${e.negative?r.height:0})`,stroke:"#333",strokeWidth:"1",opacity:"0.75"},a.createElement("line",{y1:-n,y2:-n,x1:Math.min(0,-r.width/2+2),x2:Math.max(0,r.width/2-2)}),a.createElement("line",{x1:0,x2:0,y1:-n,y2:n}),a.createElement("line",{y1:n,y2:n,x1:Math.min(0,-r.width/2+2),x2:Math.max(0,r.width/2-2)})))}));const x=b.reduce((e,t)=>e.find(e=>e===t[c].toString())?e:[...e,t[c].toString()],[]);if(c&&"none"!==c&&(x.forEach((e,t)=>{g[e]=t>18?"grey":o[t%o.length]}),y.afterElements=a.createElement($,{valueHash:{},values:x,colorHash:g,setColor:l,colors:o}),"Clustered"===s||n.length>0&&n.join(",")!==c)){y.pieceHoverAnnotation=!0;const e=[...r.dimensions,...r.metrics];y.tooltipContent=(t=>a.createElement(P,{x:t.x,y:t.y},a.createElement("div",{style:{heightMax:"300px",display:"flex",flexWrap:"wrap"}},e.map((e,r)=>a.createElement("div",{style:{margin:"2px 5px 0",display:"inline-block",minWidth:"100px"},key:`dim-${r}`},a.createElement("span",{style:{fontWeight:600}},e.name),":"," ",t[e.name])))))}n.length>0&&(1!==n.length||c!==n[0])&&b.map(e=>e[c]).reduce((e,t)=>-1===e.indexOf(t)?[...e,t]:e,[]).length;return Object.assign({type:"Clustered"===s?{type:"clusterbar",customMark:f}:{type:"bar",customMark:f},data:b,oAccessor:d,rAccessor:u,style:e=>({fill:g[e[c]]||o[0],stroke:g[e[c]]||o[0]}),oPadding:x.length>30?1:5,oLabel:!(x.length>30)&&(e=>a.createElement("text",{transform:"rotate(90)"},e)),hoverAnnotation:!0,margin:{top:10,right:10,bottom:100,left:70},axis:{orient:"left",label:u,tickFormat:L},tooltipContent:e=>a.createElement(P,{x:e.column.xyData[0].xy.x,y:e.column.xyData[0].xy.y},a.createElement("p",null,"function"==typeof d?d(e.pieces[0]):e.pieces[0][d]),a.createElement("p",null,u,":"," ",e.pieces.map(e=>e[u]).reduce((e,t)=>e+t,0)),p&&"none"!==p&&a.createElement("p",null,p,":"," ",e.pieces.map(e=>e[p]).reduce((e,t)=>e+t,0))),baseMarkProps:{forceUpdate:!0},size:[500,600]},y)}},summary:{Frame:f.ResponsiveOrdinalFrame,controls:"switch between modes",chartGenerator:(e,t,r)=>{const n={},i={},{chart:o,summaryType:l,primaryKey:s,colors:c,setColor:m}=r,{dim1:p,metric1:h}=o,d=p,u=h,y=e.reduce((e,t)=>!e.find(e=>e===t[p].toString())&&[...e,t[p].toString()]||e,[]);return p&&"none"!==p&&(y.forEach((e,t)=>{i[e]=c[t%c.length]}),n.afterElements=a.createElement($,{valueHash:{},values:y,colorHash:i,setColor:m,colors:c})),Object.assign({summaryType:{type:l,bins:16,amplitude:20},type:"violin"===l&&"swarm",projection:"horizontal",data:e,oAccessor:d,rAccessor:u,summaryStyle:e=>({fill:i[e[p]]||c[0],fillOpacity:.8,stroke:i[e[p]]||c[0]}),style:e=>({fill:i[e[p]]||c[0],stroke:"white"}),oPadding:5,oLabel:!(y.length>30)&&(e=>a.createElement("text",{textAnchor:"end",fontSize:`${e&&Q(e.length)||12}px`},e)),margin:{top:25,right:10,bottom:50,left:100},axis:{orient:"bottom",label:u,tickFormat:L},baseMarkProps:{forceUpdate:!0},pieceHoverAnnotation:"violin"===l,tooltipContent:e=>a.createElement(P,{x:e.x,y:e.y},a.createElement("h3",null,s.map(t=>e[t]).join(", ")),a.createElement("p",null,p,": ",e[p]),a.createElement("p",null,u,": ",e[u]))},n)}},network:{Frame:f.ResponsiveNetworkFrame,controls:"switch between modes",chartGenerator:(e,t,r)=>{const{networkType:n="force",chart:i,colors:o}=r,{dim1:l,dim2:s,metric1:c,networkLabel:m}=i;if(!l||"none"===l||!s||"none"===s)return{};const p={},h=[];e.forEach(e=>{p[`${e[l]}-${e[s]}`]||(p[`${e[l]}-${e[s]}`]={source:e[l],target:e[s],value:0,weight:0},h.push(p[`${e[l]}-${e[s]}`])),p[`${e[l]}-${e[s]}`].value+=e[c]||1,p[`${e[l]}-${e[s]}`].weight+=1});const d={};return e.forEach(e=>{d[e[l]]||(d[e[l]]=o[Object.keys(d).length%o.length]),d[e[s]]||(d[e[s]]=o[Object.keys(d).length%o.length])}),h.forEach(e=>{e.weight=Math.min(10,e.weight)}),{edges:h,edgeType:"force"===n&&"halfarrow",edgeStyle:X[n](d),nodeStyle:Y[n](d),nodeSizeAccessor:e=>e.degree,networkType:{type:n,iterations:1e3},hoverAnnotation:J[n],tooltipContent:e=>a.createElement(P,{x:e.x,y:e.y},a.createElement("h3",null,e.id),a.createElement("p",null,"Links: ",e.degree),e.value&&a.createElement("p",null,"Value: ",e.value)),nodeLabels:"matrix"!==n&&_[m],margin:{left:100,right:100,top:10,bottom:10}}}},hierarchy:{Frame:f.ResponsiveNetworkFrame,controls:"switch between modes",chartGenerator:(e,t,r)=>{const{hierarchyType:n="dendrogram",chart:i,selectedDimensions:o,primaryKey:l,colors:s}=r,{metric1:c}=i,m="sunburst"===n?"partition":n;if(0===o.length)return{};const p=Object(Z.nest)();o.forEach(e=>{p.key(t=>t[e])});const h={},d=[];return e.forEach(e=>{h[e[o[0]]]||(h[e[o[0]]]=s[Object.keys(h).length]),d.push(Object.assign({},e,{sanitizedR:e.r,r:void 0}))}),{edges:{values:p.entries(d)},edgeStyle:()=>({fill:"lightgray",stroke:"gray"}),nodeStyle:e=>({fill:K(h,e),stroke:1===e.depth?"white":"black",strokeOpacity:.1*e.depth+.2}),networkType:{type:m,projection:"sunburst"===n&&"radial",hierarchySum:e=>e[c],hierarchyChildren:e=>e.values,padding:"treemap"===m?3:0},edgeRenderKey:(e,t)=>t,baseMarkProps:{forceUpdate:!0},margin:{left:100,right:100,top:10,bottom:10},hoverAnnotation:[{type:"frame-hover"},{type:"highlight",style:{stroke:"red",strokeOpacity:.5,strokeWidth:5,fill:"none"}}],tooltipContent:e=>a.createElement(P,{x:e.x,y:e.y},((e,t,r)=>{const n=e.parent?W(e.parent,e.key&&[e.key]||[]).join("->"):"",i=[];return e.parent?e.key?(i.push(a.createElement("h2",{key:"hierarchy-title"},e.key)),i.push(a.createElement("p",{key:"path-string"},n)),i.push(a.createElement("p",{key:"hierarchy-value"},"Total Value: ",e.value)),i.push(a.createElement("p",{key:"hierarchy-children"},"Children: ",e.children.length))):(i.push(a.createElement("p",{key:"leaf-label"},n,"->",t.map(t=>e[t]).join(", "))),i.push(a.createElement("p",{key:"hierarchy-value"},r,": ",e[r]))):i.push(a.createElement("h2",{key:"hierarchy-title"},"Root")),i})(e,l,c))}}},parallel:{Frame:H,controls:"switch between modes",chartGenerator:(e,t,r)=>({data:e,schema:t,options:r})}};var oe=r(207);const le={line:"Line and stacked area charts for time series data where each row is a point and columns are data to be plotted.",bar:"Bar charts to compare individual and aggregate amounts.",scatter:"Scatterplot for comparing correlation between x and y values.",grid:"A table of data.",network:"Force-directed, adjacency matrix, arc diagram and sankey network visualization suitable for data that is an edge list where one dimension represents source and another dimension represents target.",summary:"Distribution plots such as boxplots and violin plots to compare.",hexbin:"Shows aggregate distribution of larger datasets across x and y metrics using hexbin, heatmap or contour plots.",parallel:"Parallel coordinates for comparing and filtering across different values in the dataset.",hierarchy:"Nest data by categorical values using treemap, dendrogram, sunburst or partition."},se={metric1:{default:"Plot this metric",scatter:"Plot this metric along the X axis",hexbin:"Plot this metric along the X axis"},metric2:{default:"Plot this metric along the Y axis"},metric3:{default:"Size the width of bars (Marimekko style) based on this metric",scatter:"Size the radius of points based on this metric"},metric4:"Error bars according to this value",dim1:{default:"Color items by this dimension",summary:"Group items into this category",network:"Use this dimension to determine the source node"},dim2:{default:"Label prominent datapoints using this dimension",network:"Use this dimension to determine the target node"},dim3:{default:"Split contours into separate groups based on this dimension"},networkType:"Represent network as a force-directed network (good for social networks) or as a sankey diagram (good for flow networks)",hierarchyType:"Represent your hierarchy as a tree (good for taxonomies) or a treemap (good for volumes) or partition (also good for volume where category volume is important)",timeseriesSort:"Sort line chart time series by its array position or by a specific metric or time",lineType:"Represent your data using a line chart, stacked area chart or ranked area chart",areaType:"Represent as a heatmap, hexbin or contour plot",lineDimensions:"Only plot the selected dimensions (or all if none are selected)",trendLine:"Select the kind of trend line you want to display on the chart",barGrouping:"Choose between a clustered or a stacked bar chart when there are multiple pieces in the same category",marginalGraphics:"Choose the kind of marginal summary you want to see for summarizing density along the axes"},ce=l.c.path`
  & {
    fill: var(--theme-app-bg);
    stroke: var(--theme-app-fg);
  }
`,me=e=>a.createElement(oe.h,{width:16,height:16,viewBox:"0 0 16 16",outerProps:e},a.createElement("title",null,"Summary Diagram"),a.createElement(ce,{d:"M 9.2300893,12.746467 15.329337,12.746467 M 0.73981357,15.376296 6.8390612,15.376296 M 3.9346579,0.6634694 3.9346579,15.376296 M 0.73981357,0.6634694 6.8390612,0.6634694 M 12.424932,1.5163867 12.424932,12.817543 M 9.2300893,1.5163867 15.329337,1.5163867 M 9.3149176,3.8522966 15.454941,3.8522966 15.454941,10.067428 9.3149176,10.067428 Z M 0.63101533,5.4042547 6.771038,5.4042547 6.771038,13.040916 0.63101533,13.040916 Z"})),pe=e=>a.createElement(oe.h,{width:16,height:16,viewBox:"0 0 16 16",outerProps:e},a.createElement("title",null,"Dendrogram"),a.createElement(ce,{d:"M 5.3462352,16.86934 5.3462352,11.568531 M 5.0378073,11.186463 10.665375,16.453304 M 5.5794816,11.049276 -0.04808655,16.316116 M 10.903757,11.840357 10.903757,6.5395482 M 10.722225,5.9958343 16.349791,11.262675 M 10.758529,6.1997119 5.1309613,11.466552 M 5.3851096,6.1997401 5.3851096,0.06818774 M 5.3488028,0.96685111 10.976372,6.2336914 M 5.3851095,0.89889187 -0.24245868,6.1657322"})),he=e=>a.createElement(oe.h,{width:16,height:16,viewBox:"0 0 16 16",outerProps:e},a.createElement("title",null,"Network"),a.createElement(ce,{d:"M 12.272948,3.9756652 9.2580839,6.8311579 M 3.7415227,3.9107679 6.435657,6.5066704 M 3.9981069,12.087859 6.6280954,9.6866496 M 12.208802,12.217654 9.0656456,9.556855 M 0.58721146,13.461599 A 2.0038971,2.0273734 0 0 0 2.591109,15.488973 2.0038971,2.0273734 0 0 0 4.5950056,13.461599 2.0038971,2.0273734 0 0 0 2.591109,11.434226 2.0038971,2.0273734 0 0 0 0.58721146,13.461599 Z M 11.483612,2.5370283 A 2.0038971,2.0273734 0 0 0 13.487509,4.5644013 2.0038971,2.0273734 0 0 0 15.491407,2.5370283 2.0038971,2.0273734 0 0 0 13.487509,0.50965432 2.0038971,2.0273734 0 0 0 11.483612,2.5370283 Z M 15.491407,13.461599 A 2.0038971,2.0273734 0 0 1 13.487509,15.488973 2.0038971,2.0273734 0 0 1 11.483612,13.461599 2.0038971,2.0273734 0 0 1 13.487509,11.434226 2.0038971,2.0273734 0 0 1 15.491407,13.461599 Z M 9.9298938,8.1089002 A 2.0038971,2.0273734 0 0 1 7.9259965,10.136275 2.0038971,2.0273734 0 0 1 5.9220989,8.1089002 2.0038971,2.0273734 0 0 1 7.9259965,6.0815273 2.0038971,2.0273734 0 0 1 9.9298938,8.1089002 Z M 4.5950056,2.5370283 A 2.0038971,2.0273734 0 0 1 2.591109,4.5644013 2.0038971,2.0273734 0 0 1 0.58721146,2.5370283 2.0038971,2.0273734 0 0 1 2.591109,0.50965432 2.0038971,2.0273734 0 0 1 4.5950056,2.5370283 Z"})),de=e=>a.createElement(oe.h,{width:16,height:16,viewBox:"0 0 16 16",outerProps:e},a.createElement("title",null,"Scatterplot"),a.createElement(ce,{d:"M 6.2333524,7.1483631 A 2.1883047,2.1883047 0 0 1 4.0450478,9.3366678 2.1883047,2.1883047 0 0 1 1.8567431,7.1483631 2.1883047,2.1883047 0 0 1 4.0450478,4.9600585 2.1883047,2.1883047 0 0 1 6.2333524,7.1483631 Z M 12.201456,4.0316868 A 2.1883047,2.1883047 0 0 1 10.013151,6.2199914 2.1883047,2.1883047 0 0 1 7.8248465,4.0316868 2.1883047,2.1883047 0 0 1 10.013151,1.8433821 2.1883047,2.1883047 0 0 1 12.201456,4.0316868 Z M 14.787634,11.45866 A 2.1883047,2.1883047 0 0 1 12.599329,13.646965 2.1883047,2.1883047 0 0 1 10.411024,11.45866 2.1883047,2.1883047 0 0 1 12.599329,9.2703555 2.1883047,2.1883047 0 0 1 14.787634,11.45866 Z M 0.06631226,-0.01336003 0.06631226,16.100519 16.113879,16.100519"})),ue=e=>a.createElement(oe.h,{width:16,height:16,viewBox:"0 0 16 16",outerProps:e},a.createElement("title",null,"Line Chart"),a.createElement(ce,{d:"M 1.98856,5.3983376 3.9789255,1.5485605 6.8981275,9.2481137 10.215403,6.6815963 15.257662,12.071285 M 0.46261318,0.00862976 0.46261318,15.600225 16.518227,15.600225"})),ye=e=>a.createElement(oe.h,{width:16,height:16,viewBox:"0 0 16 16",outerProps:e},a.createElement("title",null,"Hexbin"),a.createElement(ce,{d:"M 7.6646201,7.248835 10.200286,8.7365914 12.71271,7.2956277 12.71271,4.2993354 10.200286,2.8583717 7.6481891,4.3220885 Z M 2.5260861,7.248835 5.0617524,8.7365914 7.5741798,7.2956277 7.5741798,4.2993354 5.0617524,2.8583717 2.509655,4.3220885 Z M 10.151008,11.430063 12.686686,12.917818 15.199098,11.476854 15.199098,8.4805611 12.686686,7.0395985 10.134577,8.5033165 Z M 5.0124743,11.430063 7.5481406,12.917818 10.060567,11.476854 10.060567,8.4805611 7.5481406,7.0395985 4.9960421,8.5033165 Z M 0.59322509,-0.02976587 0.59322509,16.053058 16.562547,16.008864"})),ge=e=>a.createElement(oe.h,{width:16,height:16,viewBox:"0 0 16 16",outerProps:e},a.createElement("title",null,"Bar Chart"),a.createElement(ce,{d:"M 11.58591,8.3025699 15.255735,8.3025699 15.255735,15.691481 11.58591,15.691481 Z M 6.2401471,3.973457 9.9358173,3.973457 9.9358173,15.626376 6.2401471,15.626376 Z M 0.533269,0.53717705 4.6376139,0.53717705 4.6376139,15.583893 0.533269,15.583893 Z"})),be=e=>a.createElement(oe.h,{width:16,height:16,viewBox:"0 0 16 16",outerProps:e},a.createElement("title",null,"Parallel Coordinates"),a.createElement(ce,{d:"M 2.7232684,11.593098 8.8105743,9.8309837 14.417303,4.2242547 M 12.356336,0.72968704 15.29192,0.72968704 15.29192,8.4261754 12.356336,8.4261754 Z M 6.8447585,6.4156084 10.103282,6.4156084 10.103282,12.352066 6.8447585,12.352066 Z M 0.51572132,6.0114684 3.9294777,6.0114684 3.9294777,16.25395 0.51572132,16.25395 Z"})),fe="\nwidth: 32px;\nheight: 32px;\ncursor: pointer;\ncolor: var(--theme-app-fg);\n",xe=l.c.button`
  ${fe}
  border: 1px solid var(--theme-app-fg);
  background-color: var(--theme-app-bg);
`,Ee=l.c.button`
  ${fe}

  border: 1px outset #666;
  background-color: #aaa;
`;class ke extends a.PureComponent{render(){const{message:e,onClick:t,children:r,selected:n}=this.props,{title:i=e}=this.props,o=n?Ee:xe;return a.createElement(o,{onClick:t,key:e,title:i},r)}}const ve=l.c.div`
  display: flex;
  flex-flow: column nowrap;
  z-index: 1;
  padding: 5px;
`;function we({dimensions:e,setGrid:t,setView:r,currentView:n,componentType:i}){return a.createElement(ve,{className:"dx-button-bar"},a.createElement(ke,{title:le.grid,onClick:t,message:"Data Table",selected:!1},a.createElement(oe.d,null)),e.length>0&&a.createElement(ke,{title:le.bar,onClick:()=>r("bar"),selected:"bar"===n,message:"Bar Graph"},a.createElement(ge,null)),a.createElement(ke,{title:le.summary,onClick:()=>r("summary"),selected:"summary"===n,message:"Summary"},a.createElement(me,null)),a.createElement(ke,{title:le.scatter,onClick:()=>r("scatter"),selected:"scatter"===n,message:"Scatter Plot"},a.createElement(de,null)),a.createElement(ke,{title:le.hexbin,onClick:()=>r("hexbin"),selected:"hexbin"===n,message:"Area Plot"},a.createElement(ye,null)),e.length>1&&a.createElement(ke,{title:le.network,onClick:()=>r("network"),selected:"network"===n,message:"Network"},a.createElement(he,null)),e.length>0&&a.createElement(ke,{title:le.hierarchy,onClick:()=>r("hierarchy"),selected:"hierarchy"===n,message:"Hierarchy"},a.createElement(pe,null)),e.length>0&&a.createElement(ke,{title:le.parallel,onClick:()=>r("parallel"),selected:"parallel"===n,message:"Parallel Coordinates"},a.createElement(be,null)),a.createElement(ke,{title:le.line,onClick:()=>r("line"),selected:"line"===n,message:"Line Graph"},a.createElement(ue,null)))}we.defaultProps={componentType:"toolbar",currentView:"",dimensions:[],setGrid:()=>null,setView:()=>null};const Ce=l.c.div`
  flex: 1;
  min-width: 0;
`;const Te=({children:e,componentType:t})=>a.createElement(Ce,null,e);Te.defaultProps={componentType:"viz",children:a.createElement(function(){return a.createElement("div",null,"This should be a display element!")},null)},Te.displayName="Viz";const Me=["#DA752E","#E5C209","#1441A0","#B86117","#4D430C","#1DB390","#B3331D","#088EB2","#417505","#E479A8","#F9F39E","#5782DC","#EBA97B","#A2AB60","#B291CF","#8DD2C2","#E6A19F","#3DC7E0","#98CE5B"],Se=l.b`
  h2 {
    text-transform: capitalize;
    margin-bottom: 10px;
  }
  select {
    height: 30px;
  }

  .selected {
    background-color: #d8e1e8 !important;
    background-image: none !important;
  }
`,Oe=l.c.div`
  margin-right: 30px;
  ${Se}
`,je=l.c.div`
  display: flex;
  flex-wrap: wrap;
  justify-content: left;
  margin-bottom: 30px;
  ${Se}
`,$e=(e,t,r,n,i,o="Help me help you help yourself")=>{const l=n?e:["none",...e];let s;return s=l.length>1?a.createElement("select",{onChange:e=>{t(e.target.value)},value:i},l.map((e,t)=>a.createElement("option",{"aria-selected":i===e,key:`display-metric-${t}`,label:e,value:e},e))):a.createElement("p",{style:{margin:0}},l[0]),a.createElement(Oe,{title:o},a.createElement("div",null,a.createElement("h3",null,r)),s)},Pe=[{type:"line",label:"Line Chart"},{type:"stackedarea",label:"Stacked Area Chart"},{type:"stackedpercent",label:"Stacked Area Chart (Percent)"},{type:"bumparea",label:"Ranked Area Chart"}],Ae=[{type:"hexbin",label:"Hexbin"},{type:"heatmap",label:"Heatmap"},{type:"contour",label:"Contour Plot"}];var Ge=({view:e,chart:t,metrics:r,dimensions:n,updateChart:i,selectedDimensions:o,selectedMetrics:l,hierarchyType:s,trendLine:c,marginalGraphics:m,barGrouping:p,summaryType:h,networkType:d,setLineType:u,updateMetrics:y,updateDimensions:g,lineType:b,areaType:f,setAreaType:x,data:E})=>{const k=r.map(e=>e.name),v=n.map(e=>e.name),w=e=>r=>i({chart:Object.assign({},t,{[e]:r})}),C=(e,t)=>{if(Object.keys(se).find(e=>e===t)){const r=t,a=void 0!==se[r]?se[r]:null;return null==a?"":"string"==typeof a?a:null!=a[e]?a[e]:a.default}return""};return a.createElement(a.Fragment,null,a.createElement(je,null,("summary"===e||"scatter"===e||"hexbin"===e||"bar"===e||"network"===e||"hierarchy"===e)&&$e(k,w("metric1"),"scatter"===e||"hexbin"===e?"X":"Metric",!0,t.metric1,C(e,"metric1")),("scatter"===e||"hexbin"===e)&&$e(k,w("metric2"),"Y",!0,t.metric2,C(e,"metric2")),("scatter"===e&&E.length<1e3||"bar"===e)&&$e(k,w("metric3"),"bar"===e?"Width":"Size",!1,t.metric3,C(e,"metric3")),"bar"===e&&$e(k,w("metric4"),"Error Bars",!1,t.metric4,C(e,"metric4")),"bar"===e&&$e(["Clustered","Stacked"],e=>i({barGrouping:e}),"Stack or Cluster",!0,p,se.barGrouping),"scatter"===e&&$e(["boxplot","violin","heatmap","ridgeline","histogram"],e=>i({marginalGraphics:e}),"Marginal Graphics",!1,m,se.marginalGraphics),"scatter"===e&&$e(["linear","polynomial","power","exponential","logarithmic"],e=>i({trendLine:e}),"Trendline",!1,c,se.trendLine),("summary"===e||"scatter"===e||"hexbin"===e&&"contour"===f||"bar"===e||"parallel"===e)&&$e(v,w("dim1"),"summary"===e?"Category":"Color",!0,t.dim1,C(e,"dim1")),"scatter"===e&&$e(v,w("dim2"),"Labels",!1,t.dim2,C(e,"dim2")),"hexbin"===e&&"contour"===f&&$e(["by color"],w("dim3"),"Multiclass",!1,t.dim3,C(e,"dim3")),"network"===e&&$e(v,w("dim1"),"SOURCE",!0,t.dim1,C(e,"dim1")),"network"===e&&$e(v,w("dim2"),"TARGET",!0,t.dim2,C(e,"dim2")),"network"===e&&$e(["matrix","arc","force","sankey"],e=>i({networkType:e}),"Type",!0,d,se.networkType),"network"===e&&$e(["static","scaled"],w("networkLabel"),"Show Labels",!1,t.networkLabel,se.networkLabel),"hierarchy"===e&&$e(["dendrogram","treemap","partition","sunburst"],e=>i({hierarchyType:e}),"Type",!0,s,se.hierarchyType),"summary"===e&&$e(["violin","boxplot","joy","heatmap","histogram"],e=>i({summaryType:e}),"Type",!0,h,se.summaryType),"line"===e&&$e(["array-order",...k],w("timeseriesSort"),"Sort by",!0,t.timeseriesSort,se.timeseriesSort),"line"===e&&a.createElement("div",{title:se.lineType,style:{display:"inline-block"}},a.createElement("div",null,a.createElement("h3",null,"Chart Type")),Pe.map(e=>a.createElement("button",{key:e.type,className:`button-text ${b===e.type&&"selected"}`,onClick:()=>u(e.type)},e.label))),"hexbin"===e&&a.createElement("div",{className:"control-wrapper",title:se.areaType},a.createElement("div",null,a.createElement("h3",null,"Chart Type")),Ae.map(e=>{const t=e.type;return"contour"===t||"hexbin"===t||"heatmap"===t?a.createElement("button",{className:`button-text ${f===t&&"selected"}`,key:t,onClick:()=>x(t)},e.label):a.createElement("div",null)})),"hierarchy"===e&&a.createElement("div",{className:"control-wrapper",title:se.nestingDimensions},a.createElement("div",null,a.createElement("h3",null,"Nesting")),0===o.length?"Select categories to nest":`root, ${o.join(", ")}`),("bar"===e||"hierarchy"===e)&&a.createElement("div",{className:"control-wrapper",title:se.barDimensions},a.createElement("div",null,a.createElement("h3",null,"Categories")),n.map(e=>a.createElement("button",{key:`dimensions-select-${e.name}`,className:`button-text ${-1!==o.indexOf(e.name)&&"selected"}`,onClick:()=>g(e.name)},e.name))),"line"===e&&a.createElement("div",{className:"control-wrapper",title:se.lineDimensions},a.createElement("div",null,a.createElement("h3",null,"Metrics")),r.map(e=>a.createElement("button",{key:`metrics-select-${e.name}`,className:`button-text ${-1!==l.indexOf(e.name)&&"selected"}`,onClick:()=>y(e.name)},e.name)))))};const Le="dx-default-pk";r.d(t,"DataExplorer",function(){return Re}),r.d(t,"Toolbar",function(){return we}),r.d(t,"Viz",function(){return Te});const De="application/vnd.dataresource+json",Fe=({view:e,lineType:t,areaType:r,selectedDimensions:a,selectedMetrics:n,pieceType:i,summaryType:o,networkType:l,hierarchyType:s,trendLine:c,marginalGraphics:m,barGrouping:p,chart:h})=>`${e}-${t}-${r}-${a.join(",")}-${n.join(",")}-${i}-${o}-${l}-${s}-${c}-${m}-${p}-${JSON.stringify(h)}`,ze=[500,300],Ne=l.c.div`
  & {
    font-family: Source Sans Pro, Helvetica Neue, Helvetica, Arial, sans-serif;
  }
`,He=l.c.div`
  & {
    backgroundcolor: #cce;
    padding: 10px;
    paddingleft: 20px;
  }
`,Be=({metadata:e})=>{const t=e&&e.sampled?a.createElement("span",null,a.createElement("b",null,"NOTE:")," This data is sampled"):null;return a.createElement(Ne,null,t?a.createElement(He,null,t):null)},Ve=l.c.div`
  display: flex;
  flex-flow: row nowrap;
  width: 100%;
`,Ze=l.c.div`
  width: 100%;
  .html-legend-item {
    color: var(--theme-app-fg);
  }

  .tick > path {
    stroke: lightgray;
  }

  .axis-labels,
  .ordinal-labels {
    fill: var(--theme-app-fg);
    font-size: 14px;
  }

  path.connector,
  path.connector-end {
    stroke: var(--theme-app-fg);
  }

  path.connector-end {
    fill: var(--theme-app-fg);
  }

  text.annotation-note-label,
  text.legend-title,
  .legend-item text {
    fill: var(--theme-app-fg);
    stroke: none;
  }

  .xyframe-area > path {
    stroke: var(--theme-app-fg);
  }

  .axis-baseline {
    stroke-opacity: 0.25;
    stroke: var(--theme-app-fg);
  }
  circle.frame-hover {
    fill: none;
    stroke: gray;
  }
  .rect {
    stroke: green;
    stroke-width: 5px;
    stroke-opacity: 0.5;
  }
  rect.selection {
    opacity: 0.5;
  }
`;class Re extends a.PureComponent{constructor(e){super(e),this.updateChart=(e=>{const{view:t,dimensions:r,metrics:n,chart:i,lineType:o,areaType:l,selectedDimensions:s,selectedMetrics:c,pieceType:m,summaryType:p,networkType:h,hierarchyType:d,trendLine:u,marginalGraphics:y,barGrouping:g,colors:b,primaryKey:f,data:x}=Object.assign({},this.state,e);if(!this.props.data&&!this.props.metadata&&!this.props.initialView)return;const{data:E,height:k,onMetadataChange:v}=this.props,{Frame:w,chartGenerator:C}=ie[t],T=Fe({view:t,lineType:o,areaType:l,selectedDimensions:s,selectedMetrics:c,pieceType:m,summaryType:p,networkType:h,hierarchyType:d,chart:i,trendLine:u,marginalGraphics:y,barGrouping:g}),M=C(x,E.schema,{metrics:n,dimensions:r,chart:i,colors:b,height:k,lineType:o,areaType:l,selectedDimensions:s,selectedMetrics:c,pieceType:m,summaryType:p,networkType:h,hierarchyType:d,primaryKey:f,trendLine:u,marginalGraphics:y,barGrouping:g,setColor:this.setColor}),S=a.createElement(Ze,null,a.createElement(w,Object.assign({responsiveWidth:!0,size:ze},M)),a.createElement(Ge,Object.assign({},{data:x,view:t,chart:i,metrics:n,dimensions:r,selectedDimensions:s,selectedMetrics:c,hierarchyType:d,summaryType:p,networkType:h,trendLine:u,marginalGraphics:y,barGrouping:g,updateChart:this.updateChart,updateDimensions:this.updateDimensions,setLineType:this.setLineType,updateMetrics:this.updateMetrics,lineType:o,setAreaType:this.setAreaType,areaType:l})));v&&v(Object.assign({},this.props.metadata,{dx:{view:t,lineType:o,areaType:l,selectedDimensions:s,selectedMetrics:c,pieceType:m,summaryType:p,networkType:h,hierarchyType:d,trendLine:u,marginalGraphics:y,barGrouping:g,colors:b,chart:i}}),De),this.setState(t=>Object.assign({},e,{displayChart:Object.assign({},t.displayChart,{[T]:S})}))}),this.setView=(e=>{this.updateChart({view:e})}),this.setGrid=(()=>{this.setState({view:"grid"})}),this.setColor=(e=>{this.updateChart({colors:e})}),this.setLineType=(e=>{this.updateChart({lineType:e})}),this.setAreaType=(e=>{this.updateChart({areaType:e})}),this.updateDimensions=(e=>{const t=this.state.selectedDimensions,r=-1===t.indexOf(e)?[...t,e]:t.filter(t=>t!==e);this.updateChart({selectedDimensions:r})}),this.updateMetrics=(e=>{const t=this.state.selectedMetrics,r=-1===t.indexOf(e)?[...t,e]:t.filter(t=>t!==e);this.updateChart({selectedMetrics:r})});const{metadata:t,initialView:r}=e,n=t.dx||{},i=n.chart||{};let{fields:o=[],primaryKey:l=[]}=e.data.schema;0===l.length&&(l=[Le],o=[...o,{name:Le,type:"integer"}]);const s=o.filter(e=>"string"===e.type||"boolean"===e.type||"datetime"===e.type),c=e.data.data.map((e,t)=>{const r=Object.assign({},e);return o.forEach(e=>{e.name===Le&&(r[Le]=t),"datetime"===e.type&&(r[e.name]=new Date(r[e.name]))}),r}),m=o.filter(e=>"integer"===e.type||"number"===e.type||"datetime"===e.type).filter(e=>!l.find(t=>t===e.name));this.state=Object.assign({view:r,lineType:"line",areaType:"hexbin",trendLine:"none",marginalGraphics:"none",barGrouping:"Clustered",selectedDimensions:[],selectedMetrics:[],pieceType:"bar",summaryType:"violin",networkType:"force",hierarchyType:"dendrogram",dimensions:s,metrics:m,colors:Me,chart:Object.assign({metric1:m[0]&&m[0].name||"none",metric2:m[1]&&m[1].name||"none",metric3:"none",metric4:"none",dim1:s[0]&&s[0].name||"none",dim2:s[1]&&s[1].name||"none",dim3:"none",timeseriesSort:"array-order",networkLabel:"none"},i),displayChart:{},primaryKey:l,data:c},n)}componentDidMount(){"grid"!==this.state.view&&this.updateChart(this.state)}render(){const{view:e,dimensions:t,chart:r,lineType:n,areaType:i,selectedDimensions:o,selectedMetrics:l,pieceType:s,summaryType:c,networkType:m,hierarchyType:p,trendLine:h,marginalGraphics:d,barGrouping:u}=this.state;let y=null;if("grid"===e)y=a.createElement(b,Object.assign({},this.props));else if(["line","scatter","bar","network","summary","hierarchy","hexbin","parallel"].includes(e)){const t=Fe({view:e,lineType:n,areaType:i,selectedDimensions:o,selectedMetrics:l,pieceType:s,summaryType:c,networkType:m,hierarchyType:p,chart:r,trendLine:h,marginalGraphics:d,barGrouping:u});y=this.state.displayChart[t]}const g=a.Children.map(this.props.children,r=>{if(!a.isValidElement(r))return;const{componentType:n}=r.props;if("viz"===n){const e={children:y};return a.cloneElement(r,e)}if("toolbar"===n){const n={dimensions:t,currentView:e,setGrid:this.setGrid,setView:this.setView};return a.cloneElement(r,n)}return r});return a.createElement("div",null,a.createElement(Be,{metadata:this.props.metadata}),a.createElement(Ve,null,g))}}Re.MIMETYPE=De,Re.defaultProps={metadata:{dx:{}},height:500,mediaType:De,initialView:"grid"};const We=e=>a.createElement(Re,Object.assign({},e),a.createElement(Te,null),a.createElement(we,null));We.defaultProps={mediaType:De},We.displayName="DataExplorerDefault",We.MIMETYPE=De;t.default=We}}]);