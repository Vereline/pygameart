var text_box_send = '<li class="left clearfix">\n' +
    '<span class="chat-img float-left">\n' +
    '<img src="{% static \'user-default.png\' %}" alt="User Avatar" class="rounded-circle " />\n' +
    '</span>\n' +
    '<div class="chat-body clearfix">\n' +
    '<div class="header">\n' +
    '<strong class="primary-font">{sender}</strong>\n' +
    '<small class="float-right text-muted">{timestamp}</small>\n' +
    '</div>\n' +
    '<p class="float-left">{message}</p>\n' +
    '</div>\n' +
    '</li>';

var text_box_receive = '<li class="right clearfix">\n' +
    '<span class="chat-img float-right">\n' + //TODO: fix images, which are not displayed``
    '<img src="{% static \'user-default.png\' %}" alt="User Avatar" class="rounded-circle " />\n' +
    '</span>\n' +
    '<div class="chat-body clearfix">\n' +
    '<div class="header">\n' +
    '<strong class="primary-font float-right">{sender}</strong>\n' +
    '<small class="text-muted">{timestamp}</small>\n' +
    '</div>\n' +
    '<p class="float-right">{message}</p>\n' +
    '</div>\n' +
    '</li>';

function scrolltoend() {
    $('#board').stop().animate({
        scrollTop: $('#board')[0].scrollHeight
    }, 800);
}

function send(sender, receiver, message) {
    $.post('/chat/api/messages', '{"sender": "'+ sender +'", "receiver": "'+ receiver +'","message": "'+ message +'" }', function (data) {
        console.log(data);
        let box = text_box_send.replace('{sender}', "You");
        box = box.replace('{message}', message);
        let date_now = Date(); // TODO: change date format to be shown correctly
        box = box.replace('{timestamp}', date_now);
        $('#board').append(box);
        scrolltoend();
    })
}

function receive() {
    $.get('/chat/api/messages/'+ sender_id + '/' + receiver_id, function (data) {
        console.log(data);
        if (data.length !== 0)
        {
            for(let i=0;i<data.length;i++) {
                console.log(data[i]);
                let box = text_box_receive.replace('{sender}', data[i].sender);
                box = box.replace('{message}', data[i].message);
                box = box.replace('{timestamp}', data[i].timestamp);
                $('#board').append(box);
                scrolltoend();
            }
        }
    })
}
