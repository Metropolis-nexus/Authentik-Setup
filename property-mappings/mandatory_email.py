# Scope: email

email = request.user.email

if email == "":
  email = user.username.lower() + "@auth.metropolis.nexus"

return {
  "email": email,
  "email_verified": True
}