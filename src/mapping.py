"""
Mapping Configuration Module
============================

This module defines the field-to-XML mapping configuration used by the XML builder.

Each mapping entry describes how a source record field is transformed
and inserted into a specific ISO19139 XML structure.

Core Configuration Keys
-----------------------

xpath:
  Full dot-separated XML path to the target element.
  - Must reflect the exact ISO structure hierarchy.
  - If multiple elements share the same path, selection may rely
    on tag attributes defined in the builder.

source:
  Dot-separated path in the input record.
  Example:
    "files.0.id"
    "edhProfile.characterSet"
  - When `repeat` is used, the resolved value must be a list.

source_fr:
  Optional French source field.
  - When provided, a bilingual PT_FreeText block is populated with locale attribute.

controlled:
  Indicates that the value must be normalized using CONTROLLED_VOCAB.
  - The raw source value is mapped to a controlled vocabulary value.
  - Used for ISO codeList-compliant fields.

Repeat Configuration
--------------------

repeat:
  Used when a field generates multiple XML elements.

Required keys:
  container_xpath:
    The parent element where repeated nodes will be inserted.

  repeat_tag:
    The XML tag name of each repeated element.

  value_xpath:
    The relative path within each repeated block where the value is inserted.

The builder enforces that:
  - The resolved source must be iterable.
  - Each item generates one XML block.

Builder-Enforced Required Fields
--------------------------------

The following elements are automatically enforced in the builder
even if not explicitly defined in mapping:

  - fileIdentifier
  - dateStamp

These fields are mandatory for ISO validation.

Template-Injected Static Fields
-------------------------------

The following elements are pre-defined in the base XML template
and are not dynamically mapped:

  - hierarchyLevel
  - organisationName
  - citedResponsiblePartyOrganizationName
  - useLimitation
  - accessConstraints
  - useConstraints
  - distributionContactOrganizationName

These values are either static or template-driven.

Notes
-----

This mapping file contains configuration only.
No XML manipulation logic should be implemented here.

All XML generation logic is handled in xml_builder.py.
"""

