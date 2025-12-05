# Extract all groups the user is a member of
groups = [group.name for group in user.ak_groups.all()]

# In Nextcloud, administrators must be members of a fixed group called "admin".

# If a user is an admin in authentik, ensure that "admin" is appended to their group list.
if user.is_superuser and "admin" not in groups:
  groups.append("admin")

return {
  "name": request.user.name,
  "groups": groups,
  # Set a quota by using the "nextcloud_quota" property in the user's attributes
  "quota": user.group_attributes().get("nextcloud_quota", "20 GB"),
  # To connect an existing Nextcloud user, set "nextcloud_user_id" to the Nextcloud username.
  "user_id": user.attributes.get("nextcloud_user_id", str(user.username)),
}