# ursa-arcgispro-toolbox

## Project Description

A python toolbox for working with the Ursa Platform APIs in ArcGIS Pro.

## Requirements

- ArcGIS Pro Installation & License.
- Ursa Platform Credentials set to Invoice Only customer type.
  - New customers are required to submit this [form](https://share.hsforms.com/1OpZURWHoRfCRmRwD_3CHTg2h66d) to begin our verification process
  - Existing customers can download from GitHub & get started!
  - ** All users must be "Invoice Only" customer type, if you are unsure what you are set to contact [support@ursaspace.com](mailto:support@ursaspace.com).
- Admin privileges if ArcGIS Pro is installed at system level.
  - If you do not have Admin access, a clone of the default ArcGIS Pro Python Environment must be created in a directory that does not require Admin access. See [ESRI Documentation](https://pro.arcgis.com/en/pro-app/latest/arcpy/get-started/clone-an-environment.htm) for more details.
- This python toolbox only uses packages available in the default python environment shipped with ArcGIS Pro.

## Downloading from GitHub

- "Download ZIP" - Find and select the green "< > Code" button, then select "Download ZIP"

<img width="1800" alt="Screenshot 2023-01-24 at 15 27 11" src="https://user-images.githubusercontent.com/123033437/214444397-61d111c0-f6b6-4cbd-bbea-49637efb1a03.png">

## Installation

1. In an ArcGIS Pro Document, open "Catalog"
2. In Catalog, right-click "Toolboxes" and select "Add Toolbox"
3. Navigate to "UrsaPlatform.pyt", click "Ok"
4. Open the added toolbox. Listed are the available tools.

## Usage

- User must provide Ursa Platform credentials using the "Login" tool in order to use the Ursa Platform APIs.
- Tools can be opened by double-clicking the item in the toolbox.

## Pricing

[Ursa Virtual Constellation Pricing](https://4160389.fs1.hubspotusercontent-na1.net/hubfs/4160389/Esri%20Links/Esri-Ursa-Virtual-Constellation-Pricing-Sheet-v20230130.pdf)
- Currently Capella & ICEYE available, future iterations will include additional vendors.

## Ordering

Orders will be delivered via email with a link to download the relevant submission

## Invoicing

Orders will have relevant invoices sent via e-mail as soon as possible after a user's submission. Invoices are to be paid withtin 30 days after receiving the invoice from Ursa.

## Tests

- To run all tests, execute `tests.py` using python executable from ArcGIS Pro Conda Environment. Requires ArcPy. Test modules use the `*_test.py` pattern.

## Support

Contact [support@ursaspace.com](mailto:support@ursaspace.com).
