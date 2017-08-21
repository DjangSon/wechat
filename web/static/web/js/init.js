function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function getData(table, objTable){
    $(table).on('click','tr',function(){
        if ($(this).hasClass('selected')){
            tempData = objTable.row(this).data();
            // console.log(tempData);
        } else {
            tempData = undefined;
        }
    });
}

//提示选中数据
function tipsSel(){
    layer.alert('请选择数据', {
        skin: 'layui-layer-lan',
        closeBtn: 0
    });
}