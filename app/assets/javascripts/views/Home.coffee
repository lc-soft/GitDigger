VoteButton = require '../components/VoteButton.coffee'
FollowTopicButton = require '../components/FollowTopicButton.coffee'

init = ()->
  $feeds = $('#home-feeds')
  $btnReload = $('#btn-reload-feeds')
  $tipLoading = $('#feeds-loading-tip')
  $tipLoaded = $('#feeds-loaded-tip')
  pages = $feeds.data 'pages'
  loading = false
  page = 1

  load = ()->
    loading = true
    $.ajax
      data:
        page: page
        target: '#home-feeds'
      success: (html)->
        $tipLoading.before html
        VoteButton.init $feeds
        if page >= pages
          $tipLoading.hide()
          $tipLoaded.show()
        else
          $tipLoaded.hide()
        setTimeout ()->
          loading = false
        , 1000
      error: (res)->
        $tipLoading.addClass 'has-error'

  checkLoad = ()->
    $last = $feeds.find('.feed-card').last()
    scrollTop = $(window).scrollTop() + $(window).height()
    if scrollTop < $last.offset().top - $last.height() * 2
      return
    if loading or page >= pages
      return
    page += 1
    load()

  VoteButton.init $feeds
  FollowTopicButton.init $feeds
  $('.dropdown-toggle').dropdown()
  $(window).on 'scroll', checkLoad
  $btnReload.on 'click', load
  checkLoad()

module.exports = init: init
