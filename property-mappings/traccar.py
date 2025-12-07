# Scope: profile

# Extract all groups the user is a member of
groups = [group.name for group in user.ak_groups.all()]

if request.user.name == "":
  request.user.name = request.user.username

return {
  "username": request.user.username,
  "name": request.user.name,
  "groups": groups
}
