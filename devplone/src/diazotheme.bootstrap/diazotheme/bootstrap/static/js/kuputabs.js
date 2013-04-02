$(document).ready(function () {kuputabs={};kuputabs.idCounter=0;kuputabs.Tab=function(title,open){this.id=null;this.open=open;this.title=title;this.content=$('<div class="kuputab-content"><!-- Dynamically generated tab --></div>')};kuputabs.collectTabs=function(){$("h2.kuputab-tab-definer, h2.kuputab-tab-definer-default").parent().each(function(){var tabs=[];var collecting=false;var curTab=null;var parent=this;$(this).contents().each(function(){var t=$(this);if(t.hasClass("kuputab-tab-definer")||t.hasClass("kuputab-tab-definer-default")){var open=t.hasClass("kuputab-tab-definer-default");var tab=new kuputabs.Tab(t.text(),open);tabs.push(tab);curTab=tab;t.removeClass("kuputab-tab-definer");t.removeClass("kuputab-tab-definer-default");parent.removeChild(this)}else{if(curTab!=null){parent.removeChild(this);curTab.content.append(this)}}});var container=kuputabs.constructContainer(tabs);$(parent).append(container)})};kuputabs.constructContainer=function(tabs){var cont=$('<div class="kuputab-container"><!-- Dynamically generated tab  container --></div>');var selectors=$('<ul class="kuputab-selectors"><!-- Dynamically generated tab selectors --></ul>');var i;if(tabs.length==0){return}for(i=0;i<tabs.length;i++){var tab=tabs[i];var first=(i==0);var last=(i==tabs.length-1);tab.id=(kuputabs.idCounter++);var classes="kuputab-selector";if(first){classes+=" kuputab-selector-first"}if(last){classes+=" kuputab-selector-last"}var clicker=$("<li></li>");clicker.attr({"class":classes,"id":"kuputab-selector-"+tab.id});var link=$("<a></a>");var classes;if(tab.open){classes="selected"}else{classes=""}link.attr({id:"kuputab-link-"+tab.id,href:"#kuputab-content-"+tab.id,"class":classes});link.append("<span>"+tab.title+"</span>");link.mouseover(kuputabs.mouseover);clicker.append(link);selectors.append(clicker)}cont.append(selectors);for(i=0;i<tabs.length;i++){var tab=tabs[i];var first=(i==0);var last=(i==tabs.length-1);var content=tab.content;content.attr({"id":"kuputab-content-"+tab.id});if(tab.open){}else{tab.content.addClass("hidden")}cont.append(content)}return cont};kuputabs.mouseover=function(e){var elem=$(e.target);if(elem.get(0).tagName.toLowerCase()!="a"){elem=elem.parents("a")}var container=elem.parents(".kuputab-container");var id=elem.attr("id");if(id==null){alert("Invalid tab selector handler "+e.target);return}id=id.replace(/^kuputab-link-/,"");var selectors=container.find("li.kuputab-selector a");var panels=container.find("div.kuputab-content");selectors.removeClass('selected');panels.addClass('hidden');var panel=container.find("#kuputab-content-"+id);var selector=container.find("#kuputab-selector-"+id+" a");selector.addClass("selected");panel.removeClass("hidden");return false};kuputabs.init=function(){try{if(document.designMode.toLowerCase()=="on"){return}else{kuputabs.collectTabs();$("#portletPageColumns").appendTo("#kuputab-content-0")}}catch(e){kuputabs._printStackTrace(e)}};kuputabs.log=function(msg){if(typeof(console)!="undefined"){if(typeof(console.log)!="undefined"){console.log(msg)}}};kuputabs._printStackTrace=function(exc){function print(msg){kuputabs.log(msg)}print(exc);if(!exc.stack){print('no stacktrace available');return}var lines=exc.stack.toString().split('\n');var toprint=[];for(var i=0;i<lines.length;i++){var line=lines[i];if(line.indexOf('ecmaunit.js')>-1){break}if(line.charAt(0)=='('){line='function'+line}var chunks=line.split('@');toprint.push(chunks)}toprint.reverse();for(var j=0;j<toprint.length;j++){print('  '+toprint[j][1]);print('    '+toprint[j][0])}print()};kuputabs.click = function(e) {return false};$(kuputabs.init);
})
