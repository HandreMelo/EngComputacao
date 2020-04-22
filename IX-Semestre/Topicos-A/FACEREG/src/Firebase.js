import * as firebase from 'firebase';
import firestore from 'firebase/firestore'

const settings = {timestampsInSnapshots: true};

const config = {
  apiKey: "AIzaSyDXgjRZ2H1QnGpnMoDEN9TOTXxbYL-Pb1Q",     
  authDomain: "facerec-d9fa1.firebaseapp.com",     
  databaseURL: "https://facerec-d9fa1.firebaseio.com",     
  projectId: "facerec-d9fa1",     
  storageBucket: "facerec-d9fa1.appspot.com",     
  messagingSenderId: "1061417028783",     
  appId: "1:1061417028783:web:3ec6e7c2762137b0b2585a" 
};
firebase.initializeApp(config);

firebase.firestore().settings(settings);

export default firebase;
