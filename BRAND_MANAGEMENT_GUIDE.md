# Brand Management System - Implementation Guide

## Overview
This implementation adds a comprehensive brand management system to the IBQ QR Code Generator, addressing the following requirements:

1. ✅ **QR codes now properly link to brand-customized profiles** - When scanned, QR codes display brand-specific information
2. ✅ **Brand-wise customization for employee details** - Each QR code can be associated with a brand
3. ✅ **Dashboard options to manage brands** - Full CRUD operations for brands
4. ✅ **Brand as the main key** - Brands are now central to the system organization
5. ✅ **Ability to add new brands** - Users can create and manage multiple brands

## Key Features Implemented

### 1. Brand Model (models.py)
- New `Brand` table with the following fields:
  - `name`: Brand name
  - `description`: Brand description
  - `website`, `email`, `phone`, `address`: Brand contact information
  - `logo`: Brand logo image
  - `primary_color`, `secondary_color`: Brand colors for customization
  - `is_default`: Mark a brand as default for QR generation
  - `is_active`: Enable/disable brands

### 2. Updated QRCode Model
- Added `brand_id` foreign key to link QR codes to brands
- QR codes now inherit brand customization when displayed

### 3. Brand Management Routes (app.py)
- **GET `/brands`**: View all user's brands
- **GET/POST `/brands/create`**: Create a new brand
- **GET/POST `/brands/<id>/edit`**: Edit existing brand
- **POST `/brands/<id>/delete`**: Delete a brand (with safety checks)
- **POST `/brands/<id>/set-default`**: Set brand as default
- **GET `/brand-logo/<filename>`**: Serve brand logo files securely

### 4. Updated QR Generation
- Brand selection dropdown in QR code generation form
- Default brand is auto-selected when available
- Brand information is saved with each QR code

### 5. Brand-Customized Contact Profiles
- Contact profile pages now display brand logo (if available)
- Brand colors are used for page customization
- Falls back to user customization if no brand is selected

### 6. Dashboard Navigation
- New "Brands" menu item in the sidebar
- Easy access to brand management

## Database Migration

To migrate existing installations:

```bash
python migrate_brands.py
```

This migration script will:
1. Create the `brands` table
2. Create a default brand for each existing user using their company information
3. Link all existing QR codes to the user's default brand

## Usage Guide

### For Users

#### Creating a Brand
1. Navigate to **Dashboard > Brands**
2. Click **"Create New Brand"**
3. Fill in brand information:
   - Brand name (required)
   - Description, website, email, phone, address (optional)
   - Upload brand logo (optional)
   - Choose primary and secondary colors
   - Set as default brand (optional)
   - Activate brand
4. Click **"Save Brand"**

#### Generating QR Codes with Brands
1. Navigate to **Dashboard > Generate QR Code**
2. Fill in basic information
3. **Select a brand** from the "Brand" dropdown
4. Complete QR code details
5. Generate and download

#### Managing Brands
- **Edit**: Update brand information and colors
- **Set as Default**: Make a brand the default for new QR codes
- **Delete**: Remove brands (only if they have no associated QR codes)

### For Administrators

#### Initial Setup
1. Run the migration script:
   ```bash
   python migrate_brands.py
   ```

2. Restart the application:
   ```bash
   python app.py
   ```

3. Users will automatically have a default brand created from their profile

#### System Configuration
- Brand logos are stored in the `uploads/` folder
- Logo files are served securely through `/brand-logo/<filename>` route
- Only registered brand logos can be accessed

## Technical Implementation Details

### Brand Model Structure
```python
class Brand(db.Model):
    id = Integer (Primary Key)
    user_id = Integer (Foreign Key -> users.id)
    name = String(100)
    description = Text
    website = String(200)
    email = String(120)
    phone = String(20)
    address = Text
    logo = String(255)  # Filename
    primary_color = String(7)  # Hex color
    secondary_color = String(7)  # Hex color
    is_default = Boolean
    is_active = Boolean
    created_at = DateTime
    updated_at = DateTime
```

### QRCode Model Update
```python
class QRCode(db.Model):
    # ... existing fields ...
    brand_id = Integer (Foreign Key -> brands.id, nullable=True)
```

### Contact Profile Customization Logic
1. Check if QR code has an associated brand
2. If yes, use brand logo and colors
3. If no, fall back to user's company logo and profile color
4. If neither, use default colors (#667eea and #764ba2)

### Security Considerations
- All brand management routes require authentication
- Brand logo files are validated and stored securely
- Only brand owners can edit/delete their brands
- Deletion is prevented if brand has associated QR codes
- File path traversal prevention for logo serving

## Testing Checklist

- [x] Create new brand
- [x] Edit existing brand
- [x] Upload brand logo
- [x] Set default brand
- [x] Generate QR code with brand selection
- [x] Scan QR code and verify brand customization
- [ ] Delete brand (test with and without QR codes)
- [ ] Deactivate brand
- [ ] Test with multiple brands
- [ ] Test brand color customization in profile

## Troubleshooting

### Issue: Brands table doesn't exist
**Solution**: Run the migration script: `python migrate_brands.py`

### Issue: QR codes don't show brand customization
**Solution**:
1. Check if the QR code has a brand_id assigned
2. Verify the brand has logo and colors configured
3. Clear browser cache

### Issue: Cannot delete brand
**Solution**:
1. Check if brand has associated QR codes
2. Reassign or delete QR codes first
3. Ensure you're not trying to delete your only brand

### Issue: Brand logo not displaying
**Solution**:
1. Verify logo file exists in `uploads/` folder
2. Check file permissions
3. Ensure logo filename is correctly stored in database

## Future Enhancements

Potential features for future versions:
1. Brand templates (pre-defined color schemes)
2. Brand-specific QR code templates
3. Brand analytics and statistics
4. Brand sharing between users
5. Brand import/export functionality
6. Multi-language support for brands
7. Brand categories/tags

## Migration Notes for Existing Users

When you run the migration:
- Your existing company information becomes your first brand
- All existing QR codes are linked to this default brand
- You can create additional brands as needed
- Old QR codes will work exactly as before

## API Changes

If you use the API:
- QR code creation now accepts optional `brand_id` parameter
- Brand endpoints follow REST conventions:
  - GET `/brands` - List brands
  - POST `/brands/create` - Create brand
  - GET/POST `/brands/<id>/edit` - Update brand
  - POST `/brands/<id>/delete` - Delete brand

## Conclusion

This brand management system provides a comprehensive solution for organizing and customizing QR codes by brand, allowing users to:
- Manage multiple brands under one account
- Customize QR code appearance per brand
- Organize QR codes by brand
- Display professional, branded contact profiles

The implementation maintains backward compatibility while adding powerful new organizational features.
