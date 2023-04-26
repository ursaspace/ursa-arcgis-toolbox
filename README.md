# Ursa's ArcGIS Python Toolbox

## Ursa Overview

Ursa Space maintains robust partnerships with existing and upcoming commercial data providers, and regularly ingests and processes a variety of SAR and non-SAR (i.e. optical, infrared, multi-spectral, and hyperspectral) data. This collection of data partners is referred to as Ursa’s Virtual Constellation.

Ursa Space performs this processing through the development and deployment of the Ursa Platform. The platform contains the data and software services required to ingest data (SAR imagery, optical imagery, external data sources for algorithmic fusion, etc.), run analytics and algorithms on these data to produce results, and provide customer access to related data feeds via API.

## Project Description

A python toolbox for working with the Ursa Platform APIs in ArcGIS Pro.

## Requirements

- ArcGIS Pro Installation & License.
- Ursa Platform Credentials set to Invoice Only customer type.
  - New customers are required to submit this [form](https://share.hsforms.com/1OpZURWHoRfCRmRwD_3CHTg2h66d) to begin our verification process
  - Existing customers can download from GitHub & get started!
  - \*\* All users must be "Invoice Only" customer type, if you are unsure what you are set to contact [support@ursaspace.com](mailto:support@ursaspace.com).
- Admin privileges if ArcGIS Pro is installed at system level.
  - If you do not have Admin access, a clone of the default ArcGIS Pro Python Environment must be created in a directory that does not require Admin access. See [ESRI Documentation](https://pro.arcgis.com/en/pro-app/latest/arcpy/get-started/clone-an-environment.htm) for more details.
- This python toolbox only uses packages available in the default python environment shipped with ArcGIS Pro.

## Downloading from GitHub

- Use this link https://github.com/ursaspace/ursa-arcgis-toolbox/archive/refs/heads/main.zip
- or "Download ZIP" - Find and select the green "< > Code" button, then select "Download ZIP"
  <img width="1190" alt="download-zip" src="https://user-images.githubusercontent.com/123033437/215618368-4f7bdb8c-8e4a-4069-9794-edc4071e5b00.png">

## Installation

0. Unzip the compressed folder to your desired location

1. In an ArcGIS Pro Document, open "Catalog"

2. In Catalog, right-click "Toolboxes" and select "Add Toolbox"
   <img width="323" alt="Screenshot 2023-01-30 at 15 16 01" src="https://user-images.githubusercontent.com/123033437/215618434-a2fedc98-8153-42b7-b465-d901af682989.png">

3. Navigate to "UrsaPlatform.pyt" where you unzipped Ursa's Python Toolbox, then click "Ok"

4. Open the added toolbox. Listed are the available tools.
   <img width="323" alt="Screenshot 2023-01-30 at 15 16 21" src="https://user-images.githubusercontent.com/123033437/215618493-349f235f-2d0a-47cb-877e-e78138ab46e4.png">

## Usage

Tools can be opened by double-clicking the item in the toolbox.

### Login

- User must provide Ursa Platform credentials using the "Login" tool in order to use the Ursa Platform APIs.
- Login sessions will last up to 8 hours, after that you will receive an authentication error & you will need to log back in.

### Tasking

- Area of interest only supports point geometries
- Start Date must be 48 hours from present day/time, _if you have the need for Emergency tasking please contact us_
- End Date cannot precede start date
- Determine Imaging Mode
- Determine Preferred Vendor(s), _future iterations will include additional vendors_.

### Analytics

- Area of interest only supports point geometries
- End Date cannot precede start data
- Determine Analytic Options
- If Change Detection Analytic selected, determine specific Change Detection Analytic options

## Pricing, Terms & Conditions

[Ursa Virtual Constellation Pricing](https://4160389.fs1.hubspotusercontent-na1.net/hubfs/4160389/Esri%20Links/Esri-Ursa-Virtual-Constellation-Pricing-Sheet-v20230130.pdf)

- Currently Capella & ICEYE available, _future iterations will include additional vendors_.

[Terms & Conditions](https://ursaspace.com/terms/)

- Includes End User License Agreements by Vendor Partner

## Ordering

Orders will be delivered via email with a link to download the relevant orders contents.

## Invoicing

Relevant invoices will be sent via e-mail as soon as possible after a user's order submission. Invoices are to be paid by the user withtin 30 days after receiving the invoice from Ursa.

## Support

Contact [support@ursaspace.com](mailto:support@ursaspace.com).
