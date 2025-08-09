# Verify email when changed from user settings
# Solves https://github.com/goauthentik/authentik/issues/4097 when combined with an email stage

current = request.user.email
new = request.context["prompt_data"]["email"]

if new == '':
    return False

if new == current:
    return False

context["flow_plan"].context["pending_user"] = request.user
request.context["flow_plan"].context["email"] = request.context["prompt_data"]["email"]

return True