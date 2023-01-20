# ursa-arcgispro

## Project Description

A python toolbox for working with the Ursa Platform APIs in ArcGIS Pro.

## Requirements

- ArcGIS Pro Installation
- Ursa Platform Credentials
- Admin privileges if ArcGIS Pro is installed at system level
  - If you do not have Admin access, a clone of the default ArcGIS Pro Python Environment must be created in a directory that does not require Admin access. See [ESRI Documentation](https://pro.arcgis.com/en/pro-app/latest/arcpy/get-started/clone-an-environment.htm) for more details.
- This python toolbox only uses packages available in the default python environment shipped with ArcGIS Pro.

## Installation

1. In an ArcGIS Pro Document, open "Catalog"
2. In Catalog, right-click "Toolboxes" and select "Add Toolbox"
3. Navigate to "UrsaPlatform.pyt", click "Ok"
4. Open the added toolbox. Listed are the available tools.

## Usage

- User must provide Ursa Platform credentials using the "Login" tool in order to use the Ursa Platform APIs.

- Tools can be opened by double-clicking the item in the toolbox.

## Tests

- To run all tests, execute `tests.py` using python executable from ArcGIS Pro Conda Environment. Requires ArcPy. Test modules use the `*_test.py` pattern.

## Support

Contact [support@ursaspace.com](mailto:support@ursaspace.com).
