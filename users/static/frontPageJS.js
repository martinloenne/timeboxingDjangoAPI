$(document).ready(function () {

  document.getElementById("stopBtn").style.display = "none";
  document.getElementById("breakBtn").style.display = "inline";

  function handleFormSuccess(data, textStatus, jqXHR) {
    console.log(data)
    console.log(textStatus)
    console.log(jqXHR)
    $myForm.reset(); // reset form data
  }


  function handleFormError(jqXHR, textStatus, errorThrown) {
    console.log(jqXHR)
    console.log(textStatus)
    console.log(errorThrown)
  }


  // Loads all the products
  $(document).ready(function () {
    $.ajax({
      type: "GET",
      url: 'getProducts',
      // data:JSON.stringify(data),
      success: function (result) {
        console.log(result);
        for (var i = result.length - 1; i >= 0; i--) {
          $("#selectProducts").append('<option>' + result[i].name + '</option>');
        };
      },
    });
  });


  // Submit new product
  $('#btn_submitProduct').on('click', function () {
    $product_new_name = $('#product_new_name').val();

    if ($('#product_new_name').val() == "") {
      alert("Please fill up the required field");
    } else {
      $.ajax({
        type: "POST",
        url: "insertProduct",
        data: {
          name: $product_new_name,
          csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
        },
        success: function () {
          $("#selectProducts").append('<option>' + $('#product_new_name').val() + '</option>');
          $('#product_new_name').val('');
        }
      });
    }
  });


  // Gets all the categories
  $(document).ready(function () {
    $.ajax({
      type: "GET",
      url: 'getCategories',
      // data:JSON.stringify(data),
      success: function (result) {
        console.log(result);
        for (var i = result.length - 1; i >= 0; i--) {
          $("#selectCategory").append('<option>' + result[i].name + '</option>');
        };
      },
    });
  });


  // Gets all the timeboxes done today
  $(document).ready(function () {
    $.ajax({
      type: "GET",
      url: 'getTodaysSessions',
      // data:JSON.stringify(data),
      success: function (result) {
        for (var i = result.length - 1; i >= 0; i--) {

          var temp_n = result[i].sessiontime;
          var hours = (temp_n / 3600);
          var minutes = (temp_n / 60);
          var mins_left = Math.floor((minutes % 60));
          var secs_left = Math.floor((temp_n % 60));

          let displayString = `${mins_left < 10 ? '0' : ''}${mins_left}:${secs_left < 10 ? '0' : ''}${secs_left}`;

          $('<div id="' + 'counterContainer' + timeboxDone + '" ></div>').appendTo('#timeboxContainer');
          $('#counterContainer' + timeboxDone).append(' \
              <h6>' + result[i].product + '</h6> \
              <h6>' + result[i].category + '</h6> \
              <div class="circle">  \
              <svg width="120" viewBox="0 0 220 220" xmlns="http://www.w3.org/2000/svg"> \
              <g transform="translate(110,110)"> \
                <circle r="100" class="e-c-base"/> \
                <g transform="rotate(-90)"> \
                  <circle r="100" class="e-c-progress" div id="' + 'e-c-progressID' + timeboxDone + '"/> \
                  <g id="' + 'e-pointer' + timeboxDone + '" > \
                  </g> \
                </g> \
              </g> \
              </svg>  \
            </div> \
            <div id="timebox_time"><h6>' + displayString + '</h6></div>\
          </div> \
          ');

          timeboxDone += 1;
        };
      },
    });
  });


  // Submit new category
  $('#btn_submitCategory').on('click', function () {
    $category_new_name = $('#category_new_name').val();

    if ($('#category_new_name').val() == "") {
      alert("Please fill up the required field");
    } else {
      $.ajax({
        type: "POST",
        url: "insertCategory",
        data: {
          name: $category_new_name,
          csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
        },
        success: function () {
          $("#selectCategory").append('<option>' + $('#category_new_name').val() + '</option>');
          $('#category_new_name').val('');
        }
      });
    }

  });


});


