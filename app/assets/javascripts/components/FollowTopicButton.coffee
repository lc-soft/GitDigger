init = (el)->
  $(el + ' .btn-follow-topic').off('click.follow').on 'click.follow', ()->
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
        $('#followers-count').text count
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
        if res.status is 401
          window.location.href = '/login'
          return
        res = res.responseJSON
        $btn.prop 'disabled', false
        alert(res.message) if res and res.message

module.exports = init: init
