var jq=jQuery.noConflict();
jq(document).ready(function(){
	//load overlay effect
	if (!jq.browser.msie || parseInt(jq.browser.version, 10) >= 7) {
		jq(".ajax_form > a").prepOverlay({
			subtype: 'ajax',
			filter: '#content>*',
			formselector: '#content-core > form',
			noform: 'close',
			closeselector: '[name=form.buttons.cancel]',
		});
	}	

// image overlay 
jq('.newsImageContainer a').prepOverlay({
         subtype: 'image',
         urlmatch: '/image_view_fullscreen$',
         urlreplace: '_preview'
        });
}        
//document ready end
)