FeedList = require '../components/FeedList.coffee'
FollowTopicButton = require '../components/FollowTopicButton.coffee'

init = ()->
  FeedList.init '#topic-feeds'
  FollowTopicButton.init '#site-content-header'
  $('.dropdown-toggle').dropdown()

module.exports = init: init
