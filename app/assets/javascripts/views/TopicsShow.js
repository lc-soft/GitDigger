import FeedList from '../components/FeedList'
import FollowTopicButton from '../components/FollowTopicButton.coffee'

export default {
  init() {
    FeedList.init('#topic-feeds')
    FollowTopicButton.init('#site-content-header')
    $('.dropdown-toggle').dropdown()
  }
}
