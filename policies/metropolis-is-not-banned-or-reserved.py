if ak_is_group_member(request.context["pending_user"], name="metropolis_banned"):
  ak_message("Account banned.")
  return False

elif ak_is_group_member(request.context["pending_user"], name="metropolis_reserved"):
  ak_message("Account reserved. How did you even get this far?!")
  return False

return True
