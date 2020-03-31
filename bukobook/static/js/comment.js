function hideLayer(cls) {
    var obj = document.getElementsByClassName(cls);
    for (var i = 0; i < obj.length; i++) {
        obj[i].style.display = "none";
    }
}

function showLayer(id) {
    var obj = document.querySelector("form[data-id='"+id +"']");
    obj.style.display = "block";
}

function setReplyCookie(id, reply_to) {
    document.cookie = "reply_to=" + reply_to + ";" + "path=/reply/";
    document.cookie = "floor=" + id + ";" + "path=/reply/";
    var obj = document.querySelector("form[data-id='"+id +"']").querySelector('.reply-box');
    if (reply_to)
        obj.placeholder = '@' + reply_to + ':';
    else obj.placeholder = '请自觉遵守互联网相关的政策法规，严禁发布色情、暴力、反动的言论。'
}

function ReplyButtonAction(id, reply_to) {
    hideLayer('reply');
    showLayer(id);
    setReplyCookie(id, reply_to);
    Roll(".reply[data-id='"+ id +"']");
}

window.onscroll = function () {
    sessionStorage.setItem('scroll', window.pageYOffset||document.documentElement.scrollTop);
};

window.onload = function () {
    scroll = sessionStorage.getItem('scroll');
    window.scrollTo({top: scroll});
};

