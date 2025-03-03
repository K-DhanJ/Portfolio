let test = document.querySelectorAll('.slider .card ');
let active = 3;
function loadShow(){
    test[active].style.transform = `none`;
    test[active].style.zIndex = 1;
    test[active].style.filter = 'none';
    test[active].style.opacity = 1;
    // show after
    let stt = 0;
    for(var i = active + 1; i < test.length; i ++){
        stt++;
        test[i].style.transform = `translateX(${120*stt}px) scale(${1 - 0.2*stt}) perspective(16px) rotateY(-1deg)`;
        test[i].style.zIndex = -stt;
        test[i].style.filter = 'blur(5px)';
        test[i].style.opacity = stt > 2 ? 0 : 0.6;
    }
     stt = 0;
    for(var i = (active - 1); i >= 0; i --){
        stt++;
        test[i].style.transform = `translateX(${-120*stt}px) scale(${1 - 0.2*stt}) perspective(16px) rotateY(1deg)`;
        test[i].style.zIndex = -stt;
        test[i].style.filter = 'blur(5px)';
        test[i].style.opacity = stt > 2 ? 0 : 0.6;
    }
}
loadShow();
let next = document.getElementById('next');
let prev = document.getElementById('prev');
next.onclick = function(){
   active = active + 1 < test.length ?  active + 1 : active;
   loadShow();
}
prev.onclick = function(){
    active = active - 1 >= 0 ? active -1 : active;
    loadShow();
}