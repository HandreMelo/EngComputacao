indexController = (function($){
    var usuario, settings;

    function init(){
        customSelectedDropzone();
        addPerson();
    }

    function addPerson(){
        $('#addPerson').on('click', function(){
            convertImageToBase64();
            usuario.nome = $('#nome').val();
            settings['url'] = "https://api.luxand.cloud/subject";
            settings['data'] = {"name":usuario['nome']};
            
            $.ajax(settings).done(function(data){
                settings['url'] = "https://api.luxand.cloud/subject/"+data['id'];
                settings['data'] = {"store": "1","photo": usuario['imagem']};
                console.log(data);

                $.ajax(settings).done(function (data) {
                    console.log(data);
                });
            });
        });
    }

    function customSelectedDropzone(){
        $(".custom-file-input").on("change", function() {
            var fileName = $(this).val().split("\\").pop();
            
            $(this).siblings(".custom-file-label").addClass("selected").html(fileName);
        });
    }

    function convertImageToBase64(){
        var inputFile = document.querySelector('input[type=file]'),
            file = inputFile.files[0],
            reader = new FileReader();

        reader.onloadend = function(){
            var b64 = reader.result.replace(/^data:.+;base64,/, '');
            usuario['imagem'] = b64;
        }

        reader.readAsDataURL(file);
    }

    $(document).ready(function(){
        usuario = {
            'nome': '',
            'imagem':'',
        }
    
        settings = {
            "async": true,
            "crossDomain": true,
            "url": '',
            "method": "POST",
            "headers": {
                "token": "8f1ce726defe4e9ba4d21d9a5709320f"
            },
            "data": ''
        }
        init();
    });

})(jQuery);