$(function () {
  // don't cache ajax or content won't be fresh
  $.ajaxSetup({
    cache: false
  });
  var ajax_load = "<img src='http://automobiles.honda.com/images/current-offers/small-loading.gif' alt='loading...' />";

  // load() functions
  var loadUrl = "http://127.0.0.1:8000/users/signup";
  $("#target").click(function () {
    $("#result").html(ajax_load).load(loadUrl);
  });
  // end  
});


// TIMEBOX TIMER
var n = 0;
var saveTime = 0;
var timeInSecondsRealtime = 0.00;
var interupt = false;
var infinite = false;
var breakTime = false;
var timeboxDone = 0;
var noSave = false;
$("#buttons button").click(function () {

  if (this.id == "answer5") {
    n = 0;
    infinite = true;
  } else {
    var a = parseInt($(this).text());
    saveTime = (a * 60);
    infinite = false;
  }

  // Changes button to pressed or unpressed
  if (this.id == "answer1") {
    $('#' + this.id).addClass('answerBtnsSelected');
    $('#' + "answer2").removeClass('answerBtnsSelected');
    $('#' + "answer3").removeClass('answerBtnsSelected');
    $('#' + "answer4").removeClass('answerBtnsSelected');
    $('#' + "answer5").removeClass('answerBtnsSelected');
  } else if (this.id == "answer2") {
    $('#' + this.id).addClass('answerBtnsSelected');
    $('#' + "answer1").removeClass('answerBtnsSelected');
    $('#' + "answer3").removeClass('answerBtnsSelected');
    $('#' + "answer4").removeClass('answerBtnsSelected');
    $('#' + "answer5").removeClass('answerBtnsSelected');
  } else if (this.id == "answer3") {
    $('#' + this.id).addClass('answerBtnsSelected');
    $('#' + "answer1").removeClass('answerBtnsSelected');
    $('#' + "answer2").removeClass('answerBtnsSelected');
    $('#' + "answer4").removeClass('answerBtnsSelected');
    $('#' + "answer5").removeClass('answerBtnsSelected');
  } else if (this.id == "answer4") {
    $('#' + this.id).addClass('answerBtnsSelected');
    $('#' + "answer1").removeClass('answerBtnsSelected');
    $('#' + "answer2").removeClass('answerBtnsSelected');
    $('#' + "answer3").removeClass('answerBtnsSelected');
    $('#' + "answer5").removeClass('answerBtnsSelected');
  } else if (this.id == "answer5") {
    $('#' + this.id).addClass('answerBtnsSelected');
    $('#' + "answer1").removeClass('answerBtnsSelected');
    $('#' + "answer2").removeClass('answerBtnsSelected');
    $('#' + "answer3").removeClass('answerBtnsSelected');
    $('#' + "answer4").removeClass('answerBtnsSelected');
  }

  //CLEAR THE INPUT**
  $('#timebox_time_input').val('');

});



// Sets volume
var volume = 0;
$(document).ready(function () {

  var n_volume = $("#volume_server").html();
  volume = n_volume;
  $(".slider").val(n_volume * 100);


  $(".slider").change(function () {
    volume = $(this).val();
    volume = volume / 100;
    $("#volume_server").html(volume);
     // Upload data
      $session_data = volume;

      $.ajax({
        type: "POST",
        url: "change_volume",
        data: {
          volume_choosen: $session_data,
          csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
        },
        success: function () {

        }
      });
  });

});





// Checks if input is giving so unpress buttons
$("#timebox_time_input").change(function () {
  $('#' + "answer1").removeClass('answerBtnsSelected');
  $('#' + "answer2").removeClass('answerBtnsSelected');
  $('#' + "answer3").removeClass('answerBtnsSelected');
  $('#' + "answer4").removeClass('answerBtnsSelected');
  $('#' + "answer5").removeClass('answerBtnsSelected');
});


let intervalTimer;
let timeLeft;
let wholeTime = 0; // manage this to set the whole time (Seconds)
let isPaused = false;
let isStarted = false;


