public string ToEml(MailMessage message)
{
    var assembly = typeof(SmtpClient).Assembly;
    var mailWriterType = assembly.GetType("System.Net.Mail.MailWriter");

    using (var memoryStream = new MemoryStream())
    {
        // Get reflection info for MailWriter contructor
        var mailWriterContructor = mailWriterType.GetConstructor(BindingFlags.Instance | BindingFlags.NonPublic, null, new[] { typeof(Stream) }, null);

        // Construct MailWriter object with our FileStream
        var mailWriter = mailWriterContructor.Invoke(new object[] { memoryStream });
        // Get reflection info for Send() method on MailMessage
        var sendMethod = typeof(MailMessage).GetMethod("Send", BindingFlags.Instance | BindingFlags.NonPublic);

        // Call method passing in MailWriter
        sendMethod.Invoke(message, BindingFlags.Instance | BindingFlags.NonPublic, null, new[] { mailWriter, true, true }, null);
        // Finally get reflection info for Close() method on our MailWriter
        var closeMethod = mailWriter.GetType().GetMethod("Close", BindingFlags.Instance | BindingFlags.NonPublic);

        // Call close method
        closeMethod.Invoke(mailWriter, BindingFlags.Instance | BindingFlags.NonPublic, null, new object[] { }, null);

        return Encoding.ASCII.GetString(memoryStream.ToArray());
    }
}

public void ExportToFile(string fullFileName, XstFile xstFile)
{
    if (ShowHtml)
    {
        string receiverEmail = String.Join("; ", Recipients.Where(r => r.RecipientType == RecipientType.To)
            .Select(r => r.EmailAddress));
        string senderEmail = Properties.Single(r => r.Description == "SenderEmailAddress").Value;
        string subject = "=?UTF-8?B? " + Convert.ToBase64String(Encoding.UTF8.GetBytes(Subject)) + "?=";


        MailMessage msg = new MailMessage(senderEmail, receiverEmail, subject, GetBodyAsHtmlString());
        msg.IsBodyHtml = true;
        string eml = ToEml(msg);
        using (var stream = new FileStream(fullFileName, FileMode.Create))
        {
            var bytes = Encoding.UTF8.GetBytes(eml);
            stream.Write(bytes, 0, bytes.Count());
        }

    }
}
