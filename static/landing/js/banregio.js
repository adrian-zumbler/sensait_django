
var deleteLog = false;

  $(document).ready(function() {

    $('#img_scroll').addClass('animated fadeInUp');

    var page      = window.location.href;
    var pageIndex = page.indexOf("index");
    var pageHTMl  = page.indexOf("html");

    //console.log(pageHTMl );
    //console.log(pageIndex);

    //Titulos de las secciones para los slides.
    var secciones = [];



    if(pageIndex > 0 || pageHTMl == -1 )
      secciones = ['Home', 'QueEs','Soluciones', 'Ventajas','Paquetes','Adquierelo'];
    else
      secciones = ['Home', 'Producto1', 'Producto2','Producto3'];


    $('#pagepiling').pagepiling({
      menu: '#menu',
      anchors: secciones,
      sectionsColor: ['#FFF', '#F4F4F4', '#FFFFFF', '#40B284','#FFF','#F4F4F4'],
      loopTop: false,
      loopBottom: false,
      afterLoad: function(anchorLink, index){
          //Para mostrar el menu de arriba en MENU PRINCIPAL

          //Funciones para cambiar el menu principal
          if(index == 1 || index == 0 ){
            $("#menu_main").fadeIn(100);
            $("#menu_slides").fadeOut(100);

            //$('#solution_img').hide();
          }else{
            $("#menu_slides").fadeIn(100);
            $("#menu_main").fadeOut(100);

          }

          //Funciones de animación para los objetos
          if(index == 1 || index == 0 ){
            //$('#btn_comienza').addClass('animated fadeInLeft');
            $('#img_scroll').addClass('animated fadeInUp');

          }else if(index==2){

            //$('#solution_img').addClass('animated slideInRight');

          }

      }
    });

    $("#menu_slides").hide();

    $("#solution_1").addClass( "bg_gray_4" ); //Default

    $("#solution_1, #solution_2, #solution_3, #solution_4").mouseover(function(){
        $("#solution_1").removeClass( "bg_gray_4" ); //Default
        $( this ).addClass( "bg_gray_4" );
        var solution_id = $(this).attr("id");
        solution_id =solution_id.split("_");
        //console.log(solution_id[1]);
        $("#solution_img").attr("src", "imgs/solutions/solution_" + solution_id[1] +".png");
     });

     $("#solution_1, #solution_2, #solution_3, #solution_4").mouseout(function(){
        $( this ).removeClass( "bg_gray_4" );
        $("#solution_1").addClass( "bg_gray_4" ); //Default
        $("#solution_img").attr("src", "imgs/solutions/solution_1.png"); //Imagen default
     });



  });
