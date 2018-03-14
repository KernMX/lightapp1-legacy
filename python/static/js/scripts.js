var ignoreColorChange = false; //in order to prevent sending an ajax request whenever javascript updates the color selector
var colorTimer = {}; //Timers prevent the scroll bars and color selector from sending a lot of ajax requests on every little mouse move
var brightnessTimer = {};
var speedTimer = {};
var connected = false;


//*******************************On Startup/Refresh*******************************************
$(document).ready(function() {
  //set up jQuery Minicolors plugin for Color Picker
  $("#inputColor").minicolors({
    theme: "bootstrap",
    changeDelay: 200,
    control: "wheel",
    format: "hex",
    position: 'top left',
    letterCase: 'uppercase',
    inline: false
  });

  //********************************SOCKET IO SETUP********************************************
  //Socketio Client Documentation: https://github.com/socketio/socket.io-client/blob/master/docs/API.md
  $("#errorAlarm").html(createInfoAlert("Connecting..."));
  //get the webserver's IP address and port
  var socket = io.connect('http://' + location.host);
    //Connect to server through a Web Socket
    socket.on('connect', function() {
      if(!connected){
        console.log('connected');
        $("#errorAlarm").html(createSuccessAlert("Connected."));
        socket.emit('getState', function(data){
          var state = JSON.parse(data);
          updateState(state);
        });
        connected = true;
      }
    });

    socket.on('connect_error', function(error){ //Fires when the server isnt running
      console.log('Connection Error: ');
      $("#errorAlarm").html(createErrorAlert("Cannot Connect to Server"));
    });

    socket.on('reconnect_attempt', function(attemptNumber){
      console.log('Reconnect Attempt ' + attemptNumber);
      $("#errorAlarm").html(createInfoAlert("Attempting to Reconnect to Server..."));
    });

    socket.on('reconnect_failed', function(){
      console.log('Reconnect Attempt Failed');
      $("#errorAlarm").html(createErrorAlert("Reconnect Failed"));
    });

    socket.on('reconnect', function(attemptNumber){
        console.log('Reconnected after ' + attemptNumber + ' Attempts');
        $("#errorAlarm").html(createSuccessAlert("Reconnected After " + attemptNumber + " Attempts"));
        socket.emit('getState', function(data){
          var state = JSON.parse(data);
          updateState(state);
        });
    });



    //-----------------------------------Power Buttons---------------------------------------
    $("#btnPowerOn").click(function() {
      socket.emit("setPower", 1);
    });

    $("#btnPowerOff").click(function() {
      socket.emit("setPower", 0);
    });


    socket.on('updatePower', function(power){
      console.log('Updating Power: ' + power);
      updatePower(power);
    });

    function updatePower(value) {
      if (value == 0) {
        $("#btnPowerOn").attr("class", "btn btn-default btn-lg dusty");
        $("#btnPowerOff").attr("class", "btn btn-danger btn-lg");
      } else {
        $("#btnPowerOn").attr("class", "btn btn-success btn-lg");
        $("#btnPowerOff").attr("class", "btn btn-default btn-lg dusty");
      }
    }



    //-----------------------------------Brightness Slider---------------------------------------
    $("#inputBrightness").on("change mousemove touchmove", function() {
      $("#spanBrightness").html($(this).val());
    });

    $("#inputBrightness").on("touchstart mousedown", function() {
      $("#inputBrightness").focus();
    });

    $("#inputBrightness").on("change", function() {
      $("#spanBrightness").html($(this).val());
      delaySetBrightness();
    });


    function delaySetBrightness() {
      clearTimeout(brightnessTimer);
      brightnessTimer = setTimeout(function() {
        setBrightness($("#inputBrightness").val());
      }, 300);
    }

    function setBrightness(brightness) {
      socket.emit("setBrightness", brightness);
    }

    socket.on('updateBrightness', function(brightness){
      console.log('Updating Brightness: ' + brightness);
      updateBrightness(brightness);
    });

    function updateBrightness(brightness) {
      $("#inputBrightness").val(brightness);
      $("#spanBrightness").text(brightness);
    }



    //-----------------------------------Speed Slider---------------------------------------
    $("#inputSpeed").on("change mousemove touchmove", function() {
      $("#spanSpeed").html($(this).val());
    });

    $("#inputSpeed").on("touchstart mousedown", function() {
      $("#inputSpeed").focus();
    });

    $("#inputSpeed").on("change", function() {
      $("#spanSpeed").html($(this).val());
      delaySetSpeed();
    });

    function delaySetSpeed() {
      clearTimeout(speedTimer);
      speedTimer = setTimeout(function() {
        setSpeed($("#inputSpeed").val());
      }, 300);
    }

    function setSpeed(speed) {
      socket.emit("setSpeed", speed);
    }

    socket.on('updateSpeed', function(speed){
      console.log('Updating Speed: ' + speed);
      updateSpeed(speed);
    });

    function updateSpeed(speed) {
      $("#inputSpeed").val(speed);
      $("#spanSpeed").text(speed);
    }



    //-----------------------------------Pattern Selector---------------------------------------
    $("#inputPattern").change(function() {
      socket.emit("setPattern", $("#inputPattern option:selected").index());
    });

    socket.on('updatePattern', function(data){
      console.log(JSON.parse(data));
      updatePattern(JSON.parse(data));
      updatePower(1);
    });

    function updatePattern(data){
      $("#inputPattern").val(data.pattern);
      $("#inputVisualization").val(data.visualization);
      ignoreColorChange = true;
      $("#inputColor").minicolors('value', rgbToHex(parseInt(data.color.r), parseInt(data.color.g), parseInt(data.color.b)));
      ignoreColorChange = false;
    }



    //-----------------------------------Visualization Selector---------------------------------------
    $("#inputVisualization").change(function() {
      socket.emit("setVisualization", $("#inputVisualization option:selected").index());
    });

    socket.on('updateVisualization', function(data){
      console.log(JSON.parse(data));
      updateVisualization(JSON.parse(data));
      updatePower(1);
    });

    function updateVisualization(data){
      $("#inputPattern").val(data.pattern);
      $("#inputVisualization").val(data.visualization);
      ignoreColorChange = true;
      $("#inputColor").minicolors('value', rgbToHex(parseInt(data.color.r), parseInt(data.color.g), parseInt(data.color.b)));
      ignoreColorChange = false;
    }



    //-----------------------------------Color Picker/Buttons---------------------------------------
    $("#inputColor").change(function() {
      if (ignoreColorChange) return;
      var rgb = $("#inputColor").minicolors('rgbObject');
      delaySetColor(rgb);
    });

    $(".btn-color").click(function() {
      if (ignoreColorChange) return;

      var rgb = $(this).css('backgroundColor');
      var components = rgbToComponents(rgb);
      delaySetColor(components);
      var hexString = rgbToHex(components.r, components.g, components.b);
      ignoreColorChange = true;
      $("#inputColor").minicolors('value', hexString);
      ignoreColorChange = false;
    });

    function delaySetColor(value) {
      clearTimeout(colorTimer);
      colorTimer = setTimeout(function() {
        setColor(value);
      }, 300);
    }

    function setColor(color){
      socket.emit("setColor", color);
    }

    socket.on('updateColor', function(data){
      console.log(JSON.parse(data));
      updateColor(JSON.parse(data));
      updatePower(1);
    });

    function updateColor(data){
      $("#inputPattern").val(data.pattern);
      $("#inputVisualization").val(data.visualization);
      ignoreColorChange = true;
      $("#inputColor").minicolors('value', rgbToHex(parseInt(data.color.r), parseInt(data.color.g), parseInt(data.color.b)));
      ignoreColorChange = false;
    }



    //-----------------------------------Update State----------------------------------------
    function updateState(data) { //retrieve current state of LEDs from server

        updatePower(data.power);

        updateBrightness(data.brightness);

        updateSpeed(data.speed);

        // clear pattern list
        $("#inputPattern").find("option").remove();

        //set new pattern list
        $("#inputPattern").append("<option value=0 disabled selected value> -- select an option -- </option>");
        for (var i = 1; i <= data.patterns.length; i++) {
          var pattern = data.patterns[i - 1];
          $("#inputPattern").append("<option value='" + i + "'>" + pattern + "</option>");
        }

        // select the current pattern
        $("#inputPattern").val(data.pattern);

        //clear visualization list
        $("#inputVisualization").find("option").remove();

        //set new visualization list
        $("#inputVisualization").append("<option value=0 disabled selected value> -- select an option -- </option>");
        for (var i = 1; i <= data.visualizations.length; i++) {
          var visualization = data.visualizations[i - 1];
          $("#inputVisualization").append("<option value='" + i + "'>" + visualization + "</option>");
        }

        // select the current visualization
        $("#inputVisualization").val(data.visualization);

        //set Color Picker
        ignoreColorChange = true;
        $("#inputColor").minicolors('value', rgbToHex(parseInt(data.color.r), parseInt(data.color.g), parseInt(data.color.b)));
        ignoreColorChange = false;
    }
    //********************************END SOCKET SETUP*********************************************
}); //End $(document).ready()




