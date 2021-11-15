const navbar = new Vue({
    el:'#navbar',
    delimiters:['[[',']]'],
    data: {
        saludo:'Hola Mundo!',
        inputsearch:"",
        personas: [],
        personasFiltradas: [],
        notifications: []
    },
    methods:{
        async seeNotifications(){
            console.log('tas clickeando')
            if(this.notifications.length > 0){
                return;
            }

            try{
                let response = await axios.get('/api/get-notifications/')
                
                let responseData = response.data;
                if(responseData.valor){
                    this.notifications = responseData.data
                }
            }
            catch(err){
                Swal.fire({
                    icon: 'error',
                    title: 'Oops...',
                    text: 'Algo salió mal, intentelo de nuevo!'
                  })
            }

        },
        search(){
            console.log(this.inputsearch);
        },
        async searchPerson(){

            let body = new FormData();

            body.append('nombre',this.inputsearch);

            try {

                let result = await axios.post('/api/search-person/',body);

                if(result.status === 200){
                    let resultData = result.data;
                    if(resultData.valor){
                        this.personas = resultData.data;
                        this.personasFiltradas = resultData.data;
                    }else{
                        this.personas = [];
                    }
                }

            }catch(err){
                Swal.fire({
                    icon: 'error',
                    title: 'Oops...',
                    text: 'Algo salió mal, intentelo de nuevo!'
                  })
            }

        }
    },
    watch:{
        inputsearch(val){
            if(val.length === 1){
                if(this.personasFiltradas.length === 0){
                    this.searchPerson();
                }
            }else if(val.length > 1){
                this.personasFiltradas = [];
                let nombres;

                for(let i = 0; i < this.personas.length; i++){
                    nombres = this.personas[i].name.toLowerCase();
                    if(nombres.includes(val.toLowerCase())){
                        this.personasFiltradas.push(this.personas[i]);
                    }
                }
            }else{
                this.personasFiltradas = [];
            }
        },
        personasFiltradas(val){
            if(val.length > 0){
                $('#dropdown-search-person').addClass('show');
            }else{
                $('#dropdown-search-person').removeClass('show');
            }
        }
    },
    mounted(){
        this.seeNotifications()
    }
});