
var idleTime = 0;
var modalBtn = document.getElementById('modalBtn')
var worktimer = 0;
var eventForm = document.getElementById('menuform');
var eventSubmit = document.getElementById('entryLogBtn')
var secondsInput = document.createElement('input');
var tokenInput = document.createElement('input');
var workTimerThreshold = 30; //seconds
var logOutThreshold = 120; //seconds
secondsInput.type = "hidden";
tokenInput.type="hidden";



$(document).ready(function () {

    checkModal( function (pause) {
        if ( pause ) {
            idleTime = idleTime + workTimerThreshold;
        }
    });

    var timeInterval = setInterval(function () { checkModal(timerIncrement); }, 1000);

    $(this).mousemove( function (e) {
        checkModal(resetIdle);
    });

    $(this).keypress( function (e) {
        checkModal(resetIdle);
    });

    $(eventForm).on('submit', function () {
        secondsInput.name = "seconds"
        secondsInput.value = worktimer
        tokenInput.name = "token"
        tokenInput.value = generateUid()
        eventForm.appendChild(secondsInput)
        eventForm.appendChild(tokenInput)
    });

});

function checkModal( callback ) {
    var classes = document.getElementById('myModal').classList;
    var pause = 0;
    for (var i = 0; i < classes.length; i++){
        if (classes[i]  == "in") {
            var pause = 1
        }
    }
    callback(pause);
}

function resetIdle( pause ) {
    if (!pause){
        idleTime = 0;
    }
};

function timerIncrement( pause ) {
    if (!pause){
        if (idleTime >= workTimerThreshold) {
            eventSubmit.click()
        } else {
            worktimer = worktimer + 1;
        }
    }
    idleTime = idleTime + 1;

    document.getElementById('idleTime').innerHTML = idleTime;
    document.getElementById("workTime").innerHTML = worktimer;
    if (idleTime > logOutThreshold) {
        window.location.href = ('/logout')
    }
};

var generateUid = function (separator) {
    var delim = separator || "-";

    function S4 () {
        return(((1 + Math.random()) * 0x10000 ) | 0).toString(16).substring(1);
    }

    return (S4() + S4() + delim + S4() + delim + S4() + delim + S4() + delim + S4() + S4() + S4());
};
