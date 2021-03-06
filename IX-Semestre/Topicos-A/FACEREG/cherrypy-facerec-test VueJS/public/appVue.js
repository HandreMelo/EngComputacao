new Vue({
  el: '#app',
  vuetify: new Vuetify(),
  data: () => ({
    dialog: false,
    search: false,
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
    face: '',
    lastUser: '',
  }),

  computed: {
    formTitle () {
      return this.editedIndex === -1 ? 'Novo Cadastro' : 'Editar pessoa'
    },
  },

  watch: {
    dialog (val) {
      val || this.close()
    },
    search (val) {
      val || this.close()
    },
  },

  created () {
    this.initialize()
  },

  methods: {

    initialize () {

      if(this.persons.length > 0) {
        this.persons.splice(0, this.persons.length);
      }

      if (!firebase.apps.length) {
        firebase.initializeApp(this.config);
      }

      const dbRef = firebase.database().ref();
      const usersRef = dbRef.child('phelipe');
      
      usersRef.on("value", snap => {

        snap.forEach(childSnap => {

          let key = childSnap.key;
          let value = childSnap.val();

          this.persons.push({
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
      confirm('Você tem certeza que deseja deletar este item?') && userRef.remove()
                                     && this.persons.splice(0, this.persons.length)
                                     && this.deletePhotoPerson(userId);
      this.initialize();
    },

    close () {
      this.clearData();
      this.dialog = false
      this.search = false
      document.getElementById('face-file').src = "/static/Person.jpg";
      this.initialize();
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
        this.clearData();
        this.persons.splice(0, this.persons.length);
        this.close();

      } else {
        const dbRef = firebase.database().ref();
        const userRef = dbRef.child('phelipe');
        var newUser = {};

        newUser['nome'] = this.editedItem.nome;
        newUser['email'] = this.editedItem.email;
        newUser['telefone'] = this.editedItem.telefone;
        newUser['photo'] = btoa(newUser['photo']);
        this.persons.splice(0, this.persons.length);

        userRef.push(newUser).then(pushed => {
          this.lastUser = pushed.key;
          if(this.face != ''){
            this.sendToPy('cadastrar',this.lastUser,this.face)
          } else {
            this.face = '';
            this.clearData();
            this.close();
          }   
        });
      }
      
    },

    processFile(event){
      var file = event.target.files[0];

      document.getElementById('face-file').src = URL.createObjectURL(file);
      this.face = file;
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
      xhr.onload = function(e) {
        this.face = ''
        this.lastUser = ''
      }
	    this.close()
    },

    deletePhotoPerson(uname){
      xhr = new XMLHttpRequest();
      xhr.open('POST','/deletar',true);
      xhr.send(uname);
      xhr.onload = function(e) {
        alert(xhr.response);
      }
    },

    searchPerson(){

      var formData = new FormData()
      formData.append('ufile', this.face)
  
      xhr = new XMLHttpRequest();
  
      xhr.open('POST', '/procurar',true)
      xhr.send()
      xhr.onload = function(e) {
        document.querySelector('#searchResult').innerHTML = xhr.response;
      }
      document.querySelector('#searchResult').style.display = "block";
    },

    clearData(){
      this.editedItem.nome = '';
      this.editedItem.email = '';
      this.editedItem.telefone = '';
      this.face = '';
      document.querySelector('#face-file').src = "/static/Person.jpg";

    },
  },
})
