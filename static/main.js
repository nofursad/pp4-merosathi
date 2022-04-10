$(document).ready(function() {
    $('#update-profile').click(function(){
        $('.ui.modal')
  .modal('show');
    })

    $('.like-form').submit(function(e) {
      e.preventDefault()
      
      const post_id = $(this).attr('id')
      
      const likeBtn = $(`.like-btn${post_id}`).hasClass('blue')

      const url = $(this).attr('action')
      
      let counter;
      const likes = $(`.like-counter${post_id}`).text()
      const convLikes = parseInt(likes)
      
      
      $.ajax({
        type: 'POST',
        url: url,
        data: {
          'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val(),
          'post_id': post_id,
        },
        success: function(response) {
          if(likeBtn) {
            $(`.like-btn${post_id}`).removeClass('blue')
            counter = convLikes - 1
          } else {
            $(`.like-btn${post_id}`).addClass('blue')
            counter = convLikes + 1
          }
          $(`.like-counter${post_id}`).text(counter)
        },
        error: function(response) {
          console.log('error', response)
        }
      })
    })
})

$('.ui.accordion')
  .accordion()
;
