VoteButton = require './VoteButton.coffee'

init = (el)->
  $feeds = $(el)
  $btnReload = $('#btn-reload-feeds')
  $tipLoading = $('#feeds-loading-tip')
  $tipLoaded = $('#feeds-loaded-tip')
  pages = parseInt $feeds.data('pages')
  loading = false
  page = 1

  load = ()->
    loading = true
    $.ajax
      data:
        page: page
        target: el
      success: (html)->
        $tipLoading.before html
        VoteButton.init el
        if page >= pages
          $tipLoading.hide()
          $tipLoaded.show()
        else
          $tipLoaded.hide()
        setTimeout ()->
          loading = false
        , 500
      error: (res)->
        $tipLoading.addClass 'has-error'

  checkLoad = ()->
    $last = $feeds.find('.feed').last()
    scrollTop = $(window).scrollTop() + $(window).height()
    if scrollTop < $last.offset().top - $last.height()
      return
    if loading or page >= pages
      return
    page += 1
    load()

  if isNaN pages
    return console.error 'invalid data-pages attribute'
  VoteButton.init el
  $(window).on 'scroll', checkLoad
  $btnReload.on 'click', ()->
    $tipLoading.removeClass 'has-error'
    load()
  checkLoad()

module.exports = init: init
