$(document).ready(function() {
  /*
    Hide the success message after a few seconds
  */
  var delay_time = 2000;
  var animation_time = 500;
  $('#success_message').delay(delay_time).hide(animation_time);


  /*
    Show alert when delete is clicked but no entries are selected
  */
  $('form.list_form').submit(function(e){
    if($('tbody td input[type=checkbox]:checked').length == 0){
      alert("Please select one or more rows to delete.");
      e.preventDefault();
    }
  });


  /*
    Highlight rows while mouse is hovering over
  */
  var current_colour = '';
  $('form.list_form tbody tr').mouseenter(function(e){
    var row = $(e.currentTarget);
    current_colour = row.css('background-color');
    row.css('background-color', '#ddd');
  }).mouseleave(function(e){
    var row = $(e.currentTarget);
    row.css('background-color', current_colour);
  });


  /*
    Select a rows checkbox when the row is clicked
  */
  $('form.list_form tbody tr td').click(function(e){
    var checkbox = $(e.currentTarget).parent().children().children().filter('input')
    if(! $(e.currentTarget).children().is('[type=checkbox]')){
      if(checkbox.is(':checked')){
        checkbox.prop( "checked", false );
      }else{
        checkbox.prop( "checked", true );
      }
    }
  });
});
