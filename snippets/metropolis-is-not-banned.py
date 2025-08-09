# Make sure that the user is not in the banned group

if ak_is_group_member(request.context["pending_user"], name="metropolis-banned"):
  ak_message("Account banned.")
  return False
return True