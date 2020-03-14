var index = (function($){
    function init(){
        addImage();
        recognizeImage();
    }

    function addImage(){
        $('#addPerson').on('click', function(){

            $.ajax({
                crossDomain: true,
                url: "https://api.luxand.cloud/subject",
                method: "POST",
                headers: {
                    "token": "8f1ce726defe4e9ba4d21d9a5709320f"
                },
                
                data: {"name":"testeuploadFoto"},
                success: function(data){
                    if(!data.fail){
                        $.ajax({
                            crossDomain: true,
                            url: "https://api.luxand.cloud/subject/"+data.id,
                            method: "POST",
                            headers: {
                                "token": "8f1ce726defe4e9ba4d21d9a5709320f"
                            },
                            data: {"store": "1","photo": 'endereçoDaFoto'},
                            success: function(data){
                                console.log(data);
                            }
                        })
                    }
                }
            })
        })
    }

    function verifyImage(){

    }

    function recognizeImage(){

    }



    $(document).ready(function(){
        init();
    });

})(jQuery);