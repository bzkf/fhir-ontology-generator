LOGICAL_MODEL_TO_PROFILE = {
    "DisordersOfCardiovascularSystem": "CardiovascularDiseases",
    "Rheumatological/immunologicalDiseases": "RheumatologicalImmunologicalDiseases",
    "HistoryOfBeingATissueOrOrganRecipient": "OrganRecipient",
    "MalignantNeoplasticDiseases": "MalignantNeoplasticDisease",
    "TobaccoSmokingStatus": "SmokingStatus",
    "ChronicNeurologicalOrMentalDiseases": "ChronicNeurologicalMentalDiseases",
    "RespiratoryTherapy": "RespiratoryTherapies",
    "ImmunizationStatus": "Immunization",
    "ResuscitationOrder": "DoNotResuscitateOrder",
    # TODO: Are there more Values that are only differentiated by their type
    "ImagingProcedures": "Procedure-Radiology",
    "RadiologicalFindings": "DiagnosticReport-Radiology",
    "BiologicalSex": "SexAssignedAtBirth",
    "ContactWithPersonsSufferingFromCovid-19?": "KnownExposure",
    "Complication": "complications-covid-19",
    "StageAtDiagnosis": "DiagnosisCovid19",
    # ObservationLab  is from the Laboratory Module of the Medical Informatics Initiative (MII) and was added in geccoDataset
    "Crp": "ObservationLab",
    "Ferritin": "ObservationLab",
    "Bilirubin": "ObservationLab",
    "D-dimer": "ObservationLab",
    "GammaGlutamylTransferase": "ObservationLab",
    "AspartateAminotransferase": "ObservationLab",
    "LactateDehydrogenase": "ObservationLab",
    "CardiacTroponin": "ObservationLab",
    "Hemoglobin": "ObservationLab",
    "Creatinine": "ObservationLab",
    "Lactate": "ObservationLab",
    "Leukocytes": "ObservationLab",
    "Lymphocytes": "ObservationLab",
    "Neutrophils": "ObservationLab",
    "PartialThromboplastinTime": "ObservationLab",
    "Platelets": "ObservationLab",
    "Inr": "ObservationLab",
    "AlbuminInSerum": "ObservationLab",
    "Antithrombin": "ObservationLab",
    "Procalcitonin": "ObservationLab",
    "Interleukin6": "ObservationLab",
    "NatriureticPeptide.bProhormoneN-terminal": "ObservationLab",
    "Fibrinogen": "ObservationLab",
    "Sars-cov-2-rt-pcr": "SARS-CoV-2-RT-PCR",
    "Sars-cov-2(covid-19)IggIaQl": "SarsCoV2IgGSerPlQlIA",
    "Sars-cov-2(covid-19)IggIaQn": "SarsCoV2IgGSerPlIAaCnc",
    "Sars-cov-2(covid-19)IgmIaQl": "SarsCoV2IgMSerPlQlIA",
    "Sars-cov-2(covid-19)IgmIaQn": "SarsCoV2IgMSerPlIAaCnc",
    "Sars-cov-2(covid-19)IgaIaQl": "SarsCoV2IgASerPlQlIA",
    "Sars-cov-2(covid-19)IgaIaQn": "SarsCoV2IgASerPlIAaCnc",
    # Typo in GECCO lowercase v in Cov!
    "Sars-cov-2(covid-19)AbIaQl": "SarsCov2AbSerPlQlIA",
    "Sars-cov-2(covid-19)AbIaQn": "SarsCoV2AbSerPlIAaCnc",
    "Covid-19Therapy": "PharmacologicalTherapy",
    "AceInhibitors": "PharmacologicalTherapyACEInhibitors",
    "Anticoagulation": "PharmacologicalTherapyAnticoagulants",
    "RespiratoryOutcome": "DependenceOnVentilator",
    "TypeOfDischarge": "DischargeDisposition",
    "Follow-upSwabResult": "SARS-CoV-2-RT-PCR",
    "StudyEnrolmentDueToCovid-19": "StudyInclusionCovid19",
    "InterventionalStudiesParticipation": "InterventionalClinicalTrialParticipation",
    "Dialysis/Hemofiltration": "Dialysis",
    "EcmoTherapy": "Extracorporeal-membrane-oxygenation",
    "IsThePatientInTheIntensiveCareUnit?": "PatientInICU",
    "VentilationTherapy": "RespiratoryTherapies",
    "Paco2": "GasPanel-PaCO2",
    "Pao2": "GasPanel-PaO2",
    "Fio2": "FiO2",
    "PhValue": "GasPanel-pH",
    "Sofa-score": "SOFA",
    "DiastolicBloodPressure": "BloodPressure",
    "SystolicBloodPressure": "BloodPressure",
    "PeripheralOxygenSaturation": "OxygenSaturation",
    "Laboruntersuchung": "ObservationLab",
    "Laboranforderung": "ServiceRequestLab",
    "Wirkstoffrelation": "wirkstoffrelation",
    "Wirkstofftyp": "wirkstofftyp",
    "PatientIn": "Patient",
    "ProbandIn": "ResearchSubject",
    "Durchfuehrungsabsicht": "durchfuehrungsabsicht",
    "Dokumentationsdatum": "recordedDate",
    "MedicationAdministrationMedikation": "MedicationAdministration",
    "MedicationStatementMedikation": "MedicationStatement",
    "Mii_pr_consent_einwilligung": "MII_Consent_Einwilligung"
}