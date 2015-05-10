$(function() {
    function updateCategory(text) {
        $('#tagMarker').text(text);
    }

    $('ul.tags').click(function(event) {
        updateCategory($(event.target).text());
    });

    updateCategory('All');
});
