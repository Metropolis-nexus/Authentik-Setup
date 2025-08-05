# System Setup

- Create `/etc/ssh/sshd_config.d/10-certs.conf`:

```
PermitRootLogin yes
```
- Restart sshd
- Add NGINX's ssh key to `/root/.ssh/authorized_keys`
- rsync TLS certificates to `/srv/authentik/authentik/certs/auth.metropolis.nexus`

# Authentik Setup

Enter the admin section and configure the following:

## Directory

### Groups
- Create metropolis-default

## Customization

### Policies

#### metropolis-geoip
- Type: Expression Policy
- Name: metropolis-geoip
- Expression: `return not context["geoip"]["country"] == "GB"`

## Flow and Stages

### Example configuration:

https://docs.goauthentik.io/docs/add-secure-apps/flows-stages/flow/examples/flows

Download and import "Enrollment with email verification".

### Prompts

#### metropolis-enrollment-field-name
- Name: metropolis-enrollment-field-name
- Field Key: name
- Label: Name
- Type: Text: Simple Text input
- Not Required
- Order: 2

#### metropolis-enrollment-checkbox-age
- Name: metropolis-enrollment-checkbox-age
- Field Key: age
- Label: I am above 18 years of age.
- Type: Checkbox
- Required
- Order: 401

#### metropolis-enrollment-checkbox-residency
- Name: metropolis-enrollment-checkbox-residency
- Field Key: residency
- Label: I am not a residence of Wyoming, Ohio, South Dakota, or the United Kingdom.
- Type: Checkbox
- Required
- Order: 402

### Stages

### metropolis-user-settings
- Type: Prompt Stage
- Name: metropolis-user-settings
- Fields:
  - default-user-settings-field-locale
  - default-user-settings-field-name
- Validation policies
  - default-user-settings-authorization
 
### metropolis-enrollment-prompt-first
- Type: Prompt Stage
- Name: metropolis-enrollment-prompt-first
- Fields:
  - default-enrollment-field-password
  - default-enrollment-field-password-repeat
  - default-enrollment-field-username
  - metropolis-enrollment-checkbox-age
  - metropolis-enrollment-checkbox-residency

#### metropolis-authentication-identification
- Type: Identification Stage
- Name: metropolis-authentication-identification
- User fields: Username, email
- Password stage: default-authentication-password
- Enable Case insensitive matching
- Enable Pretend user exists
- Enable Show matched user
- Enable "Remember me on this device"
- Enrollment flow: default-enrollment-flow

### metropolis-enrollment-user-write
- Type: User Write Stage
- Name: metropolis-enrollment-user-write
- Always create new users
- Disable Create user as inactive
- User type: Internal
- Group: metropolis-default

### metropolis-user-settings-write
- Type: User Write Stage
- Name: metropolis-user-settings-write
- Never create users
- Uncheck create user as inactive
- User type: Internal

#### WebAuthn Authenticator Setup Stage
- Name: metropolis-authenticator-webauthn-setup
- Authenticator type name: WebAuthn device
- User verification: Required: User verification must occur
- Resident Key Requirement: Discouraged: The authenticator should not create a dedicated credential
- Authenticator attachment: A "roaming" authenticator
- Configuration flow: default-authenticator-webauthn-setup

#### Authenticator Validation Stage
- Name: metropolis-authentication-mfa-validation
- Device classes: Static Tokens, WebAuthn Authenticators
- Not configured action: Force the user to configure an authenticator
- WebAuthn User verification: User verification must occur
- Configuration stages: metropolis-authenticator-webauthn-setup

### Flows

#### metropolis-authentication-flow

- Name: Welcome to Metropolis Nexus!
- Title: Welcome to Metropolis Nexus!
- Slug: metropolis-authentication-flow
- Designation: Authentication
- Authentication: No requirement
- Enable compatibility mode
- Denied action: MESSAGE_CONTINUE
- Policy engine mode: any
- Layout: Sidebar left

Stage bindings:
- metropolis-authentication-identification -> 10
- metropolis-authentication-mfa-validation -> 30
- default-authentication-login -> 100

Policy bindings:
- metropolis-geoip -> 10 -> Don't pass

#### metropolis-enrollment-flow
- Name: Metropolis enrollment flow
- Title: FIDO2 token required!
- Slug: metropolis-enrollment-flow
- Designation: Enrollment
- Authentication: Require no authentication
- Enable compatibility mode
- Denied action: MESSAGE_CONTINUE
- Policy engine mode: any
- Layout: Sidebar left

Stage bindings:
- metropolis-enrollment-prompt-first -> 10
- metropolis-enrollment-user-write -> 20
- default-enrollment-user-login -> 100

Policy bindings:
- metropolis-geoip -> 10 -> Don't pass

#### metropolis-user-settings-flow
- Name: Metropolis user settings
- Title: Update your info
- Slug: metropolis-user-settings-flow
- Designation: Stage Configuration
- Authentication: Require authentication
- Enable compatibility mode
- Policy engine mode: any

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
- Enable "Default": Make this the default brand
- Title: Metropolis Nexus
- Default flow background: /media/public/flow-backgrounds/chicago.jpg
- Default flows
  - Authentication flow: metropolis-authentication-flow
  - Invalidation flow: default-invalidation-flow
  - User settings flow: metropolis-user-settings-flow
- Web Certificate: auth.metropolis.nexus

### Settings
- **DO NOT** enable "Allow users to change email" (See [this discussion](https://github.com/goauthentik/authentik/issues/4097))
- Disable "Require reason for impersonation"

# Cleanup

Delete all of the following:

## Flow and Stages

### Flows
- default-authentication-flow
- default-authenticator-totp-setup
- default-enrollment-flow
- default-user-settings-flow
- initial-setup

## Customization

### Policies
- default-authentication-flow-password-stage
- default-oobe-flow-set-authentication
- default-oobe-password-usable
- default-oobe-prefill-user

## System

### Brands
- authentik-default

### Certificates
- authentik Self-signed Certificate
