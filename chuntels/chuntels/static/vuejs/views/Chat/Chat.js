
navigator.getUserMedia = navigator.getUserMedia || navigator.webkitGetUserMedia || navigator.mozGetUserMedia;

navigator.getUserMedia({ video: true, audio: true }, function (stream) {
    // Set your video displays
    window.localStream = stream;
    var video = document.getElementById('my-video');
    if (typeof video.srcObject == "object") {
        video.srcObject = stream;
        //muteVideo(false);
        //muteAudio(false);

    } else {
        video.src = URL.createObjectURL(stream);
    }
}, function (err) {
    console.log("The following error occurred: " + err.name);
    //alert('Unable to call ' + err.name)
});


const chat = new Vue({
    el: '#chat',
    delimiters: ['[[', ']]'],
    data: {
        saludo: 'Hola Mundo!',
        friends: [],
        friend: '',
        message_send: '',
        messages: [],
        peer: '',
        peer_id: '',
        conn: '',
        theirStream: '',
        videoStatus: false,
        audioStatus: false,
        isChatSelect: false,
    },
    methods: {
        showFriendList() {
            $('#card-chat').addClass('d-none');
            $('#card-friends').removeClass('d-none');

            $('.list-group-item-action').removeClass('active');
            $('.mb-0.text-sm.text-white').removeClass('text-white');
        },/**/
        showChatFriend(friend) {
            this.isChatSelect = true;
            if ($('#card-chat').hasClass('d-none')) {
                $('#card-friends').addClass('d-none');
                $('#card-chat').removeClass('d-none');
            }
            $('#contacto-' + friend.nickname).removeClass('active');
            $('#contacto-name-' + friend.nickname).removeClass('text-white');
            $('#contacto-' + friend.nickname).addClass('active');
            $('#contacto-name-' + friend.nickname).addClass('text-white');
            this.friend = friend;

            this.getMessages();

            if (this.conn) {
                this.conn.close();
            }

            var userId = this.friend.nickname;
            let _this = this;

            if (this.friend.is_active) {
                this.conn = this.peer.connect(userId);
                if (this.conn) {
                    this.conn.on('open', function () {
                        console.log('Connected to ' + userId);
                    });
                    this.conn.on('data', function (data) {
                        console.log('Received: ' + data.user_id);
                        //$('#messages').append(`<li class="list-group-item"><span class="badge rounded-pill bg-primary p-2">${data}</span></li>`);
                        if(_this.friend.nickname == data.user_id){
                            _this.messages.push({ content: data.content, user_id: _this.friend.nickname, created_at: 'hace un momento' });
                            $("#scrollbar-chat").animate({ scrollTop: $('#scrollbar-chat')[0].scrollHeight }, 1000);
                        }
                    });
                    this.conn.on('close', function () {
                        console.log('Connection destroyed');
                    })
                    this.peer.on('error', function (err) {
                        console.log(err);
                    });
                }
            }

        },
        async listFriends() {
            let result = await axios.get('/api/get-friends/');

            if (result.data.valor) {
                this.friends = result.data.data;
                this.friend = this.friends[0].friend;
                //this.showChatFriend(this.friend)
            }
        },
        focusedInputMessage() {
            $('#input-group-message').addClass('focused');
        },
        blurInputMessage() {
            $('#input-group-message').removeClass('focused');
        },
        async sendMessage() {
            if (this.message_send.length > 0) {

                try {

                    const body = new FormData();

                    body.append('message', this.message_send);
                    body.append('friend', this.friend.iduser);

                    const response = await axios.post('/api/send-message/', body);
                    if (response.data.valor) {
                        //this.friend.messages.push(result.data.data);
                        $('#input-group-message').removeClass('focused');

                        if (this.conn && this.conn.open) {
                            this.conn.send({content:this.message_send, user_id:this.peer_id});
                            //$('#messages').append(`<li class="list-group-item d-flex justify-content-end"><span class="badge rounded-pill bg-success p-2">${message}</span></li>`);
                            this.messages.push({ content: this.message_send, user_id: this.peer_id, created_at: 'hace un momento' });
                            $("#scrollbar-chat").animate({ scrollTop: $('#scrollbar-chat')[0].scrollHeight }, 1000);
                        } else {
                            //alert('Ingresa un usario con quien hablar');
                        }

                        this.message_send = '';
                    }
                } catch (err) {
                    console.log(err);
                }

            }
        },
        async getMessages() {
            try {

                const body = new FormData();

                body.append('friend', this.friend.iduser);

                const response = await axios.post('/api/get-messages/', body);
                if (response.data.valor) {
                    this.messages = response.data.data;
                    setTimeout(() => {
                        $("#scrollbar-chat").animate({ scrollTop: $('#scrollbar-chat')[0].scrollHeight }, 1000);
                    }, 500);
                }
            } catch (err) {
                console.log(err);
            }
        },
        callFriend() {

            let _this = this;

            if (!this.friend.is_active) {
                return;
            }

            if (window.existingCall) {
                window.existingCall.close();
            }

            $('#modal-current-call').modal('show');

            console.log('llamando a ' + this.friend.nickname);

            let call = this.peer.call(this.friend.nickname, window.localStream);

            console.log(window.localStream);

            console.log(this.peer);
            console.log(call);

            window.call = call;

            call.on('stream', function (remoteStream) {
                _this.theirStream = remoteStream;
                $('#their-video').prop('srcObject', remoteStream);
            });

            call.on('close', function () {
                $('#modal-current-call').modal('hide');
                console.log('Call ended');
            });
        },
        initializePeer() {

            let _this = this;

            this.peer_id = $('#user-name').val();

            this.peer = new Peer(this.peer_id, {host: 'my-peer.herokuapp.com', port: 443, path: '/', secure: true});

            console.log(this.peer);

            this.peer.on('open', function (id) {
                console.log('My peer ID is: ' + id);
                //$('#user-name').val(id);
            });

            this.peer.on('connection', function (c) {
                _this.conn = c;
                _this.conn.on('data', function (data) {
                    console.log('Received: ' + data.user_id);
                    if(_this.friend.nickname == data.user_id){
                        _this.messages.push({ content: data.content, user_id: _this.friend.nickname, created_at: 'hace un momento' });
                        $("#scrollbar-chat").animate({ scrollTop: $('#scrollbar-chat')[0].scrollHeight }, 1000);
                    }
                });
            });

            this.peer.on('call', function (call) {
                $('#modal-call-advert').modal('show');

                window.call = call;

                call.on('close', function () {
                    $('#modal-current-call').modal('hide');
                    _this.endCall();
                });

            });

            this.peer.on('disconnected', function () {
                console.log('Connection lost. Please reconnect');

                // Workaround for peer.reconnect deleting previous id
                _this.peer.id = _this.peer_id;

                _this.peer.reconnect();
            });

            this.peer.on('close', function () {
                //_this.conn = null;
                console.log('Connection destroyed');
            });
        },
        aceptCall() {

            let _this = this;

            window.call.answer(window.localStream);
            window.call.on('stream', function (remoteStream) {
                _this.theirStream = remoteStream;
                $('#modal-call-advert').modal('hide');
                $('#modal-current-call').modal('show');
                $('#their-video').prop('srcObject', remoteStream);
            });
            window.call.on('close', function () {
                $('#modal-current-call').modal('hide');
                _this.endCall();
            });
        },
        rejectCall() {
            window.call.close();
            $('#modal-call-advert').modal('hide');
        },
        endCall() {

            if (this.theirStream) {
                this.theirStream.getAudioTracks()[0].enabled = false;
                this.theirStream.getVideoTracks()[0].enabled = false;
            }

            if (window.call) {
                window.call.close();
            }
        },
        muteAudio(status) {
            if (window.localStream) {
                var audioTracks = window.localStream.getAudioTracks()
                if (audioTracks && audioTracks[0]) {
                    audioTracks[0].enabled = status;
                }
            }
        },
        muteVideo(status) {
            if (window.localStream) {
                var videoTracks = window.localStream.getVideoTracks()
                if (videoTracks && videoTracks[0]) {
                    videoTracks[0].enabled = status;
                }
            }
        },
        muteAudioCall() {
            this.audioStatus = !this.audioStatus;
            this.muteAudio(!this.audioStatus);
            
            if($('#btn-mute-video').hasClass('btn-success')){
                $('#btn-mute-video').removeClass('btn-success');
                $('#btn-mute-video').addClass('btn-danger');
            }else{
                $('#btn-mute-video').removeClass('btn-danger');
                $('#btn-mute-video').addClass('btn-success');
            }
        },
        muteVideoCall() {
            this.videoStatus = !this.videoStatus;
            this.muteVideo(!this.videoStatus);

            if($('#btn-mute-audio').hasClass('btn-success')){
                $('#btn-mute-audio').removeClass('btn-success');
                $('#btn-mute-audio').addClass('btn-danger');
            }else{
                $('#btn-mute-audio').removeClass('btn-danger');
                $('#btn-mute-audio').addClass('btn-success');
            }
        }
    },
    mounted() {

        this.initializePeer();

        this.listFriends();
    },
    watch: {
    }
});

