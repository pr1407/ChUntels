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

const feed = new Vue({
    el:'#feed',
    delimiters:['[[',']]'],
    data: {
        saludo:'Hola Mundo!',
        publish: '',
        publicationlist: [],
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
                            toast: true,
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
                const result = await axios.get('/api/get-friends-publications/');
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