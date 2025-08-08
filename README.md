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
- default-authentication-identification
- default-authenticator-totp-setup
- default-authenticator-webauthn-setup
- default-authentication-mfa-validation
- default-enrollment-prompt-first
- default-enrollment-prompt-second
- default-enrollment-user-write
- default-source-authentication-login
- default-source-enrollment-login
- default-source-enrollment-prompt
- default-source-enrollment-write
- default-invalidation-flow
- default-user-settings
- default-user-settings-write
- stage-default-oobe-password

### Prompts
- default-enrollment-field-email
- default-enrollment-field-name
- default-source-enrollment-field-username
- default-user-settings-field-email
- default-user-settings-field-name
- initial-setup-field-email
- initial-setup-field-header
- initial-setup-field-password
- initial-setup-field-password-repeat

## Customization

### Policies
- default-authentication-flow-password-stage
- default-source-authentication-if-sso
- default-source-enrollment-if-sso
- default-source-enrollment-if-username
- default-oobe-flow-set-authentication
- default-oobe-password-usable
- default-oobe-prefill-user

## System

### Brands
- authentik-default

# Update akadmin
Directory -> User -> akadmin
- Clear out name
- Clear out email
