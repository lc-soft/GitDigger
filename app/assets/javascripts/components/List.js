export default {
  /**
   * 初始化列表，使之能在滚动时自动加载内容
   * @param {string} el 列表元素
   * @param {string} name 数据名称
   * @param {function} callback 回调，在每次加载完内容后调用
   */
  init(el, name, callback) {
    var $list = $(el)
    var $btnReload = $(`#btn-reload-${name}`)
    var $tipLoading = $(`#${name}-loading-tip`)
    var $tipLoaded = $(`#${name}-loaded-tip`)
    var pages = parseInt($list.data('pages'))
    var loading = false
    var page = 1
  
    function load() {
      loading = true
      $.ajax({
        data: {
          page: page,
          target: el
        }
      }).done(function (html) {
          $tipLoading.before(html)
          callback()
          if (page >= pages) {
            $tipLoading.hide()
            $tipLoaded.show()
          } else {
            $tipLoaded.hide()
          }
          setTimeout(function () {
            loading = false
          }, 500)
      }).fail(function () {
        $tipLoading.addClass('has-error')
      })
    }
  
    function checkLoad() {
      var $last = $list.children().last()
      var scrollTop = $(window).scrollTop() + $(window).height()

      if (scrollTop < $last.offset().top - $last.height()) {
        return
      }
      if (loading || page >= pages) {
        return
      }
      page += 1
      load()
    }
  
    if (isNaN(pages)) {
      return console.error('invalid data-pages attribute')
    }
    callback()
    if (pages > 0) {
      $(window).on('scroll', checkLoad)
      checkLoad()
    }
    $btnReload.on('click', function () {
      $tipLoading.removeClass('has-error')
      load()
    })
  }
}
