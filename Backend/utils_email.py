# import os
# import smtplib
# from email.mime.text import MIMEText
# from email.mime.multipart import MIMEMultipart

# SMTP_USER = os.getenv("SMTP_USER")      # e.g. your_email@gmail.com
# SMTP_PASS = os.getenv("SMTP_PASS")      # 16-char Gmail App Password
# FROM_NAME = os.getenv("FROM_NAME", "NeuralGuardians")  # optional display name

# def _build_message(to_email: str, subject: str, body_html: str | None = None, body_text: str | None = None):
#     """Return a MIMEMultipart message with both html and text if provided."""
#     msg = MIMEMultipart("alternative")
#     from_header = f"{FROM_NAME} <{SMTP_USER}>" if FROM_NAME else SMTP_USER
#     msg["From"] = from_header
#     msg["To"] = to_email
#     msg["Subject"] = subject

#     if body_text:
#         part1 = MIMEText(body_text, "plain", "utf-8")
#         msg.attach(part1)
#     if body_html:
#         part2 = MIMEText(body_html, "html", "utf-8")
#         msg.attach(part2)
#     return msg

# def _send_via_ssl(msg, to_email: str) -> bool:
#     try:
#         with smtplib.SMTP_SSL("smtp.gmail.com", 465, timeout=15) as server:
#             server.login(SMTP_USER, SMTP_PASS)
#             server.sendmail(SMTP_USER, to_email, msg.as_string())
#         print(f"[EMAIL DEBUG] Sent to {to_email} via SSL")
#         return True
#     except Exception as e:
#         print(f"[EMAIL DEBUG] SSL send failed: {e}")
#         return False

# def _send_via_tls(msg, to_email: str) -> bool:
#     try:
#         with smtplib.SMTP("smtp.gmail.com", 587, timeout=15) as server:
#             server.ehlo()
#             server.starttls()
#             server.login(SMTP_USER, SMTP_PASS)
#             server.sendmail(SMTP_USER, to_email, msg.as_string())
#         print(f"[EMAIL DEBUG] Sent to {to_email} via TLS")
#         return True
#     except Exception as e:
#         print(f"[EMAIL DEBUG] TLS send failed: {e}")
#         return False

# def send_email(to_email: str, subject: str, body_text: str = None, body_html: str = None) -> bool:
#     """
#     Send email using Gmail SMTP. Returns True on success.
#     Use app password in SMTP_PASS environment variable.
#     """
#     if not SMTP_USER or not SMTP_PASS:
#         print("[EMAIL ERROR] SMTP_USER or SMTP_PASS not set in environment")
#         return False

#     msg = _build_message(to_email, subject, body_html=body_html, body_text=body_text)

#     # Try SSL first, then TLS fallback
#     if _send_via_ssl(msg, to_email):
#         return True
#     return _send_via_tls(msg, to_email)

# # Convenience functions for your project
# def send_warning_email(username: str, ip: str, country: str, attempts: int) -> bool:
#     subject = "⚠️ Security Warning — Multiple Failed Login Attempts"
#     text = (
#         f"Hello {username},\n\n"
#         f"We detected {attempts} failed login attempts to your account from IP {ip} ({country}).\n"
#         "If this wasn’t you, please reset your password immediately.\n\n"
#         "Regards,\nNeuralGuardians Security Team"
#     )
#     html = f"""
#     <p>Hello {username},</p>
#     <p>We detected <strong>{attempts}</strong> failed login attempts to your account from IP <strong>{ip}</strong> ({country}).</p>
#     <p>If this wasn’t you, please reset your password immediately.</p>
#     <p>Regards,<br/><strong>NeuralGuardians Security Team</strong></p>
#     """
#     return send_email(username, subject, body_text=text, body_html=html)

# def send_block_email(username: str, ip: str, country: str, attempts: int) -> bool:
#     subject = "🚨 Account Blocked — Suspicious Activity"
#     text = (
#         f"Hello {username},\n\n"
#         f"Your account has been temporarily blocked after {attempts} failed login attempts from IP {ip} ({country}).\n"
#         "If you believe this is an error, please contact support or use account recovery.\n\n"
#         "Regards,\nNeuralGuardians Security Team"
#     )
#     html = f"""
#     <h3>Account Blocked</h3>
#     <p>Hello {username},</p>
#     <p>Your account has been <strong>blocked</strong> after <strong>{attempts}</strong> failed login attempts from IP <strong>{ip}</strong> ({country}).</p>
#     <p>If you believe this is a mistake, please contact support.</p>
#     <p>Regards,<br/><strong>NeuralGuardians Security Team</strong></p>
#     """
#     return send_email(username, subject, body_text=text, body_html=html)