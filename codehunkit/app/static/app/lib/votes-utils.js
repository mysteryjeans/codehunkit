/*
* JQuery util functions
* 
* Author: Faraz Masood Khan faraz@fanaticlab.com
* 
* Copyright (c) 2013 FanaticLab  
*/

// Update snippet vote for user action
var vote_update = function (data) {	
    if (data.status == 200) {
    	var response = JSON.parse(data.responseText);
    	var votesBoxID = '#snippet-votes-box-id-' + response.snippet_id;
        var votes = parseInt($(votesBoxID + ' .votes').html()) + response.net_effect;        
        $(votesBoxID + ' .votes').html(votes);
        
        if (response.vote_index == 1)	{
				if (!$(votesBoxID + ' .up-vote').hasClass('on'))        		
        			$(votesBoxID + ' .up-vote').addClass('on');
        		
        		$(votesBoxID + ' .down-vote').removeClass('on');
        } else if (response.vote_index == -1) {
        		$(votesBoxID + ' .up-vote').removeClass('on');
        		
        		if (!$(votesBoxID + ' .down-vote').hasClass('on'))
        			$(votesBoxID + ' .down-vote').addClass('on');
        } else {
        		$(votesBoxID + ' .up-vote').removeClass('on');
        		$(votesBoxID + ' .down-vote').removeClass('on');
        }
        
    } else if (data.status == 403) {
           window.location = data.responseText;                    
    } else {
           window.location = '/';
    }
};

// Update comment vote for user action
var comment_vote_update = function (data) {
    if (data.status == 200) {
        response = JSON.parse(data.responseText);
        votes = parseInt($('#comment-id-' + response.comment_id + ' .votes').first().html()) + response.net_effect;        
        $('#comment-id-' + response.comment_id + ' .votes').first().html(votes);
        
        if (response.vote_index == 1)	{
				if (!$('#comment-id-' + response.comment_id + ' .up-vote').first().hasClass('on'))        		
        			$('#comment-id-' + response.comment_id + ' .up-vote').first().addClass('on');
        		
        		$('#comment-id-' + response.comment_id + ' .down-vote').first().removeClass('on');
        } else if (response.vote_index == -1) {
        		$('#comment-id-' + response.comment_id + ' .up-vote').first().removeClass('on');
        		
        		if (!$('#comment-id-' + response.comment_id + ' .down-vote').first().hasClass('on'))
        			$('#comment-id-' + response.comment_id + ' .down-vote').first().addClass('on');
        } else {
        		$('#comment-id-' + response.comment_id + ' .up-vote').first().removeClass('on');
        		$('#comment-id-' + response.comment_id + ' .down-vote').first().removeClass('on');
        }
        
    } else if (data.status == 403) {
           window.location = data.responseText;                    
    } else {
           window.location = '/';
    }
};
