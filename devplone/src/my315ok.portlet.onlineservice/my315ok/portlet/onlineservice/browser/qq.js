/*
<!--

var skinID = 1; //帮助面版样式
var QQreFreshTime = 1000; //单位是ms
//设定你要显示的QQ号吧！
var QQArrayStr = "568066794:49047881:49047881:49047881:49047881:49047881:";
//设定本QQ号提供服务的功能
var QQHelpMsg = "技术支持:项目定制:客户服务:客户服务:客户服务:客户服务:";
//设定每个QQ的头像图标名称,本图片放在目录“images”下
var QQheaderFaceOnline = "online.gif:online.gif:online.gif:online.gif:online.gif:online.gif:"
var QQheaderFaceOffline = "offline.gif:offline.gif:offline.gif:offline.gif:offline.gif:offline.gif:"



/////////////////////////////////////////////////////////////////////////////////////////////////////
var QQArray = QQArrayStr.split(":");

QQHelpMsg = QQHelpMsg.split(":");
QQheaderFaceOnline = QQheaderFaceOnline.split(":");
QQheaderFaceOffline = QQheaderFaceOffline.split(":");
var QQLinkstr = "http://webpresence.qq.com/getonline?Type=1&" + QQArrayStr;
//显示位置初始化
var verticalpos="fromtop";
var online = new Array();

if (!document.layers)
document.write('<div id="divStayTopLeft" style=position:absolute>');
document.write('<table cellSpacing="0" cellPadding="0" width="110" border="0" id="qqtab">');
document.write('    <tr>');
document.write('      <td width="110"><img src="Images/'+ skinID +'/top.gif" border="0"></td>');
document.write('    </tr>');
document.write('    <tr>');
document.write('      <td id="QQStatusBody" valign="middle" align="center" background="Images/'+ skinID +'/middle.gif">');    
document.write('	  </td>');
document.write('    </tr>');
document.write('    <tr>');
document.write('      <td width="110"><img src="Images/'+ skinID +'/bottom.gif" border="0"></td>');
document.write('    </tr>');
document.write('</table>');
if (!document.layers)
document.write('</div>')
//绑定script
var element=document.createElement('script');
element.setAttribute('id', 'GetStatus');
element.setAttribute('src', QQLinkstr);
divStayTopLeft.appendChild(element);

LoadQQStatus();
JSFX_FloatTopDiv();

/////////////////////////////////////////////////////////////////////////
function scrollpo()
{
var scrollPos;
if (typeof window.pageYOffset != 'undefined') { 
   scrollPos = window.pageYOffset; 
} 
else if (typeof document.compatMode != 'undefined' && 
     document.compatMode != 'BackCompat') { 
   scrollPos = document.documentElement.scrollTop; 
} 
else if (typeof document.body != 'undefined') { 
   scrollPos = document.body.scrollTop; 
} 
return scrollPos;
}

function JSFX_FloatTopDiv()
{
	var startX = 2;
	startY = 100;
	var ns = (navigator.appName.indexOf("Netscape") != -1);
	var d = document;
	function ml(id)
	{
		var el=d.getElementById?d.getElementById(id):d.all?d.all[id]:d.layers[id];
		if(d.layers)el.style=el;
		el.sP=function(x,y){this.style.left=x;this.style.top=y;};
		el.x = startX;
		if (verticalpos=="fromtop")
		el.y = startY;
		else{
		el.y = ns ? pageYOffset + innerHeight : scrollpo() + document.body.clientHeight;
		el.y -= startY;
		}
		return el;
	}
	window.stayTopLeft=function()
	{
		if (verticalpos=="fromtop"){
		var pY = ns ? pageYOffset : scrollpo();
		ftlObj.y += (pY + startY - ftlObj.y)/8;
		}
		else{
		var pY = ns ? pageYOffset + innerHeight : scrollpo() + document.body.clientHeight;
		ftlObj.y += (pY - startY - ftlObj.y)/8;
		}
		ftlObj.sP(ftlObj.x, ftlObj.y);
		setTimeout("stayTopLeft()", 20);
	}
	ftlObj = ml("divStayTopLeft");
        //setTimeout("stayTopLeft()", 10);
	stayTopLeft();
}
////////////////////////////////////////////////////////////////////////////
function LoadQQStatus(){
	var Body = '<table border="0" width="80" cellSpacing="0" cellPadding="0">';
	Body = Body + '  <tr>';
	Body = Body + '    <td width="80" height="3" border="0" colspan="2"></td>';
	Body = Body + '  </tr>';
	for (var qqNumLen=0; qqNumLen<online.length; qqNumLen ++)
	{
			Body = Body + '  <tr>';
		if (online[qqNumLen]==1)
		{
			Body = Body + '    <td width="25" valign="middle" align="center" rowspan="2">';
			Body = Body + '		<img src="Images/'+ QQheaderFaceOnline[qqNumLen] +'" border=0 height=26>';
			Body = Body + '    </td>';
			Body = Body + '    <td width="55" height="20" valign="middle" align="left">';
			Body = Body + '		<a target=blank href=http://wpa.qq.com/msgrd?V=1&amp;Uin='+ QQArray[qqNumLen] +'&amp;Site=Foosun.cn&amp;Menu=yes><font style=font-size:12px;TEXT-DECORATION:none;color:#333399;>'+ QQHelpMsg[qqNumLen] +'</font></a><br>';
			Body = Body + '    </td>';
		}
		else
		{
			Body = Body + '    <td width="25" valign="middle" align="center" rowspan="2">';
			Body = Body + '		<img src="Images/'+ QQheaderFaceOffline[qqNumLen] +'" border=0 height=26>';
			Body = Body + '    </td>';
			Body = Body + '    <td width="55" height="20" valign="middle" align="left">';
			Body = Body + '		<a target=blank href=http://wpa.qq.com/msgrd?V=1&amp;Uin='+ QQArray[qqNumLen] +'&amp;Site=Foosun.cn&amp;Menu=yes><font style=font-size:12px;TEXT-DECORATION:none;color:#333399;>'+ QQHelpMsg[qqNumLen] +'</font></a><br>';
			Body = Body + '    </td>';
		}
			Body = Body + '  </tr>';
			Body = Body + '  <tr>';
			Body = Body + '		<td style="font-size: 10px;">'+ QQArray[qqNumLen] +'</td>';
			Body = Body + '  </tr>';
			Body = Body + '  <tr>';
			Body = Body + '    <td height="2" border="0" colspan="2" bgcolor="#DDDDDD"></td>';
			Body = Body + '  </tr>';
	}
	Body = Body + '</table>';     
	var obj = document.getElementById("QQStatusBody");
	obj.innerHTML = Body;
	//重新加载online数组
	online = new Array();
	GetStatus.src = QQLinkstr;
	setTimeout("LoadQQStatus()",QQreFreshTime);
}
//////////////////////////////////////////////////////////////////
-->


*/


