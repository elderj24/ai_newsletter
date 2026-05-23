import re
import os
import datetime
import resend

def convert_markdown_to_html(markdown_content: str) -> str:
    """
    Translates basic markdown into beautiful, responsive, inline-styled email HTML.
    Designed for premium styling and excellent client compatibility (Gmail, Outlook).
    """
    # Replace bold double stars
    html = markdown_content
    html = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', html)
    
    # Process links
    html = re.sub(
        r'\[(.*?)\]\((.*?)\)', 
        r'<a href="\2" style="color: #0284c7; text-decoration: none; font-weight: 500; border-bottom: 1px dashed #0284c7;">\1</a>', 
        html
    )
    
    lines = html.split('\n')
    output_lines = []
    in_list = False
    
    for line in lines:
        stripped = line.strip()
        if not stripped:
            if in_list:
                output_lines.append("</ul>")
                in_list = False
            continue
            
        # Headers
        if stripped.startswith("# "):
            if in_list:
                output_lines.append("</ul>")
                in_list = False
            title = stripped[2:]
            output_lines.append(
                f'<h1 style="font-family: \'Outfit\', \'Inter\', -apple-system, sans-serif; color: #0f172a; font-size: 24px; margin-top: 24px; margin-bottom: 12px; border-bottom: 2px solid #e2e8f0; padding-bottom: 6px;">{title}</h1>'
            )
        elif stripped.startswith("## "):
            if in_list:
                output_lines.append("</ul>")
                in_list = False
            title = stripped[3:]
            output_lines.append(
                f'<h2 style="font-family: \'Outfit\', \'Inter\', -apple-system, sans-serif; color: #1e3a8a; font-size: 20px; margin-top: 24px; margin-bottom: 10px;">{title}</h2>'
            )
        elif stripped.startswith("### "):
            if in_list:
                output_lines.append("</ul>")
                in_list = False
            title = stripped[4:]
            output_lines.append(
                f'<h3 style="font-family: \'Outfit\', \'Inter\', -apple-system, sans-serif; color: #3b82f6; font-size: 16px; margin-top: 18px; margin-bottom: 8px;">{title}</h3>'
            )
            
        # Lists
        elif stripped.startswith("* ") or stripped.startswith("- "):
            if not in_list:
                output_lines.append(
                    '<ul style="padding-left: 20px; margin-top: 8px; margin-bottom: 8px; font-family: \'Inter\', -apple-system, sans-serif; color: #334155; line-height: 1.6;">'
                )
                in_list = True
            item = stripped[2:]
            output_lines.append(f'<li style="margin-bottom: 6px;">{item}</li>')
            
        # Paragraphs
        else:
            if in_list:
                output_lines.append("</ul>")
                in_list = False
            output_lines.append(
                f'<p style="font-family: \'Inter\', -apple-system, sans-serif; font-size: 15px; color: #334155; line-height: 1.6; margin-top: 8px; margin-bottom: 12px;">{stripped}</p>'
            )
            
    if in_list:
        output_lines.append("</ul>")
        
    body_content = "\n".join(output_lines)
    
    # Beautiful responsive wrapper template
    date_str = datetime.date.today().strftime("%B %d, %Y")
    email_template = f"""<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Tilia AI Digest</title>
</head>
<body style="margin: 0; padding: 0; background-color: #f8fafc; -webkit-font-smoothing: antialiased;">
  <table border="0" cellpadding="0" cellspacing="0" width="100%" style="background-color: #f8fafc; padding: 20px 0;">
    <tr>
      <td align="center">
        <table border="0" cellpadding="0" cellspacing="0" width="100%" style="max-width: 680px; background-color: #ffffff; border-radius: 12px; border: 1px solid #e2e8f0; overflow: hidden; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);">
          <!-- Header -->
          <tr>
            <td style="background: linear-gradient(135deg, #1e3a8a 0%, #0f172a 100%); padding: 35px 40px; text-align: left;">
              <span style="font-family: 'Outfit', 'Inter', -apple-system, sans-serif; font-size: 11px; font-weight: 700; letter-spacing: 0.15em; color: #93c5fd; text-transform: uppercase;">Weekly Insight Pipeline</span>
              <h1 style="font-family: 'Outfit', 'Inter', -apple-system, sans-serif; font-size: 28px; font-weight: 800; color: #ffffff; margin: 5px 0 0 0; letter-spacing: -0.02em;">Tilia AI Digest</h1>
              <p style="font-family: 'Inter', -apple-system, sans-serif; font-size: 14px; color: #94a3b8; margin: 8px 0 0 0;">Ingested & Synthesized on {date_str}</p>
            </td>
          </tr>
          <!-- Content -->
          <tr>
            <td style="padding: 40px; text-align: left; background-color: #ffffff;">
              {body_content}
            </td>
          </tr>
          <!-- Footer -->
          <tr>
            <td style="background-color: #f1f5f9; padding: 25px 40px; text-align: center; border-top: 1px solid #e2e8f0;">
              <p style="font-family: 'Inter', 'Inter', -apple-system, sans-serif; font-size: 12px; color: #64748b; margin: 0;">
                Tilia LLC AI Research & Strategic Investment Operations
              </p>
              <p style="font-family: 'Inter', -apple-system, sans-serif; font-size: 11px; color: #94a3b8; margin: 5px 0 0 0;">
                This email was automatically ingested, analyzed by Gemini 1.5 Pro, and delivered serverless.
              </p>
            </td>
          </tr>
        </table>
      </td>
    </tr>
  </table>
</body>
</html>"""
    return email_template

def send_newsletter_email(html_body: str, recipient: str) -> bool:
    """
    Delivers the compiled HTML newsletter via Resend.
    """
    resend_api_key = os.environ.get("RESEND_API_KEY")
    if not resend_api_key:
        raise ValueError("RESEND_API_KEY environment variable is not set")
        
    resend.api_key = resend_api_key
    
    date_str = datetime.date.today().strftime("%B %d, %Y")
    
    try:
        response = resend.Emails.send({
            "from": "Tilia AI Digest <onboarding@resend.dev>",
            "to": recipient,
            "subject": f"[Tilia AI Digest] Weekly Ingestion & Strategic Synthesis - {date_str}",
            "html": html_body
        })
        print(f"Resend email sent successfully. ID: {getattr(response, 'id', 'N/A')}")
        return True
    except Exception as e:
        print(f"Error during Resend email delivery: {e}")
        raise e
