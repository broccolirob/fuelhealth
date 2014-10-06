$ ->
  showPoints = (e) ->
    points = $(@).data 'points'
    $(@).append "#{points}"

  $(".new").click showPoints