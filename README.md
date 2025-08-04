# Authentik-Setup

## Directory

### Groups
- Create metropolis-default

## Flow and Stages

### Importing stuff
Download link: https://docs.goauthentik.io/docs/add-secure-apps/flows-stages/flow/examples/flows
Download and import "Enrollment with email verification".

### Policies

#### Expression Policy
- Name -> metropolis-geoip
- Expression -> `return not context["geoip"]["country"] == "GB"`

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

### User Write Stage
- Name -> metropolis-enrollment-user-write
- Always create new users
- Disable Create user as inactive
- User type -> Internal
- Group -> metropolis-default

### User Write Stage
- Name -> metropolis-user-settings-write
- Never create users
- Uncheck create user as inactive
- User type -> Internal

#### WebAuthn Authenticator Setup Stage
- Name -> metropolis-authenticator-webauthn-setup
- Authenticator type name -> WebAuthn device
- User verification -> Required: User verification must occur
- Resident Key Requirement -> Discouraged: The authenticator should not create a dedicated credential
- Authenticator attachment -> A "roaming" authenticator
- Configuration flow -> default-authenticator-webauthn-setup

#### Authenticator Validation Stage
- Name -> metropolis-authentication-mfa-validation
- Device classes -> Static Tokens, TOTP Authenticators, WebAuthn Authenticators
- Not configured action -> Force the user to configure an authenticator
- WebAuthn User verification -> User verification must occur
- Configuration stages -> metropolis-authenticator-webauthn-setup

### Prompt Stage
- Fields:
  - default-user-settings-field-locale
  - default-user-settings-field-name
    
- Validation policies
  - default-user-settings-authorization

### Flows

#### metropolis-authentication-flow

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

Policy bindings:
- metropolis-geoip -> 10 -> Don't pass

#### metropolis-enrollment-flow
- Name -> Metropolis enrollment Flow
- Title -> Welcome to Metropolis Nexus!
- Slug -> metropolis-enrollment-flow
- Designation -> Enrollment
- Authentication -> Require no authentication
- Enable compatibility mode
- Denied action -> MESSAGE_CONTINUE
- Policy engine mode -> any

Stage bindings:
- default-enrollment-prompt-first -> 10
- metropolis-enrollment-user-write -> 20
- default-enrollment-user-login -> 100

Policy bindings:
- metropolis-geoip -> 10 -> Don't pass

#### metropolis-user-settings-flow
- Name -> Metropolis user settings
- Title -> Update your info
- slug -> metropolis-user-settings-flow
- Designation -> Stage Configuration
- Authentication -> Require authentication
- Enable compatibility mode
- Policy engine mode -> any

Stage bindings:
- metropolis-user-settings -> 20
- metropolis-user-settings-write -> 100

### Update
- Stage -> metropolis-authentication-identification -> Change enrollment flow to metropolis-enrollment-flow

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
  - User settings flow -> metropolis-user-settings-flow

### Settings
- **DO NOT** enable "Allow users to change email" (See [this discussion](https://github.com/goauthentik/authentik/issues/4097))
- Disable "Require reason for impersonation"
