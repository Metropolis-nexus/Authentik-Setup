# Scope: profile

if request.user.name == "":
  request.user.name = request.user.username

return {
  "preferred_username": request.user.username,
  "name": request.user.name,
  "groups": [group.name for group in user.ak_groups.all()]
}
