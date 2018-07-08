import '../stylesheets/main.scss'
import Index from './views/Index'
import Dashboard from './views/Dashboard'
import ReposNew from  './views/ReposNew'
import TopicsShow from './views/TopicsShow.coffee'
import TopicsIndex from './views/TopicsIndex.coffee'
import SnippetsIndex from './views/SnippetsIndex'
import ImportIssueModal from './components/ImportIssueModal'

const routes = {
  'index': Index,
  'explore': Index,
  'dashboard.recent': Dashboard,
  'dashboard.pinned': Dashboard,
  'topics.show': TopicsShow,
  'topics.index': TopicsIndex,
  'snippets.index': SnippetsIndex,
  'repos.new': ReposNew
}

const view = routes[app.endpoint]

if (view) {
  view.init()
}

new ImportIssueModal()
