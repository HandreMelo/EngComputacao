var lastUser = ''
var config = {
    apiKey: "AIzaSyDXgjRZ2H1QnGpnMoDEN9TOTXxbYL-Pb1Q",
    authDomain: "facerec-d9fa1.firebaseapp.com",
    databaseURL: "https://facerec-d9fa1.firebaseio.com",
    projectId: "facerec-d9fa1",
    storageBucket: "facerec-d9fa1.appspot.com",
    messagingSenderId: "1061417028783",
    appId: "1:1061417028783:web:3ec6e7c2762137b0b2585a"
};

firebase.initializeApp(config);

// Firebase Database Reference and the child
const dbRef = firebase.database().ref();
const usersRef = dbRef.child('phelipe');