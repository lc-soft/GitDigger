require '../stylesheets/main.scss'

routes =
  'index': require './views/Index.coffee'
  'topics.show': require './views/TopicsShow.coffee'

view = routes[endpoint]
view.init() if view