function scrollpo()
{
	var scrollPos;
	if (typeof window.pageYOffset != 'undefined') { 
   		scrollPos = window.pageYOffset; 
	} 
	else if (typeof document.compatMode != 'undefined' && 
     document.compatMode != 'BackCompat') { 
   scrollPos = document.documentElement.scrollTop; 
	} 
	else if (typeof document.body != 'undefined') { 
   scrollPos = document.body.scrollTop; 
	} 
	return scrollPos;
}
 function CloseQQ(id)
	{
	id.style.display="none";
	}
function QQFloat(id,startX,startY,stay)
{
 var ns = (navigator.appName.indexOf("Netscape") != -1);
 var d = document;
 function ml(id,startX,startY)
 	{
 		var el=d.getElementById?d.getElementById(id):d.all?d.all[id]:d.layers[id];
		if(d.layers)el.style=el;
		el.sP=function(x,y){this.style.left=x;this.style.top=y;};
		el.x = startX;
		if (stay=="fromtop")
		el.y = startY;
		else{
			el.y = ns ? pageYOffset + innerHeight : scrollpo() + document.body.clientHeight;
			el.y -= startY;
		}
		return el;
 	}
 window.stayTopLeft=function()
 		{
  			var pY = ns ? pageYOffset : document.body.scrollTop;
  			ftlObj.y += (pY + startY - ftlObj.y)/8;  
 			ftlObj.sP(document.body.scrollLeft + document.body.offsetWidth - 125, ftlObj.y);
  			setTimeout("stayTopLeft()", 30);
 		}
 
 ftlObj = ml(id,(document.body.scrollLeft + document.body.offsetWidth)/2 + 379,30);
 stayTopLeft();
}