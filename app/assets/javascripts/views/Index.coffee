FeedList = require '../components/FeedList.coffee'
FollowTopicButton = require '../components/FollowTopicButton.coffee'

init = ()->
  FeedList.init '#home-feeds'
  FollowTopicButton.init '#home-feeds'
  $('.dropdown-toggle').dropdown()

module.exports = init: init
