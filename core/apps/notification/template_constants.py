
WELCOMEMAIL = 1
THANKYOU = 2
RESET_PASSWORD = 3
CLAIM_STATUS_UPDATE = 4
PENDING_CLAIM_REMINDER = 5
CLAIM_SUBMISSION = 6

TEMPLATES = {
    WELCOMEMAIL: '../templates/welcome_mail.html',
    THANKYOU: '../templates/thankyou.html',
    RESET_PASSWORD: '../templates/reset_password.html',
    CLAIM_STATUS_UPDATE: 'claim_status_update.html',
    PENDING_CLAIM_REMINDER: 'pending_claim.html',
    CLAIM_SUBMISSION: 'claim_submission.html'
}

SUBJECTS = {
    WELCOMEMAIL: 'Welcome onboard!!',
    CLAIM_STATUS_UPDATE: 'Claim Status Update',
    PENDING_CLAIM_REMINDER: 'Pending Claims Reminder',
    RESET_PASSWORD: 'Password Reset Link',
    CLAIM_SUBMISSION: 'Claim Submission'
}