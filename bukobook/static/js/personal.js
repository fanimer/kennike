window.onload = function() {
    var attention = document.getElementById('attention');
    attention.onclick = function() {
      attention.nextSibling.nextSibling.value += 1;
    };
};

