from datetime import datetime

"""
Mapping field configuration

source:
  Dot-separated path in the source record (e.g. "files.0.id").
  When `repeat` is used, the resolved source value must be a list.

source_fr:
  Optional French source value.
  When provided, a bilingual (EN/FR) block is generated using PT_FreeText.
  * Do not add "gco:CharacterString" in the path for bilingual fields.

text:
  Direct value to use instead of reading from the source record.
  If present, `source` is ignored.

text_fr:
  Optional French value when using `text`.
  Generates a bilingual (EN/FR) block using PT_FreeText.
  * Do not add "gco:CharacterString" in the path for bilingual fields.

repeat:
  Optional tag name (e.g. "gmd:topicCategory") indicating 
  which child element in the path should be repeated.
  When set, one XML subtree is created per item in the source list.

path:
  XML element path from the document root to the leaf element.
  Each entry may be:
    - "gmd:tag"                   no attributes
    - ("gmd:tag", {attrib})       with attributes
"""

FIELD_MAPPING = {
  "id": {
    "source": "files.0.id",
    "path": [
      ("gmd:fileIdentifier"),
      ("gco:CharacterString")
    ]
  },
  "date_stamp": {
    "text": datetime.now().isoformat(),
    "path": [
      ("gmd:dateStamp"),
      ("gco:DateTime")
    ]
  },
  "language": {
    "source": "edhProfile.language",
    "path": [
      ("gmd:language"),
      ("gco:CharacterString")
    ]
  },
  "character_set": {
    "source": "edhProfile.characterSet",
    "path": [
      ("gmd:characterSet"),
      ("gmd:MD_CharacterSetCode", 
       { 
         "codeList": "https://schemas.metadata.geo.ca/register/napMetadataRegister.xml#IC_95",
         "codeListValue": "RI_458"
        }
      )
    ]
  },
  "hierarchy_level": {
    "source": "edhProfile.hierarchyLevel",
    "path": [
      ("gmd:hierarchyLevel"),
      ("gmd:MD_ScopeCode", 
       { 
         "codeList": "https://schemas.metadata.geo.ca/register/napMetadataRegister.xml#IC_108",
         "codeListValue": "RI_623"
        }
      )
    ]
  },

  # 
  "individual_name": {
    "source": "individualName",
    "path": [
      ("gmd:contact"),
      ("gmd:CI_ResponsibleParty"),
      ("gmd:individualName"),
    ]
  },
  "organization_name": {
    "source": "organizationName",
    "source_fr": "organizationName",
    "path": [
      ("gmd:contact"),
      ("gmd:CI_ResponsibleParty"),
      ("gmd:organisationName", {"xsi:type": "gmd:PT_FreeText_PropertyType"}),
    ]
  },
  "email_address": {
    "source": "emailAddress",
    "source_fr": "emailAddress",
    "path": [
      ("gmd:contact"),
      ("gmd:CI_ResponsibleParty"),
      ("gmd:contactInfo"),
      ("gmd:CI_Contact"),
      ("gmd:address"),
      ("gmd:electronicMailAddress", {"xsi:type": "gmd:PT_FreeText_PropertyType"}),
    ]
  },
  "role": {
    "source": "edhProfile.contactRole",
    "path": [
      ("gmd:contact"),
      ("gmd:CI_ResponsibleParty"),
      ("gmd:role"),
      ("gmd:CI_RoleCode", 
       { 
         "codeList": "https://schemas.metadata.geo.ca/register/napMetadataRegister.xml#IC_90",
         "codeListValue": "RI_414"
        }
      ),
    ]
  },

  # 
  "title": {
    "source": "title",
    "source_fr": "titleFr",
    "path": [
      ("gmd:identificationInfo"),
      ("gmd:MD_DataIdentification"),
      ("gmd:citation"),
      ("gmd:CI_Citation"),
      ("gmd:title", {"xsi:type": "gmd:PT_FreeText_PropertyType"})
    ]
  },
  "datePublication": {
    "text": datetime.now().date(),
    "path": [
      ("gmd:identificationInfo"),
      ("gmd:MD_DataIdentification"),
      ("gmd:citation"),
      ("gmd:CI_Citation"),
      ("gmd:date"),
      ("gmd:CI_Date"),
      ("gmd:date"),
      ("gco:Date")
    ]
  },
  "datePublicationTypeCode": {
    "source": "edhProfile.dataPublication",
    "path": [
      ("gmd:identificationInfo"),
      ("gmd:MD_DataIdentification"),
      ("gmd:citation"),
      ("gmd:CI_Citation"),
      ("gmd:date"),
      ("gmd:CI_Date"),
      ("gmd:dateType"),
      ("gmd:CI_DateTypeCode",
        { 
         "codeList": "https://schemas.metadata.geo.ca/register/napMetadataRegister.xml#IC_87",
         "codeListValue": "RI_367"
        }
      )
    ]
  },
  "abstract": {
    "source": "abstractEN",
    "source_fr": "abstractFR",
    "path": [
      ("gmd:identificationInfo"),
      ("gmd:MD_DataIdentification"),
      ("gmd:abstract", {"xsi:type": "gmd:PT_FreeText_PropertyType"})
    ]
  },
  "status": {
    "source": "edhProfile.datasetStatus",
    "path": [
      ("gmd:identificationInfo"),
      ("gmd:MD_DataIdentification"),
      ("gmd:status"),
      ("gmd:MD_ProgressCode", 
       { 
         "codeList": "https://schemas.metadata.geo.ca/register/napMetadataRegister.xml#IC_106",
         "codeListValue": "RI_596"
        }
      ),
    ]
  },
  "data_identification_language": {
    "source": "edhProfile.language",
    "path": [
      ("gmd:identificationInfo"),
      ("gmd:MD_DataIdentification"),
      ("gmd:language"),
      ("gco:CharacterString")
    ]
  },
  "topic_category": {
    "source": "edhProfile.topicCategory",
    "repeat": "gmd:topicCategory",
    "path": [
      ("gmd:identificationInfo"),
      ("gmd:MD_DataIdentification"),
      ("gmd:topicCategory"),
      ("gmd:MD_TopicCategoryCode")
    ]
  },
  "update_frequency": {
    "source": "updateFrequency",
    "source_fr": "updateFrequencyFr",
    "path": [
      ("gmd:resourceMaintenance"),
      ("gmd:MD_MaintenanceInformation"),
      ("gmd:maintenanceAndUpdateFrequency"),
      ("gmd:MD_MaintenanceFrequencyCode", 
       { 
         "codeList": "https://schemas.metadata.geo.ca/register/napMetadataRegister.xml#IC_102",
         "codeListValue": "RI_539"
        }
      ),
    ]
  },

  # 
  "ci_individual_name": {
    "source": "edhProfile.citedResponsiblePartyIndividualName",
    "path": [
      ("gmd:identificationInfo"),
      ("gmd:MD_DataIdentification"),
      ("gmd:citation"),
      ("gmd:CI_Citation"),
      ("gmd:citedResponsibleParty"),
      ("gmd:CI_ResponsibleParty"),
      ("gmd:individualName"),
      ("gco:CharacterString"),
    ]
  },
  "ci_organization_name": {
    "source": "edhProfile.citedResponsiblePartyOrganizationName",
    "source_fr": "edhProfile.citedResponsiblePartyOrganizationName",
    "path": [
      ("gmd:identificationInfo"),
      ("gmd:MD_DataIdentification"),
      ("gmd:citation"),
      ("gmd:CI_Citation"),
      ("gmd:citedResponsibleParty"),
      ("gmd:CI_ResponsibleParty"),
      ("gmd:organisationName", {"xsi:type": "gmd:PT_FreeText_PropertyType"}),
    ]
  },
  "ci_email": {
    "source": "edhProfile.citedResponsiblePartyEmail",
    "source_fr": "edhProfile.citedResponsiblePartyEmail",
    "path": [
      ("gmd:identificationInfo"),
      ("gmd:MD_DataIdentification"),
      ("gmd:citation"),
      ("gmd:CI_Citation"),
      ("gmd:citedResponsibleParty"),
      ("gmd:CI_ResponsibleParty"),
      ("gmd:contactInfo"),
      ("gmd:CI_Contact"),
      ("gmd:address"),
      ("gmd:CI_Address"),
      ("gmd:electronicMailAddress", {"xsi:type": "gmd:PT_FreeText_PropertyType"}),
    ]
  },
  "ci_role": {
    "source": "edhProfile.citedResponsiblePartyRole",
    "path": [
      ("gmd:identificationInfo"),
      ("gmd:MD_DataIdentification"),
      ("gmd:citation"),
      ("gmd:CI_Citation"),
      ("gmd:citedResponsibleParty"),
      ("gmd:CI_ResponsibleParty"),
      ("gmd:role"),
      ("gmd:CI_RoleCode", 
       { 
         "codeList": "https://schemas.metadata.geo.ca/register/napMetadataRegister.xml#IC_90",
         "codeListValue": "RI_415"
        }
      ),
    ]
  },

  # 
  "descriptive_keywords": {
    "source": "pacificSalmonTopicCategory",
    "source_fr": "pacificSalmonTopicCategory",
    "repeat": "gmd:keyword",
    "path": [
      ("gmd:identificationInfo"),
      ("gmd:MD_DataIdentification"),
      ("gmd:descriptiveKeywords"),
      ("gmd:MD_Keywords"),
      ("gmd:keyword", {"xsi:type": "gmd:PT_FreeText_PropertyType"}),
    ]
  },

  # 
  "useLimitation": {
    "source": "license",
    "source_fr": "license",
    "path": [
      ("gmd:identificationInfo"),
      ("gmd:MD_DataIdentification"),
      ("gmd:resourceConstraints"),
      ("gmd:MD_LegalConstraints"),
      ("gmd:useLimitation", {"xsi:type": "gmd:PT_FreeText_PropertyType"}),
    ]
  },
  "accessConstraints": {
    "source": "license",
    "path": [
      ("gmd:identificationInfo"),
      ("gmd:MD_DataIdentification"),
      ("gmd:resourceConstraints"),
      ("gmd:MD_LegalConstraints"),
      ("gmd:accessConstraints"),
      ("gmd:MD_RestrictionCode", 
       { 
         "codeList": "https://schemas.metadata.geo.ca/register/napMetadataRegister.xml#IC_107",
         "codeListValue": "RI_606"
        }
      ),
    ]
  },
  "useConstraints": {
    "source": "license",
    "path": [
      ("gmd:identificationInfo"),
      ("gmd:MD_DataIdentification"),
      ("gmd:resourceConstraints"),
      ("gmd:MD_LegalConstraints"),
      ("gmd:useConstraints"),
      ("gmd:MD_RestrictionCode", 
       { 
         "codeList": "https://schemas.metadata.geo.ca/register/napMetadataRegister.xml#IC_107",
         "codeListValue": "RI_606"
        }
      ),
    ]
  },
  "security_classification": {
    "source": "classification",
    # "source_fr": "classificationFr",
    "path": [
      ("gmd:identificationInfo"),
      ("gmd:MD_DataIdentification"),
      ("gmd:resourceConstraints"),
      ("gmd:MD_SecurityConstraints"),
      ("gmd:classification"),
      ("gmd:MD_ClassificationCode", 
       { 
         "codeList": "https://schemas.metadata.geo.ca/register/napMetadataRegister.xml#IC_96",
         "codeListValue": "RI_484"
        }
      ),
    ]
  },

  # 
  "begin_date": {
    "source": "beginDate",
    "path": [
      ("gmd:identificationInfo"),
      ("gmd:MD_DataIdentification"),
      ("gmd:extent"),
      ("gmd:EX_Extent"),
      ("gmd:EX_TemporalExtent"),
      ("gmd:extent"),
      ("gml:TimePeriod", {"gml:id": ""}),
      ("gml:beginPosition"),
    ]
  },
  "end_date": {
    "source": "endDate",
    "path": [
      ("gmd:identificationInfo"),
      ("gmd:MD_DataIdentification"),
      ("gmd:extent"),
      ("gmd:EX_Extent"),
      ("gmd:EX_TemporalExtent"),
      ("gmd:extent"),
      ("gml:TimePeriod", {"gml:id": ""}),
      ("gml:endPosition"),
    ]
  },

  # 
  "code": {
    "source": "spatialCode",
    "path": [
      ("gmd:referenceSystemInfo"),
      ("gmd:MD_ReferenceSystem"),
      ("gmd:referenceSystemIdentifier"),
      ("gmd:RS_Identifier"),
      ("gmd:code"),
      ("gco:CharacterString"),
    ]
  },
  # "code_space": {
  #   "text": "https://epsg.io",
  #   "path": [
  #     ("gmd:referenceSystemInfo"),
  #     ("gmd:MD_ReferenceSystem"),
  #     ("gmd:referenceSystemIdentifier"),
  #     ("gmd:RS_Identifier"),
  #     ("gmd:codeSpace"),
  #     ("gco:CharacterString"),
  #   ]
  # },

  # 
  "file_format_name": {
    "source": "edhProfile.fileFormatName",
    "repeat": "gmd:distributionFormat",
    "path": [
      ("gmd:distributionInfo"),
      ("gmd:MD_Distribution"),
      ("gmd:distributionFormat"),
      ("gmd:MD_Format"),
      ("gmd:name"),
      ("gco:CharacterString")
    ]
  },
  "file_format_version": {
    "source": "edhProfile.fileFormatVersion",
    "path": [
      ("gmd:distributionInfo"),
      ("gmd:MD_Distribution"),
      ("gmd:distributionFormat"),
      ("gmd:MD_Format"),
      ("gmd:version"),
      ("gco:CharacterString")
    ]
  },

  # 
  "distributor_organization_name": {
    "source": "edhProfile.distributionContactOrganizationName",
    "source_fr": "edhProfile.distributionContactOrganizationName",
    "path": [
      ("gmd:distributionInfo"),
      ("gmd:MD_Distribution"),
      ("gmd:distributor"),
      ("gmd:MD_Distributor"),
      ("gmd:distributorContact"),
      ("gmd:CI_ResponsibleParty"),
      ("gmd:organisationName", {"xsi:type": "gmd:PT_FreeText_PropertyType"})
    ]
  },
  "distributor_email": {
    "source": "edhProfile.distributionContactEmail",
    "source_fr": "edhProfile.distributionContactEmail",
    "path": [
      ("gmd:distributionInfo"),
      ("gmd:MD_Distribution"),
      ("gmd:distributor"),
      ("gmd:MD_Distributor"),
      ("gmd:distributorContact"),
      ("gmd:CI_ResponsibleParty"),
      ("gmd:contactInfo"),
      ("gmd:CI_Contact"),
      ("gmd:address"),
      ("gmd:CI_Address"),
      ("gmd:electronicMailAddress", {"xsi:type": "gmd:PT_FreeText_PropertyType"})
    ]
  },

  "distributor_role": {
    "source": "edhProfile.distributionContactRole",
    "path": [
      ("gmd:distributionInfo"),
      ("gmd:MD_Distribution"),
      ("gmd:distributor"),
      ("gmd:MD_Distributor"),
      ("gmd:distributorContact"),
      ("gmd:CI_ResponsibleParty"),
      ("gmd:role"),
      ("gmd:CI_RoleCode", 
       { 
         "codeList": "https://schemas.metadata.geo.ca/register/napMetadataRegister.xml#IC_90",
         "codeListValue": "RI_412"
        }
      ),
    ]
  },

  #### HNAP
  "metadataStandardName": {
    "text": "North American Profile of ISO 19115:2003 - Geographic information - Metadata",
    "text_fr": "Profil nord-américain de la norme ISO 19115:2003 - Information géographique - Métadonnées",
    "path": [
      ("gmd:metadataStandardName", {"xsi:type": "gmd:PT_FreeText_PropertyType"})
    ]
  },
  "metadataStandardVersion": {
    "text": "CAN/CGSB-171.100-2009",
    "path": [
      ("gmd:metadataStandardVersion"),
      ("gco:CharacterString")
    ]
  },
  "localeLanguageCode": {
    "text": "French; Français",
    "path": [
      ("gmd:locale"),
      ("gmd:PT_Locale", {"id": "fra"}),
      ("gmd:languageCode"),
      ("gmd:languageCode", 
       { 
         "codeList": "https://schemas.metadata.geo.ca/register/napMetadataRegister.xml#IC_116",
         "codeListValue": "fra"
        }
      ),
    ]
  },
  "localeCountry": {
    "text": "Canada; Canada",
    "path": [
      ("gmd:locale"),
      ("gmd:PT_Locale", {"id": "fra"}),
      ("gmd:country"),
      ("gmd:country", 
       { 
         "codeList": "https://schemas.metadata.geo.ca/register/napMetadataRegister.xml#IC_117",
         "codeListValue": "CAN"
        }
      ),
    ]
  },
  "localeCharacterEncoding": {
    "text": "utf8; utf8",
    "path": [
      ("gmd:locale"),
      ("gmd:PT_Locale", {"id": "fra"}),
      ("gmd:characterEncoding"),
      ("gmd:MD_CharacterSetCode", 
       { 
         "codeList": "https://schemas.metadata.geo.ca/register/napMetadataRegister.xml#IC_95",
         "codeListValue": "RI_458"
        }
      ),
    ]
  }
}