// Starts timebox
$('#btn_startTimebox').on('click', function () {
  // Vars
  breakTime = false;
  var validInput = false;


  var listValue = $('#selectProducts')[0].length;
  if (listValue == 0) {
    alert("Please be awesome and create a project");
    return;
  }

  // First check if input is givin
  $timebox_time_input = $('#timebox_time_input').val();
  if (($('#timebox_time_input').val() == "") && (!infinite)) {
    // No input giving
    // Check if button is pressed
    if (saveTime > 0) {
      validInput = true;
    } else if (saveTime <= 0) {
      // No button is pressed
      validInput = false;
    }
  } else {
    // Input has been giving and no button is pressed
    var a = $('#timebox_time_input').val();
    saveTime = (a * 60);
    validInput = true;
  }


  if (!infinite) {
    if (validInput) {
      // Disables the other butttons
      document.getElementById("stopBtn").style.display = "inline";
      document.getElementById("breakBtn").style.display = "none";
      document.getElementById("btn_startTimebox").style.display = "none";
      $("#answer1").attr("disabled", true);
      $("#answer2").attr("disabled", true);
      $("#answer3").attr("disabled", true);
      $("#answer4").attr("disabled", true);
      $("#answer5").attr("disabled", true);
      $("#timebox_time_input").attr("disabled", true);

      $('<div id="' + 'counterContainer' + timeboxDone + '"></div>').prependTo('#timeboxContainer');
      $('#counterContainer' + timeboxDone).append(' \
        <h6 p class="hide-this">Space</h6> \
        <h6 p class="hide-this">Space</h6> \
                <div class="circle">  \
                <svg width="120" viewBox="0 0 220 220" xmlns="http://www.w3.org/2000/svg"> \
                <g transform="translate(110,110)"> \
                <circle r="100" class="e-c-base" div id="' + 'e-c-baseID' + timeboxDone + '"/> \
                	<g transform="rotate(-90)"> \
                    <circle r="100" class="e-c-progress-current" div id="' + 'e-c-progressID' + timeboxDone + '"/> \
                    <g id="' + 'e-pointer' + timeboxDone + '" > \
                    <circle cx="100" cy="0" r="8" class="e-c-pointer"' + 'id="e-pointer-done' + timeboxDone + '"/> \
                    </g> \
                  </g> \
                </g> \
                </svg>  \
              </div> \
						<div class="controlls" div id="' + 'controllsID' + timeboxDone + '" > \
							<div class="display-remain-time" div id="' + 'remain_time' + timeboxDone + '" >00:00</div> \
						</div> \
            ');

      noSave = false;
      interupt = false;
      isStarted = true;

      // Starts timebox
      timerFunc();
    } else {
      alert("NO Input, terminate");
    }
  }



}); // End of Function


