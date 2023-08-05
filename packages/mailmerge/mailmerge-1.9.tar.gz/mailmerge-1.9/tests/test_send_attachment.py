"""Test messages with attachments."""
import future.backports.email as email
import mailmerge
from tests.test_smtp_base import TestSMTPBase


class TestSendAttachment(TestSMTPBase):
    """Test messages with attachments."""

    def _validate_message_contents(self, message):
        """Validate the contents and attachments of the message."""
        self.assertTrue(message.is_multipart())
        # Make sure the attachments are all present and valid
        email_body_present = False
        expected_attachments = {
            "test_send_attachment_1.txt": False,
            "test_send_attachment_2.pdf": False,
            "test_send_attachment_17.txt": False,
        }
        for part in message.walk():
            if part.get_content_maintype() == 'multipart':
                continue
            if part['content-type'].startswith('text/plain'):
                # This is the email body
                email_body = part.get_payload()
                expected_email_body = 'Hi, Myself,\n\nYour number is 17.'
                self.assertEqual(email_body.rstrip(), expected_email_body)
                email_body_present = True
            elif part['content-type'].startswith('application/octet-stream'):
                # This is an attachment
                filename = part.get_param('name')
                file_contents = part.get_payload(decode=True)
                self.assertIn(filename, expected_attachments)
                self.assertFalse(expected_attachments[filename])
                with open(filename, 'rb') as expected_attachment:
                    correct_file_contents = expected_attachment.read()
                self.assertEqual(file_contents, correct_file_contents)
                expected_attachments[filename] = True
        self.assertTrue(email_body_present)
        self.assertNotIn(False, expected_attachments.values())

    def test_send_attachment(self):
        """Attachments should be sent as part of the email."""
        mailmerge.api.main(
            database_filename=self.DATABASE_FILENAME,
            config_filename=self.SERVER_CONFIG_FILENAME,
            template_filename="test_send_attachment.template.txt",
            no_limit=False,
            dry_run=False,
        )

        # Check SMTP server after
        self.assertEqual(self.smtp.msg_from, "My Self <myself@mydomain.com>")
        recipients = ["myself@mydomain.com"]
        self.assertEqual(self.smtp.msg_to, recipients)

        # Check that the message is multipart
        message = email.parser.Parser().parsestr(self.smtp.msg)
        self._validate_message_contents(message)
