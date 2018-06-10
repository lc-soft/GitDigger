import '../stylesheets/main.scss'
import Index from './views/Index.coffee'
import TopicsShow from './views/TopicsShow.coffee'
import TopicsIndex from './views/TopicsIndex.coffee'
import ImportIssueModal from './components/ImportIssueModal'

const routes = {
  'index': Index,
  'recent': Index,
  'pinned': Index,
  'topics.show': TopicsShow,
  'topics.index': TopicsIndex
}

const view = routes[app.endpoint]

if (view) {
  view.init()
}

new ImportIssueModal()
