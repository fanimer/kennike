function Roll(id, behavior="smooth") {
    var top = document.querySelector(id).getBoundingClientRect().top;
    var position = window.pageYOffset - 350;
    window.scrollTo({top:position+top, behavior: behavior})
}

