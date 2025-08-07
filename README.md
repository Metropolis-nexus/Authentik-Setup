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

## Customization

### Policies

#### metropolis-enrollment-with-email
- Type: Expression Policy
- Name: metropolis-enrollment-with-email
- Expression:
```
if request.context["prompt_data"]["email"] == "":
   return False
return True
```

#### metropolis-unique-email
- Type: Expression Policy
- Name: metropolis-unique-email
- Expression:

```
from authentik.core.models import User

email = request.context["prompt_data"]["email"]
if email != "" and User.objects.filter(email=email).exists():
  ak_message("Email address already in use")
  return False
return True
```

#### metropolis-geoip
- Type: Expression Policy
- Name: metropolis-geoip
- Expression:

```
if (context["geoip"]["country"] == "GB"):
  ak_message("United Kingdom IP addresses are not allowed.")
  return False
return True
```

## Flow and Stages

### Example configuration:

https://docs.goauthentik.io/docs/add-secure-apps/flows-stages/flow/examples/flows

Download and import "Enrollment with email verification" and "Recovery with email verification".

### Prompts

#### metropolis-enrollment-field-name
- Name: metropolis-enrollment-field-name
- Field Key: name
- Label: Name (optional)
- Type: Text: Simple Text input
- Not Required
- Placeholder: Does not have to be your legal name
- Order: 0

#### metropolis-enrollment-field-email
- Name: metropolis-enrollment-field-email
- Field Key: email
- Label: Email (optional - for recovery)
- Type: Email: Text field with Email Type
- Not Required
- Placeholder: Contact support to change post sign-up
- Order: 1

#### metropolis-enrollment-checkbox-age
- Name: metropolis-enrollment-checkbox-age
- Field Key: age
- Label: I am above 18 years of age.
- Type: Checkbox
- Required
- Order: 400

#### metropolis-enrollment-checkbox-residency
- Name: metropolis-enrollment-checkbox-residency
- Field Key: residency
- Label: I am not a residence of Wyoming, Ohio, South Dakota, or the United Kingdom.
- Type: Checkbox
- Required
- Order: 401

#### metropolis-user-settings-field-name
- Name: metropolis-user-settings-field-name
- Field Key: name
- Label: Name
- Type: Text: Simple Text input
- Placeholder: Does not have to be your legal name
- Not Required
- Interpret initial value as expression
- Initial value:

```
try:
    return user.name
except:
    return ''
```
- Order: 201

#### metropolis-user-settings-field-email
- Name: metropolis-user-settings-field-email
- Field Key: email
- Label: Email
- Type: Email: Text field with Email Type
- Placeholder: Contact support to set an email address
- Not Required
- Interpret initial value as expression
- Initial value:

```
try:
    return user.name
except:
    return ''
```
- Order: 202

### Stages

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

#### metropolis-authenticator-webauthn-setup
- Type: WebAuthn Authenticator Setup Stage
- Name: metropolis-authenticator-webauthn-setup
- Authenticator type name: WebAuthn device
- User verification: Required: User verification must occur
- Resident Key Requirement: Discouraged: The authenticator should not create a dedicated credential
- Authenticator attachment: A "roaming" authenticator
- Configuration flow: default-authenticator-webauthn-setup

#### metropolis-authentication-mfa-validation
- Type: Authenticator Validation Stage
- Name: metropolis-authentication-mfa-validation
- Device classes: Static Tokens, WebAuthn Authenticators
- Not configured action: Force the user to configure an authenticator
- WebAuthn User verification: User verification must occur
- Configuration stages: metropolis-authenticator-webauthn-setup

#### metropolis-enrollment-prompt-first
- Type: Prompt Stage
- Name: metropolis-enrollment-prompt-first
- Fields:
  - default-enrollment-field-password
  - default-enrollment-field-password-repeat
  - default-enrollment-field-username
  - metropolis-enrollment-checkbox-age
  - metropolis-enrollment-checkbox-residency
 
#### metropolis-enrollment-prompt-second
- Type: Prompt Stage
- Name: metropolis-enrollment-prompt-second
- Fields:
  - metropolis-enrollment-field-email
  - metropolis-enrollment-field-name
  - default-user-settings-field-locale