function timerFunc() {
  // Checks if there is refresh and prompts message
  window.onbeforeunload = function () {
    return "Data will be lost if you leave the page, are you sure?";
  };
  wholeTime = saveTime;
  let progressBar = document.getElementById('e-c-progressID' + timeboxDone);
  let pointer = document.getElementById('e-pointer' + timeboxDone);
  let displayOutput = document.getElementById('remain_time' + timeboxDone);

  //circle start
  let length = Math.PI * 2 * 100;
  progressBar.style.strokeDasharray = length;

  function update(value, timePercent) {
    var offset = -length - length * value / (timePercent);
    progressBar.style.strokeDashoffset = offset;
    pointer.style.transform = `rotate(${360 * value / (timePercent)}deg)`;
  };


  function timer(seconds) { //counts time, takes seconds
    let remainTime = Date.now() + (seconds * 1000);
    displayTimeLeft(seconds);


    intervalTimer = setInterval(function () {
      timeLeft = Math.round((remainTime - Date.now()) / 1000);


      // Interupts the timebox
      if (noSave || interupt) {
        clearInterval(intervalTimer);
        // Clear
        if (noSave) {
          // Deletes visual counter
          var elem = document.getElementById("counterContainer" + timeboxDone);
          elem.parentNode.removeChild(elem);
        } else {
          // Saves the interupted visual counter     
        }
      }


      if (timeLeft < 0) {
        if (!breakTime) {
          alert("Saving");
          // Post request
          var e_category = document.getElementById("selectCategory");
          var result_category = e_category.options[e_category.selectedIndex].text;
          var e_product = document.getElementById("selectProducts");
          var result_product = e_product.options[e_product.selectedIndex].text;

          document.title = 'WorkOn: Timebox done';

          // Upload data
          $session_data = saveTime;
          $session_data_category = result_category;
          $session_data_product = result_product;
          $.ajax({
            type: "POST",
            url: "insertSession",
            data: {
              session_time: $session_data,
              session_time_category: $session_data_category,
              session_time_product: $session_data_product,
              csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
            },
            success: function () {
              var x_y = document.getElementById("myAudio");
              document.getElementById("myAudio").volume = volume;
              x_y.play();
            }
          });
          timeboxDone += 1;

          clearInterval(intervalTimer);
          isStarted = false;
          fadeNumberChange(wholeTime);


          return;
        }

        if (breakTime) {
          document.title = 'WorkOn: Break done';
          noSave = true;
          n = 0;
        }

        document.getElementById("stopBtn").style.display = "none";
        document.getElementById("breakBtn").style.display = "inline";
        document.getElementById("btn_startTimebox").style.display = "inline";
        $('#e-c-baseID' + (timeboxDone - 1)).removeClass('e-c-base').addClass('e-c-base-done');
        $("#answer1").attr("disabled", false);
        $("#answer2").attr("disabled", false);
        $("#answer3").attr("disabled", false);
        $("#answer4").attr("disabled", false);
        $("#answer5").attr("disabled", false);
        $("#timebox_time_input").attr("disabled", false);
      }
      displayTimeLeft(timeLeft);
    }, 1000);
  }

  function displayTimeLeft(timeLeft) { //displays time on the input
    let minutes = Math.floor(timeLeft / 60);
    let seconds = timeLeft % 60;
    let displayString = `${minutes < 10 ? '0' : ''}${minutes}:${seconds < 10 ? '0' : ''}${seconds}`;
    if (!noSave) {
      document.title = 'WorkOn: ' + displayString;
    }

    displayOutput.textContent = displayString;
    update(timeLeft, wholeTime);
  }

  timer(wholeTime);
}


$('#infinite_stop').on('click', function () {
  var e_category = document.getElementById("selectCategory");
  var result_category = e_category.options[e_category.selectedIndex].text;
  var e_product = document.getElementById("selectProducts");
  var result_product = e_product.options[e_product.selectedIndex].text;

  // Upload data
  //$session_data = $('#category_new_name').val();
  $session_data = (timeInSecondsRealtime);
  $session_data_category = result_category;
  $session_data_product = result_product;
  $.ajax({
    type: "POST",
    url: "insertSession",
    data: {
      session_time: $session_data,
      session_time_category: $session_data_category,
      session_time_product: $session_data_product,
      csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
    },
    success: function () {}
  });
  let modal = document.querySelector(".modal-interupt")
  modal.style.display = "none"
  n = 0;
  infinite = false;
  validInput = false;
});