//-----------------------------------Alert Functions---------------------------------------
function createErrorAlert(message){
    var ret = '<div class="alert alert-danger alert-dismissible" role="alert">';
    ret += '<button type="button" class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">&times;</span></button>';
    ret += '<strong>Error!</strong> ';
    ret += message;
    ret += '</div>';
    return ret;
}

function createSuccessAlert(message){
    var ret = '<div class="alert alert-success alert-dismissible" role="alert">';
    ret += '<button type="button" class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">&times;</span></button>';
    ret += '<strong>Success!</strong> ';
    ret += message;
    ret += '</div>';
    return ret;
}

function createInfoAlert(message){
    var ret = '<div class="alert alert-info alert-dismissible" role="alert" id="infoAlert">';
    ret += '<button type="button" class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">&times;</span></button>';
    ret += message;
    ret += '</div>';
    return ret;
}



//-----------------------------------Data Parsing---------------------------------------
function componentToHex(c) {
  var hex = c.toString(16);
  return hex.length == 1 ? "0" + hex : hex;
}

function rgbToHex(r, g, b) {
  return "#" + componentToHex(r) + componentToHex(g) + componentToHex(b);
}

function rgbToComponents(rgb) {
  var components = {};

  rgb = rgb.match(/^rgb\((\d+),\s*(\d+),\s*(\d+)\)$/);
  components.r = parseInt(rgb[1]);
  components.g = parseInt(rgb[2]);
  components.b = parseInt(rgb[3]);

  return components;
}

