var Channel,Component,FOCUSABLE_INPUTS,channel,component,i,len,merge_objects,origin,send,indexOf=[].indexOf;origin=new Date();FOCUSABLE_INPUTS=['text','textarea','number','email','password','search','tel','url'];Channel=class Channel{constructor(url,options={}){this.on=this.on.bind(this);this.url=url;this.retry_interval=options.retry_interval||1000;this.online=false;this.callbacks={};}
on(event_name,callback){return this.callbacks[event_name]=callback;}
trigger(event_name,...args){var base;return typeof(base=this.callbacks)[event_name]==="function"?base[event_name](...args):void 0;}
open(){var protocol,ref;if(!(typeof navigator!=="undefined"&&navigator!==null?navigator.onLine:void 0)&&(this.retry_interval!=null)){setTimeout((()=>{return this.open();}),this.retry_interval);}
if((ref=this.websocket)!=null){ref.close();}
if(window.location.protocol==='https:'){protocol='wss://';}else{protocol='ws://';}
this.websocket=new WebSocket(`${protocol}${window.location.host}${this.url}`);this.websocket.onopen=(e)=>{this.online=true;return this.trigger('open');};this.websocket.onclose=(e)=>{this.online=false;this.trigger('close');if(this.retry_interval!=null){return setTimeout((()=>{return this.open();}),this.retry_interval);}};return this.websocket.onmessage=(e)=>{var data;data=JSON.parse(e.data);return this.trigger('message',data);};}
send(command,payload){var data;data={command:command,payload:payload};if(this.online){try{return this.websocket.send(JSON.stringify(data));}catch(error){return console.log('Failed sending');}}}};channel=new Channel('/reactor');channel.open();channel.on('open',function(){var el,i,len,ref,results;console.log('ON-LINE');ref=document.querySelectorAll(reactor_components.join(','));results=[];for(i=0,len=ref.length;i<len;i++){el=ref[i];results.push(el.connect());}
return results;});channel.on('message',function({type,id,html_diff}){var el;console.log('<<<',type.toUpperCase(),id);el=document.getElementById(id);if(el!=null){if(type==='render'){return el.apply_diff(html_diff);}else if(type==='remove'){return window.requestAnimationFrame(function(){return el.remove();});}}});for(i=0,len=reactor_components.length;i<len;i++){component=reactor_components[i];Component=class Component extends HTMLElement{constructor(){super();this.tag_name=this.tagName.toLowerCase();this._last_received_html='';}
connectedCallback(){return this.connect();}
disconnectedCallback(){return channel.send('leave',{id:this.id});}
is_root(){return!this.parent_component();}
parent_component(){component=this.parentElement;while(component){if(component.dispatch!=null){return component;}
component=component.parentElement;}}
connect(){var state;if(this.is_root()){console.log('>>> JOIN',this.tag_name);state=JSON.parse(this.getAttribute('state'));return channel.send('join',{tag_name:this.tag_name,state:state});}}
apply_diff(html_diff){var cursor,diff,html,j,len1;console.log(new Date()-origin);html=[];cursor=0;console.log(html_diff);for(j=0,len1=html_diff.length;j<len1;j++){diff=html_diff[j];if(typeof diff==='string'){html.push(diff);}else if(diff<0){cursor-=diff;}else{html.push(this._last_received_html.slice(cursor,cursor+diff));cursor+=diff;}}
html=html.join('');if(this._last_received_html!==html){this._last_received_html=html;return window.requestAnimationFrame(()=>{var ref;morphdom(this,html,{onBeforeElUpdated:function(from_el,to_el){var ref;if((ref=from_el.type,indexOf.call(FOCUSABLE_INPUTS,ref)>=0)&&from_el===document.activeElement&&indexOf.call(to_el.getAttributeNames(),'reactor-orverride-value')<0){to_el.getAttributeNames().forEach(function(name){return from_el.setAttribute(name,to_el.getAttribute(name));});from_el.readOnly=to_el.readOnly;return false;}
return true;}});return(ref=this.querySelector('[focus]'))!=null?ref.focus():void 0;});}}
dispatch(name,args){var k,state,v;state=this.serialize();for(k in args){v=args[k];state[k]=v;}
console.log('>>> USER_EVENT',this.tag_name,name,state);origin=new Date();return channel.send('user_event',{name:name,state:state});}
serialize(state){var checked,j,l,len1,len2,name,obj,part,ref,ref1,satte,type,value;if(state==null){state={id:this.id};}
ref=this.querySelectorAll('[name]');for(j=0,len1=ref.length;j<len1;j++){({type,name,value,checked}=ref[j]);value=type==='checkbox'?checked:value;ref1=name.split('.').reverse();for(l=0,len2=ref1.length;l<len2;l++){part=ref1[l];obj={};obj[part]=value;value=obj;}
satte=merge_objects(state,value);}
return state;}};customElements.define(component,Component);}
merge_objects=function(target,source){var k,v;for(k in source){v=source[k];if(typeof target[k]==='object'){merge_objects(target[k],v);}else{target[k]=v;}}
return target;};send=function(element,name,args){while(element){if(element.dispatch!=null){return element.dispatch(name,args||{});}
element=element.parentElement;}};