const perfilFriend = new Vue({
  el: '#perfil-friend',
  delimiters: ['[[', ']]'],
  data: {
    saludo: 'Hola Mundo!',
    publicationlist: [],
    statusFriendRequest: 0,
  },
  methods: {
    friendRequest(name,idfriend,iduser) {
      console.log(idfriend,'idfriend')
      console.log(iduser,'iduser')

      if (this.statusFriendRequest===0) {
        const swalWithBootstrapButtons = Swal.mixin({
          customClass: {
            confirmButton: 'btn btn-success',
            cancelButton: 'btn btn-danger'
          },
          buttonsStyling: false
        })

        swalWithBootstrapButtons.fire({
          title: '¿Estás seguro de enviar solicitud a '+name+'?',
          text: "",
          icon: 'question',
          showCancelButton: true,
          confirmButtonText: 'Enviar',
          cancelButtonText: 'No',
          reverseButtons: true
        }).then((result) => {
          if (result.isConfirmed) {
            this.statusFriendRequest = 1;

            swalWithBootstrapButtons.fire(
              'Solicitud enviada!',
              'Se te notificará cuando tu solicitud de amistad sea contestada.',
              'success'
            )
          }
        })
      }else if(this.statusFriendRequest === 1){
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
        }).then((result) => {
          if (result.isConfirmed) {
            this.statusFriendRequest = 0;

            swalWithBootstrapButtons.fire(
              'Solicitud cancelada!',
              '',
              'success'
            )
          }
        })
      }else{
        const swalWithBootstrapButtons = Swal.mixin({
          customClass: {
            confirmButton: 'btn btn-success',
            cancelButton: 'btn btn-danger'
          },
          buttonsStyling: false
        })

        swalWithBootstrapButtons.fire({
          title: '¿Estás seguro de dejar de ser amigo de '+name+'?',
          text: "",
          icon: 'warning',
          showCancelButton: true,
          confirmButtonText: 'Si',
          cancelButtonText: 'No',
          reverseButtons: true
        }).then((result) => {
          if (result.isConfirmed) {
            this.statusFriendRequest = 0;

            swalWithBootstrapButtons.fire(
              'Dejaste de ser amigo de '+name+'!',
              '',
              'success'
            )
          }
        })
      }
    }
  },
  watch: {
  }
});