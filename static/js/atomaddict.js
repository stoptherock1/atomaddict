$(function () {
	'use strict';
    var $newsWrapper = $('#news-list'),
        $tagMarker = $('#tagMarker'),
		api = (function () {
			function markAsRead(articleId) {
				$.post('/article_readed', {'article_id': articleId});
			}

			function markAllAsRead() {
				$('.news input[name="article_id"]').each(function () {
					markAsRead($(this).val());
				});
			}
            
            function fetchNews() {
                $.getJSON('/fetch_articles', function (data) {
                    var presentArticles = $.map($('.news input[name="article_id"]'), function (value, index) {
                        return parseInt($(value).val(), 10);
                    });
                    $.each(data, function (tag, articles) {
                        $.each(articles, function (i, article) {
                            if (presentArticles.indexOf(article.id) < 0) {
                                console.log('new article', article.id);
                            }
                        });
                    });
                });
            }

			return {
				markAsRead: markAsRead,
				markAllAsRead: markAllAsRead,
                fetchNews: fetchNews
			};
		}());
    
    api.fetchNews();

    function handleEmptyCategory() {
        var category = $('ul.tags li.uk-active').data('uk-filter'),
            childSelector = '[data-uk-filter="' + category + '"]:visible';

        /*
         * Couses nasty bug with displaying tiles after marking as read
        if (category && $newsWrapper.children(childSelector).length === 0) {
            $('#no-news').attr('style', '').removeClass('uk-hidden');
        } else {
            $('#no-news').addClass('uk-hidden');
        }
        */
    }

    function updateCategory(text) {
        if (text === undefined) {
            text = 'All';
        }
        $tagMarker.text(text);
    }

    $('ul.tags').click(function (event) {
        updateCategory($(event.target).text());
        handleEmptyCategory();
    });
    
    $newsWrapper.delegate('.news', 'mousedown', function (event) {
        if (event.which !== 1 && event.which !== 2) {
            return;
        }
        
        var $this = $(this),
			articleId = $this.find('input[name="article_id"]').val();
        
        if ($this.hasClass('already-read')) {
            return;
        }
        $this.addClass('already-read');

        window.open($this.attr('data-url'));
		api.markAsRead(articleId);
        
        /*
        if ($target.hasClass('link-external')) {
            $target.parents('.news').remove();
        } else {
            // TODO Render article
            UIkit.modal('#modal-article').show();
        }
        */
    });

    $('#mark-as-read').click(function (event) {
        $('.news').addClass('already-read');
		api.markAllAsRead();
        handleEmptyCategory();
    });
    
    $('#modal-subscribe').delegate('button', 'click', function (event) {
        $.post('/save_tags', $('#modal-subscribe form').serialize());
    });

    updateCategory();
});
