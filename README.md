# Authentik-Setup

## Flow and Stages

### Stages

#### WebAuthn Authenticator Setup Stage
- Name -> metropolis-authenticator-webauthn-setup
- Authenticator type name -> WebAuthn device
- User verification -> Required: User verification must occur
- Resident Key Requirement -> Discouraged: The authenticator should not create a dedicated credential
- Authenticator attachment -> A "roaming" authenticator

#### Authenticator Validation Stage
- Name -> metropolis-authentication-mfa-validation
- Device classes -> WebAuthn Authenticators
- Not configured action -> Force the user to configure an authenticator
- WebAuthn User verification -> User verification must occur
- Configuration stages -> metropolis-authenticator-webauthn-setup

### Flows

#### Create a new authentication flow

- Name -> Welcome to Metropolis Nexus!
- Tite -> Welcome to Metropolis Nexus!
- Slug -> metropolis-authentication-flow
- Designation -> Authentication
- Authentication -> No requirement
- Denied action -> MESSAGE_CONTINUE
- Policy engine mode -> any

Stage bindings:
- default-authentication-identification -> 10
- default-authentication-password -> 20
- metropolis-authentication-mfa-validation -> 30
- default-authentication-login -> 100

## System

### Brands

#### authentik-default
- Disable "Default"

#### metropolis.nexus
- Domain: metropolis.nexus
- Enable "Default" -> Make this the default brand
- Title -> Metropolis Nexus
- Default flows
  - Authentication flow -> metropolis-authentication-flow
  - Invalidation flow -> default-invalidation-flow
  - User settings flow -> default-user-settings-flow

### Settings
- **DO NOT** enable "Allow users to change email" (See [this discussion](https://github.com/goauthentik/authentik/issues/4097))
- Disable "Require reason for impersonation"
