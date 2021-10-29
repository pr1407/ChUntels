const login = new Vue({
    el:'#login',
    delimiters:['[[',']]'],
    data: {
        saludo:'Hola Mundo!',
        nombre:'',
    },
    methods: {
        async saludar(){

            let body = {
                nombre:this.nombre,
            }

            try{
                let result = await axios.post('api/login',body)

                let resultData = result.data

                if(resultData.valor==true){
                    window.location.href = 'index.html'
                }else{
                    alert('Usuario o contraseña incorrectos')
                }
            }catch(err){
                alert(err);
            }
            alert('saludo');
        }
    }
});