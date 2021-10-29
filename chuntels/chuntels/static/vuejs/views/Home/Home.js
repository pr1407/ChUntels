const home = new Vue({
    el:'#home',
    delimiters:['[[',']]'],
    data: {
        saludo:'jsjasja!'
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

        }
    }
});