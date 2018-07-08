import List from './List'
import VoteButton from './VoteButton.coffee'

export default {
  init(el) {
    List.init(el, 'feeds', function () {
      VoteButton.init(el)
    })
  }
}
