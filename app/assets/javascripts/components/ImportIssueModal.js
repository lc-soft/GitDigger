function ImportIssueModal() {
  this.$modal = $('#import-issue-modal') 
  this.$url = $('#issue-url-input')
  this.$form = this.$modal.find('form')
  this.$submit = this.$modal.find('.btn-primary')
  this.$submit.on('click', () => this.validate())
  this.submitText = this.$submit.text().trim()
}

ImportIssueModal.prototype.validate = function validate() {
  var url = this.$url.val()

  url = url.replace('//github.com/', '//api.github.com/repos/')
  if (url.indexOf('//api.github.com/repos/') < 0) {
    this.$url
      .addClass('is-invalid')
      .next('.invalid-feedback')
      .text('Please provide a valid issue url')
    return
  }

  this.$url.removeClass('is-invalid')
  this.$submit
    .addClass('disabled')
    .prop('disabled', true)
    .text(this.$submit.data('text-checking'))
  $.getJSON(url, (data) => {
    this.$submit
      .removeClass('disabled')
      .prop('disabled', false)
      .text(this.submitText)
    if ((data instanceof Object) && data.url === url && data.title) {
      this.submit()
    } else {
      this.$url
        .addClass('is-invalid')
        .next('.invalid-feedback')
        .text('Please provide a valid issue url')
    }
  })
}

ImportIssueModal.prototype.submit = function submit() {
  this.$submit
    .addClass('disabled')
    .prop('disabled', true)
    .text(this.$submit.data('text-importing'))
  $.ajax({
    url: app.api.issues,
    method: 'POST',
    data: {
      html_url: this.$url.val()
    }
  })
  .done((res) => {
    console.log(res)
    this.$submit
      .removeClass('disabled')
      .prop('disabled', false)
      .text(this.submitText)
  })
  .fail((xhr, msg) => {
    if (typeof xhr.responseJSON !== 'undefined') {
      msg = xhr.responseJSON.message
    }
    this.$url
      .addClass('is-invalid')
      .next('.invalid-feedback')
      .text(msg)
    this.$submit
      .removeClass('disabled')
      .prop('disabled', false)
      .text(this.submitText)
  })
}

export default ImportIssueModal
