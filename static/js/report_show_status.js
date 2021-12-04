
const URL = window.location.href.replace('check_progress', 'check_status')
var all_messages = document.querySelector('#all_messagess_counter')
var downloaded_messages = document.querySelector('#downloaded_messagess_counter')
var evaluated_messagess = document.querySelector('#evaluated_messagess_counter')

update_counters()
setInterval(update_counters_if_not_equal, 500)

function update_counters() {
    fetch(URL).then(response => {
        return response.json()
    }).then(response => {
        all_messages.innerHTML = response.all_messagess_counter
        downloaded_messages.innerHTML = response.downloaded_messagess_counter
        evaluated_messagess_counter.innerHTML = response.evaluated_messagess_counter
    }).catch(() => {
        console.error('ERROR')
    })
}

function update_counters_if_not_equal() {
    if (all_messages.innerHTML != evaluated_messagess.innerHTML) {
        update_counters()
    } else {
        show_ready_sign()
    }
}

var elem = document.querySelector("#myBar");
var start_width = document.querySelector("#counter-messages");
var end_with = all_messages.innerHTML;

setInterval(frame, 100);

function frame() {
    // Move progress bar
    var step = 100 / parseInt(all_messages.innerHTML);
    elem.style.width = parseInt(start_width.innerHTML) * step + "%";
    start_width.innerHTML = parseInt(evaluated_messagess.innerHTML);
}

function show_ready_sign() {
    document.querySelector('#ready_sign').removeAttribute('hidden')
}

