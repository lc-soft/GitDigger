init = (el)->
  $(el + ' .btn-vote').off('click.vote').on 'click.vote', ()->
    $btn = $(this)
    voted = $btn.data 'voted'
    url = $btn.data 'vote-url' 
    action = $btn.data 'action'
    if !url
      window.location.href = '/login'
      return
    if voted
      return
    text = $btn.data 'text-upvoted'
    count = parseInt $btn.data 'vote-count'
    $btn.prop 'disabled', true
    $.ajax
      url: url
      type: 'PUT'
      success: (res)->
        $btn.find('.text').text text
        $btn.data 'vote-count', ++count
        $btn.find('.count').text count
        $btn.addClass('btn-outline-secondary').removeClass('btn-primary-light')
      error: (res)->
        res = res.responseJSON
        $btn.prop 'disabled', false
        alert(res.message) if res and res.message

module.exports = init: init
