import '../stylesheets/main.scss'
import Index from './views/Index.coffee'
import TopicsShow from './views/TopicsShow.coffee'
import TopicsIndex from './views/TopicsIndex.coffee'

const routes = {
  'index': Index,
  'recent': Index,
  'pinned': Index,
  'topics.show': TopicsShow,
  'topics.index': TopicsIndex
}

const view = routes[endpoint]

if (view) {
  view.init()
}