- Validation policies:
  - metropolis-unique-email

#### metropolis-enrollment-user-write
- Type: User Write Stage
- Name: metropolis-enrollment-user-write
- Always create new users
- Disable Create user as inactive
- User type: Internal
- Group: metropolis-default

#### metropolis-enrollment-with-email-user-write
- Type: User Write Stage
- Name: metropolis-enrollment-with-email-user-write
- Always create new users
- Create user as inactive
- User type: Internal
- Group: metropolis-default

#### metropolis-user-settings
- Type: Prompt Stage
- Name: metropolis-user-settings
- Fields:
  - default-user-settings-field-locale
  - default-user-settings-field-username
  - metropolis-user-settings-field-email
  - metropolis-user-settings-field-name
- Validation policies
  - default-user-settings-authorization

#### metropolis-user-settings-write
- Type: User Write Stage
- Name: metropolis-user-settings-write
- Never create users
- Uncheck create user as inactive
- User type: Internal

### Flows

#### metropolis-authenticator-webauthn-setup
- Name: metropolis-authenticator-webauthn-setup
- Title: Setup WebAuthn
- Slug: metropolis-authenticator-webauthn-setup
- Designation: Stage Configuration
- Authentication: Require authentication

Stage bindings:
- metropolis-authenticator-webauthn-setup -> 0

Stage update:
- Stage -> metropolis-authenticator-webauthn-setup -> Change configuration flow to metropolis-authenticator-webauthn-setup

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

#### metropolis-enrollment-with-email-flow
- Name: Metropolis enrollment with email flow
- Title: Enrollment with Email
- Slug: metropolis-enrollment-with-email-flow
- Designation: Enrollment
- Authentication: Require being redirected from another flow
- Denied action: MESSAGE_CONTINUE
- Policy engine mode: any
- Layout: Sidebar left

Stage bindings:
- metropolis-enrollment-with-email-user-write -> 10
- default-enrollment-email-verification -> 20
- metropolis-authenticator-webauthn-setup -> 30

Stage update:

- Create the following stage:

##### metropolis-enrollment-with-email
- Type: Redirect Stage
- Mode: Flow
- Target Flow: metropolis-enrollment-with-email-flow


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
- metropolis-enrollment-prompt-second -> 20
- metropolis-enrollment-with-email -> 30
  - metropolis-enrollment-with-email -> 0
- metropolis-enrollment-user-write -> 40
- metropolis-authenticator-webauthn-setup -> 50
- default-enrollment-user-login -> 100

Policy bindings:
- metropolis-geoip -> 10 -> Don't pass

Stage update:
- Stage -> metropolis-authentication-identification -> Change enrollment flow to metropolis-enrollment-flow

#### metropolis-recovery-flow
- Name: Default recovery flow
- Title: Reset your password
- Slug: metropolis-recovery-flow
- Designation: Recovery
- Authentication: No requirement (This should be "Require no authentication", but we are using No requirement temporarily due to (this bug)[https://github.com/goauthentik/authentik/issues/13714])
- Enable compatibility mode
- Denied action: MESSAGE_CONTINUE
- Policy engine mode: any
- Layout: Sidebar left

Stage bindings:

Policy evaluation is copied from the default flow, it's a little strange. Need to double check later.

- default-recovery-identification -> 10
  - Enable "Evaluate when flow is planned" (Keep "Evaluate when stage is run")
  - default-recovery-skip-if-restored -> 0
- default-recovery-email -> 20
  - Enable "Evaluate when flow is planned" (Keep "Evaluate when stage is run")
- Change your password -> 30
  - Enable "Evaluate when flow is planned" (Disable "Evaluate when stage is run")
- default-recovery-user-write -> 40
  - Enable "Evaluate when flow is planned" (Disable "Evaluate when stage is run")
- default-recovery-user-login -> 100
  - Enable "Evaluate when flow is planned" (Disable "Evaluate when stage is run")

Stage update:
- Stage -> metropolis-authentication-identification -> Change recovery flow to metropolis-recovery-flow

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
  - Recovery flow: metropolis-recovery-flow
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
