
function updateTimer() {
    var timerElement = document.getElementById('timer');
    var timerMsgElement = document.getElementById('timer_msg');
    var MsgDivElement = document.getElementById('msg_div');
    var currentTime = timerElement.innerHTML;
    var timeArray = currentTime.split(':');
    var minutes = parseInt(timeArray[0]);
    var seconds = parseInt(timeArray[1]);

    if (seconds === 0) {
        if (minutes === 0) {
            clearInterval(interval);
            MsgDivElement.style.backgroundColor = '#fda4af'
            timerMsgElement.innerText = 'OTP expired! please generate new one'
            timerMsgElement.style.color='#be123c'
            // alert("Timer expired!");
            return;
        }
        minutes--;
        seconds = 59;
    } else {
        seconds--;
    }

    seconds = seconds < 10 ? '0' + seconds : seconds;
    minutes = minutes < 10 ? '0' + minutes : minutes;

    timerElement.innerHTML = minutes + ':' + seconds;
}

var interval = setInterval(updateTimer, 1000);