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
  $('#delete_btn').click(function(){
    if($('tbody td input[type=checkbox]:checked').length == 0){
      alert("Please select one or more entries to delete.")
    }
  });
});
