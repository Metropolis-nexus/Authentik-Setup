# Scope: keycloak

if user.is_superuser:
  role = "admin"
else:
  role = "user"

return {
  "role": role
}