/* To Be used when you get a temperature slider //TODO
function tempToRgb(kelvin){
    var temp = kelvin / 100;
    var red, green, blue;
    var components = {};
    if( temp <= 66 ){
        red = 255;
        green = temp;
        green = 99.4708025861 * Math.log(green) - 161.1195681661;
        if( temp <= 19){
            blue = 0;
        } else {
            blue = temp-10;
            blue = 138.5177312231 * Math.log(blue) - 305.0447927307;
        }
    } else {
        red = temp - 60;
        red = 329.698727446 * Math.pow(red, -0.1332047592);
        green = temp - 60;
        green = 288.1221695283 * Math.pow(green, -0.0755148492 );
        blue = 255;
    }
    components.r = clamp(red,   0, 255);
    components.g = clamp(green, 0, 255);
    components.b = clamp(blue,  0, 255);
    return components;
}

function clamp( x, min, max ) {
    if(x<min){ return min; }
    if(x>max){ return max; }
    return x;
}
*/

/* Particles-js settings: */

particlesJS('particles-js',

  {
    "particles": {
      "number": {
        "value": 80,
        "density": {
          "enable": true,
          "value_area": 800
        }
      },
      "color": {
        "value": "#ffffff"
      },
      "shape": {
        "type": "circle",
        "stroke": {
          "width": 0,
          "color": "#000000"
        },
        "polygon": {
          "nb_sides": 5
        },
        "image": {
          "src": "img/github.svg",
          "width": 100,
          "height": 100
        }
      },
      "opacity": {
        "value": 0.5,
        "random": false,
        "anim": {
          "enable": true,
          "speed": 0.5,
          "opacity_min": 0.1,
          "sync": false
        }
      },
      "size": {
        "value": 5,
        "random": true,
        "anim": {
          "enable": false,
          "speed": 40,
          "size_min": 0.1,
          "sync": false
        }
      },
      "line_linked": {
        "enable": false,
        "distance": 150,
        "color": "#ffffff",
        "opacity": 0.4,
        "width": 1
      },
      "move": {
        "enable": true,
        "speed": 0.5,
        "direction": "none",
        "random": false,
        "straight": false,
        "out_mode": "out",
        "attract": {
          "enable": false,
          "rotateX": 600,
          "rotateY": 1200
        }
      }
    },
    "interactivity": {
      "detect_on": "window",
      "events": {
        "onhover": {
          "enable": false,
          "mode": "grab"
        },
        "onclick": {
          "enable": true,
          "mode": "repulse"
        },
        "resize": true
      },
      "modes": {
        "grab": {
          "distance": 400,
          "line_linked": {
            "opacity": 1
          }
        },
        "bubble": {
          "distance": 100,
          "size": 40,
          "duration": 2,
          "opacity": 8,
          "speed": 3
        },
        "repulse": {
          "distance": 200
        },
        "push": {
          "particles_nb": 4
        },
        "remove": {
          "particles_nb": 2
        }
      }
    },
    "retina_detect": true
  }

);
