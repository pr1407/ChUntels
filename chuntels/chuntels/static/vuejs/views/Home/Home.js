const home = new Vue({
    el:'#home',
    delimiters:['[[',']]'],
    data: {
        saludo:'jsjasja!',
        publish: '',
        publicationlist: [],
    },
    methods:{
        async responce(){

            const result = await axios.get('/api/saludo/');
            
            if(result.status === 200){
                let responseData = result.data

                if(responseData.valor){
                    console.log(responseData.data)
                }else{
                    console.log(responseData.msn)
                }
            }

        },
        async sendPublish(){
            /*const result = await axios.post('/api/publish/',{
                publish: this.publish
            });
            if(result.status === 200){
                let responseData = result.data
                if(responseData.valor){
                    console.log(responseData.data)
                }else{
                    console.log(responseData.msn)
                }
            }*/

            $('#publicarmodal').modal('hide')
            this.publicationlist.unshift({
                id: this.publicationlist.length + 1,
                user: 'Juan',
                publication: this.publish,
                date: 'hace un momento',
                likes:'0',
                comments:'0',
                shareds:'0'
            })
            this.publish = ''

        },
        async getPublications(){
            /*const result = await axios.get('/api/publications/');
            if(result.status === 200){
                let responseData = result.data
                if(responseData.valor){
                    this.publicationlist = responseData.data
                }else{
                    console.log(responseData.msn)
                }
            }*/
            /*this.publicationlist.push({
                id: 1,
                user: 'Juan',
                publication: 'Hola mundo',
                date: 'hace 2 horas',
                likes:'2',
                comments:'1',
                shareds:'0'
            })*/
        },
        async sendLike(index){
            if(!$('#btn-like').hasClass('active')){
                this.publicationlist[index].likes = (parseInt(this.publicationlist[index].likes) + 1).toString()
                $('#btn-like').addClass('active')
            }
        }
    },
    mounted(){
        this.getPublications()
    },
    watch: {
        publish: function(val){
            if(val.length > 0){
                $('#btn-publish').prop('disabled', false)
            }else{
                $('#btn-publish').prop('disabled', true)
            }
        }
    }
});