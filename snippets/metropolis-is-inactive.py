# Check if the user is inactive or not. Combine this with the email stage to send another email if the user is trying to login before having their email verified.

return not request.context["pending_user"].is_active