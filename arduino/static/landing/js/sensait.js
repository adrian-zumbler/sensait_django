

  var tokenCode     = 'Token d7e7f378cdc67dcd7cec11b76e017927c3e73bc3';
  var allData;
  //var urlApiBase    = 'http://dashboard:8000/api/arduinos/';
  var urlApiBase    = 'http://sensait.dyndns.org:8000/api/arduinos/';
  var actualArduino = 5;


  $(document).ready(function() {

    getArduinosFromAPI(actualArduino);
    console.log("Saludos Humanos desde MTY");
  });


    function getArduinosFromAPI(arduino_ID){
      //Peticion AJAX de los datos
      //console.log(urlApiBase + arduinosApi + actualArduino + '/');

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
          //console.log(data);
          dataArduinosCallBack(data);
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
