current_email = request.user.email
new_email = request.context["prompt_data"]["email"]

if new_email == "":
  return False

if new_email == current_email:
  return False

context["flow_plan"].context["pending_user"] = request.user
request.context["flow_plan"].context["email"] = request.context["prompt_data"]["email"]

ak_message("Waiting for email verification. If you need the cancel the change, log out and log back into your account.")

return True