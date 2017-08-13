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

$('.btn-follow-topic').on 'click', ()->
  $btn = $(this)
  url = $btn.data 'url' 
  from_ = $btn.data 'from'
  following = $btn.data 'following'
  count = $btn.data 'followers-count'
  if !url
    window.location.href = '/login'
    return
  if following
    count -= 1
    method = 'DELETE'
    following = 0
    text = $btn.data 'text-follow'
  else
    count += 1
    method = 'POST'
    following = 1
    text = $btn.data 'text-following'
  $btn.prop 'disabled', true
  $.ajax
    url: url
    type: method
    success: (res)->
      $btn.data 'following', following
      $btn.data 'followers-count', count
      $btn.parent().find('.followers-count').text count
      if from_ is 'feeds'
        if following
          $btn.addClass('btn-outline-secondary')
          $btn.removeClass('btn-primary-light')
        else
          $btn.removeClass('btn-outline-secondary')
          $btn.addClass('btn-primary-light')
        $btn.find('.text').text text
      else
        if following
          $btn.addClass('btn-secondary').removeClass('btn-success')
        else
          $btn.removeClass('btn-secondary').addClass('btn-success')
        $btn.text text
      $btn.prop 'disabled', false
    error: (res)->
      res = res.responseJSON
      $btn.prop 'disabled', false
      alert(res.message) if res and res.message
