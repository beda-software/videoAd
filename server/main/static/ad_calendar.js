$(document).ready(function(){
    $(".ad_calendar").each(function(index, item){
//        console.log(this);/
//        var list = $(item).find('input').data('dates') || [],
//            params = {dateFormat: "yy-mm-dd", altField: '#'+$(item).find('input').attr('id')};
//
//        if(list.length) {
//            params['addDates'] = list;
//        }
//
//        $(item).find('div').multiDatesPicker(params);
    });
    $('.grp-module.grp-table').bind('DOMSubtreeModified', function(e) {
        console.log(e);
//        if (e.target.innerHTML.length > 0) {
////            var newItem = $(this).find('.grp-dynamic-form');
//            var items = this.getElementsByClassName('grp-dynamic-form');
////            console.log(items[2]);
//            console.log(items.length);
//            console.log(items);
////            var items = Array.apply(Array, items);
//            for (var i in items) {
//                console.log(items[i]);
//            }
//            items.forEach(function(item){
//                console.log(item);
//            });
//        }
    });

//    $('.grp-icon.grp-add-handler').click(function(){
//        $(".ad_calendar").each(function(index, item){
//            var list = $(item).find('input').data('dates') || [],
//                params = {dateFormat: "yy-mm-dd", altField: '#'+$(item).find('input').attr('id')};
//
//            if(list.length) {
//                params['addDates'] = list;
//            }
//
//            $(item).find('div').multiDatesPicker(params);
//        });
//    });
});