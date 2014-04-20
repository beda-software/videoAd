$(document).ready(function(){
    $("#alt_id_datelist").each(function(index, item){
        var list = $(item).prev('input').data('dates') || [],
            params = {dateFormat: "yy-mm-dd", altField: '#'+$(item).prev('input').attr('id')};

        if(list.length) {
            params['addDates'] = list;
        }

        $(item).multiDatesPicker(params);
    });
});