const home = new Vue({
    el:'#home',
    delimiters:['[[',']]'],
    data: {
        saludo:'Hola Mundo!'
    },
    methods:{
        async responce(){

            const result = await axios.get('/api/saludo')


            console.log(result)
        }
    }
});