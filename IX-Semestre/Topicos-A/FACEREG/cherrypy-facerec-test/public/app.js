
// !IMPORTANT: REPLACE WITH YOUR OWN CONFIG OBJECT BELOW


// Initialize Firebase
var lastUser = ''
var config = {
    apiKey: "XXXXXXXXXXXXXXXXXXXXX",
    authDomain: "XXXXXXXXXXXXXXXXXXXXX",
    databaseURL: "XXXXXXXXXXXXXXXXXXXXX",
    projectId: "XXXXXXXXXXXXXXXXXXXXX",
    storageBucket: "XXXXXXXXXXXXXXXXXXXXX",
    messagingSenderId: "XXXXXXXXXXXXXXXXXXXXX",
    appId: "XXXXXXXXXXXXXXXXXXXXX"
};

var userName = 'andre';

firebase.initializeApp(config);

// Firebase Database Reference and the child
const dbRef = firebase.database().ref();
const usersRef = dbRef.child(userName);


readUserData(); 

const addUserBtnUI = document.getElementById("add-user-btn");
addUserBtnUI.addEventListener("click", addUserBtnClicked);

var adicionarFaceFile = document.getElementById('adicionar-face-file');
var editarFaceFile = document.getElementById('editar-face-file');
var procurarFaceFile = document.getElementById('procurar-face-file');

adicionarFaceFile.addEventListener('change', function(e) {
  var file = e.target.files[0]; 
  // Do something with the image file.
  document.getElementById('adicionar-face').src = URL.createObjectURL(file);
});
editarFaceFile.addEventListener('change', function(e) {
  var file = e.target.files[0]; 
  // Do something with the image file.
  document.getElementById('editar-face').src = URL.createObjectURL(file);
});
procurarFaceFile.addEventListener('change', function(e) {
  var file = e.target.files[0]; 
  // Do something with the image file.
  document.getElementById('procurar-face').src = URL.createObjectURL(file);
});

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

		const userRef = dbRef.child(userName+'/' + userID);

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


function addUserBtnClicked() {

	const usersRef = dbRef.child(userName);
	document.getElementById('add-user-module').style.display = "block";
	const file = document.getElementById('adicionar-face-file').files[0];
	
	const adicionarFaceFile = document.getElementById("adicionar-face-file");
	
	let newUser = {};

	const addUserInputsUI = document.getElementsByClassName("user-input");

    // loop through View to get the data for the model 
    for (let i = 0, len = addUserInputsUI.length; i < len; i++) {

        let key = addUserInputsUI[i].getAttribute('data-key');
        let value = addUserInputsUI[i].value;
        newUser[key] = value;
		newUser['photo'] = btoa(newUser['photo'])
    }
	
	usersRef.push(newUser).then(pushed => {lastUser = pushed.key;sendToPy('cadastrar',lastUser,file);});
	
}

function sendToPy(crud, userId, file){
	
	var formData = new FormData();
    
    xhr = new XMLHttpRequest();
	xhr.open('POST', '/'+crud,true);
	if(crud == 'atualizar' || crud == 'cadastrar') {
		formData.append('ufile', file);
	}
	formData.append('uname', userId);
	xhr.send(formData);
	
	
}

// --------------------------
// DELETE
// --------------------------
function deleteButtonClicked(e) {

		e.stopPropagation();

		var userID = e.target.getAttribute("userid");

		const userRef = dbRef.child(userName+'/' + userID);
		
		userRef.remove();
		sendToPy('deletar',userID,'');

}


// --------------------------
// EDIT
// --------------------------
function editButtonClicked(e) {
	
	document.getElementById('edit-user-module').style.display = "block";

	//set user id to the hidden input field
	document.querySelector(".edit-userid").value = e.target.getAttribute("userid");


	const userRef = dbRef.child(userName+'/' + e.target.getAttribute("userid"));



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

	const userRef = dbRef.child(userName+'/' + userID);

	const file = document.getElementById('editar-face-file').files[0];

	var editedUserObject = {}

	const editUserInputsUI = document.querySelectorAll(".edit-user-input");

	editUserInputsUI.forEach(function(textField) {
		let key = textField.getAttribute("data-key");
		let value = textField.value;
  		editedUserObject[textField.getAttribute("data-key")] = textField.value
	});



	userRef.update(editedUserObject);
	sendToPy(crud, userId, file)
	document.getElementById('edit-user-module').style.display = "none";


}
