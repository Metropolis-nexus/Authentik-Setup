# Scope: profile

# Extract all groups the user is a member of
groups = [group.name for group in user.ak_groups.all()]

# Note that groups and roles are treated differently in oCIS
if user.is_superuser:
  role = "admin"
else:
  role = "user"

if request.user.name == "":
  request.user.name = request.user.username

return {
  "username": request.user.username,
  "name": request.user.name,
  "groups": groups,
  "role": role
}
