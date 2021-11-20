const home = new Vue({
    el: '#home',
    delimiters: ['[[', ']]'],
    data: {
        saludo: 'Hola!',
        publish: '',
        publicationlist: [],
        photo: '',
        file: ''
    },
    methods: {
        async sendPublish(iduser) {
            try {
                let formData = new FormData();

                formData.append('publication', this.publish);
                formData.append('user', iduser);
                formData.append('photo', this.photo);
                formData.append('files', this.file);
                formData.append('typePost', 1);

                const result = await axios.post('/api/send-publication/', formData);
                if (result.status === 200) {
                    let responseData = result.data
                    if (responseData.valor) {
                        //console.log(responseData.data)
                        Swal.fire({
                            icon: 'success',
                            title: 'Publicación enviada',
                            text: responseData.mensaje
                        })
                        await this.getPublications()
                    } else {
                        //console.log(responseData.msn)
                        Swal.fire({
                            icon: 'error',
                            title: 'Ocurrio un error',
                            text: responseData.mensaje
                        })
                    }
                }
            } catch (err) {
                Swal.fire({
                    icon: 'error',
                    title: 'Ocurrio un error',
                    text: 'Recargue y vuelva a intentarlo'
                })
            }

            $('#publicarmodal').modal('hide')
            this.publish = ''

        },
        async getPublications() {
            try {
                const result = await axios.get('/api/get-publication/');
                if (result.status === 200) {
                    let responseData = result.data
                    if (responseData.valor) {
                        this.publicationlist = responseData.data
                        for(let key in this.publicationlist) {
                            moment.locale('es')
                            let fecha = moment(this.publicationlist[key].created_at)
                            moment.locale('es')
                            this.publicationlist[key].created_at = fecha.fromNow();

                        }
                    } else {
                        console.log(responseData.mensaje)
                        Swal.fire({
                            icon: 'error',
                            title: 'Ocurrio un error',
                            text: responseData.mensaje
                        })
                    }
                }
            }catch(err){
                console.log(err)
                Swal.fire({
                    icon: 'error',
                    title: 'Ocurrio un error',
                    text: 'Recargue y vuelva a intentarlo'
                })
            }
        },
        async sendLike(index) {
            if (!$('#btn-like').hasClass('active')) {
                this.publicationlist[index].likes = (parseInt(this.publicationlist[index].likes) + 1).toString()
                $('#btn-like').addClass('active')
            }
        }
    },
    mounted() {
        this.getPublications()
    },
    watch: {
        publish: function (val) {
            if (val.length > 0) {
                $('#btn-publish').prop('disabled', false)
            } else {
                $('#btn-publish').prop('disabled', true)
            }
        }
    }
});