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
- Importing the flows will be a little tricky since there is a lot of circular dependencies and Authentik does not let you import multiple files at the same time. You'll need to adjust the flows to work around this issue.
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
- Attributes:

```
settings:
  theme:
    base: dark
    background: >
      background: url('/media/public/flow-backgrounds/chicago.jpg');
      filter: blur(8px) brightness(50%);
      background-position: center;
      background-repeat: no-repeat;
      background-size: cover;

```

### Settings
- Avatars: none
- Allow users to change email
- Event rentention: days=90
- Disable "Require reason for impersonation"

# Cleanup

Delete all of the following:

## Flow and Stages

### Flows
All default flows except default-password-change

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
