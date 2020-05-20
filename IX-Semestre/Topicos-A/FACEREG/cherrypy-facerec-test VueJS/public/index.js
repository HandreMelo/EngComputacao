
    var usuario, settings;

    function addPerson(){
        $(document).on('click','#submitPerson', function(){

				$.ajax({
					type: "POST",
					url: '192.168.1.105:8080/procurar',
					data: {usuario['imagem']},
					success: success
				});
        });
    }

    function convertImageToBase64(){
        var inputFile = document.querySelector('input[type=file]'),
            file = inputFile.files[0],
            reader = new FileReader();
           // debugger

        if (file === undefined) {
            return null;
        } else {
            reader.onloadend = function(){
                var b64 = reader.result.replace(/^data:.+;base64,/, '');
                usuario['imagem'] = b64;
            }

            reader.readAsDataURL(file);
        }    
    }
	
        usuario = {
            'nome': '',
            'imagem': '',
        }
    
        settings = {
            "async": true,
            "crossDomain": true,
            "url": '192.168.1.105:8080/procurar',
            "method": "POST",
            "headers": {},
            "data": ''
        }