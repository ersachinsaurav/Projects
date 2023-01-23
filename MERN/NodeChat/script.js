const socket = io();

const userName = window.prompt('Please Enter Your Name:');
$('#userName').val(userName);

$(() => {
	$('#send').click(() => {
		let objMsg = { name: userName, msg: $('#message').val() };
		postMessage(objMsg);
	});
	getMessages();
});

socket.on('newMsg', () => {});

socket.on('newMsg', addMessage);

function addMessage(objMsg) {
	$('#messages').append(`<h4>${objMsg.name}</h4> <p>${objMsg.msg}`);
}

function getMessages() {
	$.get('http://127.0.0.1:777/messages', (objMessages) => {
		objMessages.forEach(addMessage);
	});
}

function postMessage(objMsg) {
	$.post('http://127.0.0.1:777/messages', objMsg);
}
