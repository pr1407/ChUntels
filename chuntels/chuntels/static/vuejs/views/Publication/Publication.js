const home = new Vue({
    el: '#publication',
    delimiters: ['[[', ']]'],
    data: {
        saludo: 'Hola Mundo!',
        comment: '',
        comments: [],
    },
    methods: {
        async sendComment(idpost) {
            console.log(idpost);

            try {
                let formData = new FormData();
                formData.append('idpublication', idpost);
                formData.append('coment', this.comment);

                let response = await axios.post('/api/coment-publication/', formData);
                if (response.data.valor) {
                    this.comment = '';
                    this.getComments(idpost);
                }
                console.log(response.data);
                Swal.mixin({
                    toast: true,
                    showConfirmButton: false,
                    text: response.data.mensaje,
                })

            } catch (err) {
                console.log(err);
            }
        },
        async getComments(idpost) {
            try {
                let formData = new FormData();
                formData.append('idpost', idpost);
                let response = await axios.post('/api/get-publication-coments/', formData);
                if (response.data.valor) {
                    this.comments = response.data.data;
                }

            } catch (err) {
                console.log(err);
            }
        }
    },
    mounted() {
        let URLactual = window.location.pathname;
        let id = URLactual.split('/')[2];
        this.getComments(id);
    }
});