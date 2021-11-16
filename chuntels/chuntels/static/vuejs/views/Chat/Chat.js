const chat = new Vue({
    el:'#chat',
    delimiters:['[[',']]'],
    data: {
        saludo:'Hola Mundo!',
        friends:[],
        friend:''
    },
    methods: {
        showFriendList(){
            $('#card-chat').addClass('d-none');
            $('#card-friends').removeClass('d-none');
        },
        showChatFriend(friend){
            if($('#card-chat').hasClass('d-none')){
                $('#card-friends').addClass('d-none');
                $('#card-chat').removeClass('d-none');
            }
            this.friend = friend;
        },
        async listFriends(){
            let result = await axios.get('/api/get-friends/');
            
            if(result.data.valor){
                this.friends = result.data.data;
                this.friend = this.friends[0];
            }
        }
    },
    mounted(){
        this.listFriends();
    },
    watch: {
    }
});