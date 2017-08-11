require '../stylesheets/main.scss'

$('.dropdown-toggle').dropdown()
$('.btn-vote').on 'click', ()->
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
  count = parseInt $btn.data('vote-count')
  if isNaN count
    return
  $btn.prop 'disabled', true
  $.ajax
    url: url
    type: 'PUT'
    success: (res)->
      $btn.find('.text').text text
      $btn.data 'vote-count', ++count
      $btn.find('.count').text count
    error: (res)->
      $btn.prop 'disabled', false
      alert(res.message) if res.message
