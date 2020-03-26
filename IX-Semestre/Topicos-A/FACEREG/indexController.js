indexController = (function($){
    var usuario, settings;

    function init(){
        detectChangeSelect();
        customSelectedDropzone();
        addPerson();
        listPersons();
    }

    function addPerson(){
        $(document).on('click','#submitPerson', function(){
            debugger
            

            if ($('#nome').val() !== '' && document.querySelector('input[type=file]').files[0] !== undefined) {
                convertImageToBase64();
                usuario.nome = $('#nome').val();
                settings['url'] = "https://api.luxand.cloud/subject";
                settings['data'] = {"name":usuario['nome']};
            
                $.ajax(settings).done(function(data){
                    settings['url'] = "https://api.luxand.cloud/subject/"+data['id'];
                    settings['data'] = {"store": "1","photo": usuario['imagem']};
                    settings['method'] = 'POST';
                    console.log(data);

                    $.ajax(settings).done(function (data) {
                        if(!data.fail){
                            settingsAlerts('Usuario cadastrado com sucesso!');
                        }
                    });
                });
            } else {
                settingsAlerts('Um dos campos nao foi preenchido corretamente');
            }

            
        });
    }

    function listPersons(){
        $('#submitListPersons').on('click',function(){
            settings['url'] = "https://api.luxand.cloud/subject";
            settings['data'] = {};
            settings['method'] = 'GET';

            $.ajax(settings).done(function(responseData){
                if(!responseData.fail){
                    console.log(responseData);
                    createTableListPersons(responseData);
                } else{
                    console.log(responseData);
                }
            });
        });
    }

    function createTableListPersons(responseData){
        var tbodyTable = $('#tablePersons tbody');

        for(var cont=0;cont<responseData.length;cont++){
            var newTr = $('<tr></tr>'),
                newTh = $("<tr>"+cont+"</tr>", {scope: "row"}),
                tdId = $("<td>"+responseData[cont].id+"</td>"),
                tdName = $("<td>"+responseData[cont].name+"</td>");

            newTr.append(newTh);
            newTr.append(tdId);
            newTr.append(tdName);
            tbodyTable.append(newTr);
        }

        $('#tablePersons').css({'display': 'block'});
    }

    function customSelectedDropzone(){
        $(".custom-file-input").on("change", function() {
            var fileName = $(this).val().split("\\").pop();
            
            $(this).siblings(".custom-file-label").addClass("selected").html(fileName);
        });
    }

    function settingsAlerts(setText){
        $('#alertResponse').text(setText)
                           .css({'display': 'block'});

        setTimeout(() => {
            $('#alertResponse').fadeOut();
        }, 4000);
    }

    function convertImageToBase64(){
        var inputFile = document.querySelector('input[type=file]'),
            file = inputFile.files[0],
            reader = new FileReader();
            debugger

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

    function detectChangeSelect(){
        $(document).on('change','#selectOption',function(){
            var idOptionSelected = $(this).find("option:selected").attr('rel');
            changeCardBody(idOptionSelected);
       });
    }

    function changeCardBody(idCardBody){
        cardBodyCurrent = $('.active');
        cardBodySelected = $("#"+idCardBody);
        $('#tablePersons').css({'display': 'none'});

        cardBodyCurrent.css({'display':'none'}).removeClass('active');
        cardBodySelected.css({'display':'block'}).addClass('active');
    }

    $(document).ready(function(){
        usuario = {
            'nome': '',
            'imagem': '',
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