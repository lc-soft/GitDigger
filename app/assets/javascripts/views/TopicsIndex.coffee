FollowTopicButton = require '../components/FollowTopicButton.coffee'

init = ()->
  FollowTopicButton.init '#site-content'
  $('.dropdown-toggle').dropdown()

module.exports = init: init
