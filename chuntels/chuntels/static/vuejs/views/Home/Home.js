/*Dropzone.options.myDropzone = {
    addRemoveLinks: true,
    // Configuration options go here
};*/
Dropzone.autoDiscover = false;
$(document).ready(function(e) {
    const filesdropzone = $("#publish-dropzone").dropzone( {
        url: "/api/file-upload/",
        addRemoveLinks: true,
        success: function (file, response) {
            var imgName = response.data;
            file.previewElement.classList.add("dz-success");
            console.log(imgName);
            if(imgName.type == "file") {
                $('#file-name').val(imgName.url);
            }else{
                $('#photo-name').val(imgName.url);
            }
        },
        error: function (file, response) {
            file.previewElement.classList.add("dz-error");
        }
    });

    $("#publicarmodal").on('hidden.bs.modal', function (e) {
        console.log("removed all files");
        filesdropzone[0].dropzone.removeAllFiles( true );
    });
})

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
        async deletePublish(publication) {
            console.log(publication)
            try {
                let formData = new FormData();
                
                formData.append('idPublication', publication.idpost);

                const response = await axios.post(`/api/delete-publication/`,formData);
                if (response.status === 200) {
                    let responseData = response.data
                    if (responseData.valor) {
                        Swal.fire({
                            icon: 'success',
                            title: 'Publicación enviada',
                            text: responseData.mensaje
                        })
                        await this.getPublications()
                    } else {
                        Swal.fire({
                            icon: 'error',
                            title: 'Ocurrio un error',
                            text: responseData.mensaje
                        })
                    }
                }
            }catch(e){
                console.log(e)
            }
        },
        async sendPublish(iduser) {
            try {
                let formData = new FormData();

                formData.append('publication', this.publish);
                formData.append('user', iduser);
                formData.append('photo', $('#photo-name').val());
                formData.append('files', $('#file-name').val());
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
                        for (let key in this.publicationlist) {
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
            } catch (err) {
                console.log(err)
                Swal.fire({
                    icon: 'error',
                    title: 'Ocurrio un error',
                    text: 'Recargue y vuelva a intentarlo'
                })
            }
        },
        async sendLike(publication) {
            if (!$('#btn-like').hasClass('active')) {
                console.log(publication)
                $('#btn-like-'+publication.idpost).addClass('active')
                try {
                    let formData = new FormData();
                    formData.append('idpublication', publication.idpost);
                    const result = await axios.post('/api/send-likes-post/', formData);
                    if (result.status === 200) {
                        let responseData = result.data
                        if (responseData.valor) {
                            Swal.fire({
                                icon: 'success',
                                title: 'Like enviado',
                                text: responseData.mensaje
                            })
                            await this.getPublications()
                        } else {
                            Swal.fire({
                                icon: 'error',
                                title: 'Ocurrio un error',
                                text: responseData.mensaje
                            })
                        }
                    }
                }catch(err) {
                    console.log(err)
                }
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