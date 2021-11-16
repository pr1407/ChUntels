const perfilFriend = new Vue({
  el: '#perfil-friend',
  delimiters: ['[[', ']]'],
  data: {
    saludo: 'Hola Mundo!',
    publicationlist: [],
    statusFriendRequest: 0,
  },
  methods: {
    async getPublications() {

      let URLactual = window.location.pathname;
      let friend = URLactual.split('/')[2];
      try {
        let formData = new FormData();
        formData.append('user', friend);

        let response = await axios.post('/api/get-publication/',formData);

        if (response.data.valor) {
          this.publicationlist = response.data.data;
        }

      } catch (err) {
        console.log(err);
      }

    },
    async friendRequest(name, idfriend, iduser) {
      console.log(idfriend, 'idfriend')
      console.log(iduser, 'iduser')

      if (this.statusFriendRequest === 0) {
        const swalWithBootstrapButtons = Swal.mixin({
          customClass: {
            confirmButton: 'btn btn-success',
            cancelButton: 'btn btn-danger'
          },
          buttonsStyling: false
        })

        swalWithBootstrapButtons.fire({
          title: '¿Estás seguro de enviar solicitud a ' + name + '?',
          text: "",
          icon: 'question',
          showCancelButton: true,
          confirmButtonText: 'Enviar',
          cancelButtonText: 'No',
          reverseButtons: true
        }).then(async (result) => {
          if (result.isConfirmed) {
            this.statusFriendRequest = 1;

            let formData = new FormData();
            formData.append('user', iduser);
            formData.append('friend', idfriend);
            formData.append('state', this.statusFriendRequest.toString());

            let response = await axios.post('/api/send-friend-request/', formData);

            if (response.data.valor) {
              swalWithBootstrapButtons.fire(
                'Solicitud enviada!',
                'Se te notificará cuando tu solicitud de amistad sea contestada.',
                'success'
              )
            } else {
              swalWithBootstrapButtons.fire(
                'Ocurrio un error',
                response.data.mensaje,
                'error'
              )
            }
          }
        })
      } else if (this.statusFriendRequest === 1) {
        const swalWithBootstrapButtons = Swal.mixin({
          customClass: {
            confirmButton: 'btn btn-success',
            cancelButton: 'btn btn-danger'
          },
          buttonsStyling: false
        })

        swalWithBootstrapButtons.fire({
          title: '¿Estás seguro de cancelar la solicitud de amistad?',
          text: "",
          icon: 'warning',
          showCancelButton: true,
          confirmButtonText: 'Cancelar',
          cancelButtonText: 'No',
          reverseButtons: true
        }).then(async (result) => {
          if (result.isConfirmed) {
            this.statusFriendRequest = 0;

            let formData = new FormData();
            formData.append('user', iduser);
            formData.append('friend', idfriend);
            formData.append('state', this.statusFriendRequest.toString());

            let response = await axios.post('/api/send-friend-request/', formData);

            if (response.data.valor) {
              swalWithBootstrapButtons.fire(
                'Solicitud cancelada!',
                '',
                'success'
              )
            } else {
              swalWithBootstrapButtons.fire(
                'Ocurrio un error',
                response.data.mensaje,
                'success'
              )
            }
          }
        })
      } else {
        const swalWithBootstrapButtons = Swal.mixin({
          customClass: {
            confirmButton: 'btn btn-success',
            cancelButton: 'btn btn-danger'
          },
          buttonsStyling: false
        })

        swalWithBootstrapButtons.fire({
          title: '¿Estás seguro de dejar de ser amigo de ' + name + '?',
          text: "",
          icon: 'warning',
          showCancelButton: true,
          confirmButtonText: 'Si',
          cancelButtonText: 'No',
          reverseButtons: true
        }).then(async (result) => {
          if (result.isConfirmed) {
            this.statusFriendRequest = 3;

            let formData = new FormData();
            formData.append('user', iduser);
            formData.append('friend', idfriend);
            formData.append('state', this.statusFriendRequest.toString());

            let response = await axios.post('/api/send-friend-request/', formData);

            if (response.data.valor) {
              swalWithBootstrapButtons.fire(
                'Dejaste de ser amigo de ' + name + '!',
                '',
                'success'
              )
            } else {
              swalWithBootstrapButtons.fire(
                'Ocurrio un error',
                response.data.mensaje,
                'error'
              )
            }
          }
        })
      }
    }
  },
  mounted() {
    this.getPublications()
  },
  watch: {
  }
});