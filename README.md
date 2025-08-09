# System Setup

- Create `/etc/ssh/sshd_config.d/10-certs.conf`:

```
PermitRootLogin prohibit-password
```
- Restart sshd
- Add NGINX's ssh key to `/root/.ssh/authorized_keys`
- rsync TLS certificates to `/srv/authentik/authentik/certs/auth.metropolis.nexus`

# Authentik Setup

Enter the admin section and configure the following:

## Directory

### Groups
- Create metropolis-default

## Customization, Flow and Stages

Import from the flows directory.

### Notes:
- Cloudflare Turnstile is used with metropolis-enrollment-flow. It is not included here to avoid leaking secrets.
- metropolis-recovery-flow should "Require no authentication", but we are using No requirement temporarily due to [this bug](https://github.com/goauthentik/authentik/issues/13714).
- Stage binding for the recovery flow is copied from the default flow. It's a bit strange how policy evaluation is configured there. Need further investigation later.
- We are changing the default password change stage and flow instead of making our own due to [this issue](https://github.com/goauthentik/authentik/issues/6388).

## System

### Brands

#### authentik-default
- Disable "Default"

#### metropolis.nexus
- Domain: auth.metropolis.nexus
- Enable "Default": Make this the default brand
- Title: Metropolis Nexus
- Default flow background: /media/public/flow-backgrounds/chicago.jpg
- Default flows
  - Authentication flow: metropolis-authentication-flow
  - Invalidation flow: metropolis-invalidation-flow
  - Recovery flow: metropolis-recovery-flow
  - User settings flow: metropolis-user-settings-flow
- Web Certificate: auth.metropolis.nexus

### Settings
- Avatars: none
- Allow users to change email
- Disable "Require reason for impersonation"

# Cleanup

Delete all of the following:

## Flow and Stages

### Flows
- default-authentication-flow
- default-authenticator-totp-setup
- default-source-authentication
- default-enrollment-flow
- default-source-enrollment
- default-source-pre-authentication
- default-recovery-flow
- default-user-settings-flow
- initial-setup

### Stages
All stages not used by a flow

### Prompts
All flows not used by a stage 

## Customization

### Policies
All policies not assigned to at least 1 object

## System

### Brands
- authentik-default

# Update akadmin
Directory -> User -> akadmin
- Clear out name
- Clear out email
