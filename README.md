# Authentik-Setup

## Flow and Stages

### Stages

#### WebAuthn Authenticator Setup Stage
- Authenticator type name -> WebAuthn device
- Name -> metropolis-authenticator-webauthn-setup
- User verification -> Required: User verification must occur
- Resident Key Requirement -> Required: The authenticator MUST create a dedicated credential
- Authenticator attachment -> A "roaming" authenticator

#### Authenticator Validation Stage
- Name -> metropolis-authentication-mfa-validation
- Device classes -> WebAuthn Authenticators
- Not configured action -> Force the user to configure an authenticator
- WebAuthn User verification -> User verification must occur
- Configuration stages -> metropolis-authenticator-webauthn-setup

## System

### Settings
- Avatar -> Change to 'initials' only - we do not want Gravatar.
- Enable "Allow users to change email"
- Disable "Require reason for impersonation"
