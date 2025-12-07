# Scope: profile

# oCIS does not sync groups after first login with OIDC, so we keep this simple
# Note that groups and roles are treated differently in oCIS

if user.is_superuser:
  groups = [ "admin" ]
  role = "admin"
else:
  groups = [ "metropolis-vip" ]
  role = "user"

if request.user.name == "":
  request.user.name = request.user.username

return {
  "preferred_username": request.user.username,
  "name": request.user.name,
  "groups": groups,
  "role": role
}