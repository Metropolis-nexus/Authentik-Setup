# Authentik-Setup

## Directory

### Groups
- Create metropolis-default

## Flow and Stages

### Importing stuff
Download link: https://docs.goauthentik.io/docs/add-secure-apps/flows-stages/flow/examples/flows
Download and import "Enrollment with email verification".

### Stages

#### Identification Stage
- Name -> metropolis-authentication-identification
- User fields -> Username, email
- Password stage -> default-authentication-password
- Enable Case insensitive matching
- Enable Pretend user exists
- Enable Show matched user
- Enable "Remember me on this device"
- Enrollment flow -> default-enrollment-flow

#### WebAuthn Authenticator Setup Stage
- Name -> metropolis-authenticator-webauthn-setup
- Authenticator type name -> WebAuthn device
- User verification -> Required: User verification must occur
- Resident Key Requirement -> Discouraged: The authenticator should not create a dedicated credential
- Authenticator attachment -> A "roaming" authenticator
- Configuration flow -> default-authenticator-webauthn-setup

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
- Enable compatibility mode
- Denied action -> MESSAGE_CONTINUE
- Policy engine mode -> any

Stage bindings:
- metropolis-authentication-identification -> 10
- metropolis-authentication-mfa-validation -> 30
- default-authentication-login -> 100

### Cleanup
- Delete initial-setup flow
- Delete stage-default-oobe-password stage

## System

### Brands

#### authentik-default
- Disable "Default"

#### metropolis.nexus
- Domain: auth.metropolis.nexus
- Enable "Default" -> Make this the default brand
- Title -> Metropolis Nexus
- Default flows
  - Authentication flow -> metropolis-authentication-flow
  - Invalidation flow -> default-invalidation-flow
  - User settings flow -> default-user-settings-flow

#### Cleanup
- Delete authentik-default

### Settings
- **DO NOT** enable "Allow users to change email" (See [this discussion](https://github.com/goauthentik/authentik/issues/4097))
- Disable "Require reason for impersonation"