// Break button
$('#breakBtn').on('click', function () {
  // Vars
  breakTime = true;
  var validInput = false;

  // First check if input is givin
  $timebox_time_input = $('#timebox_time_input').val();
  if (($('#timebox_time_input').val() == "") && (!infinite)) {
    // No input giving
    // Check if button is pressed
    if (saveTime > 0) {
      validInput = true;
    } else if (saveTime <= 0) {
      // No button is pressed
      validInput = false;
    }
  } else {
    // Input has been giving and no button is pressed
    var a = $('#timebox_time_input').val();
    saveTime = (a * 60);
    validInput = true;
  }


  if (!infinite) {
    if (validInput) {
      // Disables the other butttons
      document.getElementById("stopBtn").style.display = "inline";
      document.getElementById("breakBtn").style.display = "none";
      document.getElementById("btn_startTimebox").style.display = "none";
      $("#answer1").attr("disabled", true);
      $("#answer2").attr("disabled", true);
      $("#answer3").attr("disabled", true);
      $("#answer4").attr("disabled", true);
      $("#answer5").attr("disabled", true);
      $("#timebox_time_input").attr("disabled", true);

      $('<div id="' + 'counterContainer' + timeboxDone + '"></div>').prependTo('#timeboxContainer');
      $('#counterContainer' + timeboxDone).append(' \
        <h6 style="color: #74667F;">Break</h6>\
        <h6 p class="hide-this">Space</h6> \
                <div class="circle">  \
                <svg width="120" viewBox="0 0 220 220" xmlns="http://www.w3.org/2000/svg"> \
                <g transform="translate(110,110)"> \
                <circle r="100" class="e-c-base" div id="' + 'e-c-baseID' + timeboxDone + '"/> \
                	<g transform="rotate(-90)"> \
                    <circle r="100" class="e-c-progress-current" div id="' + 'e-c-progressID' + timeboxDone + '" style="stroke: #74667F;"/> \
                    <g id="' + 'e-pointer' + timeboxDone + '" > \
                    <circle cx="100" cy="0" r="8" class="e-c-pointer"' + 'id="e-pointer-done' + timeboxDone + '" style="stroke: #74667F;"/> \
                    </g> \
                  </g> \
                </g> \
                </svg>  \
              </div> \
						<div class="controlls" div id="' + 'controllsID' + timeboxDone + '" > \
              <div class="display-remain-time" div id="' + 'remain_time' + timeboxDone + '" style="color: #74667F;" >00:00</div> \
						</div> \
            ');

      noSave = false;
      interupt = false;
      isStarted = true;

      // Starts timebox
      timerFunc();
    } else {
      alert("NO Input, terminate");
    }
  }


});


// Interupt popup
$('#stopBtn').on('click', function () {
  if (!breakTime) {
    let modal = document.querySelector(".modal-interupt")
    // Ask, save data anyway?
    modal.style.display = "block"
  } else {
    noSave = true;
    n = 0;
    document.getElementById("stopBtn").style.display = "none";
    document.getElementById("breakBtn").style.display = "inline";
    document.getElementById("btn_startTimebox").style.display = "inline";
    $("#answer1").attr("disabled", false);
    $("#answer2").attr("disabled", false);
    $("#answer3").attr("disabled", false);
    $("#answer4").attr("disabled", false);
    $("#answer5").attr("disabled", false);
    $("#timebox_time_input").attr("disabled", false);
  }

});


$('#modal-btn_yes').on('click', function () {
  interupt = true;

  var e_category = document.getElementById("selectCategory");
  var result_category = e_category.options[e_category.selectedIndex].text;
  var e_product = document.getElementById("selectProducts");
  var result_product = e_product.options[e_product.selectedIndex].text;

  document.getElementById("stopBtn").style.display = "none";
  document.getElementById("breakBtn").style.display = "inline";
  document.getElementById("btn_startTimebox").style.display = "inline";


  // Upload data
  //$session_data = $('#category_new_name').val();
  $session_data = (saveTime - timeLeft);
  $session_data_category = result_category;
  $session_data_product = result_product;
  $.ajax({
    type: "POST",
    url: "insertSession",
    data: {
      session_time: $session_data,
      session_time_category: $session_data_category,
      session_time_product: $session_data_product,
      csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
    },
    success: function () {

    }
  });
  let modal = document.querySelector(".modal-interupt")
  modal.style.display = "none"
  timeboxDone += 1;
  var temp_n = (saveTime - timeLeft);

  $("#answer1").attr("disabled", false);
  $("#answer2").attr("disabled", false);
  $("#answer3").attr("disabled", false);
  $("#answer4").attr("disabled", false);
  $("#answer5").attr("disabled", false);
  $("#timebox_time_input").attr("disabled", false);

  setTimeout(function () {
    fadeNumberChange(temp_n);
  }, 2000);

  document.title = 'WorkOn - Timebox your work';
  var x_y = document.getElementById("myAudio");
  document.getElementById("myAudio").volume = volume;
  x_y.play();

});


