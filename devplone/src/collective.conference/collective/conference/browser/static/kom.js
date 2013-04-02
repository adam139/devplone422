var jq=jQuery.noConflict();
jq(document).ready(function(){

	
	//cancel link redirect
	jq("#portaltab-study_topic a,#portaltab-explore a,#logo a").click(function (e) {
													  return false;
	})
	
	var start=0;
	
    jq("#ajaxmore").live("click",function() {
        
       var action = jq("#ajaxdisplay").attr('data-ajax-target');
	   start++;
       jq.post(action, 
           {formstart:start},
           function(data) {
 				 var outhtml = data['outhtml'];
				 jq(outhtml).insertBefore('#ajaxmore-link');
				 var ifmore = data['ifmore'];
               if (ifmore==1){
			   		jq('#ajaxmore-link').remove();
			   }
            },
            'json');        
       return false;
    });
	
//load overlay effect
// No overlays for IE6
	if (!jq.browser.msie ||
	parseInt(jq.browser.version, 10) >= 7) {
		// Set up overlays
		jq(".add_obj_button > a").prepOverlay({
		subtype: 'ajax',
		filter: '#content>*'&'#form-widgets-affiliatedtopics-contenttree-window>*',
		formselector: '#content-core > form',
		noform: 'close',
		closeselector: '[name=form.buttons.cancel]',
		});
	}

jq("#modifytitle button[name='ok']").live("click",function() {
	var action = jq("#modifytitle").attr('title-ajax-target');
	var formval = jq("#modifytitle textarea").val();
	var title = {'title':formval};
	jq.post(action,title,function(title) {
		jq("#modifytitleform").hide();
		jq("#showtitle").html(formval).show();
		jq("#edittitle").show();
	},'json');
	return false;
});

jq("#modifytitle button[name='cancel']").live("click",function() {
	var action = jq("#modifytitle").attr('title-ajax-target');
	var formval = jq("#showtitle").html();
	var title = {'title':formval};
	jq.post(action,title,function(title) {
		jq("#modifytitleform").hide();
		jq("#showtitle").html(formval).show();
		jq("#edittitle").show();
	},'json');
	return false;
});

jq("#modifydescription button[name='ok']").live("click",function() {	  
	var action = jq("#modifydescription").attr('description-ajax-target');
	var formval = jq("#modifydescription textarea").val();
	var description = {'description':formval};
	jq.post(action,description,function(description) {
		jq("#modifydescriptionform").hide();
		jq("#showdescription").html(formval).show();
		jq("#editdescription").show();
	},'json');
	return false;
});

jq("#modifydescription button[name='cancel']").live("click",function() {	  
	var action = jq("#modifydescription").attr('description-ajax-target');
	var formval = jq("#showdescription").html();
	var description = {'description':formval};
	jq.post(action,description,function(description) {
		jq("#modifydescriptionform").hide();
		jq("#showdescription").html(formval).show();
		jq("#editdescription").show();
	},'json');
	return false;
});
var start=0;
// ajax multicondition search
jq("#ajaxmore").live("click",function() {
    
   var action = jq("#ajaxdisplay").attr('data-ajax-target');
   start++;
   jq.post(action, 
       {formstart:start},
       function(data) {
				 var outhtml = data['outhtml'];
			 jq(outhtml).insertBefore('#ajaxmore-link');
			 var ifmore = data['ifmore'];
           if (ifmore==1){
		   		jq('#ajaxmore-link').remove();
		   }
        },
        'json');        
   return false;
});


//ajax-follow-question
jq(".followjq").live("click",function() {
	jq(this).siblings("input").addClass("followform");
	var id = jq(".followform").attr('value');
	var questionid = {'questionid': id};
	if (jq(".followform").attr('id')) {
		var ida = jq(".followform").attr('id');
		var action = jq("#ajax-question-follow-" + id + ida).attr('question-follow');
		jq.post(action, questionid, function(){
			jq("#ajax-question-follow-" + id + ida).hide();
			jq("#ajax-question-unfollow-" + id + ida).show();
		}, 'json');
		jq(this).siblings("input").removeClass("followform");
	}else{
		var action = jq("#ajax-question-follow-" + id).attr('question-follow');
		jq.post(action, questionid, function(){
			jq("#ajax-question-follow-" + id).hide();
			jq("#ajax-question-unfollow-" + id).show();
		}, 'json');
		jq(this).siblings("input").removeClass("followform");
	}return false;
});

//ajax-unfollow-question
jq(".unfollowjq").live("click",function() {
	jq(this).siblings("input").addClass("unfollowform");
	var id = jq(".unfollowform").attr('value');
	var questionid = {'questionid':id};
	if (jq(".unfollowform").attr('id')){
		var ida = jq(".unfollowform").attr('id');
		var action = jq("#ajax-question-unfollow-" + id + ida).attr('question-unfollow');
		jq.post(action, questionid, function(){
			jq("#ajax-question-unfollow-" + id + ida).hide();
			jq("#ajax-question-follow-" + id + ida).show();
		}, 'json');
		jq(this).siblings("input").removeClass("unfollowform");
	}else{
		var action = jq("#ajax-question-unfollow-" + id).attr('question-unfollow');
		jq.post(action, questionid, function(){
			jq("#ajax-question-unfollow-" + id).hide();
			jq("#ajax-question-follow-" + id).show();
		}, 'json');
		jq(this).siblings("input").removeClass("unfollowform");
	}return false;
});



//prepOverlay
jq(".prepOverlay").prepOverlay({
	subtype: 'ajax',
	filter: '#content>*',
	formselector: '#content-core > form',
	noform: 'reload',
	closeselector: '[name=form.buttons.cancel]'
});

});
