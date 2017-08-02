require '../stylesheets/main.scss'

$header = $('#site-header')
$('.dropdown-toggle').dropdown()

stickNavbar = ()->
  top = $(window).scrollTop()
  if top > 56
    $header.parent().addClass 'header-fixed-top'
  else
    $header.parent().removeClass 'header-fixed-top'

if $header.find('.navbar').length > 1
  $(window).on 'scroll', stickNavbar
  stickNavbar()
