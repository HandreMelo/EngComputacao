
// !IMPORTANT: REPLACE WITH YOUR OWN CONFIG OBJECT BELOW


// Initialize Firebase
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
const usersRef = dbRef.child('andre');

readUserData(); 

var camera = document.getElementById('face-in');
var camera2 = document.getElementById('face-in2');
var frame = document.getElementById('face');
var frame2 = document.getElementById('face2');

  camera.addEventListener('change', function(e) {
    var file = e.target.files[0]; 
    // Do something with the image file.
    frame.src = URL.createObjectURL(file);
  });
  
camera2.addEventListener('change', function(e) {
    var file = e.target.files[0]; 
    // Do something with the image file.
    frame2.src = URL.createObjectURL(file);
  });

 var usuario = {
 	'imagem': ''
 }
 usuario['imagem'] = "";

//VOLTAR

// --------------------------
// READ
// --------------------------
function readUserData() {

	const userListUI = document.getElementById("user-list");

	usersRef.on("value", snap => {

		userListUI.innerHTML = ""

		snap.forEach(childSnap => {

			let key = childSnap.key,
				value = childSnap.val()
  			
			let $li = document.createElement("li");

			// edit icon
			let editIconUI = document.createElement("span");
			editIconUI.class = "edit-user";
			editIconUI.innerHTML = " ✎";
			editIconUI.setAttribute("userid", key);
			editIconUI.addEventListener("click", editButtonClicked)

			// delete icon
			let deleteIconUI = document.createElement("span");
			deleteIconUI.class = "delete-user";
			deleteIconUI.innerHTML = " ☓";
			deleteIconUI.setAttribute("userid", key);
			deleteIconUI.addEventListener("click", deleteButtonClicked)
			
			$li.innerHTML = value.nome;
			$li.append(editIconUI);
			$li.append(deleteIconUI);

			$li.setAttribute("user-key", key);
			$li.addEventListener("click", userClicked)
			userListUI.append($li);

 		});


	})
	

}

function retornoProcurar() {
	console.log(lastUser);
}


function userClicked(e) {


		var userID = e.target.getAttribute("user-key");

		const userRef = dbRef.child('andre/' + userID);
		const userDetailUI = document.getElementById("user-detail");

		userRef.on("value", snap => {

			userDetailUI.innerHTML = ""

			snap.forEach(childSnap => {
				var $p = document.createElement("p");
				$p.innerHTML = childSnap.key  + " - " +  childSnap.val();
				userDetailUI.append($p);
			})

		});
	

}

// --------------------------
// ADD
// --------------------------

const addUserBtnUI = document.getElementById("add-user-btn");
addUserBtnUI.addEventListener("click", addUserBtnClicked)

var USERPHOTO;
function addUserBtnClicked() {
	let newUser = {};
	const usersRef = dbRef.child('andre');

	const addUserInputsUI = document.getElementsByClassName("user-input");

    

    // loop through View to get the data for the model 
    for (let i = 0, len = addUserInputsUI.length; i < len; i++) {

        let key = addUserInputsUI[i].getAttribute('data-key');
        let value = addUserInputsUI[i].value;
        newUser[key] = value;
		USERPHOTO = newUser['photo'];
		newUser['photo'] = btoa(newUser['photo'])
    }
	//const fs = require('fs') 
	usersRef.push(newUser).then(pushed => {lastUser = pushed.key;sendToPy();});
	
}

function sendToPy(){
	//file = document.getElementById('face-in').files[0];
	const file = document.getElementById('face-in').files[0];
	var formData = new FormData();
    //file = document.getElementById('cad-user').file;
    xhr = new XMLHttpRequest();
	xhr.open('POST', '/cadastrar',false);
	//xhr.setRequestHeader("type", "multipart/form-data");
	formData.append('ufile', file);
	formData.append('uname', lastUser);
	xhr.send(formData);
	
}

// --------------------------
// DELETE
// --------------------------
function deleteButtonClicked(e) {

		e.stopPropagation();

		var userID = e.target.getAttribute("userid");

		const userRef = dbRef.child('andre/' + userID);
		
		userRef.remove();

}


// --------------------------
// EDIT
// --------------------------
function editButtonClicked(e) {
	
	document.getElementById('edit-user-module').style.display = "block";

	//set user id to the hidden input field
	document.querySelector(".edit-userid").value = e.target.getAttribute("userid");

	const userRef = dbRef.child('andre/' + e.target.getAttribute("userid"));

	// set data to the user field
	const editUserInputsUI = document.querySelectorAll(".edit-user-input");


	userRef.on("value", snap => {

		for(var i = 0, len = editUserInputsUI.length; i < len; i++) {

			var key = editUserInputsUI[i].getAttribute("data-key");
					editUserInputsUI[i].value = snap.val()[key];
		}

	});




	const saveBtn = document.querySelector("#edit-user-btn");
	saveBtn.addEventListener("click", saveUserBtnClicked)
}


function saveUserBtnClicked(e) {
 
	const userID = document.querySelector(".edit-userid").value;
	const userRef = dbRef.child('andre/' + userID);

	var editedUserObject = {}

	const editUserInputsUI = document.querySelectorAll(".edit-user-input");

	editUserInputsUI.forEach(function(textField) {
		let key = textField.getAttribute("data-key");
		let value = textField.value;
  		editedUserObject[textField.getAttribute("data-key")] = textField.value
	});



	userRef.update(editedUserObject);

	document.getElementById('edit-user-module').style.display = "none";


}
