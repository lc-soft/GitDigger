function getRatingLevel(rating) {
  const data = [
    [0, 'so easy'],
    [2, 'easy'],
    [4, 'normal'],
    [6, 'difficult'],
    [8, 'so difficult']
  ]
  for (let i = data.length - 1; i >= 0; --i) {
      if (rating > data[i][0]) {
          return [i, data[i][1]]
      }
  }
  return [0, data[1]]
}

export default {
  init(el) {
    const app = window.app
    const api = app.api.snippet_voters

    $(el).find('[data-target="snippet"]').on('click', function () {
      const $this = $(this)
      const id = $this.data('target-id')
      const value = $this.data('value')
      const $snippet = $this.parents('.snippet')
      const $rating = $snippet.find('.js-rating')

      $.ajax({
        type: 'PUT',
        data: {
          rating: value
        },
        url: api.replace(':id', id).replace(':username', app.user.login)
      }).done(function (res) {
        const s = res.snippet
        const level = getRatingLevel(s.rating)
        $snippet.find('.js-ratings-count').text(s.ratings_count)
        $snippet.find('.js-rating-text').text(level[1])
        $rating.data('value', s.rating).attr('data-value', s.rating)
        .next('.js-rating-text')
          .data('value', level[0])
          .attr('data-value', level[0])
      }).fail(function (xhr, msg) {
        console.log(xhr.responseJSON.message)
      })
    })
  }
}
