const chat = new Vue({
    el:'#chat',
    delimiters:['[[',']]'],
    data: {
        saludo:'Hola Mundo!',
    },
    methods: {
        showFriendList(){
            $('#card-chat').addClass('d-none');
            $('#card-friends').removeClass('d-none');
        },
        showChatFriend(){
            if($('#card-chat').hasClass('d-none')){
                $('#card-friends').addClass('d-none');
                $('#card-chat').removeClass('d-none');
            }
        },
    },
    mounted(){
    },
    watch: {
    }
});