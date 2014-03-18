/* Execute util functions after page load to avoid ie issues.
 * This script should be place after all html elements
 */

function contextMenu() {
	$(document).click(function(e) {
		$('[context-menu]').each(function() {
			if (!$(e.target).parent('[context-menu]').andSelf().is(this) && !$(e.target).parents().andSelf().is($(this).attr('context-menu')))
				$(this).fadeOut('fast');
		});
	});

	$('[context-menu]').each(function() {
		var $contextMenu = $(this);
		$($contextMenu.attr('context-menu')).click(function() {
			$contextMenu.fadeIn('fast');			
		});
	});
}

function shareLink() {
	$('[data-action="share:twitter"]').click(shareOnTwitter);

	$('[data-action="share:facebook"]').click(shareOnFacebook);

	$('[data-action="share:googleplus"]').click(shareOnGooglePlus);
}

function playMedia() {
	$('[data-action="play:video"]').click(function() {
		var iframe = $(this).attr('data-content');
		if ($(iframe).attr('src') == '') {
			$(iframe).attr('src', $(iframe).attr('data-content'));
			$(iframe).fadeIn('slow');
			$('span', this).html('&#8211;');
		} else {
			$(iframe).attr('src', '');
			$(iframe).html('');
			$(iframe).fadeOut('fast');
			$('span', this).html('+');
		}
		return false;
	});
}

function shareOnTwitter() {
	var link = this.href == '#' ? location.href : this.href;
	var title = this.href == '#' ? document.title : $(this).attr('data-content');

	// twitter add space between url and text
	if ((title.length + link.length) > 139)
		title = title.substring(0, 136 - link.length) + '...';

	PopupCenter('https://twitter.com/intent/tweet?url=' + encodeURIComponent(link) + '&text=' + encodeURIComponent(title), 'Twitter Share Dailog', 550, 400);
	return false;
}

function shareOnFacebook() {
	var link = this.href == '#' ? location.href : this.href;
	PopupCenter('https://www.facebook.com/sharer/sharer.php?u=' + encodeURIComponent(link), 'Facebook Share Dailog', 626, 436);
	return false;
}

function shareOnGooglePlus() {
	var link = this.href == '#' ? location.href : this.href;
	PopupCenter('https://plus.google.com/share?url=' + encodeURIComponent(link), 'Google+ Share Dailog', 600, 600);
	return false;
}

function PopupCenter(url, title, w, h) {
	// Fixes dual-screen position                       Most browsers      Firefox
	var dualScreenLeft = window.screenLeft != undefined ? window.screenLeft : screen.left;
	var dualScreenTop = window.screenTop != undefined ? window.screenTop : screen.top;

	var left = ((screen.width / 2) - (w / 2)) + dualScreenLeft;
	var top = ((screen.height / 2) - (h / 2)) + dualScreenTop;
	var win = window.open(url, title, 'menubar=no,toolbar=no,resizable=yes,scrollbars=yes,width=' + w + ',height=' + h + ',top=' + top + ',left=' + left);

	// For chrome
	try {
		win.moveTo(left, top);
	} catch (e) {
	}

	// Puts focus on the newWindow
	if (window.focus) {
		win.focus();
	}
}

function __stringToColor(str) {

    // str to hash
    str = "    " + str;
    for (var i = 0, hash = 0; i < str.length; hash = str.charCodeAt(i++) + ((hash << 5) - hash));

    // int/hash to hex
    for (var i = 0, color = "#"; i < 3; color += ("00" + ((hash >> i++ * 8) & 0xFF).toString(16)).slice(-2));

    return color;
}

$(document).ready(function() {
	contextMenu();
	shareLink();
	playMedia();
}); 