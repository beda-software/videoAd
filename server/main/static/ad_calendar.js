$(document).ready(function(){
    $("#alt_id_datelist, .grp-dynamic-form .ad_calendar").each(function(index, item){
        var list = $(item).find('input').data('dates') || [],
            params = {dateFormat: "yy-mm-dd", altField: '#'+$(item).find('input').attr('id')};

        if(list.length) {
            params['addDates'] = list;
        }

        $(item).find('div').multiDatesPicker(params);
        $(item).multiDatesPicker(params);
    });
});