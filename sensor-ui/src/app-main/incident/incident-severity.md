## 4-Level Severity Matrix

### SEV-1
-  **Critical** impact: significant degradation of customer experience
- Postmortem required, *leadership invited*
- require immediate response 24/7 for resolution

### SEV-2
- **High** impact: meaningful degradation of customer experience
- Postmortem required, *team invited*
- require quick Response paging engineering team

### SEV-3
- **Medium** impact: minor degradation of customer experience
- Postmortem optional
- notify relevant enegineering manager
- Respond during working hours

### SEV-4
- **Low** impact: no impact on customer experience
- Postmortem optional
- Respond during working hours

### For Example:
For example Database storage is often consumed at predictable rates and has a maximum configured size, this means that alarms can be constructed similar to:

- Cut a SEV-1 if a critical database completely runs out of storage
- Cut a SEV-2 if a critical database is likely to run out of storage - in the next 24 hours
- Cut a SEV-3 if a critical database is likely to run out of storage in the next week
- Cut a SEV-4 if a critical database is likely to run out of storage in the next 2 months