FIELD_MAPPING = [
  # language
  {
    "xpath": ".//gmd:language/gco:CharacterString",
    "source": "edhProfile.language",
    "controlled": "language"
  },
  # characterSet
  {
    "xpath": ".//gmd:characterSet/gco:MD_CharacterSetCode",
    "source": "edhProfile.characterSet",
    "controlled": "characterSet"
  },
  # hierarchyLevel
  # {
  #   "xpath": ".//gmd:hierarchyLevel/gmd:MD_ScopeCode",
  #   "source": "edhProfile.hierarchyLevel"
  # },


  # organizationName
  # {
  #   "xpath": ".//gmd:contact/gmd:CI_ResponsibleParty/gmd:organisationName/gco:CharacterString",
  #   "source": "organizationName"
  # },
  # emailAddress
  {
    "xpath": ".//gmd:contact/gmd:CI_ResponsibleParty/gmd:contactInfo/gmd:CI_Contact/gmd:address/gmd:CI_Address/gmd:electronicMailAddress/gco:CharacterString",
    "source": "emailAddress",
    "source_fr": "emailAddress"
  },
  # role
  {
    "xpath": ".//gmd:contact/gmd:CI_ResponsibleParty/gmd:role/gmd:CI_RoleCode",
    "source": "edhProfile.contactRole",
    "controlled": "role"
  },


  # title
  {
    "xpath": ".//gmd:identificationInfo/gmd:MD_DataIdentification/gmd:citation/gmd:CI_Citation/gmd:title/gco:CharacterString",
    "source": "title",
    "source_fr": "titleFr"
  },
  # date publication
  {
    "xpath": ".//gmd:identificationInfo/gmd:MD_DataIdentification/gmd:citation/gmd:CI_Citation/gmd:date/gmd:CI_Date[gmd:dateType/gmd:CI_DateTypeCode[@codeListValue='RI_367']]/gmd:date/gco:Date",
    "source": "lastModified"
  },
  # date createdAt
  {
    "xpath": ".//gmd:identificationInfo/gmd:MD_DataIdentification/gmd:citation/gmd:CI_Citation/gmd:date/gmd:CI_Date[gmd:dateType/gmd:CI_DateTypeCode[@codeListValue='RI_366']]/gmd:date/gco:Date",
    "source": "createdAt"
  },
  # abstract
  {
    "xpath": ".//gmd:identificationInfo/gmd:MD_DataIdentification/gmd:abstract/gco:CharacterString",
    "source": "abstractEN",
    "source_fr": "abstractFR"
  },
  # status
  {
    "xpath": ".//gmd:identificationInfo/gmd:MD_DataIdentification/gmd:status/gmd:MD_ProgressCode",
    "source": "edhProfile.datasetStatus",
    "controlled": "status"
  },
  # data_identification_language
  {
    "xpath": ".//gmd:identificationInfo/gmd:MD_DataIdentification/gmd:language/gco:CharacterString",
    "source": "edhProfile.language",
    "controlled": "language"
  },
  # topicCategory
  {
    "repeat": True,
    "container_xpath": ".//gmd:identificationInfo/gmd:MD_DataIdentification",
    "repeat_tag": "gmd:topicCategory",
    "value_xpath": "gmd:MD_TopicCategoryCode",
    "source": "edhProfile.topicCategory",
    "controlled": "topicCategory"
  },
  # updateFrequency
  {
    "xpath": ".//gmd:identificationInfo/gmd:MD_DataIdentification/gmd:resourceMaintenance/gmd:MD_MaintenanceInformation/gmd:maintenanceAndUpdateFrequency/gmd:MD_MaintenanceFrequencyCode",
    "source": "updateFrequency",
    "source_fr": "updateFrequencyFr",
    "controlled": "updateFrequency"
  },


  # edhProfile.citedResponsiblePartyOrganizationName 

  # citedResponsiblePartyEmail
  {
    "xpath": ".//gmd:identificationInfo/gmd:MD_DataIdentification/gmd:citation/gmd:CI_Citation/gmd:citedResponsibleParty/gmd:CI_ResponsibleParty/gmd:contactInfo/gmd:CI_Contact/gmd:address/gmd:CI_Address/gmd:electronicMailAddress/gco:CharacterString",
    "source": "edhProfile.citedResponsiblePartyEmail",
    "source_fr": "edhProfile.citedResponsiblePartyEmail"
  },
  # citedResponsiblePartyRole
  {
    "xpath": ".//gmd:identificationInfo/gmd:MD_DataIdentification/gmd:citation/gmd:CI_Citation/gmd:citedResponsibleParty/gmd:CI_ResponsibleParty/gmd:role/gmd:CI_RoleCode",
    "source": "edhProfile.citedResponsiblePartyRole",
    "controlled": "role"
  },


  # keyword
  {
    "repeat": True,
    "container_xpath": ".//gmd:identificationInfo/gmd:MD_DataIdentification/gmd:descriptiveKeywords/gmd:MD_Keywords",
    "repeat_tag": "gmd:keyword",
    "value_xpath": "gco:CharacterString",
    "source": "pacificSalmonTopicCategory",
    "source_fr": "pacificSalmonTopicCategoryFr",
    "controlled": "keyword"
  },


  # useLimitation
  # {
  #   "xpath": ".//gmd:identificationInfo/gmd:MD_DataIdentification/gmd:resourceConstraints/gmd:MD_LegalConstraints/gmd:useLimitation/gco:CharacterString",
  #   "source": "license",
  #   "source_fr": "license"
  # },
  # accessConstraints
  # {
  #   "xpath": ".//gmd:identificationInfo/gmd:MD_DataIdentification/gmd:resourceConstraints/gmd:MD_LegalConstraints/gmd:accessConstraints/gmd:MD_RestrictionCode",
  #   "source": "license"
  # },
  # useConstraints
  # {
  #   "xpath": ".//gmd:identificationInfo/gmd:MD_DataIdentification/gmd:resourceConstraints/gmd:MD_LegalConstraints/gmd:useConstraints/gmd:MD_RestrictionCode",
  #   "source": "license"
  # },
  # classification
  {
    "xpath": ".//gmd:identificationInfo/gmd:MD_DataIdentification/gmd:resourceConstraints/gmd:MD_SecurityConstraints/gmd:classification/gmd:MD_ClassificationCode",
    "source": "classification",
    "source_fr": "classificationFr",
    "controlled": "classification"
  },


  # begin_date
  {
    "xpath": ".//gmd:identificationInfo/gmd:MD_DataIdentification/gmd:extent/gmd:EX_Extent/gmd:temporalElement/gmd:EX_TemporalExtent/gmd:extent/gml:TimePeriod/gml:beginPosition",
    "source": "beginDate"
  },
  # end_date
  {
    "xpath": ".//gmd:identificationInfo/gmd:MD_DataIdentification/gmd:extent/gmd:EX_Extent/gmd:temporalElement/gmd:EX_TemporalExtent/gmd:extent/gml:TimePeriod/gml:endPosition",
    "source": "endDate"
  },


  # spatialCode
  {
    "xpath": ".//gmd:referenceSystemInfo/gmd:MD_ReferenceSystem/gmd:referenceSystemIdentifier/gmd:RS_Identifier/gmd:code/gco:CharacterString",
    "source": "spatialCode"
  },
  # spatialType
  {
    "xpath": ".//gmd:identificationInfo/gmd:MD_DataIdentification/gmd:spatialRepresentationType/gmd:MD_SpatialRepresentationTypeCode",
    "source": "spatialType",
    "controlled": "spatialType"
  },


  # fileFormatName
  # value is a list, get only the first file format since version is a string
  {
    "xpath": ".//gmd:distributionInfo/gmd:MD_Distribution/gmd:distributionFormat/gmd:MD_Format/gmd:name/gco:CharacterString",
    "source": "edhProfile.fileFormatName.0"
  },
  # fileFormatVersion
  {
    "xpath": ".//gmd:distributionInfo/gmd:MD_Distribution/gmd:distributionFormat/gmd:MD_Format/gmd:version/gco:CharacterString",
    "source": "edhProfile.fileFormatVersion"
  },
  # distributionContactOrganizationName
  # {
  #   "xpath": ".//gmd:distributionInfo/gmd:MD_Distribution/gmd:distributor/gmd:MD_Distributor/gmd:distributorContact/gmd:CI_ResponsibleParty/gmd:organisationName/gco:CharacterString",
  #   "source": "edhProfile.distributionContactOrganizationName",
  #   "source_fr": "edhProfile.distributionContactOrganizationName"
  # },
  # distributionContactEmail
  {
    "xpath": ".//gmd:distributionInfo/gmd:MD_Distribution/gmd:distributor/gmd:MD_Distributor/gmd:distributorContact/gmd:CI_ResponsibleParty/gmd:contactInfo/gmd:CI_Contact/gmd:address/gmd:CI_Address/gmd:electronicMailAddress/gco:CharacterString",
    "source": "edhProfile.distributionContactEmail",
    "source_fr": "edhProfile.distributionContactEmail"
  },
  # distributionContactRole
  {
    "xpath": ".//gmd:distributionInfo/gmd:MD_Distribution/gmd:distributor/gmd:MD_Distributor/gmd:distributorContact/gmd:CI_ResponsibleParty/gmd:role/gmd:CI_RoleCode",
    "source": "edhProfile.distributionContactRole",
    "controlled": "role"
  },
]
