# QR Code Types Guide

This guide provides detailed information about all the QR code types supported by the IBQ QR Code Generator.

## Table of Contents

1. [Business Card / vCard](#business-card--vcard)
2. [Website URL](#website-url)
3. [Plain Text](#plain-text)
4. [Email](#email)
5. [SMS / Text Message](#sms--text-message)
6. [Phone Number](#phone-number)
7. [WiFi Network](#wifi-network)
8. [Social Media Profiles](#social-media-profiles)
9. [App Store Links](#app-store-links)
10. [Calendar Event](#calendar-event)
11. [Location / Map](#location--map)

---

## Business Card / vCard

**Description**: Create a digital business card that can be scanned and saved directly to contacts.

**Use Cases**:
- Networking events
- Business cards
- Professional profiles
- Conference badges

**Fields**:
- Contact Name: Full name of the person
- Job Title: Professional title
- Company: Organization name
- Email: Email address
- Phone: Phone number with country code
- Website: Company or personal website
- Address: Full mailing address

**Tips**:
- Fill in as much information as possible for a complete profile
- Include country code in phone number (e.g., +1 for USA)
- Use https:// for website URLs
- Test scanning with multiple devices

**Example**:
```
Name: John Doe
Title: Software Engineer
Company: Tech Corp
Email: john.doe@techcorp.com
Phone: +1-555-123-4567
Website: https://johndoe.com
Address: 123 Main St, San Francisco, CA 94102
```

---

## Website URL

**Description**: Direct users to any website or web page by scanning the QR code.

**Use Cases**:
- Marketing materials
- Product packaging
- Business cards
- Event signage
- Restaurant menus (link to online menu)
- Social media links

**Fields**:
- URL: Full website address

**Tips**:
- Always include https:// or http:// in the URL
- Shorter URLs create simpler, more scannable QR codes
- Test the link before generating the QR code
- Use URL shorteners for long links
- Ensure the website is mobile-friendly

**Examples**:
```
Website: https://www.example.com
Landing Page: https://example.com/promo
Product Info: https://example.com/products/12345
```

---

## Plain Text

**Description**: Encode any text information into a QR code.

**Use Cases**:
- Instructions or directions
- Product serial numbers
- Coupon codes
- Passwords or access codes
- Configuration strings
- Short messages

**Fields**:
- Text Content: Any text up to 2000 characters

**Tips**:
- Keep text concise for better scanning
- Shorter text creates smaller, easier-to-scan QR codes
- Maximum 2000 characters recommended
- Consider line breaks for readability
- Great for information that needs to be typed

**Examples**:
```
Simple Message: "Welcome to our store! Show this code at checkout for 10% off."
Configuration: "Server: 192.168.1.1\nPort: 8080\nProtocol: HTTPS"
Serial Number: "SN:ABC123XYZ789"
```

---

## Email

**Description**: Create a QR code that opens an email client with pre-filled information.

**Use Cases**:
- Customer support
- Contact forms
- Feedback collection
- Newsletter signup
- Report issues
- Quick inquiries

**Fields**:
- Email Address: Recipient email
- Subject: Email subject line (optional)
- Body: Pre-filled message (optional)

**Tips**:
- Subject and body are optional
- Body text should be concise
- Works with all email clients
- Great for support and feedback forms
- Consider privacy when pre-filling information

**Examples**:
```
Support Email:
- Email: support@example.com
- Subject: Support Request
- Body: Please describe your issue here.

Feedback:
- Email: feedback@example.com
- Subject: Product Feedback
- Body: 
```

---

## SMS / Text Message

**Description**: Create a QR code that opens SMS with a pre-filled message.

**Use Cases**:
- Quick customer service
- Contest entries
- Voting or polls
- Appointment confirmations
- Two-factor authentication
- Event RSVPs

**Fields**:
- Phone Number: Recipient phone number with country code
- Message: Pre-filled text message (optional)

**Tips**:
- Include country code in phone number (e.g., +1234567890)
- Message is optional
- Keep messages short and clear
- Test on multiple devices
- Great for quick responses and interactions

**Examples**:
```
Customer Support:
- Phone: +1-555-SUPPORT
- Message: "I need help with order #"

Contest Entry:
- Phone: +1-555-CONTEST
- Message: "ENTER"
```

---

## Phone Number

**Description**: Create a QR code that initiates a phone call.

**Use Cases**:
- Business cards
- Emergency contacts
- Customer service hotlines
- Sales inquiries
- Support numbers
- Booking appointments

**Fields**:
- Phone Number: Full phone number with country code

**Tips**:
- Always include country code (+1 for USA, +44 for UK, etc.)
- Format: +1234567890 (no spaces or dashes)
- Perfect for quick calls
- Test that the number is correct
- Consider toll-free numbers for better customer experience

**Examples**:
```
USA Number: +15551234567
UK Number: +442071234567
Toll-Free: +18005551234
```

---

## WiFi Network

**Description**: Allow users to connect to WiFi by scanning a QR code.

**Use Cases**:
- Guest WiFi in offices
- Coffee shops and restaurants
- Hotels and accommodations
- Conference venues
- Retail stores
- Homes (for guests)

**Fields**:
- Network Name (SSID): Exact WiFi network name
- Password: Network password
- Security Type: WPA/WPA2, WEP, or No Password
- Hidden Network: Check if network is hidden

**Tips**:
- Enter exact network name (case-sensitive)
- Choose correct security type
- Test before printing/sharing
- Great for guests and public spaces
- Update QR code when password changes
- Consider security implications

**Examples**:
```
Guest Network:
- SSID: GuestNetwork
- Password: Welcome2023
- Security: WPA/WPA2
- Hidden: No

Office WiFi:
- SSID: CompanyWiFi
- Password: SecurePass123!
- Security: WPA/WPA2
- Hidden: No
```

---

## Social Media Profiles

**Description**: Link directly to your social media profiles.

**Supported Platforms**:
- Facebook
- Twitter
- Instagram
- LinkedIn
- YouTube

**Use Cases**:
- Business cards
- Marketing materials
- Product packaging
- Event signage
- Promotional materials
- Store displays

**Fields**:
- Profile URL: Full URL to your social media profile

**Tips**:
- Use the full URL from your profile
- Test the link before generating
- Works for both profiles and pages
- Great for increasing followers
- Update if you change your handle

**Examples**:
```
Facebook:
- https://facebook.com/yourpage

Twitter:
- https://twitter.com/yourhandle

Instagram:
- https://instagram.com/yourhandle

LinkedIn:
- https://linkedin.com/in/yourprofile
- https://linkedin.com/company/yourcompany

YouTube:
- https://youtube.com/c/yourchannel
- https://youtube.com/@yourhandle
```

---

## App Store Links

**Description**: Direct users to your app on app stores.

**Supported Stores**:
- Apple App Store
- Google Play Store

**Use Cases**:
- App marketing materials
- Print advertisements
- Product packaging
- Website promotion
- Business cards
- Event materials

**Fields**:
- App Store URL: Full URL to your app

**Tips**:
- Use the direct app store URL
- Test the link on target devices
- Perfect for app promotion
- Include app icon or screenshot nearby
- Consider platform-specific QR codes

**Examples**:
```
Apple App Store:
- https://apps.apple.com/us/app/app-name/id123456789

Google Play Store:
- https://play.google.com/store/apps/details?id=com.example.app
```

---

## Calendar Event

**Description**: Add events to calendars by scanning.

**Use Cases**:
- Event invitations
- Meeting reminders
- Conference schedules
- Webinar registrations
- Appointment cards
- Trade show booths

**Fields**:
- Event Title: Name of the event
- Location: Event location
- Start Date/Time: When the event begins
- End Date/Time: When the event ends
- Description: Event details (optional)

**Tips**:
- Include all event details
- Use proper date/time format
- Perfect for invitations
- Add location for navigation
- Include description for context
- Test on multiple calendar apps

**Examples**:
```
Conference:
- Title: Tech Conference 2024
- Location: Convention Center, 123 Main St
- Start: 2024-06-15T09:00:00
- End: 2024-06-15T17:00:00
- Description: Annual technology conference featuring...

Webinar:
- Title: Product Launch Webinar
- Location: Online (Zoom)
- Start: 2024-03-20T14:00:00
- End: 2024-03-20T15:00:00
- Description: Join us for the launch of our new product.
```

---

## Location / Map

**Description**: Direct users to a specific location on maps.

**Use Cases**:
- Business locations
- Event venues
- Meeting points
- Delivery addresses
- Tourist attractions
- Emergency assembly points

**Fields**:
- Latitude: Geographic latitude
- Longitude: Geographic longitude
- Location Name: Name or description (optional)

**Tips**:
- Use accurate coordinates
- Get coordinates from Google Maps or similar
- Add location name for context
- Great for navigation
- Test on multiple map apps
- Consider accessibility

**Examples**:
```
Business Location:
- Latitude: 37.7749
- Longitude: -122.4194
- Name: Our Office

Event Venue:
- Latitude: 40.7589
- Longitude: -73.9851
- Name: Times Square, New York

Parking Location:
- Latitude: 34.0522
- Longitude: -118.2437
- Name: Parking Lot Entrance
```

---

## Best Practices

### Design Tips
1. **High Contrast**: Ensure good contrast between foreground and background colors
2. **Size Matters**: Larger QR codes are easier to scan
3. **Error Correction**: Use high error correction for codes with logos
4. **Test Thoroughly**: Always test on multiple devices before printing
5. **Keep It Simple**: Simpler designs scan better

### Printing Guidelines
1. **Resolution**: Use at least 300 DPI for printing
2. **Format**: PNG for digital, SVG for scaling, PDF for printing
3. **Size**: Minimum 2cm x 2cm for reliable scanning
4. **Placement**: Ensure QR code is easily accessible
5. **Surface**: Print on flat, non-reflective surfaces when possible

### Security Considerations
1. **Public WiFi**: Be cautious about sharing password-protected networks
2. **Contact Information**: Only share information you're comfortable making public
3. **URLs**: Verify links before creating QR codes
4. **Testing**: Always test QR codes before mass distribution
5. **Updates**: Keep QR codes up to date when information changes

### Accessibility
1. **Instructions**: Provide text instructions near QR codes
2. **Alternative**: Offer alternative ways to access information
3. **Placement**: Position at accessible heights
4. **Lighting**: Ensure adequate lighting for scanning
5. **Size**: Make codes large enough for easy scanning

---

## Troubleshooting

### QR Code Won't Scan
1. Increase size of QR code
2. Improve contrast between colors
3. Ensure adequate lighting
4. Check for damage or distortion
5. Try different scanning apps

### Wrong Information
1. Verify data before generating
2. Test on multiple devices
3. Check for typos in URLs or text
4. Ensure proper format (e.g., https:// in URLs)

### Poor Quality
1. Use higher resolution
2. Choose PNG or SVG format
3. Increase size
4. Use darker foreground color
5. Avoid excessive customization

---

## Support

For additional help or questions:
- Check the FAQ section
- Visit the Help & Support page
- Contact support through the application
- Review documentation

---

**Version 1.0** - IBQ QR Code Generator
