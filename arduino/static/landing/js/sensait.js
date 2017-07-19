

  var tokenCode     = 'Token d7e7f378cdc67dcd7cec11b76e017927c3e73bc3';
  var allData;
  //var urlApiBase    = 'http://dashboard:8000/api/arduinos/';
  var urlApiBase    = 'http://sensait.dyndns.org/api/arduinos/';
  var actualArduino = 23;

  var actualUrl = window.location.href;


  $(document).ready(function() {
    console.log("Saludos Humanos desde MTY");

    console.log(actualUrl);

    //Mismo dominio de sensait
    if(actualUrl.indexOf("sensait") === 0 ){
      console.log(actualUrl);
      urlApiBase    = 'http://sensait.dyndns.org/api/arduinos/';
      //Sensait desde servidor local
    }else if(actualUrl.indexOf("sensait") == -1){
      urlApiBase    = 'http://192.168.253.31/api/arduinos/';
      console.log("actualUrl");
    }else{
      console.log("dos");
    }

    getArduinosFromAPI(actualArduino);
    console.log(urlApiBase);
  });

    //Peticion AJAX de los datos
    function getArduinosFromAPI(arduino_ID){
      $.ajax({
        url: urlApiBase + actualArduino + '/',
        type: 'GET',
        contentType: 'json/application',
        dataType: 'json',
        processData: false,
        xhrFields: {
          withCredentials: false
        },
        headers: {
          'Authorization': tokenCode
        },
        success: function(data) {
          console.log('AJAX API SUCCESS - PROYECTO SELECCIONADO ');
          //Se hara un return con el JSON obtenido en la API
          console.log(data);
          //dataArduinosCallBack(data);
        },
        error: function() {
          console.log('Hubo un problema, solucionalo...!');
        }
      });
    }


      function dataArduinosCallBack( data ){
        console.log("Llego la información ARDUINO");
        console.log(data);
        //actualArduino = data.id; //ID del arduino seleccionado

        $('#realTimeDemo').html(" ");

        var rowData = " ";
        rowData += '<span>' + data.name + '</span>';

        $('#realTimeDemo').html(rowData);

        for(var i=0 ; i < data.sensors.length; i++){
          //$('#my_arduinos').append(data.sensors[i] + '<br/>');
          //$('#my_arduinos').append('<div id=ard_'+data.id+ '_sens_'+ i + '></div>');
          //$('#my_arduinos').append('----------------------------<br/>' );
          getSensorsFromAPI(data.sensors[i], actualArduino, i);
        }
      }


      function getSensorsFromAPI(sensor_ID, arduinoID, sensID){

        var passData_arduinoID  = arduinoID;
        var passData_sensID     = sensor_ID;


        //Peticion AJAX de los datos
        var allData;
        $.ajax({
          url: urlApiBase + actualArduino +'/sensors/'+ sensor_ID + '/data/' ,
          type: 'GET',
          contentType: 'json/application',
          dataType: 'json',
          processData: false,
          xhrFields: {
            withCredentials: false
          },
          headers: {
            'Authorization': tokenCode
          },
          success: function(data) {
            //console.log('AJAX API SUCCESS! SENSORS');
            //Se hara un return con el JSON obtenido en la API
            console.log(data);
            dataSensorsCallBack(data,passData_arduinoID,passData_sensID);
          },
          error: function() {
            console.log('Hubo un problema, solucionalo...!');
          }
        });
      }


      function dataSensorsCallBack(data,passData_arduinoID,passData_sensID){
        console.log(data);

      }
