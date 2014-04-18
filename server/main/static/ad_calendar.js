$(document).ready(function(){
    $("#alt_id_datelist").each(function(index, item){
        var list = $(item).find('input').data('dates') || [],
            params = {dateFormat: "yy-mm-dd", altField: '#'+$(item).prev('input').attr('id')};

        if(list.length) {
            params['addDates'] = list;
        }

        $(item).find('div').multiDatesPicker(params);
        $(item).multiDatesPicker(params);
    });
});