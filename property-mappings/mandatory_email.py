email = user.email

if email == "":
  email = user.username + "@auth.metropolis.nexus"

return {
  "email": email,
  "email_verified": True
}