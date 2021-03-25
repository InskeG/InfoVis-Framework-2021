function switchFilter(obj) {
    current_classes = $(obj).attr('class');

    if (current_classes.includes("filter_top_active")) {
        return;
    } else {
        $('div.filter_top_active').removeClass('filter_top_active')
        $(obj).addClass("filter_top_active");

        if ($(obj).attr('id') == 'filter_top_button_artists') {
            $('div.filter_type_range').removeClass('filter_type_active');
            $('div.filter_type_artists').addClass('filter_type_active');
        } else {
            $('div.filter_type_artists').removeClass('filter_type_active');
            $('div.filter_type_range').addClass('filter_type_active');
        }

        return;
    }
}