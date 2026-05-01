# Model Airplane: Tracking Login Event

## Situation
A user successfully logs in.

## Bad Pattern
Track login before the auth result is confirmed.
Track the password or token.
Scatter analytics calls across unrelated files.

## Good Pattern
Track only after successful authentication.
Capture safe properties only.
Keep the event close to the business action.

## Example Shape

```ts
const result = await loginUser(email, password)

if (result.success) {
  analytics.capture("user_logged_in", {
    method: result.method,
    user_id: result.user.id,
  })
}

return result
```

## Notes
Never capture passwords, tokens, full request bodies, or secret values.
