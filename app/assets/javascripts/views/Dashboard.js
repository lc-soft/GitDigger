import FeedList from '../components/FeedList'
import FollowTopicButton from '../components/FollowTopicButton.coffee'

export default {
  init() {
    FeedList.init('#feeds-container')
    FollowTopicButton.init('#feeds-container')
    $('.dropdown-toggle').dropdown()
  }
}
