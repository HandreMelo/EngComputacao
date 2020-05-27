new Vue({
  el: '#app',
  vuetify: new Vuetify(),
  data: () => ({
    dialog: false,
    headers: [
      {
        text: 'Nome',
        align: 'start',
        sortable: false,
        value: 'nome',
      },
      { image: 'Photo', value: 'photo'},
      { text: 'Email', value: 'email' },
      { text: 'Telefone', value: 'telefone' },
      { text: 'Actions', value: 'actions', sortable: false },
    ],
    persons: [],
    editedIndex: -1,
    config: {
      apiKey: "AIzaSyDXgjRZ2H1QnGpnMoDEN9TOTXxbYL-Pb1Q",
      authDomain: "facerec-d9fa1.firebaseapp.com",
      databaseURL: "https://facerec-d9fa1.firebaseio.com",
      projectId: "facerec-d9fa1",
      storageBucket: "facerec-d9fa1.appspot.com",
      messagingSenderId: "1061417028783",
      appId: "1:1061417028783:web:3ec6e7c2762137b0b2585a"
    },
    editedItem: {
      key: '',
      photo: '',
      nome: '',
      email: '',
      telefone: 0,
    },
    defaultItem: {
      nome: '',
      photo: '',
      email: '',
      telefone: 0,
    },
  }),

  computed: {
    formTitle () {
      return this.editedIndex === -1 ? 'New Item' : 'Edit Item'
    },
  },

  watch: {
    dialog (val) {
      val || this.close()
    },
  },

  created () {
    this.initialize()
  },

  methods: {

    initialize () {
      if(this.persons.length>0){
        this.persons.splice(0, this.person.length-1)
      } 
      var refPerson = this.persons;
      var lastUser = ''

      firebase.initializeApp(this.config);

      // Firebase Database Reference and the child
      const dbRef = firebase.database().ref();
      const usersRef = dbRef.child('phelipe');
      
      usersRef.on("value", snap => {

        snap.forEach(childSnap => {

          let key = childSnap.key;
          let value = childSnap.val();

          refPerson.push({
            key: key,
            nome: value.nome, 
            email: value.email, 
            telefone: value.telefone,
          });
        });
      });

    },

    editItem (item) {
      this.editedIndex = this.persons.indexOf(item)
      this.editedItem = Object.assign({}, item)
      this.dialog = true
    },

    deleteItem (item) {
      const index = this.persons.indexOf(item)
      const dbRef = firebase.database().ref();
      var userId = item.key;
      const userRef = dbRef.child('phelipe/' + userId);
      confirm('Você tem certeza que deseja deletar este item?') && userRef.remove();
    },

    close () {
      this.dialog = false
  //    this.$nextTick(() => {
  //      this.editedItem = Object.assign({}, this.defaultItem)
  //      this.editedIndex = -1
  //    })
    },

    save () {
      if (this.editedIndex > -1) {
        const dbRef = firebase.database().ref();
        var userID = this.editedItem.key;
        const userRef = dbRef.child('phelipe/' + userID);
        var editedUserObject = {};

        editedUserObject['nome'] = this.editedItem.nome;
        editedUserObject['email'] = this.editedItem.email;
        editedUserObject['telefone'] = this.editedItem.telefone;

        userRef.update(editedUserObject);

      } else {
        const dbRef = firebase.database().ref();
        const userRef = dbRef.child('phelipe');
        var newUser = {};

        newUser['nome'] = this.editedItem.nome;
        newUser['email'] = this.editedItem.email;
        newUser['telefone'] = this.editedItem.telefone;
        userRef.push(newUser);
      }
      this.close()
    },

    processFile(event){
      var file = event.target.files[0]; 

      document.getElementById('face-file').src = URL.createObjectURL(file);
    },

    sendToPy(crud, userId, file){
      var formData = new FormData();
    
      xhr = new XMLHttpRequest();
	    xhr.open('POST', '/'+crud,true);
      if(crud == 'atualizar' || crud == 'cadastrar') {
        formData.append('ufile', file);
      }
      formData.append('uname', userId);
      xhr.send(formData);

	    this.close();
    },
  },
})