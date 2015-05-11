$(function() {
    var $newsWrapper = $('#news-list'),
        $tagMarker = $('#tagMarker');

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

    $('ul.tags').click(function(event) {
        updateCategory($(event.target).text());
        handleEmptyCategory();
    });
    
    $newsWrapper.delegate('.news', 'click', function(event) {
        // TODO Render article
        UIkit.modal('#modal-article').show();
    });

    $('#mark-as-read').click(function(event) {
        $newsWrapper.children(':visible').remove();
        handleEmptyCategory();
        // TODO Sync with server
    });

    updateCategory();
});