$('#modal-btn_no').on('click', function () {
  noSave = true;
  n = 0;
  let modal = document.querySelector(".modal-interupt")
  modal.style.display = "none"
  document.getElementById("stopBtn").style.display = "none";
  document.getElementById("breakBtn").style.display = "inline";
  document.getElementById("btn_startTimebox").style.display = "inline";
  $("#answer1").attr("disabled", false);
  $("#answer2").attr("disabled", false);
  $("#answer3").attr("disabled", false);
  $("#answer4").attr("disabled", false);
  $("#answer5").attr("disabled", false);
  $("#timebox_time_input").attr("disabled", false);
  document.title = 'WorkOn - Timebox your work';
});


function fadeNumberChange(temp_n) {
  // Changes the number to be how much time you timeboxed instead
  $('#e-c-progressID' + (timeboxDone - 1)).removeClass('e-c-progress-current').addClass('e-c-progress');
  let minutes = Math.floor(temp_n / 60);
  let seconds = temp_n % 60;
  let displayString = `${minutes < 10 ? '0' : ''}${minutes}:${seconds < 10 ? '0' : ''}${seconds}`;

  $('#remain_time' + (timeboxDone - 1)).remove();
  $('#controllsID' + (timeboxDone - 1)).prepend('<div id="timebox_time_done"><h6>' + displayString + '</h6></div>');
  $('#e-pointer-done' + (timeboxDone - 1)).remove();
  //$('#e-pointer-done' + (timeboxDone - 1)).removeClass('e-c-pointer').addClass('e-c-pointer-done');

  var e_category = document.getElementById("selectCategory");
  var result_category = e_category.options[e_category.selectedIndex].text;
  var e_product = document.getElementById("selectProducts");
  var result_product = e_product.options[e_product.selectedIndex].text;
  $(".hide-this").remove();
  $('#counterContainer' + (timeboxDone - 1)).prepend(' \
  <h6>' + result_product + '</h6> \
  <h6>' + result_category + '</h6> \
  ');
}



// Login and Sign-up buttons
$(function () {
  // Log in button
  $(".login-btn").modalForm({
    formURL: "/login/"
  });

});
$(function () {
  // Sign up button
  $(".signup-btn").modalForm({
    formURL: "/signup/"
  });

});



$("#choose_visibility").on('change', function () {
  if ($(this).val() == 'selectionKey') {

  } else {
    if ($(this).val() == "public") {
      $.ajax({
        type: "GET",
        url: 'change_visibility',
        data: {
          'visibility_choosen': "public",
        },
        success: function () {},
      });
    }
    if ($(this).val() == "private") {
      $.ajax({
        type: "GET",
        url: 'change_visibility',
        data: {
          'visibility_choosen': "private",
        },
        success: function () {},
      });
    }
  }
});



// Submit changes to Startpage Journal
$('#change_timezone').on('click', function () {
  var value = $('#choose_timezone :selected').text()

  if (window.location.href.indexOf("profile") > -1) {
    $.ajax({
      type: "POST",
      url: "changeTimezone_profile",
      data: {
        name: value,
        csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
      },
      success: function () {
        document.getElementById("current_timezone").innerHTML = value;
      }
    });
  } else {
    $.ajax({
      type: "POST",
      url: "changeTimezone",
      data: {
        name: value,
        csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
      },
      success: function () {
        document.getElementById("current_timezone").innerHTML = value;
      }
    });
  }
});

























// FOR PROFILE
// Startpage
var button_change = $("#submit_changes");
var form_original_data = $("#startPageJounal").serialize();
button_change.hide();
$("#startPageJounal").on('change keyup paste', function () {
  if ($("#startPageJounal").serialize() != form_original_data) {
    button_change.show();
  } else {
    button_change.hide();
  }
});


// Submit changes to Startpage Journal
$('#submit_changes').on('click', function () {
  $startpage_journal = $("#startPageJounal").val();
  $.ajax({
    type: "POST",
    url: "insertStartPageJournal",
    data: {
      name: $startpage_journal,
      csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
    },
    success: function () {
      form_original_data = $("#startPageJounal").serialize();
      button_change.hide();
    }
  });
});

