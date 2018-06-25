function loadDataFromRemote(onSuccess, onError) {
  const user = window.app.user
  if (!user.login) {
    return callback()
  }
  $.ajax({
    url: 'https://api.github.com/users/' + user.github_username + '/repos',
  }).done(function (res) {
    if (res.message) {
      onError(res.message)
    } else {
      onSuccess(res)
    }
  }).fail(function (xhr, msg) {
    onError(msg)
  })
}

function loadData(onSuccess, onError) {
  const store = window.localStorage
  if (typeof store === 'undefined' ||
    typeof store.userPublicRepos === 'undefined') {
    return loadDataFromRemote(onSuccess, onError)
  }
  const time = Number(store.userPublicReposTime)
  if (time && (new Date()).getTime() - time > 15 * 3600 * 1000) {
    return loadDataFromRemote(onSuccess, onError)
  }
  return onSuccess(JSON.parse(store.userPublicRepos))
}

function saveData(repos) {
  if (typeof window.localStorage === 'undefined') {
    return false
  }
  const data = repos.map(function (repo) {
    return {
      html_url: repo.html_url,
      full_name: repo.full_name
    }
  })
  window.localStorage.userPublicRepos = JSON.stringify(data)
  window.localStorage.userPublicReposTime = (new Date()).getTime()
}

export default {
  init() {
    const $el = $('#select-user-repo')
    const $btn = $el.parents('form').find('input[type="submit"]')
    
    $btn.addClass('disabled').prop('disabled', true)
    loadData(function (repos) {
      if (repos.length < 1) {
        $el.addClass('is-invalid').next('.invalid-feedback').text($el.data('text-empty'))
        return
      }
      repos.forEach(function (repo) {
        $el.append('<option value="' + repo.html_url + '">' + repo.full_name + '</option>')
      })
      $btn.removeClass('disabled').prop('disabled', false)
      saveData(repos)
    }, function (msg) {
      $el.addClass('is-invalid').next('.invalid-feedback').text(msg)
    })
  }
}
