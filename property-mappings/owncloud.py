# Scope: profile

# Note that groups and roles are treated differently in oCIS
if user.is_superuser:
  role = "admin"
else:
  role = "user"

if request.user.name == "":
  request.user.name = request.user.username

return {
  "name": request.user.name,
  "preferred_username": request.user.username,
  "groups": [group.name for group in user.ak_groups.all()],
  "role": role
}