// Checks if we are on profile page and loads weekly statestic
$(document).ready(function () {
  if (window.location.href.indexOf("profile") > -1) {
    var pathArray = window.location.pathname.split('/');
    var secondLevelLocation = pathArray[2];
    document.title = 'WorkOn | ' + secondLevelLocation;
    show_statestic = 1;

    $("#current_week_show").addClass("button_selected");

    var category = [];
    var product = [];
    $.each($("input[name='checkboxCategory']:checked"), function () {
      category.push($(this).val());
    });
    $.each($("input[name='checkboxProduct']:checked"), function () {
      product.push($(this).val());
    });

    // Gets new statestic for current week
    $.ajax({
      type: "GET",
      url: 'get_statestic',
      data: {
        'user_category': category,
        'user_product': product
      },
      success: function (result) {
        $('#bokeh_graph').html(result)
      },
    });
    document.getElementById("month_show").style.display = "none";
    document.querySelector('#journal_button_top').setAttribute('href', document.getElementById("logo_top").href);
    document.getElementById("journal_button_top").text = "Timeboxing";
  } else {
    document.title = 'WorkOn - Timebox your work';
  }
});

// 0 = null, 1 = week, 2 = year, 3 = month
var show_statestic = 0;
var current_month = "";

// Submit changes to the statestic for ....
$('#submit_statestic_current_week').on('click', function () {
  event.preventDefault()
  $('.close-modal').trigger("click")
  var category = [];
  var product = [];
  $.each($("input[name='checkboxCategory']:checked"), function () {
    category.push($(this).val());
  });
  $.each($("input[name='checkboxProduct']:checked"), function () {
    product.push($(this).val());
  });

  if (show_statestic == 1) {
    // Gets new statestic for current week
    $.ajax({
      type: "GET",
      url: 'get_statestic',
      data: {
        'user_category': category,
        'user_product': product
      },
      success: function (result) {
        $('#bokeh_graph').html(result);
        var x = document.getElementById("totaltime_graph").value;
        document.getElementById("Change_circle_text").innerHTML = " " + x;
      },
    });
  } else if (show_statestic == 2) {
    // Gets new statestic for year
    $.ajax({
      type: "GET",
      url: 'get_statestic_year',
      data: {
        'user_category': category,
        'user_product': product
      },
      success: function (result) {
        $('#bokeh_graph').html(result);
        var x = document.getElementById("totaltime_graph").value;
        document.getElementById("Change_circle_text").innerHTML = " " + x;
      },
    });
  } else if (show_statestic == 3) {
    // Gets new statestic for month
    $.ajax({
      type: "GET",
      url: 'get_statestic_month',
      data: {
        'user_category': category,
        'user_product': product,
        'month': current_month,
      },
      success: function (result) {
        $('#bokeh_graph').html(result);
        var x = document.getElementById("totaltime_graph").value;
        document.getElementById("Change_circle_text").innerHTML = " " + x;
      },
    });
  }

});


// Submit changes to the statestic for current week
$('#current_week_show').on('click', function () {
  event.preventDefault()
  document.getElementById("month_show").style.display = "none";
  $("#current_year_show").removeClass("button_selected");
  $("#time_journal_show").removeClass("button_selected");
  $("#current_week_show").addClass("button_selected");
  show_statestic = 1;
  //select all checkboxes
  var checkboxes_category = document.getElementsByClassName("Checkbox_category"); //checkbox items
  var checkboxes_product = document.getElementsByClassName("Checkbox_product"); //checkbox items
  for (i = 0; i < checkboxes_category.length; i++) {
    checkboxes_category[i].checked = true;
  }
  for (i = 0; i < checkboxes_product.length; i++) {
    checkboxes_product[i].checked = true;
  }

  var category = [];
  var product = [];
  $.each($("input[name='checkboxCategory']:checked"), function () {
    category.push($(this).val());
  });
  $.each($("input[name='checkboxProduct']:checked"), function () {
    product.push($(this).val());
  });

  // Gets new statestic for current week
  $.ajax({
    type: "GET",
    url: 'get_statestic',
    data: {
      'user_category': category,
      'user_product': product
    },
    success: function (result) {
      $('#bokeh_graph').html(result)
      var x = document.getElementById("totaltime_graph").value;
      document.getElementById("Change_circle_text").innerHTML = " " + x;
    },
  });
});


