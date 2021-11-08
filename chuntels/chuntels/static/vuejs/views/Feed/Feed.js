const feed = new Vue({
    el:'#feed',
    delimiters:['[[',']]'],
    data: {
        saludo:'Hola Mundo!',
        publish: '',
        publicationlist: [],
    },
    methods: {
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