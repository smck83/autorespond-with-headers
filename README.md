# Autorespond with headers
- This service connects to an IMAP e-mail server and looks for e-mail that are unread/unseen in the Inbox
- An e-mail is created with the body of the e-mail being the header of the original inbound e-mail.
- The e-mail is sent back (auto responds) to the original sender

 
# Environment Variables
| VARIABLE  | Description |
| ------------- | ------------- |
| IMAP_SERVER | `(REQUIRED)`The IP or hostname of the IMAP server  |
| IMAP_USERNAME | `(REQUIRED)`The username the authentication with your IMAP server  |
| IMAP_PASSWORD | `(REQUIRED)`The password the authentication with your IMAP server  |
| ALLOWED_SENDERS | `(REQUIRED)` Space seperated e-mail addresses or domain names, `e.g. bgates@contoso.com gmail.com`  |
| SCHEDULE | `(OPTIONAL)` The time (in seconds) between checking the e-mail account `Default: 30`  |
| SMTP_SERVER | `(OPTIONAL)` The IP or hostname of the SMTP server `Default: IMAP_SERVER` |
| SMTP_USERNAME | `(OPTIONAL)` The username the authentication with your IMAP server `Default: IMAP_USERNAME` |
| SMTP_PASSWORD | `(OPTIONAL)` The password the authentication with your IMAP server `Default: IMAP_PASSWORD` |
| SMTP_SENDER | `(OPTIONAL)` The Display name and from e-mail address `Default: Autoresponse <IMAP_USERNAME>` |