// Checks if month button is pressed and gets the month statestic
$(".month_buttons").click(function (e) {
  var idClicked = e.target.id;
  $(".month_buttons").removeClass("button_selected");
  $("#" + idClicked).addClass("button_selected");
  current_month = idClicked;

  var category = [];
  var product = [];
  $.each($("input[name='checkboxCategory']:checked"), function () {
    category.push($(this).val());
  });
  $.each($("input[name='checkboxProduct']:checked"), function () {
    product.push($(this).val());
  });



  $.ajax({
    type: "GET",
    url: 'get_statestic_month',
    data: {
      'user_category': category,
      'user_product': product,
      'month': idClicked,
    },
    success: function (result) {
      $('#bokeh_graph').html(result)
    },
  });
});


// Submit changes to the statestic for current week
$('#current_year_show').on('click', function () {
  event.preventDefault()

  document.getElementById("month_show").style.display = "none";
  $("#current_week_show").removeClass("button_selected");
  $("#time_journal_show").removeClass("button_selected");
  $("#current_year_show").addClass("button_selected");

  show_statestic = 2;
  //select all checkboxes
  var checkboxes_category = document.getElementsByClassName("Checkbox_category"); //checkbox items
  var checkboxes_product = document.getElementsByClassName("Checkbox_product"); //checkbox items
  for (i = 0; i < checkboxes_category.length; i++) {
    checkboxes_category[i].checked = true;
  }
  for (i = 0; i < checkboxes_product.length; i++) {
    checkboxes_product[i].checked = true;
  }

  var category = [];
  var product = [];
  $.each($("input[name='checkboxCategory']:checked"), function () {
    category.push($(this).val());
  });
  $.each($("input[name='checkboxProduct']:checked"), function () {
    product.push($(this).val());
  });

  // Gets new statestic for current week
  $.ajax({
    type: "GET",
    url: 'get_statestic_year',
    data: {
      'user_category': category,
      'user_product': product,
    },
    success: function (result) {
      $('#bokeh_graph').html(result)
      var x = document.getElementById("totaltime_graph").value;
      document.getElementById("Change_circle_text").innerHTML = " " + x;
    },
  });
});


// Time journal
$('#time_journal_show').on('click', function () {
  event.preventDefault()
  show_statestic = 3;
  document.getElementById("month_show").style.display = "block";
  $("#current_year_show").removeClass("button_selected");
  $("#current_week_show").removeClass("button_selected");
  $("#time_journal_show").addClass("button_selected");
  $(".month_buttons").first().addClass("button_selected");

  //select all checkboxes
  var checkboxes_category = document.getElementsByClassName("Checkbox_category"); //checkbox items
  var checkboxes_product = document.getElementsByClassName("Checkbox_product"); //checkbox items
  for (i = 0; i < checkboxes_category.length; i++) {
    checkboxes_category[i].checked = true;
  }
  for (i = 0; i < checkboxes_product.length; i++) {
    checkboxes_product[i].checked = true;
  }
  var category = [];
  var product = [];
  $.each($("input[name='checkboxCategory']:checked"), function () {
    category.push($(this).val());
  });
  $.each($("input[name='checkboxProduct']:checked"), function () {
    product.push($(this).val());
  });

  // Get the first month the user has
  var month_choosen = $(".month_buttons").first().val();
  current_month = $(".month_buttons").first().val();

  // Gets new statestic for current week
  $.ajax({
    type: "GET",
    url: 'get_statestic_month',
    data: {
      'user_category': category,
      'user_product': product,
      'month': month_choosen,
    },
    success: function (result) {
      $('#bokeh_graph').html(result)
      var x = document.getElementById("totaltime_graph").value;
      document.getElementById("Change_circle_text").innerHTML = " " + x;
    },
  });
});


// For modal
$('#modal_project').on('click', function () {
  event.preventDefault()
  document.getElementById('modal_product_link').click();
});
$('#modal_category').on('click', function () {
  event.preventDefault()
  document.getElementById('modal_category_link').click();
});