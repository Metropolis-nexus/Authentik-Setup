# Based on https://github.com/goauthentik/authentik/issues/3134

if ak_is_group_member(request.user, name="metropolis_storage"):
  prompt_data = context['prompt_data']['attributes']['sshPublicKey']
  sshKeyList = prompt_data.split("\n")
  context['prompt_data']['attributes']['sshPublicKey'] = sshKeyList
  return True

request.context["prompt_data"]["attributes"]["sshPublicKey"] = []
return True