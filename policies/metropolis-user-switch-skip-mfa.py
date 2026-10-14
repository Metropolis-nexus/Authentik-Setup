from datetime import timedelta

from authentik.core.user_switching import is_user_switch_target_recent

return not is_user_switch_target_recent(request, timedelta(hours=72))