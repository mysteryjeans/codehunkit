/*
* JQuery util functions
* 
* Author: Faraz Masood Khan faraz@fanaticlab.com
* 
* Copyright (c) 2013 FanaticLab  
*/

// Update post vote for user action
function update_vote(data) {
    if (data.status == 200) {
        response = JSON.parse(data.responseText);
        votes = parseInt($('#snippet-id-' + response.post_id + ' .votes').html()) + response.net_effect;        
        $('#snippet-id-' + response.post_id + ' .votes').html(votes);
        
        if (response.vote_index == 1)	{
				if (!$('#snippet-id-' + response.post_id + ' .up-vote').hasClass('up-vote-on'))        		
        			$('#snippet-id-' + response.post_id + ' .up-vote').addClass('up-vote-on');
        		
        		$('#snippet-id-' + response.post_id + ' .down-vote').removeClass('down-vote-on');
        } else if (response.vote_index == -1) {
        		$('#snippet-id-' + response.post_id + ' .up-vote').removeClass('up-vote-on');
        		
        		if (!$('#snippet-id-' + response.post_id + ' .down-vote').hasClass('down-vote-on'))
        			$('#snippet-id-' + response.post_id + ' .down-vote').addClass('down-vote-on');
        } else {
        		$('#snippet-id-' + response.post_id + ' .up-vote').removeClass('up-vote-on');
        		$('#snippet-id-' + response.post_id + ' .down-vote').removeClass('down-vote-on');
        }
        
    } else if (data.status == 403) {
           window.location = data.responseText;                    
    } else {
           window.location = '/';
    }
}

// Update comment vote for user action
function update_comment_vote(data) {
    if (data.status == 200) {
        response = JSON.parse(data.responseText);
        votes = parseInt($('#comment-id-' + response.comment_id + ' .votes').first().html()) + response.net_effect;        
        $('#comment-id-' + response.comment_id + ' .votes').first().html(votes);
        
        if (response.vote_index == 1)	{
				if (!$('#comment-id-' + response.comment_id + ' .up-vote').first().hasClass('up-vote-on'))        		
        			$('#comment-id-' + response.comment_id + ' .up-vote').first().addClass('up-vote-on');
        		
        		$('#comment-id-' + response.comment_id + ' .down-vote').first().removeClass('down-vote-on');
        } else if (response.vote_index == -1) {
        		$('#comment-id-' + response.comment_id + ' .up-vote').first().removeClass('up-vote-on');
        		
        		if (!$('#comment-id-' + response.comment_id + ' .down-vote').first().hasClass('down-vote-on'))
        			$('#comment-id-' + response.comment_id + ' .down-vote').first().addClass('down-vote-on');
        } else {
        		$('#comment-id-' + response.comment_id + ' .up-vote').first().removeClass('up-vote-on');
        		$('#comment-id-' + response.comment_id + ' .down-vote').first().removeClass('down-vote-on');
        }
        
    } else if (data.status == 403) {
           window.location = data.responseText;                    
    } else {
           window.location = '/';
    }
}